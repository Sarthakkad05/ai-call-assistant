from langchain.tools import tool
from hotel_data import MENU

@tool
def get_menu():
    """Get the food menu with prices"""
    return MENU

@tool
def place_order(items: list[str]):
    """Place a food order"""
    for item in items:
        if item not in MENU:
            return f"{item} is not available."
    return f"Order confirmed: {items}"