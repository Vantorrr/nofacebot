"""
Modern keyboard utilities with enhanced design.
"""

from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.config import settings
from app.core.service_categories import SERVICE_CATEGORIES, GENERAL_OPTIONS


def get_main_menu() -> InlineKeyboardMarkup:
    """
    Get main menu keyboard with modern design.
    
    Returns:
        InlineKeyboardMarkup: Main menu keyboard
    """
    keyboard = InlineKeyboardBuilder()
    
    # Main action buttons with emojis
    keyboard.row(
        InlineKeyboardButton(
            text="🛠 Заказать услугу",
            callback_data="order_service"
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="👥 Присоединиться к команде", 
            callback_data="join_team"
        )
    )
    
    # Additional options
    keyboard.row(
        InlineKeyboardButton(
            text="📞 Связаться напрямую",
            callback_data="direct_contact"
        ),
        InlineKeyboardButton(
            text="ℹ️ О компании",
            callback_data="company_info"
        )
    )
    
    return keyboard.as_markup()


def get_services_menu() -> InlineKeyboardMarkup:
    """
    Get services selection keyboard.
    
    Returns:
        InlineKeyboardMarkup: Services menu keyboard
    """
    keyboard = InlineKeyboardBuilder()
    
    # Services grid (2 columns for better UX)
    for i in range(0, len(settings.services), 2):
        row_buttons = []
        
        # First service in row
        service = settings.services[i]
        row_buttons.append(
            InlineKeyboardButton(
                text=service,
                callback_data=f"service_{i}"
            )
        )
        
        # Second service in row (if exists)
        if i + 1 < len(settings.services):
            service = settings.services[i + 1]
            row_buttons.append(
                InlineKeyboardButton(
                    text=service,
                    callback_data=f"service_{i + 1}"
                )
            )
        
        keyboard.row(*row_buttons)
    
    # Navigation
    keyboard.row(
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_to_main"
        ),
        InlineKeyboardButton(
            text="💬 Консультация",
            callback_data="direct_contact"
        )
    )
    
    return keyboard.as_markup()


def get_back_button(callback_data: str = "back_to_main") -> InlineKeyboardMarkup:
    """
    Get simple back button.
    
    Args:
        callback_data: Callback data for back button
        
    Returns:
        InlineKeyboardMarkup: Back button keyboard
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=callback_data
        )
    )
    return keyboard.as_markup()


def get_cancel_button() -> InlineKeyboardMarkup:
    """
    Get cancel button for service forms.
    
    Returns:
        InlineKeyboardMarkup: Cancel button keyboard
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="❌ Отменить",
            callback_data="cancel_service"
        )
    )
    return keyboard.as_markup()


def get_team_cancel_button() -> InlineKeyboardMarkup:
    """
    Get cancel button for team forms.
    
    Returns:
        InlineKeyboardMarkup: Cancel button keyboard
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="❌ Отменить",
            callback_data="cancel_team"
        ),
        InlineKeyboardButton(
            text="🔙 В меню",
            callback_data="back_to_main"
        )
    )
    return keyboard.as_markup()


def get_confirmation_keyboard(
    confirm_text: str = "✅ Подтвердить",
    cancel_text: str = "❌ Отменить",
    confirm_data: str = "confirm",
    cancel_data: str = "cancel"
) -> InlineKeyboardMarkup:
    """
    Get confirmation keyboard.
    
    Args:
        confirm_text: Text for confirm button
        cancel_text: Text for cancel button
        confirm_data: Callback data for confirm
        cancel_data: Callback data for cancel
        
    Returns:
        InlineKeyboardMarkup: Confirmation keyboard
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text=confirm_text,
            callback_data=confirm_data
        ),
        InlineKeyboardButton(
            text=cancel_text,
            callback_data=cancel_data
        )
    )
    return keyboard.as_markup()


def get_admin_keyboard(application_id: int) -> InlineKeyboardMarkup:
    """
    Get admin keyboard for application management.
    
    Args:
        application_id: Application ID
        
    Returns:
        InlineKeyboardMarkup: Admin keyboard
    """
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(
            text="✅ Принять",
            callback_data=f"admin_approve_{application_id}"
        ),
        InlineKeyboardButton(
            text="❌ Отклонить",
            callback_data=f"admin_reject_{application_id}"
        )
    )
    
    keyboard.row(
        InlineKeyboardButton(
            text="💬 Ответить",
            callback_data=f"admin_reply_{application_id}"
        ),
        InlineKeyboardButton(
            text="📊 Детали",
            callback_data=f"admin_details_{application_id}"
        )
    )
    
    return keyboard.as_markup()


