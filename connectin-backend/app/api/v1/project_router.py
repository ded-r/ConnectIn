"""
Этот модуль отвечает за CRUD-операции над моделью Проекта.
Пользователи могут создавать, просматривать, редактировать и удалять свои проекты.
Добавлена система заявок: пользователи могут подавать заявки, а владельцы проектов их одобрять/отклонять.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
<<<<<<< HEAD:connectin-backend/app/api/v1/project_router.py
from sqlalchemy import Integer, case, func
from fastapi import APIRouter, Depends, HTTPException #,status
=======
from sqlalchemy import case, func
>>>>>>> backup_before_reset:connectin-backend/app/api/v2/projects_v2.py
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.project import Project
from app.models.user import User
<<<<<<< HEAD:connectin-backend/app/api/v1/project_router.py
from app.schemas import UserOut
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate, ApplicationOut
from app.api.v1.auth_router import get_current_user
=======
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.api.v1.auth import get_current_user
>>>>>>> backup_before_reset:connectin-backend/app/api/v2/projects_v2.py
from app.models.project import project_applications, project_members_association, project_tags_association, project_skills_association
from app.schemas.project import ApplicationDecisionRequest, ApplicationStatus
from app.models.vote import ProjectVote
from app.models.comment import ProjectComment
from app.schemas.comment import CommentOut, CommentCreate

router = APIRouter()

class VoteRequest(BaseModel):
    is_upvote: bool

class VoteStatusResponse(BaseModel):
    has_voted: bool
    is_upvote: bool | None = None

# 🔹 Создать проект с тегами и навыками
@router.post("/", response_model=ProjectOut, summary="Создать проект")
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создание нового проекта.
    Текущий пользователь становится владельцем проекта.
    Принимает список тегов (tag_ids) и навыков (skill_ids).
    """
    # ✅ Создаем проект
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # ✅ Добавляем теги, если они переданы
    if project_data.tag_ids:
        for tag_id in project_data.tag_ids:
            db.execute(
                project_tags_association.insert().values(
                    project_id=new_project.id, tag_id=tag_id
                )
            )

    # ✅ Добавляем навыки, если они переданы
    if project_data.skill_ids:
        for skill_id in project_data.skill_ids:
            db.execute(
                project_skills_association.insert().values(
                    project_id=new_project.id, skill_id=skill_id
                )
            )

    db.commit()

    # ✅ Fetch project again with related tags and skills
    db.refresh(new_project)
    project_with_tags_and_skills = db.query(Project).filter(Project.id == new_project.id).first()

    return {
        "id": project_with_tags_and_skills.id,
        "name": project_with_tags_and_skills.name,
        "description": project_with_tags_and_skills.description,
        "owner_id": project_with_tags_and_skills.owner_id,
        "members": [ {"id": user.id, "username": user.username} for user in project_with_tags_and_skills.members ],
        "applicants": [ {"id": user.id, "username": user.username} for user in project_with_tags_and_skills.applicants ],
        "tags": [ {"id": tag.id, "name": tag.name} for tag in project_with_tags_and_skills.tags ],  # ✅ Convert tags to dict
        "skills": [ {"id": skill.id, "name": skill.name} for skill in project_with_tags_and_skills.skills ]  # ✅ Convert skills to dict
    }

