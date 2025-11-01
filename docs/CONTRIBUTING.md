# Contributing to TaskFlow API

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## Branch Strategy

We use Git Flow branching strategy:

- `main` - Production-ready code (protected)
- `develop` - Development branch (protected)
- `feature/*` - New features (e.g., `feature/add-user-roles`)
- `bugfix/*` - Bug fixes (e.g., `bugfix/fix-auth-token`)
- `hotfix/*` - Emergency production fixes
- `release/*` - Release preparation

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/taskflow-api.git
   cd taskflow-api
   ```

2. **Create a branch from develop**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   pre-commit install
   ```

4. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new features
   - Update documentation if needed

5. **Run tests and linters**
   ```bash
   # Run tests
   pytest

   # Run linters
   black app tests
   isort app tests
   flake8 app tests
   mypy app

   # Or use pre-commit
   pre-commit run --all-files
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

7. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, missing semicolons, etc.)
- `refactor` - Code refactoring (no functional changes)
- `test` - Adding or updating tests
- `chore` - Maintenance tasks (dependencies, build config, etc.)
- `perf` - Performance improvements
- `ci` - CI/CD changes

### Examples:
```
feat(auth): add password reset functionality

fix(tasks): resolve issue with task deletion

docs(readme): update installation instructions

test(auth): add tests for login endpoint
```

## Testing Guidelines

- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Group related tests in classes
- Use fixtures for common setup

```python
class TestFeatureName:
    """Tests for feature name."""

    @pytest.mark.asyncio
    async def test_specific_behavior(self, client: AsyncClient):
        """Test description."""
        # Arrange
        # Act
        # Assert
        pass
```

## Code Style

- Follow PEP 8
- Use type hints
- Max line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions/classes

```python
async def create_user(
    db: AsyncSession,
    user_data: UserCreate,
) -> User:
    """
    Create a new user in the database.

    Args:
        db: Database session
        user_data: User creation data

    Returns:
        User: Created user object

    Raises:
        ConflictException: If user already exists
    """
    # Implementation
```

## Pull Request Process

1. **Before submitting:**
   - Run all tests and ensure they pass
   - Run linters and fix any issues
   - Update documentation if needed
   - Rebase on latest develop branch

2. **PR Description should include:**
   - What changes were made and why
   - Related issue numbers (if any)
   - Testing performed
   - Screenshots (if UI changes)

3. **PR Review:**
   - Address reviewer comments
   - Keep discussions focused and professional
   - Update PR based on feedback

4. **After approval:**
   - Squash commits if needed
   - Ensure CI/CD passes
   - Merge to develop

## Bug Reports

When reporting bugs, please include:

- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and logs
- Screenshots if applicable

## Feature Requests

For feature requests, please describe:

- The problem you're trying to solve
- Proposed solution
- Alternative solutions considered
- Additional context

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update API documentation if endpoints change
- Include code examples when helpful

## Questions

If you have questions:

- Check existing documentation
- Search closed issues
- Open a new issue with [Question] tag
- Join our community discussions

## Code of Conduct

- Be respectful and professional
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README

Thank you for contributing!

