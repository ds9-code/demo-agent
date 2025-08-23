# Zitnik Lab Repository Template

[![Release](https://img.shields.io/github/v/release/mims-harvard/template)](https://img.shields.io/github/v/release/mims-harvard/template)
[![Build status](https://img.shields.io/github/actions/workflow/status/mims-harvard/template/main.yml?branch=main)](https://github.com/mims-harvard/template/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mims-harvard/template)](https://img.shields.io/github/commit-activity/m/mims-harvard/template)
[![License](https://img.shields.io/github/license/mims-harvard/template)](https://img.shields.io/github/license/mims-harvard/template)

A modern, production-ready template for Python-based research projects in the Zitnik Lab.

- **Template repository**: <https://github.com/mims-harvard/template/>
- **Documentation** <https://zitniklab.hms.harvard.edu/template>

## Highlights

- 🚀 **Fast setup** with automated environment configuration and dependency management.
- 🛠️ **Pre-configured tooling** including linting, formatting, and testing with [pre-commit hooks](https://pre-commit.com/).
- 📦 **Modern Python packaging** using [uv](https://docs.astral.sh/uv/) for lightning-fast dependency resolution.
- 🔄 **CI/CD ready** with [GitHub Actions](https://github.com/features/actions) for automated testing and deployment.
- 📝 **Documentation ready** with automatic documentation generation with [MkDocs](https://squidfunk.github.io/mkdocs-material/).
- 🧪 **Testing framework** pre-configured with [pytest](https://docs.pytest.org/en/stable/) and coverage reporting.
- 🔧 **Development tools** including [Makefile](Makefile) commands for common tasks.

This template provides everything you need to start a new research project with modern Python best practices built-in.

## Quick Start

### Prerequisites

Minimal requirements:

- [GNU Make](https://www.gnu.org/software/make/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

Optional:

- [Docker](https://docs.docker.com/engine/install/)

### Getting Started

1. **Create your project** by using this template on GitHub or cloning it locally

2. **Set up your development environment:**
   ```bash
   make install
   ```
   This command will:
   - Create a virtual environment
   - Install all dependencies
   - Set up pre-commit hooks
   - Configure development tools

3. **Verify everything works:**
   ```bash
   make check
   ```
   This runs code formatting and linting checks to ensure your setup is correct.

4. **Commit your initial setup:**
   ```bash
   git add .
   git commit -m "Initial project setup"
   git push origin main
   ```

You're now ready to start development! The CI/CD pipeline will automatically run when you open pull requests or push to main.

## Development Commands

The template includes convenient Makefile commands for common development tasks:

- `make install` - Set up development environment
- `make check` - Run linting and formatting checks
- `make test` - Run test suite
- `make docs` - Build documentation
- `make clean` - Clean up build artifacts

You can see all available commands running `make help`:

```console
$ make

Usage: make <command>
    help                 List available commands with their descriptions
    install              Create the virtual environment and install the pre-commit hooks
    check                Run code quality tools.
    test                 Test the code with pytest
    build                Build wheel file
    clean-build          Clean build artifacts
    docs-test            Test if documentation can be built without warnings or errors
    docs                 Build and serve the documentation
    clean                Clean up the project
```

## Support

For questions about using this template or contributing improvements, please open an issue in the GitHub repository.

## License

This template is released under the [MIT License](LICENSE).
