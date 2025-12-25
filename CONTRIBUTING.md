# Contributing Guide

Thank you for your interest in contributing to this project!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/project.git
   cd project
   ```

3. Set up development environment:
   ```bash
   make setup
   # Edit .env with your configuration
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If you have dev dependencies
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests:
   ```bash
   make test
   ```

4. Ensure code quality:
   ```bash
   black app/ scripts/ tests/
   isort app/ scripts/ tests/
   flake8 app/ scripts/ tests/
   ```

5. Commit your changes:
   ```bash
   git commit -m "Add: your feature description"
   ```

6. Push and create a pull request

## Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions focused and small

## Testing

- Write tests for new features
- Aim for >80% code coverage
- Include both unit and integration tests
- Test edge cases and error handling

## Pull Request Process

1. Update README.md if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Request review from maintainers

## Questions?

Open an issue for questions or discussions about the project.


