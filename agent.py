from langchain.agents import create_agent
from langchain.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from tools import get_menu, place_order
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.4
)

memory = InMemorySaver()

agent = create_agent(
    model,
    tools=[get_menu, place_order],
    system_prompt=SystemMessage(
        content="""You are a food ordering assistant.

        Rules:
        - Only order items from the menu
        - Always confirm before placing order
        - Be polite and concise"""
    ),
    checkpointer=memory
)

