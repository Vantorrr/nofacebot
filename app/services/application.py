"""
Application management service.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.application import Application, ApplicationType, ApplicationStatus
from app.models.user import User
from app.core.logger import get_logger

logger = get_logger(__name__)


class ApplicationService:
    """Service for managing applications."""
    
    def __init__(self, db: Session | AsyncSession):
        self.db = db
    
    def create_service_application(
        self,
        user: User,
        name: str,
        contact: str,
        service: str,
        description: str
    ) -> Application:
        """
        Create a new service application.
        
        Args:
            user: User instance
            name: Contact name
            contact: Contact information
            service: Selected service
            description: Project description
            
        Returns:
            Created application instance
        """
        application = Application(
            user_id=user.id,
            type=ApplicationType.SERVICE,
            name=name,
            contact=contact,
            service=service,
            description=description
        )
        
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        
        logger.info(f"Created service application #{application.id} for user {user.telegram_id}")
        return application
    
    def create_application(
        self,
        user_id: int,
        application_type: ApplicationType,
        name: str,
        contact: str,
        service: Optional[str] = None,
        subcategory: Optional[str] = None,
        budget: Optional[str] = None,
        timeline: Optional[str] = None,
        has_content: Optional[str] = None,
        has_design: Optional[str] = None,
        support_level: Optional[str] = None,
        additional_options: Optional[str] = None,
        description: Optional[str] = None,
        activity: Optional[str] = None,
        experience: Optional[str] = None,
        portfolio: Optional[str] = None
    ) -> Application:
        """
        Create a new detailed application (sync version).
        
        Args:
            user_id: User ID
            application_type: Type of application
            name: Contact name
            contact: Contact information
            service: Selected service (for service applications)
            subcategory: Service subcategory
            budget: Selected budget
            timeline: Project timeline
            has_content: Content availability
            has_design: Design availability  
            support_level: Support level
            additional_options: Additional options (JSON string)
            description: Project description
            activity: Professional activity (for team applications)
            experience: Work experience (for team applications)
            portfolio: Portfolio information (for team applications)
            
        Returns:
            Created application instance
        """
        application = Application(
            user_id=user_id,
            type=application_type,
            name=name,
            contact=contact,
            service=service,
            subcategory=subcategory,
            budget=budget,
            timeline=timeline,
            has_content=has_content,
            has_design=has_design,
            support_level=support_level,
            additional_options=additional_options,
            description=description,
            activity=activity,
            experience=experience,
            portfolio=portfolio
        )
        
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        
        # Принудительно загружаем связанного пользователя для избежания lazy loading проблем
        _ = application.user  # Это инициирует загрузку
        
        logger.info(f"Created {application_type.value} application #{application.id} for user {user_id}")
        return application
    
    def create_team_application(
        self,
        user: User,
        name: str,
        activity: str,
        experience: str,
        portfolio: str
    ) -> Application:
        """
        Create a new team application.
        
        Args:
            user: User instance
            name: Applicant name
            activity: Professional activity
            experience: Work experience
            portfolio: Portfolio information
            
        Returns:
            Created application instance
        """
        application = Application(
            user_id=user.id,
            type=ApplicationType.TEAM,
            name=name,
            contact="",  # Team applications don't require separate contact
            activity=activity,
            experience=experience,
            portfolio=portfolio
        )
        
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        
        logger.info(f"Created team application #{application.id} for user {user.telegram_id}")
        return application
    
    def get_application_by_id(self, application_id: int) -> Optional[Application]:
        """
        Get application by ID.
        
        Args:
            application_id: Application ID
            
        Returns:
            Application instance if found, None otherwise
        """
        return self.db.query(Application).filter(
            Application.id == application_id
        ).first()
    
    def get_user_applications(
        self,
        user: User,
        application_type: Optional[ApplicationType] = None
    ) -> List[Application]:
        """
        Get all applications for a user.
        
        Args:
            user: User instance
            application_type: Optional filter by application type
            
        Returns:
            List of applications
        """
        query = self.db.query(Application).filter(
            Application.user_id == user.id
        )
        
        if application_type:
            query = query.filter(Application.type == application_type)
        
        return query.order_by(Application.created_at.desc()).all()
    
    def get_applications_by_status(
        self,
        status: ApplicationStatus,
        application_type: Optional[ApplicationType] = None,
        limit: Optional[int] = None
    ) -> List[Application]:
        """
        Get applications by status.
        
        Args:
            status: Application status
            application_type: Optional filter by type
            limit: Optional limit
            
        Returns:
            List of applications
        """
        query = self.db.query(Application).filter(
            Application.status == status
        )
        
        if application_type:
            query = query.filter(Application.type == application_type)
        
        query = query.order_by(Application.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def update_application_status(
        self,
        application: Application,
        status: ApplicationStatus,
        admin_notes: Optional[str] = None
    ) -> Application:
        """
        Update application status.
        
        Args:
            application: Application instance
            status: New status
            admin_notes: Optional admin notes
            
        Returns:
            Updated application instance
        """
        old_status = application.status
        application.status = status
        
        if admin_notes:
            application.admin_notes = admin_notes
        
        self.db.commit()
        
        logger.info(
            f"Updated application #{application.id} status: "
            f"{old_status.value} -> {status.value}"
        )
        
        return application
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get application statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_applications = self.db.query(Application).count()
        
        service_applications = self.db.query(Application).filter(
            Application.type == ApplicationType.SERVICE
        ).count()
        
        team_applications = self.db.query(Application).filter(
            Application.type == ApplicationType.TEAM
        ).count()
        
        new_applications = self.db.query(Application).filter(
            Application.status == ApplicationStatus.NEW
        ).count()
        
        completed_applications = self.db.query(Application).filter(
            Application.status == ApplicationStatus.COMPLETED
        ).count()
        
        return {
            "total": total_applications,
            "service": service_applications,
            "team": team_applications,
            "new": new_applications,
            "completed": completed_applications
        }
    
    def get_applications_count(self) -> int:
        """
        Get total applications count.
        
        Returns:
            Total number of applications
        """
        return self.db.query(Application).count() 