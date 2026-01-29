from agent import agent
from langchain.messages import HumanMessage

# One call = one thread
thread_id = "call_001"   # later: phone number / session id

config = {
    "configurable": {
        "thread_id": thread_id
    }
}

print("AI Call Assistant started. Type 'exit' to stop.\n")

while True:
    user_input = input("Customer: ")
    if user_input.lower() == "exit":
        break

    response = agent.invoke(
        {
            "messages": [HumanMessage(content=user_input)]
        },
        config=config
    )

    print("Assistant:", response["messages"][-1].content)


