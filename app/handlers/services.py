"""
Service order handlers with step-by-step selection.
"""

import json
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from app.core.states import ServiceFormStates
from app.core.service_categories import SERVICE_CATEGORIES
from app.models.application import Application, ApplicationType
from app.models.user import User
from app.services.application import ApplicationService
from app.services.notification import NotificationService
from app.utils.keyboards import (
    create_services_keyboard, create_subcategories_keyboard, 
    create_budget_keyboard, create_timeline_keyboard,
    create_content_keyboard, create_design_keyboard,
    create_support_keyboard, create_additional_options_keyboard,
    create_final_step_keyboard, create_main_menu_keyboard,
    create_cancel_keyboard, create_confirmation_keyboard,
    get_main_menu
)
from app.core.logger import get_logger

logger = get_logger(__name__)

services_router = Router()


@services_router.callback_query(F.data == "order_service")
async def start_service_selection(callback: CallbackQuery, state: FSMContext):
    """Start service selection process."""
    await state.clear()
    await state.set_state(ServiceFormStates.waiting_for_service)
    
    # Всегда удаляем предыдущее сообщение и отправляем новое с фото
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="https://i.ibb.co/kfTJqZx/B5-C581-C7-51-E9-4-BEF-B66-B-0615-B766-C386.png",
        caption="🛠 <b>ВЫБЕРИТЕ УСЛУГУ</b>\n\n"
                "Выберите категорию услуги из списка ниже:",
        reply_markup=create_services_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data.startswith("service:"), ServiceFormStates.waiting_for_service)
async def handle_service_selection(callback: CallbackQuery, state: FSMContext):
    """Handle service selection."""
    service = callback.data.split(":", 1)[1]
    await state.update_data(service=service)
    await state.set_state(ServiceFormStates.waiting_for_subcategory)
    
    # Получаем описания подкатегорий
    subcategories = SERVICE_CATEGORIES[service]["subcategories"]
    description_text = "\n".join([f"• <b>{name}</b> - {desc}" for name, desc in subcategories.items()])
    
    await callback.message.delete()
    await callback.message.answer(
        f"📋 <b>ВЫБЕРИТЕ ТИП: {service}</b>\n\n"
        f"{description_text}\n\n"
        "Выберите подходящий вариант:",
        reply_markup=create_subcategories_keyboard(service),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data.startswith("subcategory:"), ServiceFormStates.waiting_for_subcategory)
async def handle_subcategory_selection(callback: CallbackQuery, state: FSMContext):
    """Handle subcategory selection."""
    subcategory = callback.data.split(":", 1)[1]
    await state.update_data(subcategory=subcategory)
    await state.set_state(ServiceFormStates.waiting_for_budget)
    
    # Получаем данные о сервисе для показа бюджетов
    data = await state.get_data()
    service = data["service"]
    
    await callback.message.delete()
    await callback.message.answer(
        f"💰 <b>ВЫБЕРИТЕ БЮДЖЕТ</b>\n\n"
        f"<b>Услуга:</b> {service}\n"
        f"<b>Тип:</b> {subcategory}\n\n"
        "Выберите подходящий бюджет для вашего проекта:",
        reply_markup=create_budget_keyboard(service),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data.startswith("budget:"), ServiceFormStates.waiting_for_budget)
async def handle_budget_selection(callback: CallbackQuery, state: FSMContext):
    """Handle budget selection."""
    budget = callback.data.split(":", 1)[1]
    await state.update_data(budget=budget)
    await state.set_state(ServiceFormStates.waiting_for_timeline)
    
    await callback.message.delete()
    await callback.message.answer(
        f"⏰ <b>ВЫБЕРИТЕ СРОКИ</b>\n\n"
        f"<b>Бюджет:</b> {budget}\n\n"
        "В какие сроки нужно выполнить проект?",
        reply_markup=create_timeline_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data.startswith("timeline:"), ServiceFormStates.waiting_for_timeline)
async def handle_timeline_selection(callback: CallbackQuery, state: FSMContext):
    """Handle timeline selection."""
    timeline = callback.data.split(":", 1)[1]
    await state.update_data(timeline=timeline)
    await state.set_state(ServiceFormStates.waiting_for_content)
    
    await callback.message.delete()
    await callback.message.answer(
        f"📄 <b>КОНТЕНТ ДЛЯ ПРОЕКТА</b>\n\n"
        f"<b>Сроки:</b> {timeline}\n\n"
        "У вас есть готовый контент (тексты, фото, видео)?",
        reply_markup=create_content_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data.startswith("content:"), ServiceFormStates.waiting_for_content)
