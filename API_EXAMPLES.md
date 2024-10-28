# API Usage Examples

Complete examples of using TaskFlow API.

## Authentication

### Register a New User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

Response:
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-31T10:00:00",
  "updated_at": "2025-10-31T10:00:00"
}
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Task Management

**Note:** All task endpoints require authentication. Include the bearer token in the Authorization header.

### Create a Task

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation with examples",
    "priority": "high",
    "status": "todo",
    "due_date": "2025-11-15T17:00:00"
  }'
```

Response:
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation with examples",
  "priority": "high",
  "status": "todo",
  "is_completed": false,
  "completed_at": null,
  "due_date": "2025-11-15T17:00:00",
  "created_at": "2025-10-31T10:00:00",
  "updated_at": "2025-10-31T10:00:00",
  "owner_id": 1
}
```

### List All Tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Response:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive API documentation",
      "priority": "high",
      "status": "todo",
      "is_completed": false,
      "completed_at": null,
      "due_date": "2025-11-15T17:00:00",
      "created_at": "2025-10-31T10:00:00",
      "updated_at": "2025-10-31T10:00:00",
      "owner_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### Filter Tasks by Status

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?status=todo" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Filter Tasks by Priority

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?priority=high" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get a Specific Task

```bash
curl -X GET http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Update a Task

```bash
curl -X PUT http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "status": "in_progress",
    "priority": "medium"
  }'
```

### Mark Task as Completed

```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/1/complete \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Response:
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "priority": "high",
  "status": "completed",
  "is_completed": true,
  "completed_at": "2025-10-31T15:30:00",
  "due_date": "2025-11-15T17:00:00",
  "created_at": "2025-10-31T10:00:00",
  "updated_at": "2025-10-31T15:30:00",
  "owner_id": 1
}
```

### Delete a Task

```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Returns: `204 No Content`

## Python Examples

### Using `requests` library

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Register
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "email": "user@example.com",
        "username": "username",
        "password": "password123"
    }
)
print(response.json())

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "username": "username",
        "password": "password123"
    }
)
token = response.json()["access_token"]

# Create headers with token
headers = {"Authorization": f"Bearer {token}"}

# Create task
response = requests.post(
    f"{BASE_URL}/tasks",
    json={
        "title": "My Task",
        "description": "Task description",
        "priority": "high"
    },
    headers=headers
)
print(response.json())

# List tasks
response = requests.get(
    f"{BASE_URL}/tasks",
    headers=headers
)
print(response.json())
```

### Using `httpx` (async)

```python
import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/v1"

async def main():
    async with httpx.AsyncClient() as client:
        # Register
        response = await client.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": "user@example.com",
                "username": "username",
                "password": "password123"
            }
        )
        print(response.json())

        # Login
        response = await client.post(
            f"{BASE_URL}/auth/login",
            json={
                "username": "username",
                "password": "password123"
            }
        )
        token = response.json()["access_token"]

        # Create headers
        headers = {"Authorization": f"Bearer {token}"}

        # Create task
        response = await client.post(
            f"{BASE_URL}/tasks",
            json={
                "title": "Async Task",
                "priority": "medium"
            },
            headers=headers
        )
        print(response.json())

asyncio.run(main())
```

## JavaScript Examples

### Using `fetch` API

```javascript
const BASE_URL = 'http://localhost:8000/api/v1';

// Register
async function register() {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: 'user@example.com',
      username: 'username',
      password: 'password123'
    })
  });
  return await response.json();
}

// Login
async function login() {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: 'username',
      password: 'password123'
    })
  });
  const data = await response.json();
  return data.access_token;
}

// Create task
async function createTask(token) {
  const response = await fetch(`${BASE_URL}/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      title: 'New Task',
      description: 'Task description',
      priority: 'high'
    })
  });
  return await response.json();
}

// Usage
(async () => {
  await register();
  const token = await login();
  const task = await createTask(token);
  console.log(task);
})();
```

### Using `axios`

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Login and get token
async function authenticate() {
  const response = await api.post('/auth/login', {
    username: 'username',
    password: 'password123'
  });
  
  const token = response.data.access_token;
  
  // Set token for future requests
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  
  return token;
}

// Create task
async function createTask() {
  const response = await api.post('/tasks', {
    title: 'Important Task',
    priority: 'high',
    status: 'todo'
  });
  return response.data;
}

// Get all tasks
async function getTasks() {
  const response = await api.get('/tasks', {
    params: {
      page: 1,
      page_size: 10,
      status: 'todo'
    }
  });
  return response.data;
}

// Usage
(async () => {
  await authenticate();
  const task = await createTask();
  console.log('Created:', task);
  
  const tasks = await getTasks();
  console.log('All tasks:', tasks);
})();
```

## Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Task Management API",
  "version": "1.0.0",
  "environment": "development"
}
```

## Interactive Documentation

Once the API is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation where you can:
- See all endpoints
- View request/response schemas
- Try out API calls directly in the browser
- Authenticate and test protected endpoints

## Token Management

JWT tokens expire after 30 minutes by default. When you receive a 401 error, re-authenticate:

```python
# Check if token is expired
def is_token_expired(response):
    return response.status_code == 401

# Re-authenticate if needed
if is_token_expired(response):
    token = login()
    headers = {"Authorization": f"Bearer {token}"}
```

## Best Practices

1. Store tokens securely - Use environment variables or secure storage
2. Handle errors gracefully - Check response status codes
3. Use pagination - Don't fetch all records at once
4. Implement retry logic - For network failures
5. Validate input - Before sending to API
6. Use HTTPS in production - Never send credentials over HTTP

For more examples and detailed documentation, visit the interactive docs at `/docs` endpoint.

