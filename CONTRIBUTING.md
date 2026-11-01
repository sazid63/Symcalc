# Contributing to Calculas

Thank you for your interest in contributing to Calculas! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/calculas.git
   cd calculas
   ```
3. Set up your development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8
   ```

## Development Workflow

### Branch Organization

We use the following branch structure:

- `master` - Main production branch
- `ui-enhancements` - For UI/UX improvements
- `audit-automation` - For audit system improvements
- `repo-organization` - For repository structure changes
- `feature/*` - For other features
- `bugfix/*` - For bug fixes
- `hotfix/*` - For emergency fixes

### Creating a Feature Branch

1. Start from `master`:
   ```bash
   git checkout master
   git pull origin master
   ```

2. Create a new feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. Make your changes

4. Run audits to verify code quality:
   ```bash
   cd audits
   python run_audits.py
   ```

5. Run tests:
   ```bash
   python -m pytest tests/ -v
   ```

6. Commit your changes with clear messages:
   ```bash
   git add .
   git commit -m "feat(calculus): add integration with advanced ODE solvers"
   ```

7. Push and create a pull request

## Code Style and Quality

### Python Code Style

- Follow PEP 8 style guidelines
- Use `black` for code formatting:
  ```bash
  black .
  ```
- Use `flake8` for linting:
  ```bash
  flake8 .
  ```

### Commit Message Format

Use conventional commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build process or auxiliary tool changes

Examples:
```
feat(calculus): add support for multivariable limits
fix(ui): resolve button alignment issues
docs: update installation instructions
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_calculus.py -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Audit System

The project includes a 10-loop audit system that validates code quality:

```bash
cd audits
python run_audits.py
```

Audit loops check:
1. Syntax & imports
2. Class/method structure
3. Variable initialization
4. Operation coverage
5. Memory/resource leaks
6. Error handling
7. Thread safety
8. UI consistency
9. Calculation correctness
10. Final integration

## Pull Request Process

1. Ensure your code passes all audits and tests
2. Update documentation as needed
3. Add tests for new functionality
4. Create a pull request with a clear description
5. Link to any related issues
6. Wait for review and feedback

## Reporting Issues

When reporting bugs, please include:

1. Environment information (OS, Python version)
2. Steps to reproduce
3. Expected vs actual behavior
4. Error messages (if any)
5. Relevant code snippets

## Development Branches

### Feature Branches

For new features, create branches from `master`:
```bash
git checkout -b feature/new-feature-name
```

### Bugfix Branches

For bug fixes, create branches from `master`:
```bash
git checkout -b bugfix/issue-description
```

### Hotfix Branches

For emergency fixes, create from the latest tag:
```bash
git checkout -b hotfix/urgent-fix v1.0.1
```

## Release Process

1. Update version in appropriate files
2. Create a new tag:
   ```bash
   git tag -a v1.0.2 -m "Release v1.0.2: New features and bug fixes"
   ```
3. Push the tag:
   ```bash
   git push origin v1.0.2
   ```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.