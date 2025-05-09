from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, Date, Index
from sqlalchemy.orm import relationship
from .base import Base
from .relations.associations import user_teams_association, project_members_association, project_applications, \
    user_skills_association, conversation_participants, todo_watchers_association, todo_tags_association
from sqlalchemy import Column, DateTime
from datetime import datetime
# from app import enums as MyEnum
from sqlalchemy import Column, Integer, String, DateTime, Enum, func, Index  # Добавьте Enum


class SubscriptionStatusEnum(PyEnum):
    FREE = "free"
    ACTIVE = "active"
    PAST_DUE = "past_due"  # Платеж просрочен
    CANCELED = "canceled"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    city = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    github = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    telegram = Column(String(255), nullable=True)
    avatar_url = Column(String, nullable=True)
    cover_photo_url = Column(String, nullable=True)
    google_id = Column(String(255), unique=True)
    google_refresh_token = Column(String(255))

    # -------------------------Subscription Section----------------------------------------------
    subscription_status = Column(Enum(SubscriptionStatusEnum), default=SubscriptionStatusEnum.FREE, nullable=False,
                                 server_default=SubscriptionStatusEnum.FREE.value)
    stripe_customer_id = Column(String, unique=True, nullable=True, index=True)  # ID клиента в Stripe
    stripe_subscription_id = Column(String, unique=True, nullable=True, index=True)  # ID подписки в Stripe
    subscription_plan_id = Column(String, nullable=True)  # ID ценового плана (price_...)
    subscription_expires_at = Column(DateTime(timezone=True),
                                     nullable=True)  # Дата окончания текущего оплаченного периода (с часовым поясом)

    # --- Индекс для статуса ---
    __table_args__ = (
        Index('ix_users_subscription_status', 'subscription_status'),
        # Добавьте другие индексы/ограничения при необходимости
    )
    # ---------------

    status = Column(String, default="in progress")
    # last active
    last_active = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=True)

    teams = relationship("Team", secondary=user_teams_association, back_populates="members")
    owned_projects = relationship("Project", back_populates="owner")
    projects = relationship("Project", secondary=project_members_association, back_populates="members")
    applied_projects = relationship("Project", secondary=project_applications, back_populates="applicants")
    posts = relationship("Post", back_populates="author")
    skills = relationship("Skill", secondary=user_skills_association, back_populates="users")
    education = relationship("Education", back_populates="user", cascade="all, delete-orphan")
    experience = relationship("Experience", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", secondary=conversation_participants, back_populates="participants")
    messages = relationship("Message", back_populates="sender")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    post_comments = relationship("PostComment", back_populates="user", cascade="all, delete")
    project_comments = relationship("ProjectComment", back_populates="user", cascade="all, delete")
    saved_posts = relationship("SavedPost", back_populates="user", cascade="all, delete-orphan")

    # В классе User (app/models/user.py)
    sent_recommendations = relationship("Recommendation", foreign_keys="[Recommendation.from_user_id]",
                                        back_populates="from_user")
    received_recommendations = relationship("Recommendation", foreign_keys="[Recommendation.to_user_id]",
                                            back_populates="to_user")

    # Todos created by the user
    todos = relationship("Todo", back_populates="user")

    # 25.03.25:
    # Новые отношения
    watched_todos = relationship(
        "Todo",
        secondary=todo_watchers_association,
        back_populates="watchers"
    )

    # Добавляем обратные связи для комментариев
    todo_comments = relationship("TodoComment", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"


class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    field_of_study = Column(String(255), nullable=True)
    start_year = Column(Date, nullable=False)
    end_year = Column(Date, nullable=True)
    relevant_courses = Column(Text, nullable=True)
    description = Column(Text, nullable=True)

    user = relationship("User", back_populates="education")


class Experience(Base):
    __tablename__ = "experience"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    start_year = Column(Date, nullable=False)
    end_year = Column(Date, nullable=True)
    description = Column(Text, nullable=True)

    user = relationship("User", back_populates="experience")
