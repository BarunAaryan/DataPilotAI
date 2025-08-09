import pandas as pd
from gen_ai_hub.proxy.langchain.init_models import init_llm
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_experimental.agents import create_pandas_dataframe_agent

def create_agents(db_engine):
    print("Initializing custom LLM and agents")
    # primary LLM
    llm = init_llm('gpt-4', max_tokens=1500, temperature=0)

    #SQL Agent
    db = SQLDatabase(engine=db_engine)
    sql_agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="openai-tools", 
        verbose=False
    )
    #print("SQL Agent created.")

    #Analysis Agent
    def create_pandas_agent(df: pd.DataFrame):
        return create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            verbose=False,
            allow_dangerous_code=True
        )
    
    #print("Pandas Agent creator function created.")
    print("All agents initialized successfully.")
    return sql_agent_executor, create_pandas_agent