async def handle_content_selection(callback: CallbackQuery, state: FSMContext):
    """Handle content availability selection."""
    content = callback.data.split(":", 1)[1]
    await state.update_data(has_content=content)
    await state.set_state(ServiceFormStates.waiting_for_design)
    
    await callback.message.delete()
    await callback.message.answer(
        f"🎨 <b>ДИЗАЙН ПРОЕКТА</b>\n\n"
        f"<b>Контент:</b> {content}\n\n"
        "У вас есть готовый дизайн-макет?",
        reply_markup=create_design_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data.startswith("design:"), ServiceFormStates.waiting_for_design)
async def handle_design_selection(callback: CallbackQuery, state: FSMContext):
    """Handle design availability selection."""
    design = callback.data.split(":", 1)[1]
    await state.update_data(has_design=design)
    await state.set_state(ServiceFormStates.waiting_for_support)
    
    await callback.message.delete()
    await callback.message.answer(
        f"🛡 <b>УРОВЕНЬ ПОДДЕРЖКИ</b>\n\n"
        f"<b>Дизайн:</b> {design}\n\n"
        "Какой уровень поддержки вам нужен после запуска?",
        reply_markup=create_support_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data.startswith("support:"), ServiceFormStates.waiting_for_support)
async def handle_support_selection(callback: CallbackQuery, state: FSMContext):
    """Handle support level selection."""
    support = callback.data.split(":", 1)[1]
    await state.update_data(support_level=support)
    await state.set_state(ServiceFormStates.waiting_for_additional_options)
    
    # Получаем сервис для показа специфичных опций
    data = await state.get_data()
    service = data["service"]
    
    await callback.message.delete()
    await callback.message.answer(
        f"⚙️ <b>ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ</b>\n\n"
        f"<b>Поддержка:</b> {support}\n\n"
        f"<b>Выбрано опций:</b> 0\n\n"
        "Выберите дополнительные опции которые вам нужны.\n"
        "Можно выбрать несколько вариантов:",
        reply_markup=create_additional_options_keyboard(service, []),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data.startswith("option:"), ServiceFormStates.waiting_for_additional_options)
async def handle_additional_option(callback: CallbackQuery, state: FSMContext):
    """Handle additional option selection."""
    option = callback.data.split(":", 1)[1]
    
    # Получаем текущие опции
    data = await state.get_data()
    current_options = data.get("additional_options", [])
    
    # Добавляем или удаляем опцию
    if option in current_options:
        current_options.remove(option)
        await callback.answer("❌ Опция убрана")
    else:
        current_options.append(option)
        await callback.answer("✅ Опция добавлена")
    
    await state.update_data(additional_options=current_options)
    
    # Обновляем сообщение
    service = data["service"]
    
    await callback.message.delete()
    await callback.message.answer(
        f"⚙️ <b>ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ</b>\n\n"
        f"<b>Поддержка:</b> {data.get('support_level', '')}\n\n"
        f"<b>Выбрано опций:</b> {len(current_options)}\n\n"
        "Выберите дополнительные опции которые вам нужны.\n"
        "Можно выбрать несколько вариантов:",
        reply_markup=create_additional_options_keyboard(service, current_options),
        parse_mode="HTML"
    )


@services_router.callback_query(F.data == "skip_options", ServiceFormStates.waiting_for_additional_options)
async def skip_additional_options(callback: CallbackQuery, state: FSMContext):
    """Skip additional options."""
    await callback.answer("⏭ Пропускаем опции")
    await state.update_data(additional_options=[])
    await show_final_step(callback, state)


@services_router.callback_query(F.data == "options_done", ServiceFormStates.waiting_for_additional_options)
async def finish_additional_options(callback: CallbackQuery, state: FSMContext):
    """Finish selecting additional options."""
    await callback.answer("✅ Опции выбраны")
    await show_final_step(callback, state)


async def show_final_step(callback: CallbackQuery, state: FSMContext):
    """Show final step - description or skip."""
    await state.set_state(ServiceFormStates.waiting_for_description)
    
    data = await state.get_data()
    options_text = ", ".join(data.get("additional_options", [])) or "Не выбрано"
    
    await callback.message.delete()
    await callback.message.answer(
        f"📝 <b>ДОПОЛНИТЕЛЬНОЕ ОПИСАНИЕ</b>\n\n"
        f"<b>Доп. опции:</b> {options_text}\n\n"
        "Хотите добавить подробное описание вашего проекта?\n"
        "Это поможет нам лучше понять ваши потребности.",
        reply_markup=create_final_step_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data == "add_description", ServiceFormStates.waiting_for_description)