@router.get("/my", response_model=List[ProjectOut], summary="Мои проекты")
def get_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить список проектов, которые создал текущий пользователь.
    """
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()

    formatted_projects = []
    for project in projects:
        formatted_projects.append({
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "owner": {
                "id": project.owner.id,
                "username": project.owner.username,
                "avatar_url": project.owner.avatar_url
            },
            "tags": [{"id": tag.id, "name": tag.name} for tag in project.tags],  # ✅ Include Tags
            "skills": [{"id": skill.id, "name": skill.name} for skill in project.skills],  # ✅ Include Skills
        })

    return formatted_projects


# 🔹 Получить все проекты
@router.get("/", response_model=List[ProjectOut])
def read_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    return [
        ProjectOut(
            id=project.id,
            name=project.name,
            description=project.description,
            owner={
                "id": project.owner.id,
                "username": project.owner.username,
                "avatar_url": project.owner.avatar_url
            } if project.owner else None,
            tags=[{"id": tag.id, "name": tag.name} for tag in project.tags],
            skills=[{"id": skill.id, "name": skill.name} for skill in project.skills],
            members=[{"id": user.id, "username": user.username} for user in project.members],
            applicants=[{"id": user.id, "username": user.username} for user in project.applicants],
            comments_count=len(project.comments),
            vote_count=db.query(
                func.sum(case((ProjectVote.is_upvote, 1), else_=-1))
            ).filter(ProjectVote.project_id == project.id).scalar() or 0
        )
        for project in projects
    ]

@router.get("/{project_id}", response_model=ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    vote_count = db.query(
        func.sum(case((ProjectVote.is_upvote, 1), else_=-1))
    ).filter(ProjectVote.project_id == project_id).scalar() or 0

    return ProjectOut(
        id=project.id,
        name=project.name,
        description=project.description,
        owner={
            "id": project.owner.id,
            "username": project.owner.username,
            "avatar_url": project.owner.avatar_url
        } if project.owner else None,
        tags=[{"id": tag.id, "name": tag.name} for tag in project.tags],
        skills=[{"id": skill.id, "name": skill.name} for skill in project.skills],
        members=[{"id": user.id, "username": user.username} for user in project.members],
        applicants=[{"id": user.id, "username": user.username} for user in project.applicants],
        comments_count=len(project.comments),
        vote_count=vote_count
    )

# 🔹 Обновить проект
@router.put("/{project_id}", response_model=ProjectOut, summary="Обновить проект")
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновляет существующий проект (только если пользователь - владелец).
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не можете редактировать чужой проект")

    project.name = project_data.name or project.name
    project.description = project_data.description or project.description

    db.commit()
    db.refresh(project)
    return project


# 🔹 Удалить проект
@router.delete("/{project_id}", summary="Удалить проект")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удалить проект (только если пользователь - владелец).
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не можете удалить чужой проект")

    db.delete(project)
    db.commit()
    return {"detail": "Проект успешно удалён"}


# 🔹 Подать заявку на участие в проекте
@router.post("/{project_id}/apply", summary="Подать заявку на проект")
def apply_to_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Пользователь подает заявку на участие в проекте.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    # Проверяем, не является ли пользователь уже участником
    if db.query(project_members_association).filter_by(user_id=current_user.id, project_id=project_id).first():
        raise HTTPException(status_code=400, detail="Вы уже являетесь участником проекта")

    # Проверяем, не подал ли пользователь уже заявку
    if db.query(project_applications).filter_by(user_id=current_user.id, project_id=project_id).first():
        raise HTTPException(status_code=400, detail="Вы уже подали заявку")

    # Добавляем заявку в таблицу заявок
    new_application = project_applications.insert().values(user_id=current_user.id, project_id=project_id)
    db.execute(new_application)
    db.commit()

    return {"detail": "Заявка подана"}


# 🔹 Получить список участников проекта
from sqlalchemy import select


@router.get("/{project_id}/members", response_model=list[UserOut])
def get_project_members(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить участников проекта с проверкой доступа"""
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Проект не найден")

<<<<<<< HEAD:connectin-backend/app/api/v1/project_router.py
    # Проверка, что пользователь имеет доступ
    if not project.is_visible_to(current_user):
        raise HTTPException(403, "Нет прав доступа")
=======
    # Получаем информацию о пользователях
    member_ids = [member["user_id"] for member in members]
    users = db.query(User).filter(User.id.in_(member_ids)).all()

    return [{"id": user.id, "username": user.username, "email": user.email} for user in users]
>>>>>>> backup_before_reset:connectin-backend/app/api/v2/projects_v2.py

    # Оптимизированный запрос через JOIN
    stmt = (
        select(User)
        .join(project_members_association, User.id == project_members_association.c.user_id)
        .where(project_members_association.c.project_id == project_id)
    )

    members = db.execute(stmt).scalars().all()
    return members

