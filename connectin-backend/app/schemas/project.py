"""
project.py:
Схемы для CRUD-операций над проектами:
- ProjectBase: общие поля (name, description)
- ProjectCreate: поля, нужные при создании
- ProjectUpdate: поля, которые можно менять
- ProjectOut: ответ API с дополнительными данными (список участников, рейтинг и т.д.)
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from app.enums import ApplicationStatus

class ApplicationDecisionRequest(BaseModel):
    decision: ApplicationStatus

class ProjectBase(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    
class TagOut(BaseModel):
    """ Schema for tags """
    id: int
    name: str

class UserOut(BaseModel):
    """ Schema to represent project owner. """
    id: int
    username: str
    avatar_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    """
    Схема для создания проекта.
    Добавлены теги и навыки.
    """
    tag_ids: List[int] = []  # ✅ IDs of selected tags
    skill_ids: List[int] = []  # ✅ IDs of required skills


class ProjectUpdate(BaseModel):
    """
    Схема обновления проекта.
    """
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    tag_ids: List[int] = []  # ✅ Allow updating tags
    skill_ids: List[int] = []  # ✅ Allow updating skills

class ProjectOut(BaseModel):
    """ Updated schema to return project details. """
    id: int
    name: str
    description: str
    owner: UserOut  # ✅ Include full owner details instead of just owner_id
    members: List[Dict] = []  
    applicants: List[Dict] = []  
    tags: List[Dict] = []  
    skills: List[Dict] = []  

    class Config:
        from_attributes = True  # ✅ Ensure ORM conversion works correctly
