# Calculas Repository Structure

## Overview

Calculas is a university calculus solver built with Python, featuring both desktop and web interfaces. This document explains the repository structure and organization.

## Directory Structure

```
calculas/
├── .github/                    # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml             # CI/CD pipeline
├── audits/                     # Audit system (10 loops)
│   ├── run_audits.py          # Main audit runner
│   ├── audit_loop_1.py        # Syntax & imports
│   ├── audit_loop_2.py        # Class/method structure
│   ├── audit_loop_3.py        # Variable initialization
│   ├── audit_loop_4.py        # Operation coverage
│   ├── audit_loop_5.py        # Memory/resource leaks
│   ├── audit_loop_6.py        # Error handling
│   ├── audit_loop_7.py        # Thread safety
│   ├── audit_loop_8.py        # UI consistency
│   ├── audit_loop_9.py        # Calculation correctness
│   └── audit_loop_10.py       # Final integration
├── static/                     # Web frontend assets
│   ├── index.html            # Main web interface
│   ├── style.css             # Web application styles
│   └── app.js                # Web application logic
├── tests/                      # Test suite
│   ├── test_all.py           # Comprehensive test suite
│   ├── test_calculus.py      # Calculus operation tests
│   ├── test_ode.py           # ODE solver tests
│   ├── test_qt.py            # Qt widget tests
│   ├── test_api.py           # Flask API tests
│   ├── test_frontend.py      # Frontend tests
│   ├── test_debug.py         # Debug functionality tests
│   └── debug_x.py            # Debug utilities
├── main.py                     # PySide6 desktop application (1400+ lines)
├── calculus_core.py            # SymPy calculus engine (280 lines)
├── app.py                      # Flask web backend (REST API)
├── run.py                      # Desktop entry point
├── start.bat                   # Windows launcher
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── CONTRIBUTING.md             # Contribution guidelines
├── .gitignore                  # Git ignore rules
└── LICENSE                     # MIT License
```

## Core Components

### Desktop Application (`main.py`)

The main desktop application built with PySide6 (Qt for Python):

- **MainWindow**: Main application window with sidebar and main panel
- **OperationPanel**: Dynamic UI for different calculus operations
- **ComputeThread**: Background computation thread for non-blocking UI
- **Interactive graphs** using Matplotlib
- **Real-time calculation** with SymPy

### Calculus Engine (`calculus_core.py`)

The mathematical core of the application:

- **Expression parsing** with SymPy
- **Derivatives** (all orders)
- **Integrals** (indefinite, definite, improper)
- **Limits** and series expansions
- **Multivariable calculus** (partials, gradients, Hessians)
- **Vector calculus** (divergence, curl)
- **ODE solvers** and advanced operations

### Web Backend (`app.py`)

Flask-based REST API for web interface:

- **RESTful endpoints** for all calculus operations
- **JSON API** for frontend communication
- **Error handling** and validation
- **Caching** for performance

### Audit System (`audits/`)

Comprehensive 10-loop audit system:

1. **Syntax & Imports**: Validate Python syntax and imports
2. **Class Structure**: Verify class and method organization
3. **Variables**: Check variable initialization and usage
4. **Operations**: Ensure all 21 calculus operations are covered
5. **Memory**: Detect memory leaks and resource issues
6. **Error Handling**: Verify proper exception handling
7. **Thread Safety**: Check thread safety for concurrent operations
8. **UI Consistency**: Validate UI component consistency
9. **Correctness**: Test mathematical calculation accuracy
10. **Integration**: Final integration and compatibility tests

## Branch Strategy

### Main Branches

- **master**: Production-ready code
- **main**: Alternative production branch (if used)

### Feature Branches

- **ui-enhancements**: UI/UX improvements and new features
- **audit-automation**: Audit system improvements
- **repo-organization**: Repository structure changes
- **feature/***: Other new features
- **bugfix/***: Bug fixes
- **hotfix/***: Emergency fixes

### Version Control

- **Semantic Versioning**: Follows v1.0.0, v1.0.1, etc.
- **Git Tags**: Annotated tags for releases
- **Commit Messages**: Conventional commits format

## Development Workflow

### Local Development

1. Clone and set up environment
2. Create feature branch from `master`
3. Make changes and run audits
4. Commit with clear messages
5. Push and create pull request

### CI/CD Pipeline

Automated workflows in `.github/workflows/ci.yml`:

- **Testing**: Multi-Python version testing
- **Audits**: Run audit system
- **Code Coverage**: Upload to Codecov
- **Build**: Create distribution packages
- **Deployment**: Upload artifacts

## Testing Strategy

### Unit Tests

Located in `tests/` directory:

- **test_calculus.py**: Core calculus operations
- **test_ode.py**: ODE solver functionality
- **test_qt.py**: Qt widget testing
- **test_api.py**: API endpoint testing
- **test_frontend.py**: Frontend functionality

### Integration Tests

- **test_all.py**: Comprehensive integration tests
- **Audit System**: Full workflow validation

### Test Coverage

- Target: 90%+ code coverage
- Tools: pytest, pytest-cov
- Reports: XML for CI, HTML for local review

## File Organization Principles

### Separation of Concerns

- **UI Logic**: Main application (PySide6)
- **Math Engine**: Core calculations (SymPy)
- **API Layer**: Web interface (Flask)
- **Tests**: Separate test files
- **Audits**: Quality assurance system

### Naming Conventions

- **Snake_case** for Python files and variables
- **PascalCase** for classes
- **kebab-case** for branches and tags
- **UPPER_CASE** for constants

### Documentation

- **README.md**: Project overview and usage
- **CONTRIBUTING.md**: Development guidelines
- **Inline comments**: Code documentation
- **Docstrings**: Function and class documentation

## Dependencies

### Core Dependencies

- **PySide6**: Qt GUI framework
- **SymPy**: Symbolic mathematics
- **NumPy**: Numerical computing
- **Matplotlib**: Plotting and visualization
- **Flask**: Web framework

### Development Dependencies

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatter
- **flake8**: Code linter

## Deployment

### Desktop Application

- **Windows**: `start.bat` launcher
- **Cross-platform**: `run.py` entry point
- **Dependencies**: Bundled with requirements.txt

### Web Application

- **Backend**: Flask API
- **Frontend**: HTML/CSS/JavaScript
- **Static Files**: Served from `/static` directory

### Distribution

- **Source Distribution**: Build with `python -m build`
- **Artifacts**: Uploaded via GitHub Actions
- **Installation**: `pip install` from distribution