"""
FSM States for handling user interactions.
"""

from aiogram.fsm.state import State, StatesGroup


class ServiceFormStates(StatesGroup):
    """States for service order form with detailed selection."""
    waiting_for_service = State()
    waiting_for_subcategory = State() 
    waiting_for_budget = State()
    waiting_for_timeline = State()
    waiting_for_content = State()
    waiting_for_design = State()
    waiting_for_support = State()
    waiting_for_additional_options = State()
    waiting_for_description = State()
    waiting_for_name = State()
    waiting_for_contact = State()


class TeamFormStates(StatesGroup):
    """States for team application form."""
    waiting_for_name = State()
    waiting_for_activity = State()
    waiting_for_experience = State()
    waiting_for_portfolio = State()
    waiting_for_contact = State()


class AdminStates(StatesGroup):
    """States for admin operations."""
    waiting_for_broadcast_message = State()
    waiting_for_broadcast_confirmation = State() 