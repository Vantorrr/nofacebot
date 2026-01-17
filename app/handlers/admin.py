"""
Admin panel for NOFACE.digital bot management.
"""

from datetime import datetime, timedelta
from typing import Optional
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.user import User
from app.models.application import Application, ApplicationType
from app.services.user import UserService
from app.services.application import ApplicationService
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)
router = Router(name="admin")


class BroadcastForm(StatesGroup):
    """States for broadcast message form."""
    waiting_for_message = State()


def is_admin(user_id: int) -> bool:
    """Check if user is admin."""
    return user_id in settings.admin_ids


def get_admin_menu():
    """Get admin main menu keyboard."""
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    keyboard = InlineKeyboardBuilder()
    
    # Основные функции
    keyboard.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
        InlineKeyboardButton(text="📝 Заявки", callback_data="admin_applications")
    )
    keyboard.row(
        InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users"),
        InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")
    )
    keyboard.row(
        InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_settings"),
        InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_refresh")
    )
    keyboard.row(
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")
    )
    
    return keyboard.as_markup()


def get_applications_menu():
    """Get applications management menu."""
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(text="🛠 Услуги", callback_data="admin_apps_services"),
        InlineKeyboardButton(text="👥 Команда", callback_data="admin_apps_team")
    )
    keyboard.row(
        InlineKeyboardButton(text="📋 Все заявки", callback_data="admin_apps_all"),
        InlineKeyboardButton(text="⭐ Новые", callback_data="admin_apps_new")
    )
    keyboard.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_main")
    )
    
    return keyboard.as_markup()


