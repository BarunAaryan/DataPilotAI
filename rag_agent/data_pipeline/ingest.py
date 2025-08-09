import pandas as pd
from.database import get_db_engine

def ingest_data(excel_path: str):
    
    #print("Starting data ingestion process...")

    # Read all sheets from the Excel file into a dictionary of DataFrames.
    try:
        all_sheets_dict = pd.read_excel(excel_path, sheet_name=None)
        #print(f"Successfully loaded sheets: {list(all_sheets_dict.keys())}")
    except FileNotFoundError:
        print(f"Error: The file at {excel_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None

    # Step 2: Clean and standardize each DataFrame.
    cleaned_sheets = []  # initialize list to collect cleaned sheets
    for sheet_name, df in all_sheets_dict.items():
        # Standardize column names: convert to lowercase and replace spaces.
        df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
        
        # Add a column for data provenance to track the original source sheet.
        df['source_sheet'] = sheet_name
        
        # Convert date columns to datetime objects, coercing errors.
        if 'ticket_date' in df.columns:
            df['ticket_date'] = pd.to_datetime(df['ticket_date'], errors='coerce')

        cleaned_sheets.append(df)
    
    # print("Standardized column names and cleaned data for all sheets.")

    # Concatenate all cleaned DataFrames into a single master DataFrame.
    if not cleaned_sheets:
        print("No data to ingest. Exiting.")
        return None
        
    master_df = pd.concat(cleaned_sheets, ignore_index=True)
    print(f"Concatenated all sheets into a master DataFrame with shape: {master_df.shape}")

    # Persist the master DataFrame to the SQL database.
    engine = get_db_engine()
    table_name = 'tickets_data'

    master_df.to_sql(
        name=table_name,
        con=engine,
        if_exists='replace', 
        index=False           
    )
    

    print(f"Data successfully written to SQL table '{table_name}' in the database file.")
    print("Data ingestion complete.")
    
    # Return the engine so it can be used by the agent.
    return engine