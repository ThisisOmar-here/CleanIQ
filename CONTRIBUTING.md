# Contributing to CleanIQ

First off, thank you for considering contributing to CleanIQ! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (file paths, error messages, etc.)
- **Describe the behavior you observed** and what you expected
- **Include your environment details** (OS, Python version, Ollama version)

### Suggesting Features

Feature suggestions are welcome! Please:

- **Check if the feature has already been suggested**
- **Provide a clear and detailed explanation** of the feature
- **Explain why this feature would be useful** to most CleanIQ users

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the code style** of the project
3. **Add tests** if applicable
4. **Update documentation** if needed
5. **Write a clear PR description** explaining your changes

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/cleaniq.git
   cd cleaniq
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Ollama and pull a model:
   ```bash
   ollama pull llama3.2
   ```

5. Run the development server:
   ```bash
   uvicorn app:app --reload
   ```

## Code Style Guidelines

- Follow **PEP 8** for Python code
- Use **type hints** for function arguments and return values
- Write **docstrings** for all functions and classes
- Keep functions focused and small
- Use meaningful variable names

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Keep the first line under 72 characters
- Reference issues and pull requests when relevant

## Questions?

Feel free to open an issue with the "question" label if you have any questions!

---

Thank you for contributing! ❤️
