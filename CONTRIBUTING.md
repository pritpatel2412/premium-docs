# Contributing to premium-docs

Thank you for your interest in contributing to `premium-docs`! We welcome bug fixes, documentation improvements, new themes, and additional agent adapters.

---

## Development Setup

### Prerequisites
- Python 3.9 or higher
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/pritpatel2412/premium-docs.git
   cd premium-docs
   ```

2. Install development dependencies:
   ```bash
   pip install markdown pygments pytest
   ```

---

## Running Tests

We maintain a 100% green test suite covering compiler AST parsing, validator quality gates, contrast ratios, and installer operations:

```bash
# Run the complete test suite
python -m pytest -v tests/

# Run contrast checks only
python -m pytest -v tests/test_contrast.py

# Run validator tests only
python -m pytest -v tests/test_validator.py
```

---

## Testing Compiler & Validator

You can manually build and validate any markdown document:

```bash
# Build an example
python skills/premium-docs/scripts/build_doc.py skills/premium-docs/examples/technical-report.md -o output.html

# Validate the output
python skills/premium-docs/scripts/validate_doc.py output.html
```

---

## Code Guidelines

1. **Zero Runtime Dependencies**: The output HTML must remain 100% self-contained and offline. Never introduce external runtime CDN dependencies (`<script src="https://...">` or `<link href="https://...">`).
2. **WCAG AA Compliance**: All themes must achieve a minimum 4.5:1 text-to-canvas contrast ratio in both light and dark modes. Run `pytest tests/test_contrast.py` to mathematically verify contrast.
3. **Cross-Platform**: Python scripts (`install.py`, `build_doc.py`, `validate_doc.py`) must use standard library modules (`pathlib`, `shutil`) and work uniformly on Windows, macOS, and Linux.
4. **Conventional Commits**: Format your commit messages using Conventional Commits:
   - `feat(...)`: New features or containers
   - `fix(...)`: Bug fixes
   - `docs(...)`: Documentation updates
   - `test(...)`: Test additions or refactoring

---

## Pull Request Process

1. Create a branch: `git checkout -b feature/my-new-feature`
2. Implement your changes.
3. Verify all tests pass: `python -m pytest -v tests/`
4. Commit your changes: `git commit -m "feat(theme): add nord theme"`
5. Submit a Pull Request on GitHub.
