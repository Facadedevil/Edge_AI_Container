# Contributing to Edge AI Container

First off, thank you for considering contributing to the Universal Edge AI Container Solution! It's people like you that help make this project better for everyone working with edge AI applications.

## Table of Contents

- [Contributing to Edge AI Container](#contributing-to-edge-ai-container)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
  - [Development Environment](#development-environment)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Pull Request Process](#pull-request-process)
    - [Pull Request Requirements](#pull-request-requirements)
  - [Development Guidelines](#development-guidelines)
    - [Code Style](#code-style)
    - [Commit Messages](#commit-messages)
    - [Testing](#testing)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
    - [Feature Request Template](#feature-request-template)
  - [License](#license)
  - [Questions?](#questions)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [project maintainer's email].

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/Facadedevil/Edge_AI_Container.git
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/Facadedevil/Edge_AI_Container.git
   ```

## Development Environment

### Prerequisites
- NVIDIA GPU with CUDA support or Jetson device
- Docker and Docker Compose
- NVIDIA Container Toolkit
- Python 3.9 or higher

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the development container:
   ```bash
   docker compose -f docker-compose.dev.yml build
   ```

3. Run tests:
   ```bash
   python -m pytest tests/
   ```

## Pull Request Process

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git commit -m "Add some feature"
   ```

3. Keep your branch updated:
   ```bash
   git pull upstream main
   git rebase upstream/main
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Submit a Pull Request

### Pull Request Requirements
- Update documentation as needed
- Add tests for new features
- Ensure CI/CD pipeline passes
- Follow coding standards
- Include relevant issue numbers
- Update CHANGELOG.md if applicable

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb in present tense
- Keep first line under 50 characters
- Reference issues when applicable

Example:
```
Add GPU memory optimization for Xavier NX

- Implement dynamic memory allocation
- Add temperature-based throttling
- Update documentation
Fixes #123
```

### Testing
- Write unit tests for new features
- Include integration tests for GPU functionality
- Test on multiple Jetson platforms if possible
- Verify memory usage and performance

## Reporting Bugs

When reporting bugs, include:
1. Your operating system and version
2. Hardware specifications (GPU model, Jetson device type)
3. Steps to reproduce the issue
4. Expected vs actual behavior
5. Relevant logs and screenshots

Use the bug report template when creating an issue.

## Suggesting Enhancements

For enhancement suggestions:
1. Clearly describe the feature
2. Provide use cases
3. Consider impact on different hardware platforms
4. Discuss potential implementation approaches

### Feature Request Template
```markdown
## Feature Description
[Describe the feature]

## Use Cases
- [Use case 1]
- [Use case 2]

## Proposed Implementation
[Your ideas about implementation]

## Potential Impact
[Impact on performance/resources]
```

## License

By contributing to this project, you agree that your contributions will be licensed under the GNU General Public License v3.0.

## Questions?

Don't hesitate to create an issue for questions or join our [community chat/forum] for discussions.

Thank you for contributing! 🚀