# 🔹 Получить список заявок в проект
@router.get("/{project_id}/applications", response_model=list[ApplicationOut])
def get_project_applications(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить заявки с проверкой прав владельца"""
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Проект не найден")

    if project.owner_id != current_user.id:
        raise HTTPException(403, "Только владелец может просматривать заявки")

    # Запрос с явным указанием колонок
    stmt = select(
        project_applications.c.user_id,
        User.username,
        User.email
    ).join(User, User.id == project_applications.c.user_id)

<<<<<<< HEAD:connectin-backend/app/api/v1/project_router.py
    applications = db.execute(stmt).all()
    return [{"user_id": app["user_id"], "username": app["username"]} for app in applications]
=======
    return [{"user_id": app["user_id"]} for app in applicants]
>>>>>>> backup_before_reset:connectin-backend/app/api/v2/projects_v2.py


# 🔹 Одобрить/Отклонить заявку
@router.post("/{project_id}/applications/{user_id}/decision", summary="Принять или отклонить заявку")
def decide_application(
    project_id: int,
    user_id: int,
    request: ApplicationDecisionRequest,  # Accepting JSON body instead of query
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Владелец проекта принимает или отклоняет заявку пользователя.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не владелец проекта")

    application = db.execute(
        project_applications.select().where(
            (project_applications.c.project_id == project_id) &
            (project_applications.c.user_id == user_id)
        )
    ).fetchone()

    if not application:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    if request.decision == ApplicationStatus.ACCEPTED:
        # ✅ Add user to project members table
        db.execute(project_members_association.insert().values(user_id=user_id, project_id=project_id))
        # ✅ Remove application after approval
        db.execute(project_applications.delete().where(
            (project_applications.c.project_id == project_id) &
            (project_applications.c.user_id == user_id)
        ))
        db.commit()
        return {"detail": "Пользователь принят в проект"}

    elif request.decision == ApplicationStatus.REJECTED:
        # ✅ Remove application from applications table
        db.execute(project_applications.delete().where(
            (project_applications.c.project_id == project_id) &
            (project_applications.c.user_id == user_id)
        ))
        db.commit()
        return {"detail": "Заявка отклонена"}


# 🔹 Удалить пользователя из проекта (только владелец проекта)
@router.delete("/{project_id}/members/{user_id}", summary="Удалить пользователя из проекта")
def remove_user_from_project(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Владелец проекта может удалить участника из проекта.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не владелец проекта")

    # Проверяем, является ли пользователь участником
    member = db.execute(
        project_members_association.select().where(
            (project_members_association.c.project_id == project_id) &
            (project_members_association.c.user_id == user_id)
        )
    ).fetchone()

    if not member:
        raise HTTPException(status_code=404, detail="Пользователь не является участником проекта")

    # Удаляем пользователя из таблицы участников проекта
    db.execute(project_members_association.delete().where(
        (project_members_association.c.project_id == project_id) &
        (project_members_association.c.user_id == user_id)
    ))
    db.commit()

    return {"detail": "Пользователь удален из проекта"}

# ✅ Upvote/Downvote Project
@router.post("/{project_id}/vote")
def vote_project(
    project_id: int,
    vote_data: VoteRequest,  # Use the Pydantic model instead of a plain parameter
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    existing_vote = db.query(ProjectVote).filter_by(user_id=current_user.id, project_id=project_id).first()

    if existing_vote:
        if existing_vote.is_upvote == vote_data.is_upvote:
            db.delete(existing_vote)
            db.commit()
            return {"detail": "Vote removed"}
        else:
            existing_vote.is_upvote = vote_data.is_upvote
            db.commit()
            return {"detail": "Vote changed"}

    new_vote = ProjectVote(user_id=current_user.id, project_id=project_id, is_upvote=vote_data.is_upvote)
    db.add(new_vote)
    db.commit()
    return {"detail": "Vote added"}

# New endpoint to check vote status
@router.get("/{project_id}/vote_status", response_model=VoteStatusResponse)
def get_vote_status(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Check if the current user has voted on a project and whether it's an upvote or downvote.
    """
    vote = db.query(ProjectVote).filter_by(user_id=current_user.id, project_id=project_id).first()
    if vote:
        return {"has_voted": True, "is_upvote": vote.is_upvote}
    return {"has_voted": False, "is_upvote": None}

# ✅ Comment on Project
@router.post("/{project_id}/comment", response_model=CommentOut)
def comment_project(
    project_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create new comment
    new_comment = ProjectComment(
        content=comment_data.content,
        user_id=current_user.id,
        project_id=project_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    # Construct response matching CommentOut
    return CommentOut(
        id=new_comment.id,
        content=new_comment.content,
        user_id=new_comment.user_id,
        created_at=new_comment.created_at,  # Ensure this field exists in ProjectComment
        user={
            "username": current_user.username,
            "avatar_url": current_user.avatar_url
        }
    )

@router.get("/{project_id}/comments", response_model=List[CommentOut])
def get_project_comments(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve all comments for a specific project.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    comments = db.query(ProjectComment).filter(ProjectComment.project_id == project_id).all()

    return [
        CommentOut(
            id=comment.id,
            content=comment.content,
            user_id=comment.user_id,
            created_at=comment.created_at,
            user={
                "username": comment.user.username if comment.user else "Unknown",
                "avatar_url": comment.user.avatar_url if comment.user else None
            }
        )
        for comment in comments
    ]