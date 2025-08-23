# Zitnik Lab Repository Template

[![Release](https://img.shields.io/github/v/release/mims-harvard/template)](https://img.shields.io/github/v/release/mims-harvard/template)
[![Build status](https://img.shields.io/github/actions/workflow/status/mims-harvard/template/main.yml?branch=main)](https://github.com/mims-harvard/template/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mims-harvard/template)](https://img.shields.io/github/commit-activity/m/mims-harvard/template)
[![License](https://img.shields.io/github/license/mims-harvard/template)](https://img.shields.io/github/license/mims-harvard/template)

This is a template repository for Python projects that use uv for their dependency management.

- **Github repository**: <https://github.com/mims-harvard/template/>
- **Documentation** <https://zitniklab.hms.harvard.edu/template>

## Getting started with your project

### 1. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 2. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 3. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m "Fix formatting issues"
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