def get_pagination_keyboard(
    current_page: int,
    total_pages: int,
    callback_prefix: str,
    show_info: bool = True
) -> InlineKeyboardMarkup:
    """
    Get pagination keyboard.
    
    Args:
        current_page: Current page number (1-based)
        total_pages: Total number of pages
        callback_prefix: Prefix for callback data
        show_info: Whether to show page info
        
    Returns:
        InlineKeyboardMarkup: Pagination keyboard
    """
    keyboard = InlineKeyboardBuilder()
    
    buttons = []
    
    # Previous page
    if current_page > 1:
        buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"{callback_prefix}_{current_page - 1}"
            )
        )
    
    # Page info
    if show_info and total_pages > 1:
        buttons.append(
            InlineKeyboardButton(
                text=f"{current_page}/{total_pages}",
                callback_data="page_info"
            )
        )
    
    # Next page
    if current_page < total_pages:
        buttons.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"{callback_prefix}_{current_page + 1}"
            )
        )
    
    if buttons:
        keyboard.row(*buttons)
    
    return keyboard.as_markup()


def create_services_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard with all services."""
    buttons = []
    for service in SERVICE_CATEGORIES.keys():
        buttons.append([InlineKeyboardButton(
            text=service, 
            callback_data=f"service:{service}"
        )])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_subcategories_keyboard(service: str) -> InlineKeyboardMarkup:
    """Create keyboard with subcategories for selected service."""
    buttons = []
    
    if service in SERVICE_CATEGORIES:
        subcategories = SERVICE_CATEGORIES[service]["subcategories"]
        for subcat, description in subcategories.items():
            buttons.append([InlineKeyboardButton(
                text=subcat,
                callback_data=f"subcategory:{subcat}"
            )])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад к услугам", callback_data="back_to_services")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_budget_keyboard(service: str) -> InlineKeyboardMarkup:
    """Create keyboard with budget options for selected service."""
    buttons = []
    
    if service in SERVICE_CATEGORIES:
        budgets = SERVICE_CATEGORIES[service]["budgets"]
        for budget in budgets:
            buttons.append([InlineKeyboardButton(
                text=budget,
                callback_data=f"budget:{budget}"
            )])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_subcategory")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_timeline_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard with timeline options."""
    buttons = []
    
    for timeline, description in GENERAL_OPTIONS["timeline"].items():
        buttons.append([InlineKeyboardButton(
            text=timeline,
            callback_data=f"timeline:{timeline}"
        )])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_budget")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_content_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for content availability."""
    buttons = []
    
    for option, description in GENERAL_OPTIONS["has_content"].items():
        buttons.append([InlineKeyboardButton(
            text=option,
            callback_data=f"content:{option}"
        )])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_timeline")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_design_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for design availability."""
    buttons = []
    
    for option, description in GENERAL_OPTIONS["has_design"].items():
        buttons.append([InlineKeyboardButton(
            text=option,
            callback_data=f"design:{option}"
        )])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_content")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_support_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for support level."""
    buttons = []
    
    for option, description in GENERAL_OPTIONS["support"].items():
        buttons.append([InlineKeyboardButton(
            text=option,
            callback_data=f"support:{option}"
        )])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_design")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_additional_options_keyboard(service: str, selected_options: list = None) -> InlineKeyboardMarkup:
    """Create keyboard for additional service-specific options."""
    if selected_options is None:
        selected_options = []
    
    buttons = []
    
    if service in SERVICE_CATEGORIES:
        options = SERVICE_CATEGORIES[service]["options"]
        for option_key, option_name in options.items():
            # Показываем ✅ если опция выбрана, иначе ⭕
            if option_key in selected_options:
                text = f"✅ {option_name}"
            else:
                text = f"⭕ {option_name}"
            
            buttons.append([InlineKeyboardButton(
                text=text,
                callback_data=f"option:{option_key}"
            )])
    
    buttons.extend([
        [InlineKeyboardButton(text="⏭ Пропустить", callback_data="skip_options")],
        [InlineKeyboardButton(text="✅ Готово", callback_data="options_done")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_support")]
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_final_step_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for final step (description or skip)."""
    buttons = [
        [InlineKeyboardButton(text="📝 Добавить описание", callback_data="add_description")],
        [InlineKeyboardButton(text="⏭ Пропустить", callback_data="skip_description")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_options")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_team_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for team application."""
    buttons = [
        [InlineKeyboardButton(text="📝 Подать заявку", callback_data="start_team_form")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Create main menu keyboard."""
    buttons = [
        [InlineKeyboardButton(text="🛠 Заказать услугу", callback_data="order_service")],
        [InlineKeyboardButton(text="👥 Стать частью команды", callback_data="join_team")],
        [InlineKeyboardButton(text="ℹ️ О компании", callback_data="company_info")],
        [InlineKeyboardButton(text="📞 Связаться напрямую", callback_data="direct_contact")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_contact_keyboard() -> InlineKeyboardMarkup:
    """Create contact keyboard."""
    buttons = [
        [InlineKeyboardButton(text="💬 Написать в Telegram", url="https://t.me/pavel_xdev")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """Create simple back to main menu keyboard."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
    ])


def create_cancel_keyboard(cancel_type: str = "service") -> InlineKeyboardMarkup:
    """Create cancel keyboard for forms."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel_{cancel_type}")]
    ])


def create_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Create confirmation keyboard for form submission."""
    buttons = [
        [InlineKeyboardButton(text="✅ Отправить заявку", callback_data="confirm_application")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_service")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons) 