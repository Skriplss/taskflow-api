"""
Tests for task management endpoints.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskPriority, TaskStatus
from app.models.user import User


@pytest.fixture
async def test_task(db_session: AsyncSession, test_user: User) -> Task:
    """
    Create a test task in the database.

    Args:
        db_session: Test database session
        test_user: Test user

    Returns:
        Task: Created test task
    """
    task = Task(
        title="Test Task",
        description="Test task description",
        priority=TaskPriority.MEDIUM.value,
        status=TaskStatus.TODO.value,
        owner_id=test_user.id,
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


class TestCreateTask:
    """Tests for creating tasks."""

    @pytest.mark.asyncio
    async def test_create_task_success(self, client: AsyncClient, auth_headers: dict):
        """Test successful task creation."""
        response = await client.post(
            "/api/v1/tasks",
            json={
                "title": "New Task",
                "description": "Task description",
                "priority": "high",
                "status": "todo",
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["description"] == "Task description"
        assert data["priority"] == "high"
        assert data["status"] == "todo"
        assert data["is_completed"] is False
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_task_minimal(self, client: AsyncClient, auth_headers: dict):
        """Test creating task with minimal required fields."""
        response = await client.post(
            "/api/v1/tasks",
            json={"title": "Simple Task"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Simple Task"
        assert data["priority"] == "medium"  # Default
        assert data["status"] == "todo"  # Default

    @pytest.mark.asyncio
    async def test_create_task_unauthorized(self, client: AsyncClient):
        """Test creating task without authentication fails."""
        response = await client.post(
            "/api/v1/tasks",
            json={"title": "Unauthorized Task"},
        )

        assert response.status_code == 403


class TestGetTasks:
    """Tests for listing tasks."""

    @pytest.mark.asyncio
    async def test_list_tasks_success(
        self, client: AsyncClient, auth_headers: dict, test_task: Task
    ):
        """Test listing tasks."""
        response = await client.get("/api/v1/tasks", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert "page" in data
        assert data["total"] >= 1
        assert len(data["tasks"]) >= 1

    @pytest.mark.asyncio
    async def test_list_tasks_pagination(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test task list pagination."""
        # Create multiple tasks
        for i in range(5):
            task = Task(
                title=f"Task {i}",
                owner_id=test_user.id,
            )
            db_session.add(task)
        await db_session.commit()

        response = await client.get(
            "/api/v1/tasks?page=1&page_size=2", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 2
        assert data["page"] == 1
        assert data["page_size"] == 2
        assert data["total"] >= 5

    @pytest.mark.asyncio
    async def test_list_tasks_filter_by_status(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test filtering tasks by status."""
        # Create tasks with different statuses
        task1 = Task(title="Todo Task", status=TaskStatus.TODO.value, owner_id=test_user.id)
        task2 = Task(
            title="In Progress Task",
            status=TaskStatus.IN_PROGRESS.value,
            owner_id=test_user.id,
        )
        db_session.add_all([task1, task2])
        await db_session.commit()

        response = await client.get(
            "/api/v1/tasks?status=todo", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(task["status"] == "todo" for task in data["tasks"])

    @pytest.mark.asyncio
    async def test_list_tasks_unauthorized(self, client: AsyncClient):
        """Test listing tasks without authentication fails."""
        response = await client.get("/api/v1/tasks")

        assert response.status_code == 403


class TestGetTask:
    """Tests for getting a specific task."""

    @pytest.mark.asyncio
    async def test_get_task_success(
        self, client: AsyncClient, auth_headers: dict, test_task: Task
    ):
        """Test getting a specific task."""
        response = await client.get(
            f"/api/v1/tasks/{test_task.id}", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_task.id
        assert data["title"] == test_task.title

    @pytest.mark.asyncio
    async def test_get_nonexistent_task(self, client: AsyncClient, auth_headers: dict):
        """Test getting non-existent task fails."""
        response = await client.get("/api/v1/tasks/99999", headers=auth_headers)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_task_unauthorized(self, client: AsyncClient, test_task: Task):
        """Test getting task without authentication fails."""
        response = await client.get(f"/api/v1/tasks/{test_task.id}")

        assert response.status_code == 403


class TestUpdateTask:
    """Tests for updating tasks."""

    @pytest.mark.asyncio
    async def test_update_task_success(
        self, client: AsyncClient, auth_headers: dict, test_task: Task
    ):
        """Test successful task update."""
        response = await client.put(
            f"/api/v1/tasks/{test_task.id}",
            json={"title": "Updated Task", "priority": "high"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"
        assert data["priority"] == "high"

    @pytest.mark.asyncio
    async def test_update_nonexistent_task(self, client: AsyncClient, auth_headers: dict):
        """Test updating non-existent task fails."""
        response = await client.put(
            "/api/v1/tasks/99999",
            json={"title": "Updated Task"},
            headers=auth_headers,
        )

        assert response.status_code == 404


class TestDeleteTask:
    """Tests for deleting tasks."""

    @pytest.mark.asyncio
    async def test_delete_task_success(
        self, client: AsyncClient, auth_headers: dict, test_task: Task
    ):
        """Test successful task deletion."""
        response = await client.delete(
            f"/api/v1/tasks/{test_task.id}", headers=auth_headers
        )

        assert response.status_code == 204

        # Verify task is deleted
        get_response = await client.get(
            f"/api/v1/tasks/{test_task.id}", headers=auth_headers
        )
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_nonexistent_task(self, client: AsyncClient, auth_headers: dict):
        """Test deleting non-existent task fails."""
        response = await client.delete("/api/v1/tasks/99999", headers=auth_headers)

        assert response.status_code == 404


class TestCompleteTask:
    """Tests for marking tasks as completed."""

    @pytest.mark.asyncio
    async def test_complete_task_success(
        self, client: AsyncClient, auth_headers: dict, test_task: Task
    ):
        """Test successfully completing a task."""
        response = await client.patch(
            f"/api/v1/tasks/{test_task.id}/complete", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["is_completed"] is True
        assert data["status"] == "completed"
        assert data["completed_at"] is not None

    @pytest.mark.asyncio
    async def test_complete_nonexistent_task(self, client: AsyncClient, auth_headers: dict):
        """Test completing non-existent task fails."""
        response = await client.patch(
            "/api/v1/tasks/99999/complete", headers=auth_headers
        )

        assert response.status_code == 404