@router.message(Command("admin"))
async def admin_main(
    message: Message,
    user: User,
    db: Session
):
    """Main admin panel."""
    if not is_admin(user.telegram_id):
        await message.answer("❌ У вас нет прав администратора")
        return
    
    logger.info(f"Admin {user.telegram_id} opened admin panel")
    
    # Получаем базовую статистику
    user_service = UserService(db)
    app_service = ApplicationService(db)
    
    total_users = user_service.get_users_count()
    total_applications = app_service.get_applications_count()
    
    # Новые заявки за сегодня
    today = datetime.now().date()
    new_apps_today = db.query(Application).filter(
        func.date(Application.created_at) == today
    ).count()
    
    admin_text = (
        f"👨‍💻 <b>Админ-панель NOFACE.digital</b>\n\n"
        f"📊 <b>Быстрая статистика:</b>\n"
        f"👥 Пользователи: <b>{total_users}</b>\n"
        f"📝 Всего заявок: <b>{total_applications}</b>\n"
        f"🆕 Новых сегодня: <b>{new_apps_today}</b>\n\n"
        f"🕐 <b>Время:</b> {datetime.now().strftime('%H:%M, %d.%m.%Y')}\n\n"
        f"🎛 <b>Выберите раздел:</b>"
    )
    
    await message.answer(
        admin_text,
        reply_markup=get_admin_menu(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin_main")
async def admin_main_callback(
    callback: CallbackQuery,
    user: User,
    db: Session
):
    """Return to admin main."""
    if not is_admin(user.telegram_id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    # Получаем статистику
    user_service = UserService(db)
    app_service = ApplicationService(db)
    
    total_users = user_service.get_users_count()
    total_applications = app_service.get_applications_count()
    
    today = datetime.now().date()
    new_apps_today = db.query(Application).filter(
        func.date(Application.created_at) == today
    ).count()
    
    admin_text = (
        f"👨‍💻 <b>Админ-панель NOFACE.digital</b>\n\n"
        f"📊 <b>Быстрая статистика:</b>\n"
        f"👥 Пользователи: <b>{total_users}</b>\n"
        f"📝 Всего заявок: <b>{total_applications}</b>\n"
        f"🆕 Новых сегодня: <b>{new_apps_today}</b>\n\n"
        f"🕐 <b>Время:</b> {datetime.now().strftime('%H:%M, %d.%m.%Y')}\n\n"
        f"🎛 <b>Выберите раздел:</b>"
    )
    
    await callback.message.edit_text(
        admin_text,
        reply_markup=get_admin_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_stats")
async def admin_statistics(
    callback: CallbackQuery,
    user: User,
    db: Session
):
    """Show detailed statistics."""
    if not is_admin(user.telegram_id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    # Детальная статистика
    user_service = UserService(db)
    
    total_users = user_service.get_users_count()
    
    # Статистика за периоды
    now = datetime.now()
    today = now.date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Новые пользователи
    new_users_today = db.query(User).filter(
        func.date(User.created_at) == today
    ).count()
    
    new_users_week = db.query(User).filter(
        User.created_at >= week_ago
    ).count()
    
    # Заявки
    total_apps = db.query(Application).count()
    service_apps = db.query(Application).filter(
        Application.type == ApplicationType.SERVICE
    ).count()
    team_apps = db.query(Application).filter(
        Application.type == ApplicationType.TEAM
    ).count()
    
    apps_today = db.query(Application).filter(
        func.date(Application.created_at) == today
    ).count()
    
    # Популярные услуги
    popular_services = db.query(
        Application.service,
        func.count(Application.id).label('count')
    ).filter(
        Application.type == ApplicationType.SERVICE,
        Application.service.isnot(None)
    ).group_by(Application.service).order_by(desc('count')).limit(3).all()
    
    stats_text = (
        f"📊 <b>Детальная статистика</b>\n\n"
        
        f"👥 <b>Пользователи:</b>\n"
        f"• Всего: <b>{total_users}</b>\n"
        f"• Сегодня: <b>{new_users_today}</b>\n"
        f"• За неделю: <b>{new_users_week}</b>\n\n"
        
        f"📝 <b>Заявки:</b>\n"
        f"• Всего: <b>{total_apps}</b>\n"
        f"• На услуги: <b>{service_apps}</b>\n"
        f"• В команду: <b>{team_apps}</b>\n"
        f"• Сегодня: <b>{apps_today}</b>\n\n"
    )
    
    if popular_services:
        stats_text += f"🔥 <b>Популярные услуги:</b>\n"
        for service, count in popular_services:
            service_short = service.split()[0] if service else "Услуга"
            stats_text += f"• {service_short}: <b>{count}</b>\n"
        stats_text += "\n"
    
    stats_text += f"🕐 <b>Обновлено:</b> {now.strftime('%H:%M:%S')}"
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_stats"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_main")
    )
    
    await callback.message.edit_text(
        stats_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_applications")
async def admin_applications_menu(
    callback: CallbackQuery,
    user: User
):
    """Show applications management menu."""
    if not is_admin(user.telegram_id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    apps_text = (
        f"📝 <b>Управление заявками</b>\n\n"
        f"🛠 <b>Услуги</b> - заявки на разработку\n"
        f"👥 <b>Команда</b> - анкеты кандидатов\n"
        f"📋 <b>Все заявки</b> - полный список\n"
        f"⭐ <b>Новые</b> - необработанные\n\n"
        f"📊 <b>Выберите категорию:</b>"
    )
    
    await callback.message.edit_text(
        apps_text,
        reply_markup=get_applications_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin_apps_"))
async def admin_applications_list(
    callback: CallbackQuery,
    user: User,
    db: Session
):
    """Show applications list."""
    if not is_admin(user.telegram_id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    filter_type = callback.data.split("_")[-1]
    
    # Формируем запрос
    query = db.query(Application).order_by(desc(Application.created_at))
    
    if filter_type == "services":
        query = query.filter(Application.type == ApplicationType.SERVICE)
        title = "🛠 Заявки на услуги"
    elif filter_type == "team":
        query = query.filter(Application.type == ApplicationType.TEAM)
        title = "👥 Заявки в команду"
    elif filter_type == "new":
        # Новые за последние 24 часа
        yesterday = datetime.now() - timedelta(days=1)
        query = query.filter(Application.created_at >= yesterday)
        title = "⭐ Новые заявки"
    else:
        title = "📋 Все заявки"
    
    applications = query.limit(10).all()
    
    if not applications:
        apps_text = f"{title}\n\n❌ <b>Заявок нет</b>"
    else:
        apps_text = f"{title}\n\n"
        
        for app in applications:
            date_str = app.created_at.strftime("%d.%m %H:%M")
            type_emoji = "🛠" if app.type == ApplicationType.SERVICE else "👥"
            
            if app.type == ApplicationType.SERVICE:
                service_short = app.service.split()[0] if app.service else "Услуга"
                apps_text += (
                    f"{type_emoji} <b>#{app.id}</b> | {date_str}\n"
                    f"👤 {app.name} | {service_short}\n"
                    f"📱 {app.contact}\n\n"
                )
            else:
                activity_short = app.activity.split()[0] if app.activity else "Специалист"
                apps_text += (
                    f"{type_emoji} <b>#{app.id}</b> | {date_str}\n"
                    f"👤 {app.name} | {activity_short}\n\n"
                )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data=callback.data),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_applications")
    )
    
    await callback.message.edit_text(
        apps_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_start(
    callback: CallbackQuery,
    user: User,
    state: FSMContext
):
    """Start broadcast message."""
    if not is_admin(user.telegram_id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    broadcast_text = (
        f"📢 <b>Рассылка сообщений</b>\n\n"
        f"📝 <b>Отправьте сообщение для рассылки</b>\n\n"
        f"⚠️ <b>Внимание:</b>\n"
        f"• Сообщение получат ВСЕ пользователи\n"
        f"• Отменить после отправки нельзя\n"
        f"• Поддерживается HTML-разметка\n\n"
        f"💬 <b>Введите текст сообщения:</b>"
    )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="❌ Отменить", callback_data="admin_main")
    )
    
    await callback.message.edit_text(
        broadcast_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    
    await state.set_state(BroadcastForm.waiting_for_message)
    await callback.answer()


@router.message(BroadcastForm.waiting_for_message)
async def admin_broadcast_send(
    message: Message,
    user: User,
    state: FSMContext,
    db: Session
):
    """Send broadcast message."""
    if not is_admin(user.telegram_id):
        await state.clear()
        return
    
    broadcast_message = message.text.strip()
    
    if len(broadcast_message) < 1:
        await message.answer("❌ Сообщение не может быть пустым")
        return
    
    # Получаем всех пользователей
    user_service = UserService(db)
    all_users = user_service.get_all_users()
    
    if not all_users:
        await message.answer("❌ Нет пользователей для рассылки")
        await state.clear()
        return
    
    # Подтверждение
    confirm_text = (
        f"📢 <b>Подтверждение рассылки</b>\n\n"
        f"👥 <b>Получатели:</b> {len(all_users)} пользователей\n\n"
        f"📝 <b>Сообщение:</b>\n"
        f"<code>{broadcast_message[:200]}{'...' if len(broadcast_message) > 200 else ''}</code>\n\n"
        f"❓ <b>Отправить рассылку?</b>"
    )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="✅ Отправить", callback_data="broadcast_confirm"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="admin_main")
    )
    
    # Сохраняем сообщение в состояние
    await state.update_data(broadcast_message=broadcast_message)
    
    await message.answer(
        confirm_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "broadcast_confirm")
async def admin_broadcast_confirm(
    callback: CallbackQuery,
    user: User,
    state: FSMContext,
    db: Session
):
    """Confirm and execute broadcast."""
    if not is_admin(user.telegram_id):
        await callback.answer("❌ Нет прав", show_alert=True)
        await state.clear()
        return
    
    # Получаем сообщение из состояния
    data = await state.get_data()
    broadcast_message = data.get("broadcast_message")
    
    if not broadcast_message:
        await callback.answer("❌ Ошибка: сообщение не найдено", show_alert=True)
        await state.clear()
        return
    
    # Получаем всех пользователей
    user_service = UserService(db)
    all_users = user_service.get_all_users()
    
    await callback.message.edit_text(
        f"📤 <b>Отправляю рассылку...</b>\n👥 Пользователей: {len(all_users)}",
        parse_mode="HTML"
    )
    
    # Отправляем рассылку
    success_count = 0
    error_count = 0
    
    for target_user in all_users:
        try:
            await callback.bot.send_message(
                chat_id=target_user.telegram_id,
                text=broadcast_message,
                parse_mode="HTML"
            )
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to send broadcast to user {target_user.telegram_id}: {e}")
            error_count += 1
    
    # Результат
    result_text = (
        f"📢 <b>Рассылка завершена!</b>\n\n"
        f"✅ <b>Отправлено:</b> {success_count}\n"
        f"❌ <b>Ошибок:</b> {error_count}\n"
        f"👥 <b>Всего:</b> {len(all_users)}\n\n"
        f"🕐 <b>Время:</b> {datetime.now().strftime('%H:%M:%S')}"
    )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🏠 Главная", callback_data="admin_main")
    )
    
    await callback.message.edit_text(
        result_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    
    await state.clear()
    await callback.answer("✅ Рассылка выполнена!")
    
    logger.info(f"Admin {user.telegram_id} sent broadcast to {success_count} users")


@router.callback_query(F.data == "admin_users")
async def admin_users(
    callback: CallbackQuery,
    user: User,
    db: Session
):
    """Show users management."""
    if not is_admin(user.telegram_id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    user_service = UserService(db)
    total_users = user_service.get_users_count()
    
    # Последние 10 пользователей
    recent_users = db.query(User).order_by(User.created_at.desc()).limit(10).all()
    
    users_text = f"👥 <b>Управление пользователями</b>\n\n"
    users_text += f"📊 <b>Всего пользователей:</b> {total_users}\n\n"
    
    if recent_users:
        users_text += f"👤 <b>Последние пользователи:</b>\n"
        for u in recent_users:
            username = f"@{u.username}" if u.username else "без username"
            date_str = u.created_at.strftime("%d.%m %H:%M")
            blocked = " 🚫" if u.is_blocked else ""
            users_text += f"• {u.first_name} ({username}) - {date_str}{blocked}\n"
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_users"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_main")
    )
    
    await callback.message.edit_text(
        users_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_settings")
async def admin_settings(
    callback: CallbackQuery,
    user: User
):
    """Show bot settings."""
    if not is_admin(user.telegram_id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    admin_list = ", ".join(str(id) for id in settings.admin_ids) if settings.admin_ids else "Не настроено"
    settings_text = (
        f"⚙️ <b>Настройки бота</b>\n\n"
        f"🤖 <b>Бот:</b> {settings.bot_name}\n"
        f"👨‍💻 <b>Админы:</b> {admin_list}\n"
        f"📞 <b>Контакт:</b> @{settings.contact_username}\n"
        f"🔧 <b>Debug режим:</b> {'Включен' if settings.debug else 'Выключен'}\n"
        f"📊 <b>Лог уровень:</b> {settings.log_level}\n\n"
        f"🛠 <b>Услуги ({len(settings.services)}):</b>\n"
    )
    
    for i, service in enumerate(settings.services, 1):
        service_short = service.split()[0]
        settings_text += f"{i}. {service_short}\n"
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_main")
    )
    
    await callback.message.edit_text(
        settings_text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_refresh")
async def admin_refresh(
    callback: CallbackQuery,
    user: User,
    db: Session
):
    """Refresh admin panel."""
    if not is_admin(user.telegram_id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    # Получаем свежую статистику с временем
    user_service = UserService(db)
    app_service = ApplicationService(db)
    
    total_users = user_service.get_users_count()
    total_applications = app_service.get_applications_count()
    
    today = datetime.now().date()
    new_apps_today = db.query(Application).filter(
        func.date(Application.created_at) == today
    ).count()
    
    # Добавляем секунды для гарантии изменения контента
    current_time = datetime.now().strftime('%H:%M:%S, %d.%m.%Y')
    
    admin_text = (
        f"👨‍💻 <b>Админ-панель NOFACE.digital</b>\n\n"
        f"📊 <b>Быстрая статистика:</b>\n"
        f"👥 Пользователи: <b>{total_users}</b>\n"
        f"📝 Всего заявок: <b>{total_applications}</b>\n"
        f"🆕 Новых сегодня: <b>{new_apps_today}</b>\n\n"
        f"🔄 <b>Обновлено:</b> {current_time}\n\n"
        f"🎛 <b>Выберите раздел:</b>"
    )
    
    await callback.message.edit_text(
        admin_text,
        reply_markup=get_admin_menu(),
        parse_mode="HTML"
    )
    await callback.answer("🔄 Панель обновлена!") 