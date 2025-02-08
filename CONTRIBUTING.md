# Contributing to disk-canvas

Thank you for your interest in contributing to disk-canvas! We welcome contributions from the community.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/disk-canvas.git
   cd disk-canvas
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```
4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

The pre-commit hooks will automatically:
- Format your code with Black
- Sort imports with isort
- Check code style with flake8
- Fix common issues like trailing whitespace
- Run basic file checks

You can manually run the hooks on all files:
```bash
pre-commit run --all-files
```

## Development Process

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```

2. Make your changes and ensure:
   - All tests pass: `pytest`
   - Pre-commit hooks pass on your changes
   - Code is automatically formatted by Black and isort
   - No linting errors from flake8

3. Write tests for new functionality

4. Update documentation as needed

5. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

6. Push to your fork:
   ```bash
   git push origin feature-name
   ```

7. Create a Pull Request

## Pull Request Guidelines

- Include a clear description of the changes
- Link any related issues
- Ensure all tests pass
- Follow the existing code style
- Include tests for new functionality
- Update documentation as needed

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Maximum line length is 88 characters (Black default)
- Use descriptive variable names
- Add docstrings for functions and classes

## Running Tests

```bash
pytest
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
