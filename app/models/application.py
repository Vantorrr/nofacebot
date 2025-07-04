"""
Application model for storing user applications.
"""

import enum
from sqlalchemy import Column, String, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class ApplicationType(enum.Enum):
    """Types of applications."""
    SERVICE = "service"
    TEAM = "team"


class ApplicationStatus(enum.Enum):
    """Application status."""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class Application(Base, TimestampMixin):
    """Application model for storing user requests."""
    
    __tablename__ = "applications"
    
    # Foreign keys
    user_id = Column(ForeignKey("users.id"), nullable=False)
    
    # Application data
    type = Column(SqlEnum(ApplicationType), nullable=False)
    status = Column(SqlEnum(ApplicationStatus), default=ApplicationStatus.NEW)
    
    # Contact information
    name = Column(String(255), nullable=False)
    contact = Column(String(255), nullable=False)
    
    # Service application fields
    service = Column(String(500), nullable=True)
    subcategory = Column(String(500), nullable=True)
    budget = Column(String(100), nullable=True)
    timeline = Column(String(100), nullable=True)
    has_content = Column(String(100), nullable=True)
    has_design = Column(String(100), nullable=True)
    support_level = Column(String(100), nullable=True)
    additional_options = Column(Text, nullable=True)  # JSON строка с дополнительными опциями
    description = Column(Text, nullable=True)
    
    # Team application fields
    activity = Column(String(500), nullable=True)
    experience = Column(Text, nullable=True)
    portfolio = Column(Text, nullable=True)
    
    # Admin notes
    admin_notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    
    def __repr__(self):
        return f"<Application(id={self.id}, type={self.type.value}, user_id={self.user_id})>"
    
    @property
    def is_service_application(self) -> bool:
        """Check if this is a service application."""
        return self.type == ApplicationType.SERVICE
    
    @property
    def is_team_application(self) -> bool:
        """Check if this is a team application."""
        return self.type == ApplicationType.TEAM
    
    def to_admin_message(self) -> str:
        """Format application data for admin notification."""
        if self.is_service_application:
            msg = f"🛠 <b>НОВАЯ ЗАЯВКА НА УСЛУГУ #{self.id}</b>\n\n"
            msg += f"👤 <b>Имя:</b> {self.name}\n"
            msg += f"📱 <b>Контакт:</b> {self.contact}\n"
            msg += f"🎯 <b>Услуга:</b> {self.service}\n"
            
            if self.subcategory:
                msg += f"📋 <b>Тип:</b> {self.subcategory}\n"
            if self.budget:
                msg += f"💰 <b>Бюджет:</b> {self.budget}\n"
            if self.timeline:
                msg += f"⏰ <b>Сроки:</b> {self.timeline}\n"
            if self.has_content:
                msg += f"📄 <b>Контент:</b> {self.has_content}\n"
            if self.has_design:
                msg += f"🎨 <b>Дизайн:</b> {self.has_design}\n"
            if self.support_level:
                msg += f"🛡 <b>Поддержка:</b> {self.support_level}\n"
            if self.additional_options:
                msg += f"⚙️ <b>Доп. опции:</b> {self.additional_options}\n"
            if self.description:
                msg += f"\n📝 <b>Описание:</b>\n{self.description}\n"
            
            msg += f"\n👨‍💻 <b>Пользователь:</b> {self.user.mention} (ID: {self.user.telegram_id})\n"
            msg += f"🕐 <b>Время:</b> {self.created_at.strftime('%d.%m.%Y %H:%M')}"
            return msg
        else:
            return (
                f"👥 <b>НОВАЯ ЗАЯВКА В КОМАНДУ #{self.id}</b>\n\n"
                f"👤 <b>Имя:</b> {self.name}\n"
                f"💼 <b>Деятельность:</b> {self.activity}\n"
                f"🎯 <b>Опыт:</b>\n{self.experience}\n\n"
                f"🎨 <b>Портфолио:</b>\n{self.portfolio}\n\n"
                f"👨‍💻 <b>Пользователь:</b> {self.user.mention} (ID: {self.user.telegram_id})\n"
                f"🕐 <b>Время:</b> {self.created_at.strftime('%d.%m.%Y %H:%M')}"
            ) 