async def request_description(callback: CallbackQuery, state: FSMContext):
    """Request project description."""
    await callback.message.delete()
    await callback.message.answer(
        "📝 <b>ОПИСАНИЕ ПРОЕКТА</b>\n\n"
        "Опишите ваш проект подробнее:\n"
        "• Цели и задачи\n"
        "• Особые требования\n"
        "• Примеры работ\n"
        "• Любые дополнительные детали\n\n"
        "Напишите ваше описание одним сообщением:",
        reply_markup=create_cancel_keyboard("service"),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data == "skip_description", ServiceFormStates.waiting_for_description)
async def skip_description(callback: CallbackQuery, state: FSMContext):
    """Skip description and proceed to contact info."""
    await callback.answer("⏭ Пропускаем описание")
    await state.update_data(description="")
    await request_contact_info(callback, state)


@services_router.message(ServiceFormStates.waiting_for_description)
async def handle_description(message: Message, state: FSMContext):
    """Handle project description."""
    await state.update_data(description=message.text)
    await request_contact_info(message, state)


async def request_contact_info(message_or_callback, state: FSMContext):
    """Request contact information."""
    await state.set_state(ServiceFormStates.waiting_for_name)
    
    text = (
        "👤 <b>ВАШИ КОНТАКТНЫЕ ДАННЫЕ</b>\n\n"
        "Пожалуйста, укажите ваше имя:"
    )
    
    # Проверяем тип объекта более точно
    from aiogram.types import CallbackQuery, Message
    
    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.delete()
        await message_or_callback.message.answer(
            text,
            reply_markup=create_cancel_keyboard("service"),
            parse_mode="HTML"
        )
        await message_or_callback.answer()  # ВАЖНО! Закрываем callback
    elif isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            text,
            reply_markup=create_cancel_keyboard("service"),
            parse_mode="HTML"
        )


@services_router.message(ServiceFormStates.waiting_for_name)
async def handle_name(message: Message, state: FSMContext):
    """Handle user name."""
    await state.update_data(name=message.text)
    await state.set_state(ServiceFormStates.waiting_for_contact)
    
    await message.answer(
        "📱 <b>СПОСОБ СВЯЗИ</b>\n\n"
        "Выберите удобный способ связи:",
        reply_markup=create_contact_method_keyboard(),
        parse_mode="HTML"
    )


