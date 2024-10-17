"""
Task service for CRUD operations on tasks.
"""

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskList, TaskUpdate
from app.utils.exceptions import ForbiddenException, NotFoundException


class TaskService:
    """Service for handling task operations."""

    @staticmethod
    async def create_task(db: AsyncSession, task_data: TaskCreate, user: User) -> Task:
        """
        Create a new task for the authenticated user.

        Args:
            db: Database session
            task_data: Task creation data
            user: Authenticated user

        Returns:
            Task: Created task
        """
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority.value,
            status=task_data.status.value,
            due_date=task_data.due_date,
            owner_id=user.id,
        )

        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)

        return db_task

    @staticmethod
    async def get_task(db: AsyncSession, task_id: int, user: User) -> Task:
        """
        Get a specific task by ID.

        Args:
            db: Database session
            task_id: Task ID
            user: Authenticated user

        Returns:
            Task: Requested task

        Raises:
            NotFoundException: If task not found
            ForbiddenException: If user doesn't own the task
        """
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()

        if not task:
            raise NotFoundException("Task not found")

        if task.owner_id != user.id and not user.is_superuser:
            raise ForbiddenException("Not authorized to access this task")

        return task

    @staticmethod
    async def get_tasks(
        db: AsyncSession,
        user: User,
        skip: int = 0,
        limit: int = 20,
        status: str | None = None,
        priority: str | None = None,
    ) -> TaskList:
        """
        Get paginated list of tasks for the authenticated user.

        Args:
            db: Database session
            user: Authenticated user
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Optional status filter
            priority: Optional priority filter

        Returns:
            TaskList: Paginated task list
        """
        # Build query
        query = select(Task).where(Task.owner_id == user.id)

        # Apply filters
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination and order
        query = query.order_by(Task.created_at.desc()).offset(skip).limit(limit)

        # Execute query
        result = await db.execute(query)
        tasks = result.scalars().all()

        # Calculate pagination info
        page = (skip // limit) + 1 if limit > 0 else 1
        total_pages = (total + limit - 1) // limit if limit > 0 else 1

        return TaskList(
            tasks=list(tasks),
            total=total,
            page=page,
            page_size=limit,
            total_pages=total_pages,
        )

    @staticmethod
    async def update_task(
        db: AsyncSession, task_id: int, task_data: TaskUpdate, user: User
    ) -> Task:
        """
        Update a task.

        Args:
            db: Database session
            task_id: Task ID
            task_data: Task update data
            user: Authenticated user

        Returns:
            Task: Updated task

        Raises:
            NotFoundException: If task not found
            ForbiddenException: If user doesn't own the task
        """
        # Get existing task
        task = await TaskService.get_task(db, task_id, user)

        # Update fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(task, field):
                if field in ["priority", "status"] and value:
                    setattr(task, field, value.value)
                else:
                    setattr(task, field, value)

        await db.commit()
        await db.refresh(task)

        return task

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int, user: User) -> None:
        """
        Delete a task.

        Args:
            db: Database session
            task_id: Task ID
            user: Authenticated user

        Raises:
            NotFoundException: If task not found
            ForbiddenException: If user doesn't own the task
        """
        task = await TaskService.get_task(db, task_id, user)
        await db.delete(task)
        await db.commit()

    @staticmethod
    async def complete_task(db: AsyncSession, task_id: int, user: User) -> Task:
        """
        Mark a task as completed.

        Args:
            db: Database session
            task_id: Task ID
            user: Authenticated user

        Returns:
            Task: Completed task

        Raises:
            NotFoundException: If task not found
            ForbiddenException: If user doesn't own the task
        """
        task = await TaskService.get_task(db, task_id, user)

        task.is_completed = True
        task.completed_at = datetime.utcnow()
        task.status = TaskStatus.COMPLETED.value

        await db.commit()
        await db.refresh(task)

        return task

