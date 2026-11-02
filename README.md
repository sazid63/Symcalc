# SymCalc — University Calculus Solver

A modern web + desktop application for solving university-level calculus problems. Built with **Flask**, **PySide6 (Qt for Python)**, and **SymPy** — 21 operations with KaTeX math rendering, interactive graphs, and a polished dark-theme UI.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![PySide6](https://img.shields.io/badge/PySide6-6.12+-green.svg)](https://pypi.org/project/PySide6/)
[![SymPy](https://img.shields.io/badge/SymPy-1.14+-orange.svg)](https://www.sympy.org/)
[![KaTeX](https://img.shields.io/badge/KaTeX-0.16+-purple.svg)](https://katex.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Backend Audits](https://img.shields.io/badge/Audits-10/10-passing-brightgreen.svg)](#-running-backend-audits)
[![Frontend Audits](https://img.shields.io/badge/Frontend%20Audits-5/5-passing-brightgreen.svg)](#-frontend-audits)

## ✨ Features

| Category | Operations |
|----------|-----------|
| **Single Variable** | Derivatives (all orders), Integrals (indefinite, definite, improper), Limits, Taylor/Maclaurin Series, Tangent & Normal Lines, Arc Length, Volume & Surface of Revolution |
| **Multivariable** | Partial Derivatives, Gradient (∇f), Hessian Matrix, Critical Points, Laplacian (∇²f) |
| **Vector Calculus** | Divergence (∇·F), Curl (∇×F), Double & Triple Integrals |
| **Advanced** | ODE Solvers, Residue Calculus, Fourier Series, Laplace Transforms & Inverse |

### UI Highlights (v2.0)

- **Modern dark theme** — deep space palette with gradient headings and subtle glow
- **KaTeX math rendering** — beautiful typeset results with plain-text fallback
- **Responsive layout** — collapsible mobile sidebar, adaptive grids, full-width drawers
- **Toast notifications** — non-blocking success/error feedback (no `alert()`)
- **Persistent history** — last 50 calculations saved to `localStorage`
- **Keyboard shortcuts** — `Ctrl/Cmd+Enter` solve, `Ctrl/Cmd+K` focus input, `Esc` close
- **Accessibility** — ARIA labels, focus-visible outlines, `prefers-reduced-motion` support
- **Interactive graphs** — every single-variable operation plots the function with derivatives, critical points, and result markers
- **Two frontends** — web (Flask + HTML/CSS/JS) and native desktop (PySide6)

## 🚀 Quick Start

### Web (default)

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

### Desktop (PySide6)

```bash
python run.py
# or double-click start.bat on Windows
```

## 📁 Project Structure

```
calculas/
├── main.py                 # PySide6 desktop app
├── calculus_core.py        # SymPy calculus engine
├── app.py                  # Flask web backend (REST API)
├── run.py                  # Desktop entry point
├── start.bat               # Windows launcher
├── requirements.txt        # Dependencies
├── README.md               # This file
│
├── static/                 # Web frontend
│   ├── index.html          # App shell (HTML5, ARIA, KaTeX)
│   ├── style.css           # Modern dark theme, responsive
│   └── app.js              # Frontend logic, toasts, history
│
├── tests/                  # Unit & integration tests
│   ├── test_all.py         # Core operations suite
│   ├── test_calculus.py    # Single-variable tests
│   ├── test_ode.py         # ODE-specific tests
│   ├── test_qt.py          # Qt widget tests
│   ├── test_api.py         # Flask API tests
│   └── ...
│
└── audits/                 # Audit system (10 backend + 5 frontend loops)
    ├── run_audits.py       # Backend audit runner
    ├── audit_loop_1..10.py # Backend audits (syntax, structure, ...)
    ├── frontend_audit_1.py # Structure & accessibility
    ├── frontend_audit_2.py # CSS, responsiveness, visual integrity
    ├── frontend_audit_3.py # JS syntax & backend integration
    ├── frontend_audit_4.py # UI-backend communication integrity
    └── frontend_audit_5.py # Code style & maintainability
```

## 🧪 Running Backend Audits

The project ships with a **10-loop backend audit system** that validates the Python codebase line-by-line:

```bash
cd audits
python run_audits.py
```

| Loop | Check | Status |
|------|-------|--------|
| 1 | Syntax & import validation | ✅ |
| 2 | Class & method structure | ✅ |
| 3 | Variable initialization | ✅ |
| 4 | Operation coverage (21 ops) | ✅ |
| 5 | Memory & resource leaks | ✅ |
| 6 | Error handling | ✅ |
| 7 | Thread safety | ✅ |
| 8 | UI consistency | ✅ |
| 9 | Calculation correctness | ✅ (16/16 tests) |
| 10 | Final integration | ✅ |

## 🧪 Frontend Audits

A **5-loop frontend audit system** validates the web UI line-by-line (HTML, CSS, JS):

```bash
cd audits
python frontend_audit_1.py   # Structure & accessibility
python frontend_audit_2.py   # CSS styling & responsiveness
python frontend_audit_3.py   # JS syntax & API integration
python frontend_audit_4.py   # UI-backend communication integrity
python frontend_audit_5.py   # Code style & maintainability
```

| Loop | Check | Status |
|------|-------|--------|
| 1 | HTML5 structure, ARIA labels, landmarks | ✅ |
| 2 | CSS theming, responsive breakpoints, grid | ✅ |
| 3 | JS functions, API endpoints, form data, toasts | ✅ |
| 4 | UI↔backend data flow, error handling, history | ✅ |
| 5 | Code style, docstrings, indentation, duplication | ✅ |

## 📝 Input Syntax

```
# Powers & functions
x^2 + 2*x + 1          sin(x)*cos(x)      exp(-x^2)
log(x^2 + 1)           sqrt(1 - x^2)      abs(x)

# Constants
pi                     e                    oo (infinity)
I                      (imaginary unit)

# Variables
x, y, z, t             a, b, c, n         (parameters)

# ODE format
y' = y                              # dy/dx = y
y'' + y = 0                         # harmonic oscillator
y' + 2*y = exp(x)                   # first-order linear
y''' - 3*y'' + 2*y' = 0             # third-order
```

Or SymPy native: `Eq(Derivative(y(x), x), y(x))`

## 🖥️ UI Overview

```
┌─────────────────────────────────────────────────────────┐
│  ∂ Calculas                              [⏱] [?]       │
├──────────────┬──────────────────────────────────────────┤
│ SINGLE VAR   │  Derivative                              │
│  d/dx ── ●   │  Compute the derivative of a function    │
│  ∫           │                                          │
│  lim         │  f(x)                                    │
│  Σ           │  ┌────────────────────────────────────┐  │
│  ⟋          │  │ x^3*sin(2*x) + exp(-x^2)           │  │
│              │  └────────────────────────────────────┘  │
│ MULTI-VAR    │  Variable [x ▾]  Order [1]              │
│  ∂  ∇  H     │                                          │
│              │  [ ▶ Solve ]  [ Clear ]  [ Examples ]    │
│ VECTOR CALC  │                                          │
│  ∇· ∇×      │  ┌────────────────────────────────────┐  │
│              │  │  Result  3*x^2*cos(2*x) - ...      │  │
│ ADVANCED     │  └────────────────────────────────────┘  │
│  dy/dx  F    │  ┌────────────────────────────────────┐  │
│  ℒ  ℒ⁻¹     │  │  📊  Interactive graph             │  │
└──────────────┴──────────────────────────────────────────┘
```

## 🔧 Dependencies

| Package | Min Version | Purpose |
|---------|------------|---------|
| Flask | 3.0+ | Web backend (REST API) |
| PySide6 | 6.12+ | Qt GUI framework (desktop) |
| SymPy | 1.14+ | Symbolic mathematics engine |
| NumPy | 1.26+ | Numerical array operations |
| Matplotlib | 3.8+ | Function plotting (desktop) |

```bash
pip install -r requirements.txt
```

## 🧠 Built With

- **[Flask](https://flask.palletsprojects.com/)** — Lightweight web backend
- **[PySide6](https://pypi.org/project/PySide6/)** — Qt for Python (desktop GUI)
- **[SymPy](https://www.sympy.org/)** — Computer algebra system
- **[KaTeX](https://katex.org/)** — Fast math rendering
- **[Matplotlib](https://matplotlib.org/)** — Publication-quality plotting

## 📄 License

MIT License — Built with ❤️ using DeepSeek Harness

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run audits to verify (`cd audits && python run_audits.py`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 🐛 Issues

Found a bug? Have a feature request? Please [open an issue](https://github.com/sazid63/symcalc/issues).

---

**Version:** 2.0.0 · **Branch:** master · **Author:** Sajid
