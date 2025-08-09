# DataPilotAI: Multi-Agent Data Analyst

DataPilotAI is a Python-based command-line tool for intelligent data analysis using a multi-agent workflow. It leverages LLMs (Large Language Models), LangChain, and LangGraph to ingest, store, query, and analyze tabular data (such as Excel files) with natural language. The system is modular, extensible, and designed for enterprise data workflows.

---

## Features

- **Automated Data Ingestion:** Reads and cleans Excel files, standardizes columns, and loads data into a local SQLite database.
- **Multi-Agent Workflow:** Uses a graph-based pipeline with specialized agents for SQL retrieval, pandas-based analysis, and response synthesis.
- **Natural Language Interface:** Query your data using plain English; the system translates questions into SQL and DataFrame operations.
- **Session Isolation:** Each CLI session is uniquely identified for clean, independent conversations.
- **Extensible & Modular:** Easily add new agents or data sources.

---

## Architecture Overview

```
User Query
   │
   ▼
[SQL Agent] ──► [Pandas Analysis Agent] ──► [Response Synthesizer]
   │                │                           │
   ▼                ▼                           ▼
Database        DataFrame                  Final Answer
```

- **SQL Agent:** Converts user questions to SQL, queries the database, and returns results.
- **Pandas Analysis Agent:** Receives SQL results, performs advanced analysis using pandas.
- **Response Synthesizer:** Formats and returns the final answer to the user.

---

## Project Structure

```
DataPilotAI/
├── main.py                  # CLI entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (API keys, etc.)
├── .gitignore               # Files/folders to ignore in git
├── README.md                # Project documentation
├── data/
│   ├── May24_April25_INC_FRs.xlsx  # Example data source
│   └── tickets.db           # SQLite database (auto-generated)
└── rag_agent/
    ├── agent/
    │   ├── agents.py        # Agent definitions (SQL, pandas)
    │   ├── graph.py         # Workflow graph (node connections)
    │   └── state.py         # State structure for agent communication
    └── data_pipeline/
        ├── ingest.py        # Data ingestion and cleaning
        └── database.py      # Database engine setup
```

---

## Getting Started

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd DataPilotAI
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```sh
python -m venv env
./env/Scripts/activate  # On Windows
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory (see `.env.example` if provided) and add your API credentials for LLM access.


### 4. Add or Replace Your Data
You can use your own Excel file for analysis:

- Place your Excel file in the `data/` directory (e.g., `data/YourData.xlsx`).
- In `main.py`, update the path in the line:
   ```python
   db_engine = ingest_data('data/May24_April25_INC_FRs.xlsx')
   ```
   to point to your file, e.g.:
   ```python
   db_engine = ingest_data('data/YourData.xlsx')
   ```
- The system will ingest and process your file automatically on startup.

### 5. Run the CLI
```sh
python main.py
```

---

## Usage
- On startup, the tool ingests your Excel data and builds the agent workflow.
- Type your questions in natural language (e.g., "How many tickets were opened in May?").
- The system will process your query and return the final answer.
- Type `quit` or `exit` to end the session.

---

## Customization & Extensibility
- **Change data source:** Place your own Excel file in the `data/` directory and update the path in `main.py` as described above.
- **Integrate new LLMs:**
   - By default, the project uses Gen AI Hub for LLM access.
   - You can also use OpenAI models (such as GPT-3.5 or GPT-4) by updating the LLM initialization in `agents.py` to use `langchain-openai` instead of Gen AI Hub. Make sure your `.env` contains the appropriate OpenAI API keys.

---

## License
[MIT License](LICENSE)  

---

## Acknowledgments
- Built with LangChain, LangGraph, and Generative AI Hub.
- Inspired by best practices in multi-agent data analysis and LLM orchestration.

---

## Contact
For questions or support, please contact the project maintainer.
