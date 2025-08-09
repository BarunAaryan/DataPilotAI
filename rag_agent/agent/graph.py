import pandas as pd
import ast
from langgraph.graph import StateGraph, END
from.state import AgentState
from.agents import create_agents

def create_graph(db_engine):
    sql_agent_executor, create_pandas_agent_func = create_agents(db_engine)

    # Node Functions    
    def sql_retrieval_node(state: AgentState):
        print("---NODE: SQL Data Retrieval---")
        question = state["question"]
        
        # Invoke SQL agent to get the raw data result
        result = sql_agent_executor.invoke({"input": question})
        
        # Update the state with the retrieved data
        return {"retrieved_data": result["output"]}

    def analysis_node(state: AgentState):
        print("---NODE: Data Analysis---")
        question = state["question"]
        retrieved_data_str = state["retrieved_data"]

        try:            
            data_list = ast.literal_eval(retrieved_data_str)
            # Convert list of data into a pandas DataFrame 
            df = pd.DataFrame(data_list)
            #print(f"Successfully created DataFrame with shape: {df.shape}")
        except (ValueError, SyntaxError):
            print(f"Could not parse data into DataFrame. Passing as text.")
            return {"analysis_result": retrieved_data_str}

        pandas_agent_executor = create_pandas_agent_func(df)

        # Invoke the pandas agent for analysis
        result = pandas_agent_executor.invoke({"input": question})
        
        return {"analysis_result": result["output"]}

    def response_synthesis_node(state: AgentState):
        print("---NODE: Response Synthesis---")
        analysis_result = state["analysis_result"]
        return {"final_answer": analysis_result}

    #Graph Building
    workflow = StateGraph(AgentState)

    # Add the nodes to the graph
    workflow.add_node("sql_agent", sql_retrieval_node)
    workflow.add_node("analysis_agent", analysis_node)
    workflow.add_node("response_synthesizer", response_synthesis_node)

    # This dictates the flow: sql_agent -> analysis_agent -> response_synthesizer -> END
    workflow.add_edge("sql_agent", "analysis_agent")
    workflow.add_edge("analysis_agent", "response_synthesizer")
    workflow.add_edge("response_synthesizer", END)

    workflow.set_entry_point("sql_agent")

    app = workflow.compile()
    print("Graph compiled successfully.")
    return app