from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from os import getenv

load_dotenv()

@tool
def calculator(a:float, b:float) -> str:
    """Useful for performing basic arthimatic calculation with numbers"""
    print("\ncalculator tool has been called")
    return f"The Sum of {a} and {b} is {a+b}"

def main():
    model = ChatOpenAI(
        temperature=0,
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_API_BASE"),
        model=getenv("OPENAI_MODEL_NAME")
    )
    

    tools = [calculator]
    agent_executor = create_react_agent(model , tools)
    print("Welcome! I am your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculation or chat with me.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input =="quit":
            break
        
        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {
                "messages":[HumanMessage(content = user_input)]
            }
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content,end="")
        print()

if __name__=="__main__":
    main()
    

