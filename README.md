# Calculas — University Calculus Solver

A native Windows desktop application for solving university-level calculus problems. Built with **PySide6 (Qt for Python)** and **SymPy** — no browser, no localhost server required.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.12+-green.svg)](https://pypi.org/project/PySide6/)
[![SymPy](https://img.shields.io/badge/SymPy-1.14+-orange.svg)](https://www.sympy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![10-Audit Loops](https://img.shields.io/badge/Audits-10/10-passing-brightgreen.svg)](#-running-audits)

## ✨ Features

| Category | Operations |
|----------|-----------|
| **Single Variable** | Derivatives (all orders), Integrals (indefinite, definite, improper), Limits, Taylor/Maclaurin Series, Tangent & Normal Lines, Arc Length, Volume & Surface of Revolution |
| **Multivariable** | Partial Derivatives, Gradient (∇f), Hessian Matrix, Critical Points, Laplacian (∇²f) |
| **Vector Calculus** | Divergence (∇·F), Curl (∇×F), Double & Triple Integrals |
| **Advanced** | ODE Solvers, Residue Calculus, Fourier Series, Laplace Transforms |

Each operation includes an **interactive graph** visualizing the function, its derivative, critical points, and result markers.

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python run.py
# or double-click start.bat on Windows
```

## 📁 Project Structure

```
calculas/
├── main.py                 # PySide6 desktop app (1400+ lines)
├── calculus_core.py        # SymPy calculus engine (280 lines)
├── app.py                  # Flask web backend (REST API)
├── run.py                  # Desktop entry point
├── start.bat               # Windows launcher
├── requirements.txt        # Dependencies
├── README.md               # This file
│
├── static/                 # Web frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── tests/                  # Unit & integration tests
│   ├── test_all.py         # Core operations suite
│   ├── test_calculus.py    # Single-variable tests
│   ├── test_ode.py         # ODE-specific tests
│   ├── test_qt.py          # Qt widget tests
│   ├── test_api.py         # Flask API tests
│   └── ...
│
└── audits/                 # 10-loop audit system
    ├── run_audits.py       # Runner script
    ├── audit_loop_1.py     # Syntax & imports
    ├── audit_loop_2.py     # Class/method structure
    ├── audit_loop_3.py     # Variable initialization
    ├── audit_loop_4.py     # Operation coverage
    ├── audit_loop_5.py     # Memory/resource leaks
    ├── audit_loop_6.py     # Error handling
    ├── audit_loop_7.py     # Thread safety
    ├── audit_loop_8.py     # UI consistency
    ├── audit_loop_9.py     # Calculation correctness
    └── audit_loop_10.py    # Final integration
```

## 🧪 Running Audits

The project ships with a **10-loop audit system** that validates the codebase line-by-line:

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
┌─────────────────┬──────────────────────────────────────┐
│ 📂 Sidebar      │  ∂ Calculus Solver                   │
│                 │                                      │
│ Single Variable │  [Expression: x^3*sin(2*x) ]         │
│  • Derivative   │                                      │
│  • Integral     │  [Variable: x] [Order: 1]            │
│  • Limit        │                                      │
│  • Series       │  ▶ Solve   ✕ Clear   ★ Fill Example │
│  • Tangent      │                                      │
│ Multivariable   ├──────────────────────────────────────┤
│  • Partial      │  Result:  3*x^2*cos(2*x) - 2*x^3*   │
│  • Gradient     │         sin(2*x)                     │
│  • Hessian      │                                      │
│ Vector Calculus │  [📊 Plot Function] [✕ Clear]        │
│ Advanced        │                                      │
│  • ODE          │  [Interactive graph appears here]    │
│  • Fourier      │                                      │
│  • Laplace      │                                      │
└─────────────────┴──────────────────────────────────────┘
```

## 🔧 Dependencies

| Package | Min Version | Purpose |
|---------|------------|---------|
| PySide6 | 6.12+ | Qt GUI framework |
| SymPy | 1.14+ | Symbolic mathematics engine |
| NumPy | 1.26+ | Numerical array operations |
| Matplotlib | 3.8+ | Function plotting |

```bash
pip install -r requirements.txt
```

## 🧠 Built With

- **[PySide6](https://pypi.org/project/PySide6/)** — Qt for Python (desktop GUI)
- **[SymPy](https://www.sympy.org/)** — Computer algebra system (symbolic math)
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

Found a bug? Have a feature request? Please [open an issue](https://github.com/sazid63/calculas/issues).

---

**Version:** 1.0.0 · **Branch:** master · **Author:** Sajid