def create_contact_method_keyboard():
    """Create keyboard for contact method selection."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = [
        [InlineKeyboardButton(text="📞 Телефон", callback_data="contact_method:phone")],
        [InlineKeyboardButton(text="💬 Telegram", callback_data="contact_method:telegram")],
        [InlineKeyboardButton(text="📧 Email", callback_data="contact_method:email")],
        [InlineKeyboardButton(text="🌐 WhatsApp", callback_data="contact_method:whatsapp")],
        [InlineKeyboardButton(text="✏️ Ввести вручную", callback_data="contact_method:manual")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_service")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@services_router.callback_query(F.data.startswith("contact_method:"))
async def handle_contact_method(callback: CallbackQuery, state: FSMContext):
    """Handle contact method selection."""
    method = callback.data.split(":", 1)[1]
    
    if method == "phone":
        text = "📞 <b>НОМЕР ТЕЛЕФОНА</b>\n\nВведите ваш номер телефона:"
    elif method == "telegram":
        text = "💬 <b>TELEGRAM</b>\n\nВведите ваш @username в Telegram:"
    elif method == "email":
        text = "📧 <b>EMAIL</b>\n\nВведите ваш email адрес:"
    elif method == "whatsapp":
        text = "🌐 <b>WHATSAPP</b>\n\nВведите ваш номер для WhatsApp:"
    else:  # manual
        text = "✏️ <b>КОНТАКТ</b>\n\nВведите любой удобный способ связи:"
    
    await callback.message.delete()
    await callback.message.answer(
        text,
        reply_markup=create_cancel_keyboard("service"),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.message(ServiceFormStates.waiting_for_contact)
async def handle_contact(message: Message, state: FSMContext, db: Session):
    """Handle contact info and show confirmation."""
    await state.update_data(contact=message.text)
    
    # Показываем сводку заявки
    data = await state.get_data()
    
    summary = f"📋 <b>ПОДТВЕРЖДЕНИЕ ЗАЯВКИ</b>\n\n"
    summary += f"👤 <b>Имя:</b> {data['name']}\n"
    summary += f"📱 <b>Контакт:</b> {data['contact']}\n\n"
    summary += f"🎯 <b>Услуга:</b> {data['service']}\n"
    summary += f"📋 <b>Тип:</b> {data['subcategory']}\n"
    summary += f"💰 <b>Бюджет:</b> {data['budget']}\n"
    summary += f"⏰ <b>Сроки:</b> {data['timeline']}\n"
    summary += f"📄 <b>Контент:</b> {data['has_content']}\n"
    summary += f"🎨 <b>Дизайн:</b> {data['has_design']}\n"
    summary += f"🛡 <b>Поддержка:</b> {data['support_level']}\n"
    
    if data.get('additional_options'):
        summary += f"⚙️ <b>Доп. опции:</b> {', '.join(data['additional_options'])}\n"
    
    if data.get('description'):
        summary += f"\n📝 <b>Описание:</b>\n{data['description']}\n"
    
    summary += "\n✅ Проверьте данные и отправьте заявку"
    
    await message.answer(
        summary,
        reply_markup=create_confirmation_keyboard(),
        parse_mode="HTML"
    )


@services_router.callback_query(F.data == "confirm_application")
async def confirm_application(callback: CallbackQuery, state: FSMContext, db: Session, user: User):
    """Confirm and save application."""
    data = await state.get_data()
    
    # Проверяем что все обязательные данные есть
    required_fields = ['name', 'contact', 'service', 'subcategory', 'budget', 'timeline', 'has_content', 'has_design', 'support_level']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        await callback.answer(f"❌ Не хватает данных: {', '.join(missing_fields)}", show_alert=True)
        logger.error(f"Missing required fields for user {user.telegram_id}: {missing_fields}")
        return
    
    # Создаем заявку
    application_service = ApplicationService(db)
    
    additional_options_json = json.dumps(data.get('additional_options', []), ensure_ascii=False)
    
    application = application_service.create_application(
        user_id=user.id,
        application_type=ApplicationType.SERVICE,
        name=data['name'],
        contact=data['contact'],
        service=data['service'],
        subcategory=data.get('subcategory'),
        budget=data.get('budget'),
        timeline=data.get('timeline'),
        has_content=data.get('has_content'),
        has_design=data.get('has_design'),
        support_level=data.get('support_level'),
        additional_options=additional_options_json,
        description=data.get('description', '')
    )
    
    # Отправляем уведомление админу
    try:
        notification_service = NotificationService(callback.bot)
        await notification_service.send_application_notification(application)
    except Exception as e:
        # Не блокируем пользователя если не удалось отправить уведомление
        logger.error(f"Failed to send notification: {e}")
        pass
    
    await state.clear()
    
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="https://i.ibb.co/3m4bCScL/AB6-FA99-A-E1-CA-4498-9-DE7-2-A64-DA7-B96-E4.png",
        caption=f"✅ <b>ЗАЯВКА ОТПРАВЛЕНА!</b>\n\n"
               f"Номер заявки: <b>#{application.id}</b>\n\n"
               f"Спасибо за ваш заказ! Мы рассмотрим заявку и свяжемся с вами "
               f"в ближайшее время для уточнения деталей.\n\n"
               f"📞 Если у вас есть срочные вопросы, можете написать напрямую: @pavel_xdev\n\n"
               f"🎯 <b>Выберите, что вас интересует:</b>",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer("✅ Заявка успешно отправлена!")


# ALL NAVIGATION CALLBACKS WITH DELETE+ANSWER
@services_router.callback_query(F.data == "back_to_services")
async def back_to_services(callback: CallbackQuery, state: FSMContext):
    """Go back to services selection."""
    await start_service_selection(callback, state)


@services_router.callback_query(F.data == "back_to_subcategory")
async def back_to_subcategory(callback: CallbackQuery, state: FSMContext):
    """Go back to subcategory selection."""
    data = await state.get_data()
    service = data["service"]
    await state.set_state(ServiceFormStates.waiting_for_subcategory)
    
    subcategories = SERVICE_CATEGORIES[service]["subcategories"]
    description_text = "\n".join([f"• <b>{name}</b> - {desc}" for name, desc in subcategories.items()])
    
    await callback.message.delete()
    await callback.message.answer(
        f"📋 <b>ВЫБЕРИТЕ ТИП: {service}</b>\n\n"
        f"{description_text}\n\n"
        "Выберите подходящий вариант:",
        reply_markup=create_subcategories_keyboard(service),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data == "back_to_budget")
async def back_to_budget(callback: CallbackQuery, state: FSMContext):
    """Go back to budget selection."""
    data = await state.get_data()
    service = data["service"]
    subcategory = data["subcategory"]
    await state.set_state(ServiceFormStates.waiting_for_budget)
    
    await callback.message.delete()
    await callback.message.answer(
        f"💰 <b>ВЫБЕРИТЕ БЮДЖЕТ</b>\n\n"
        f"<b>Услуга:</b> {service}\n"
        f"<b>Тип:</b> {subcategory}\n\n"
        "Выберите подходящий бюджет для вашего проекта:",
        reply_markup=create_budget_keyboard(service),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data == "back_to_timeline")
async def back_to_timeline(callback: CallbackQuery, state: FSMContext):
    """Go back to timeline selection."""
    data = await state.get_data()
    await state.set_state(ServiceFormStates.waiting_for_timeline)
    
    await callback.message.delete()
    await callback.message.answer(
        f"⏰ <b>ВЫБЕРИТЕ СРОКИ</b>\n\n"
        f"<b>Бюджет:</b> {data.get('budget', '')}\n\n"
        "В какие сроки нужно выполнить проект?",
        reply_markup=create_timeline_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data == "back_to_content")
async def back_to_content(callback: CallbackQuery, state: FSMContext):
    """Go back to content selection."""
    data = await state.get_data()
    await state.set_state(ServiceFormStates.waiting_for_content)
    
    await callback.message.delete()
    await callback.message.answer(
        f"📄 <b>КОНТЕНТ ДЛЯ ПРОЕКТА</b>\n\n"
        f"<b>Сроки:</b> {data.get('timeline', '')}\n\n"
        "У вас есть готовый контент (тексты, фото, видео)?",
        reply_markup=create_content_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data == "back_to_design")
async def back_to_design(callback: CallbackQuery, state: FSMContext):
    """Go back to design selection."""
    data = await state.get_data()
    await state.set_state(ServiceFormStates.waiting_for_design)
    
    await callback.message.delete()
    await callback.message.answer(
        f"🎨 <b>ДИЗАЙН ПРОЕКТА</b>\n\n"
        f"<b>Контент:</b> {data.get('has_content', '')}\n\n"
        "У вас есть готовый дизайн-макет?",
        reply_markup=create_design_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data == "back_to_support")
async def back_to_support(callback: CallbackQuery, state: FSMContext):
    """Go back to support selection."""
    data = await state.get_data()
    await state.set_state(ServiceFormStates.waiting_for_support)
    
    await callback.message.delete()
    await callback.message.answer(
        f"🛡 <b>УРОВЕНЬ ПОДДЕРЖКИ</b>\n\n"
        f"<b>Дизайн:</b> {data.get('has_design', '')}\n\n"
        "Какой уровень поддержки вам нужен после запуска?",
        reply_markup=create_support_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data == "back_to_options")
async def back_to_options(callback: CallbackQuery, state: FSMContext):
    """Go back to additional options."""
    data = await state.get_data()
    service = data["service"]
    await state.set_state(ServiceFormStates.waiting_for_additional_options)
    
    current_options = data.get("additional_options", [])
    
    await callback.message.delete()
    await callback.message.answer(
        f"⚙️ <b>ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ</b>\n\n"
        f"<b>Поддержка:</b> {data.get('support_level', '')}\n\n"
        f"<b>Выбрано опций:</b> {len(current_options)}\n\n"
        "Выберите дополнительные опции которые вам нужны.\n"
        "Можно выбрать несколько вариантов:",
        reply_markup=create_additional_options_keyboard(service, current_options),
        parse_mode="HTML"
    )
    await callback.answer()


@services_router.callback_query(F.data == "cancel_service")
async def cancel_service_form(callback: CallbackQuery, state: FSMContext):
    """Cancel service form."""
    await state.clear()
    
    # Всегда удаляем и отправляем новое сообщение с фото
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="https://i.ibb.co/3m4bCScL/AB6-FA99-A-E1-CA-4498-9-DE7-2-A64-DA7-B96-E4.png",
        caption="❌ <b>Заявка отменена</b>\n\n"
                "Вы можете начать заново в любое время.\n\n"
                "🎯 <b>Выберите, что вас интересует:</b>",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer("❌ Заявка отменена") 