# Calculas — University Calculus Solver

A native Windows desktop application for solving university-level calculus problems. Built with **PySide6 (Qt for Python)** and **SymPy** — no browser, no localhost server required.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.12+-green.svg)
![SymPy](https://img.shields.io/badge/SymPy-1.14+-orange.svg)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
# Or double-click start.bat
```

## ✨ Features

### Single Variable Calculus
- **Derivatives** — First, second, and higher-order derivatives
- **Integrals** — Indefinite, definite, and improper integrals
- **Limits** — Two-sided, one-sided, and limits at infinity
- **Series Expansion** — Taylor and Maclaurin series
- **Tangent & Normal Lines** — Equations at any point
- **Arc Length** — Curve length over an interval
- **Volume/Surface of Revolution** — Disc, shell, and surface area methods

### Multivariable Calculus
- **Partial Derivatives** — Mixed and higher-order partials
- **Gradient** — ∇f vector field
- **Hessian Matrix** — Second derivative matrix
- **Critical Points** — Solve ∇f = 0
- **Laplacian** — ∇²f operator

### Vector Calculus
- **Divergence** — ∇·F for vector fields
- **Curl** — ∇×F in 3D
- **Multiple Integrals** — Double and triple integrals

### Advanced Topics
- **Ordinary Differential Equations (ODEs)** — First and second order
- **Residue Calculus** — Complex analysis residues
- **Fourier Series** — a₀, aₙ, bₙ coefficients
- **Laplace Transforms** — Forward and inverse transforms

## 📁 Project Structure

```
calculas/
├── main.py                 # PySide6 desktop application (1400+ lines)
├── calculus_core.py        # SymPy calculus operations (280 lines)
├── run.py                  # Application entry point
├── start.bat               # Windows launcher
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── static/                 # Web frontend (Flask backend: app.py)
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── tests/                  # Unit and integration tests
│   ├── test_all.py
│   ├── test_calculus.py
│   ├── test_ode.py
│   ├── test_qt.py
│   └── ...
│
└── audits/                 # 10-loop audit system
    ├── run_audits.py
    ├── audit_loop_1.py     # Syntax & import validation
    ├── audit_loop_2.py     # Class & method structure
    ├── audit_loop_3.py     # Variable initialization
    ├── audit_loop_4.py     # Operation coverage
    ├── audit_loop_5.py     # Memory & resource leaks
    ├── audit_loop_6.py     # Error handling
    ├── audit_loop_7.py     # Thread safety
    ├── audit_loop_8.py     # UI consistency
    ├── audit_loop_9.py     # Calculation correctness
    └── audit_loop_10.py    # Final integration test
```

## 🧪 Running Audits

The project includes a comprehensive 10-loop audit system that validates the codebase line-by-line:

```bash
cd audits
python run_audits.py
```

**Audit Coverage:**
1. **Syntax & Import Validation** — Python syntax, module availability
2. **Class & Method Structure** — Class definitions, method signatures
3. **Variable Initialization** — Proper initialization before use
4. **Operation Coverage** — All operations have handlers
5. **Memory & Resource Leaks** — Array allocations, recursion checks
6. **Error Handling** — try/except blocks, error messages
7. **Thread Safety** — Qt thread primitives, signal/slot usage
8. **UI Consistency** — Qt component usage, styling
9. **Calculation Correctness** — Mathematical verification
10. **Final Integration** — Full application import and smoke test

## 📝 Input Syntax

| Element | Syntax | Examples |
|---------|--------|----------|
| Powers | `^` or `**` | `x^2`, `(1+x)^10` |
| Trig Functions | `sin`, `cos`, `tan`, `cot`, `sec`, `csc` | `sin(x)*cos(x)` |
| Inverse Trig | `asin`, `acos`, `atan` | `asin(x)` |
| Hyperbolic | `sinh`, `cosh`, `tanh` | `sinh(x)` |
| Exp/Log | `exp`, `log` (natural), `log2`, `log10` | `exp(x)`, `log(x)` |
| Roots/Abs | `sqrt`, `abs` | `sqrt(1-x^2)`, `abs(x)` |
| Constants | `pi`, `e`, `oo` (∞), `I` (imaginary) | `2*pi`, `exp(-oo)` |
| Variables | `x`, `y`, `z`, `t`, `a`, `b`, `c`, `n` | `x^2 + y^2 + z^2` |

### ODE Input Format

```
y' = y                    # First order: dy/dx = y
y'' + y = 0               # Second order: harmonic oscillator
y' + 2*y = exp(x)         # First order linear
y''' - 3*y'' + 2*y' = 0   # Third order
```

Or use SymPy native format:
```
Eq(Derivative(y(x), x), y(x))
Eq(Derivative(y(x), x, 2) + y(x), 0)
```

## 🖥️ UI Overview

- **Left Sidebar** — Browse operations by category (Single Variable, Multivariable, Vector Calculus, Advanced)
- **Center Panel** — Enter expression, configure parameters (variable, order, bounds, etc.)
- **Action Buttons** — Solve, Clear, Fill Example
- **Result Panel** — View computed result, step-by-step explanation, and LaTeX output
- **Plot Widget** — Visualize functions with interactive graphs
- **History Drawer** — Access recent calculations

## 🔧 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PySide6 | 6.12+ | Qt GUI framework |
| SymPy | 1.14+ | Symbolic mathematics |
| NumPy | 1.26+ | Numerical array support |
| Matplotlib | 3.8+ | Function plotting |

Install all at once:
```bash
pip install -r requirements.txt
```

## 📸 Screenshots

*(Coming soon — desktop app in action)*

## 🧠 Built With

- [PySide6](https://pypi.org/project/PySide6/) — Qt for Python
- [SymPy](https://www.sympy.org/) — Computer algebra system
- [Matplotlib](https://matplotlib.org/) — Visualization library

## 📄 License

MIT License — Built with ❤️ using DeepSeek Harness

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Issues

Found a bug? Have a feature request? Please open an issue on GitHub.

---

**Version:** 1.0.0  
**Last Updated:** 2026  
**Author:** Sajid
