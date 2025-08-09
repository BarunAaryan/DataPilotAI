import uuid
from dotenv import load_dotenv
from rag_agent.data_pipeline.ingest import ingest_data
from rag_agent.agent.graph import create_graph

def main():
    load_dotenv()
    #print("Environment variables loaded.")

    # data ingestion
    db_engine = ingest_data('data/May24_April25_INC_FRs.xlsx')
    
    if db_engine is None:
        print("Database engine could not be initialized. Exiting.")
        return

    # Agent and graph initialization
    app = create_graph(db_engine)

    # Generate a unique conversation ID for this session
    conversation_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": conversation_id}}

    print("\nWelcome to LogIG. Type 'quit' or 'exit' to end.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Exiting. Goodbye!")
            break

        inputs = {
            "question": user_input,
            "messages": [], 
        }
        
        print("\nAgent is thinking...")
        last_output = None
        for output in app.stream(inputs, config=config):
            last_output = output
        
        if last_output is None:
            print("Agent did not return a state. Please try again.")
            continue

        # The final answer is in the output of the 'response_synthesizer' node
        final_answer = "Sorry, I couldn't find an answer."
        if "response_synthesizer" in last_output:
            final_answer = last_output["response_synthesizer"].get("final_answer", final_answer)

        print(f"\nAgent: {final_answer}")

if __name__ == "__main__":
    main()