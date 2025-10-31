"""
Task management API endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.task import TaskPriority, TaskStatus
from app.models.user import User
from app.schemas.task import Task, TaskCreate, TaskList, TaskUpdate
from app.services.task import TaskService

router = APIRouter()


@router.post(
    "",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create task",
    description="Create a new task for the authenticated user.",
)
async def create_task(
    task_data: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Create a new task.

    - **title**: Task title (required, 1-200 characters)
    - **description**: Optional task description
    - **priority**: Task priority (low, medium, high)
    - **status**: Task status (todo, in_progress, completed, cancelled)
    - **due_date**: Optional due date

    Requires authentication.
    """
    return await TaskService.create_task(db, task_data, current_user)


@router.get(
    "",
    response_model=TaskList,
    summary="List tasks",
    description="Get paginated list of tasks with optional filters.",
)
async def list_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[TaskStatus | None, Query()] = None,
    priority: Annotated[TaskPriority | None, Query()] = None,
):
    """
    Get list of tasks for the current user.

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **status**: Filter by status (optional)
    - **priority**: Filter by priority (optional)

    Requires authentication.
    """
    skip = (page - 1) * page_size
    status_value = status.value if status else None
    priority_value = priority.value if priority else None

    return await TaskService.get_tasks(
        db, current_user, skip, page_size, status_value, priority_value
    )


@router.get(
    "/{task_id}",
    response_model=Task,
    summary="Get task",
    description="Get a specific task by ID.",
)
async def get_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get task by ID.

    - **task_id**: Task ID

    Requires authentication. Users can only access their own tasks.
    """
    return await TaskService.get_task(db, task_id, current_user)


@router.put(
    "/{task_id}",
    response_model=Task,
    summary="Update task",
    description="Update a task (all fields are optional).",
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Update task by ID.

    All fields are optional. Only provided fields will be updated.

    - **title**: Task title (1-200 characters)
    - **description**: Task description
    - **priority**: Task priority
    - **status**: Task status
    - **due_date**: Due date

    Requires authentication. Users can only update their own tasks.
    """
    return await TaskService.update_task(db, task_id, task_data, current_user)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task by ID.",
)
async def delete_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Delete task by ID.

    - **task_id**: Task ID

    Requires authentication. Users can only delete their own tasks.
    """
    await TaskService.delete_task(db, task_id, current_user)


@router.patch(
    "/{task_id}/complete",
    response_model=Task,
    summary="Complete task",
    description="Mark a task as completed.",
)
async def complete_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Mark task as completed.

    - **task_id**: Task ID

    Sets is_completed to true, status to 'completed', and records completion time.

    Requires authentication. Users can only complete their own tasks.
    """
    return await TaskService.complete_task(db, task_id, current_user)
