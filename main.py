"""
Calculas — University-Level Calculus Solver
Native Windows desktop application using PySide6 (Qt for Python)
"""
import sys
import os
import math
import json
import threading
from typing import Optional

import matplotlib
matplotlib.use('QtAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QGroupBox, QLabel, QFormLayout, QStackedWidget,
    QToolButton, QFrame, QSizePolicy, QMessageBox, QSplitter,
    QAbstractItemView, QTreeWidget, QTreeWidgetItem, QHeaderView,
    QLineEdit, QSpinBox, QPushButton
)
from PySide6.QtGui import QFont, QIcon, QTextCursor, QColor, QPalette
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QFileDialog

from calculus_core import (
    parse_expression, _get_var_symbol, GLOBAL_SYMBOLS, format_result,
    derivative, partial_derivative, integral, multiple_integral,
    limit_expr, series_expansion, solve_ode, gradient, divergence,
    curl, laplacian, critical_points, hessian_matrix, tangent_line,
    arc_length, surface_area, volume_of_revolution, improper_integral,
    residue, fourier_series, laplace_transform, inverse_laplace_transform,
    parse_ode_expression
)
import sympy as sp

# ============ OPERATION DEFINITIONS ============

CATEGORIES = [
    ("Single Variable", "sv"),
    ("Multivariable", "mv"),
    ("Vector Calculus", "vc"),
    ("Advanced", "adv"),
]

OPERATIONS = {
    "sv": [
        {
            "name": "Derivative",
            "key": "derivative",
            "desc": "f'(x), f''(x), higher order",
            "fields": [
                ("variable", "Variable", {"x": "x", "y": "y", "z": "z", "t": "t"}, "combo", "x"),
                ("order", "Order", None, "number", "1"),
            ],
            "examples": [
                "x^3 + 2*x^2 - 5*x + 1",
                "sin(x)*cos(x)",
                "exp(x^2)",
                "log(x^2 + 1)",
            ],
        },
        {
            "name": "Integral",
            "key": "integral",
            "desc": "Indefinite and definite",
            "fields": [
                ("variable", "Variable", {"x": "x", "y": "y", "z": "z", "t": "t"}, "combo", "x"),
                ("lower", "Lower bound (blank=indefinite)", None, "text", ""),
                ("upper", "Upper bound (∞ = oo)", None, "text", ""),
            ],
            "examples": [
                "x^2*sin(x)",
                "1/(x^2 + 1)",
                "exp(-x^2)",
                "sin(x)/x",
            ],
        },
        {
            "name": "Limit",
            "key": "limit",
            "desc": "lim, one-sided, at infinity",
            "fields": [
                ("variable", "Variable", {"x": "x", "y": "y", "z": "z", "t": "t"}, "combo", "x"),
                ("point", "Approach point", None, "text", "0"),
                ("direction", "Direction", {"+-": "both (+-)", "+": "right (+)", "-": "left (-)"}, "combo", "+-"),
            ],
            "examples": [
                "sin(x)/x",
                "(1 + 1/x)^x",
                "(x^2 - 1)/(x - 1)",
                "log(x)/x",
            ],
        },
        {
            "name": "Series Expansion",
            "key": "series",
            "desc": "Taylor / Maclaurin",
            "fields": [
                ("variable", "Variable", {"x": "x", "y": "y", "z": "z", "t": "t"}, "combo", "x"),
                ("point", "Expansion point", None, "text", "0"),
                ("terms", "Number of terms", None, "number", "6"),
            ],
            "examples": [
                "exp(x)",
                "sin(x)",
                "log(1+x)",
                "1/(1-x)",
            ],
        },
        {
            "name": "Tangent Line",
            "key": "tangent_line",
            "desc": "Equation of tangent at a point",
            "fields": [
                ("variable", "Variable", {"x": "x", "y": "y", "z": "z", "t": "t"}, "combo", "x"),
                ("point", "Point (x0)", None, "text", "1"),
            ],
            "examples": [
                "x^2",
                "sin(x)",
                "exp(x)",
            ],
        },
        {
            "name": "Arc Length",
            "key": "arc_length",
            "desc": "Length of y=f(x) on [a, b]",
            "fields": [
                ("variable", "Variable", {"x": "x", "y": "y", "z": "z", "t": "t"}, "combo", "x"),
                ("a", "Lower bound a", None, "text", "0"),
                ("b", "Upper bound b", None, "text", "1"),
            ],
            "examples": [
                "sqrt(1 - x^2)",
                "x^2",
            ],
        },
        {
            "name": "Volume of Revolution",
            "key": "volume_revolution",
            "desc": "Disc / shell method",
            "fields": [
                ("variable", "Variable", {"x": "x", "y": "y"}, "combo", "x"),
                ("a", "Lower bound a", None, "text", "0"),
                ("b", "Upper bound b", None, "text", "1"),
                ("axis", "Axis", {"x": "x-axis", "y": "y-axis"}, "combo", "x"),
            ],
            "examples": [
                "sqrt(1 - x^2)",
                "x^2",
            ],
        },
        {
            "name": "Improper Integral",
            "key": "improper_integral",
            "desc": "Infinite bounds",
            "fields": [
                ("variable", "Variable", {"x": "x", "y": "y"}, "combo", "x"),
                ("lower", "Lower bound (-∞ = -oo)", None, "text", "0"),
                ("upper", "Upper bound (+∞ = oo)", None, "text", "oo"),
            ],
            "examples": [
                "exp(-x)",
                "1/x^2",
            ],
        },
    ],
    "mv": [
        {
            "name": "Partial Derivative",
            "key": "partial_derivative",
            "desc": "∂/∂x, ∂²/∂x∂y",
            "fields": [
                ("variables_list", "Differentiate w.r.t. (comma-sep)", None, "text", "x, y"),
            ],
            "examples": [
                "x^2*y + y^3",
                "exp(x*y)*sin(z)",
            ],
        },
        {
            "name": "Gradient",
            "key": "gradient",
            "desc": "∇f",
            "fields": [
                ("variables_list", "Variables (comma-sep)", None, "text", "x, y"),
            ],
            "examples": [
                "x^2 + y^2",
                "x*y*z",
            ],
        },
        {
            "name": "Hessian Matrix",
            "key": "hessian",
            "desc": "2nd partial derivative matrix",
            "fields": [
                ("variables_list", "Variables (comma-sep)", None, "text", "x, y"),
            ],
            "examples": [
                "x^2*y + x*y^2",
            ],
        },
        {
            "name": "Critical Points",
            "key": "critical_points",
            "desc": "Solve ∇f = 0",
            "fields": [
                ("variables_list", "Variables (comma-sep)", None, "text", "x, y"),
            ],
            "examples": [
                "x^3 - 3*x + y^3 - 3*y",
            ],
        },
        {
            "name": "Laplacian",
            "key": "laplacian",
            "desc": "∇²f",
            "fields": [
                ("variables_list", "Variables (comma-sep)", None, "text", "x, y, z"),
            ],
            "examples": [
                "x^2 + y^2 + z^2",
                "sin(x)*cos(y)",
            ],
        },
    ],
    "vc": [
        {
            "name": "Divergence",
            "key": "divergence",
            "desc": "∇·F",
            "fields": [
                ("component_0", "Component P", None, "text", "x^2"),
                ("component_1", "Component Q", None, "text", "y^2"),
                ("component_2", "Component R", None, "text", "z^2"),
            ],
            "examples": ["x^2, y^2, z^2", "x, y, z"],
            "needs_expr": False,
        },
        {
            "name": "Curl",
            "key": "curl",
            "desc": "∇×F (3D)",
            "fields": [
                ("component_0", "Component P", None, "text", "-y"),
                ("component_1", "Component Q", None, "text", "x"),
                ("component_2", "Component R", None, "text", "0"),
            ],
            "examples": ["-y, x, 0"],
            "needs_expr": False,
        },
        {
            "name": "Multiple Integral",
            "key": "multiple_integral",
            "desc": "Double / triple",
            "fields": [
                ("lim0_var", "Inner var", {"x": "x", "y": "y", "z": "z"}, "combo", "x"),
                ("lim0_low", "Inner lower", None, "text", "0"),
                ("lim0_high", "Inner upper", None, "text", "1"),
                ("lim1_var", "Outer var", {"x": "x", "y": "y", "z": "z"}, "combo", "y"),
                ("lim1_low", "Outer lower", None, "text", "0"),
                ("lim1_high", "Outer upper", None, "text", "1"),
            ],
            "examples": [
                "x*y",
                "x^2 + y^2",
            ],
        },
    ],
    "adv": [
        {
            "name": "Differential Equation (ODE)",
            "key": "ode",
            "desc": "y' = y, y'' + y = 0",
            "fields": [
                ("function", "Dependent variable", {"y": "y", "u": "u", "f": "f"}, "combo", "y"),
            ],
            "examples": [
                "y' = y",
                "y'' + y = 0",
                "y' + 2*y = exp(x)",
            ],
            "needs_expr": False,
        },
        {
            "name": "Residue",
            "key": "residue",
            "desc": "Complex analysis",
            "fields": [
                ("variable", "Variable", {"z": "z", "x": "x"}, "combo", "z"),
                ("point", "Point (z0)", None, "text", "I"),
            ],
            "examples": [
                "1/(z^2 + 1)",
            ],
        },
        {
            "name": "Fourier Series",
            "key": "fourier_series",
            "desc": "a0, an, bn coefficients",
            "fields": [
                ("variable", "Variable", {"x": "x", "t": "t"}, "combo", "x"),
                ("period", "Period", None, "text", "2*pi"),
                ("terms", "Number of terms", None, "number", "5"),
            ],
            "examples": [
                "x",
                "x^2",
            ],
        },
        {
            "name": "Laplace Transform",
            "key": "laplace",
            "desc": "F(s) = L{f(t)}",
            "fields": [
                ("t_var", "Time variable", {"t": "t", "x": "x"}, "combo", "t"),
                ("s_var", "Frequency variable", {"s": "s"}, "combo", "s"),
            ],
            "examples": [
                "t^2",
                "exp(-a*t)*sin(b*t)",
            ],
        },
        {
            "name": "Inverse Laplace",
            "key": "inverse_laplace",
            "desc": "f(t) = L^-1{F(s)}",
            "fields": [
                ("t_var", "Time variable", {"t": "t", "x": "x"}, "combo", "t"),
                ("s_var", "Frequency variable", {"s": "s"}, "combo", "s"),
            ],
            "examples": [
                "1/(s^2 + 1)",
                "s/(s^2 + 4)",
            ],
        },
    ],
}

# ============ COMPUTE THREAD ============

class ComputeThread(QThread):
    """Background thread for long calculus computations."""
    result_ready = Signal(object, object)  # (success:bool, data:str|dict)
    
    def __init__(self, operation_key: str, params: dict):
        super().__init__()
        self.op_key = operation_key
        self.params = params
    
    def run(self):
        try:
            params = self.params
            expr_str = params.get('expression', '').strip()
            op_key = self.op_key
            variables = {}
            
            # Parse expression
            needs_expr = op_key not in ('divergence', 'curl', 'ode')
            if needs_expr:
                if not expr_str:
                    self.result_ready.emit(False, "Please enter an expression.")
                    return
                expr = parse_expression(expr_str)
            else:
                expr = None
            
            var = params.get('variable', 'x')
            var_sym = _get_var_symbol(expr, var)
            
            result = None
            step_text = ""
            
            def _compute_graph_data(expr_to_plot, var_for_graph, op_type, params):
                """Compute graph data for the current operation."""
                data = {'curves': [], 'points': [], 'title': '', 'shade': None}
                # Helper: generate curve data
                def _make_curve(expr, color, label, x_range=None):
                    try:
                        x_vals = np.linspace(x_range[0] if x_range else -10, x_range[1] if x_range else 10, 800)
                        sym = _get_var_symbol(expr, var_for_graph)
                        f = sp.lambdify(sym, expr, modules=['numpy'])
                        y_vals = np.array(f(x_vals), dtype=float)
                        y_vals = np.where(np.abs(y_vals) > 1e6, np.nan, y_vals)
                        if np.any(~np.isnan(y_vals)):
                            data['curves'].append({
                                'x': x_vals.tolist(),
                                'y': y_vals.tolist(),
                                'color': color,
                                'label': label
                            })
                    except Exception:
                        pass
                
                # Generate main function curve
                try:
                    expr_obj = sp.sympify(expr_to_plot) if isinstance(expr_to_plot, str) else expr_to_plot
                except Exception:
                    expr_obj = None
                if expr_obj is not None:
                    _make_curve(expr_obj, '#58a6ff', 'f(x)', x_range=[-20, 20])
                
                # Generate derivative/integral curves if applicable
                if op_type == 'derivative':
                    try:
                        der = sp.diff(expr_obj, var_for_graph)
                        _make_curve(der, '#3fb950', "f'(x)")
                    except Exception:
                        pass
                elif op_type == 'integral':
                    try:
                        ind = sp.integrate(expr_obj, var_for_graph)
                        _make_curve(ind, '#3fb950', '∫f(x) dx')
                    except Exception:
                        pass
                
                # Add critical points, roots, etc.
                if op_type in ['derivative', 'gradient']:
                    try:
                        grad = sp.diff(expr_obj, var_for_graph) if op_type == 'derivative' else gradient(expr_obj, var_for_graph)
                        crit = sp.solve(grad, var_for_graph, dict=True)
                        for sol in crit:
                            for var_val in sol.values():
                                data['points'].append({
                                    'x': float(var_val),
                                    'y': float(expr_obj.subs(var_for_graph, var_val)),
                                    'label': 'critical'
                                })
                    except Exception:
                        pass
                
                # Add limit point
                if op_type == 'limit':
                    try:
                        pt = float(point)
                        data['points'].append({
                            'x': pt,
                            'y': float(result) if result.is_number else None,
                            'label': 'limit'
                        })
                    except Exception:
                        pass
                
                # Add integral shading
                if op_type == 'integral':
                    try:
                        lo = float(lower) if lower else -10
                        hi = float(upper) if upper else 10
                        data['shade'] = {'x_min': lo, 'x_max': hi, 'color': 'rgba(63,185,80,0.3)'}
                    except Exception:
                        pass
                
                # Add tangent/normal points
                if op_type in ['tangent_line', 'normal_line']:
                    try:
                        pt = float(point)
                        y_pt = float(expr_obj.subs(var_for_graph, pt))
                        data['points'].append({'x': pt, 'y': y_pt, 'label': 'point'})
                    except Exception:
                        pass
                
                data['title'] = f"{op_type.capitalize()} of {expr_str}" if expr_str else "Function Graph"
                return data

            # ---- SINGLE VARIABLE ----
            if op_key == "derivative":
                order = int(params.get('order', 1))
                var_sym = _get_var_symbol(expr, var)
                result = derivative(expr, var_sym, order)
                step_text = f"d/d{var} ({expr_str}) = {format_result(result)}"
                graph_data = _compute_graph_data(str(expr), var, 'derivative', params)
                
            elif op_key == "integral":
                var_sym = _get_var_symbol(expr, var)
                lower_str = params.get('lower', '').strip()
                upper_str = params.get('upper', '').strip()
                lower = parse_expression(lower_str) if lower_str else None
                upper = parse_expression(upper_str) if upper_str else None
                result = integral(expr, var_sym, lower, upper)
                var_sym = _get_var_symbol(expr, var)
                lower_str = params.get('lower', '').strip()
                upper_str = params.get('upper', '').strip()
                lower = parse_expression(lower_str) if lower_str else None
                upper = parse_expression(upper_str) if upper_str else None
                result = integral(expr, var_sym, lower, upper)
                if lower is not None:
                    step_text = f"Integral[{lower}]^{[upper]} {expr_str} d{var} = {format_result(result)}"
                else:
                    step_text = f"Integral {expr_str} d{var} = {format_result(result)} + C"
                # Graph: original function with shaded area if definite
                gd = {'curves': [], 'title': f"Integral of {expr_str}"}
                g = _make_graph(expr, var)
                if g:
                    g['color'] = '#58a6ff'
                    gd['curves'].append(g)
                if lower is not None and upper is not None:
                    try:
                        lo = float(lower)
                        hi = float(upper)
                        gd['shade'] = {'x_min': lo, 'x_max': hi, 'color': 'rgba(63,185,80,0.3)'}
                    except Exception:
                        pass
                if gd['curves']:
                    graph_data = gd
                    
            elif op_key == "limit":
                var_sym = _get_var_symbol(expr, var)
                point = parse_expression(params.get('point', '0'))
                direction = params.get('direction', '+-')
                result = limit_expr(expr, var_sym, point, direction)
                dir_str = {'+': '+', '-': '-', '+-': ''}.get(direction, '')
                step_text = f"lim x->[{point}{dir_str}] {expr_str} = {format_result(result)}"
                # Graph: function with point marker
                gd = {'curves': [], 'points': [], 'title': f"Limit at {point}"}
                g = _make_graph(expr, var, x_min=float(point)-5, x_max=float(point)+5)
                if g:
                    g['color'] = '#58a6ff'
                    gd['curves'].append(g)
                try:
                    pt = float(point)
                    gd['points'].append({'x': pt, 'y': float(result) if result.is_number else None, 'label': 'limit'})
                except Exception:
                    pass
                if gd['curves']:
                    graph_data = gd
                    
            elif op_key == "series":
                var_sym = _get_var_symbol(expr, var)
                point = parse_expression(params.get('point', '0'))
                n_terms = int(params.get('terms', 6))
                result = series_expansion(expr, var_sym, point, n_terms)
                step_text = f"Series at x={point}: {format_result(result)}"
                
            elif op_key == "tangent_line":
                var_sym = _get_var_symbol(expr, var)
                point = parse_expression(params.get('point', '0'))
                result = tangent_line(expr, var_sym, point)
                step_text = f"Tangent at x={point}: y = {format_result(result)}"
                
            elif op_key == "arc_length":
                var_sym = _get_var_symbol(expr, var)
                a = parse_expression(params.get('a', '0'))
                b = parse_expression(params.get('b', '1'))
                result = arc_length(expr, var_sym, a, b)
                step_text = f"Arc length [{a}, {b}]: {format_result(result)}"
                
            elif op_key == "volume_revolution":
                var_sym = _get_var_symbol(expr, var)
                a = parse_expression(params.get('a', '0'))
                b = parse_expression(params.get('b', '1'))
                axis = params.get('axis', 'x')
                result = volume_of_revolution(expr, var_sym, a, b, axis)
                step_text = f"Volume (axis={axis}) [{a}, {b}]: {format_result(result)}"
                
            elif op_key == "improper_integral":
                var_sym = _get_var_symbol(expr, var)
                lower = parse_expression(params.get('lower', '0'))
                upper = parse_expression(params.get('upper', 'oo'))
                result = improper_integral(expr, var_sym, lower, upper)
                step_text = f"Improper integral [{lower}, {upper}]: {format_result(result)}"
                
            # ---- MULTIVARIABLE ----
            elif op_key == "partial_derivative":
                vs = [v.strip() for v in params.get('variables_list', 'x, y').split(',')]
                var_symbols = [_get_var_symbol(expr, v) for v in vs]
                result = partial_derivative(expr, *var_symbols)
                step_text = f"Partial d/d{', '.join(vs)}: {format_result(result)}"
                
            elif op_key == "gradient":
                vs = [v.strip() for v in params.get('variables_list', 'x, y').split(',')]
                var_symbols = [_get_var_symbol(expr, v) for v in vs]
                result = gradient(expr, *var_symbols)
                step_text = f"Gradient: {format_result(result)}"
                
            elif op_key == "hessian":
                vs = [v.strip() for v in params.get('variables_list', 'x, y').split(',')]
                var_symbols = [_get_var_symbol(expr, v) for v in vs]
                result = hessian_matrix(expr, *var_symbols)
                step_text = f"Hessian:\n{result}"
                
            elif op_key == "critical_points":
                vs = [v.strip() for v in params.get('variables_list', 'x, y').split(',')]
                var_symbols = [_get_var_symbol(expr, v) for v in vs]
                result = critical_points(expr, *var_symbols)
                step_text = f"Critical points: {format_result(result)}"
                
            elif op_key == "laplacian":
                vs = [v.strip() for v in params.get('variables_list', 'x, y').split(',')]
                var_symbols = [_get_var_symbol(expr, v) for v in vs]
                result = laplacian(expr, *var_symbols)
                step_text = f"Laplacian: {format_result(result)}"
                
            # ---- VECTOR CALCULUS ----
            elif op_key == "divergence":
                comp = [parse_expression(params.get(f'component_{i}', '0')) for i in range(3)]
                vs = [v.strip() for v in params.get('variables_list', 'x, y, z').split(',')]
                var_symbols = [GLOBAL_SYMBOLS[v] for v in vs]
                result = divergence(comp, *var_symbols)
                step_text = f"Divergence: {format_result(result)}"
                
            elif op_key == "curl":
                comp = [parse_expression(params.get(f'component_{i}', '0')) for i in range(3)]
                var_symbols = [GLOBAL_SYMBOLS['x'], GLOBAL_SYMBOLS['y'], GLOBAL_SYMBOLS['z']]
                result = curl(comp, var_symbols)
                step_text = f"Curl: {format_result(result)}"
                
            elif op_key == "multiple_integral":
                limits = []
                for idx in (0, 1):
                    var = params.get(f'lim{idx}_var', 'x')
                    low = parse_expression(params.get(f'lim{idx}_low', '0'))
                    high = parse_expression(params.get(f'lim{idx}_high', '1'))
                    v_sym = _get_var_symbol(expr, var)
                    limits.append((v_sym, low, high))
                result = multiple_integral(expr, *limits)
                step_text = f"Multiple integral: {format_result(result)}"
                
            # ---- ADVANCED ----
            elif op_key == "ode":
                func_name = params.get('function', 'y')
                func = sp.Function(func_name)
                var = params.get('variable', 'x')
                eq = parse_ode_expression(expr_str, func_name, var)
                var_sym = _get_var_symbol(None, var)
                result = solve_ode(eq, func(var_sym))
                step_text = f"ODE solution: {format_result(result)}"
                
            elif op_key == "residue":
                z_var = _get_var_symbol(expr, var)
                point = parse_expression(params.get('point', 'I'))
                result = residue(expr, z_var, point)
                step_text = f"Residue at z0={point}: {format_result(result)}"
                
            elif op_key == "fourier_series":
                var_sym = _get_var_symbol(expr, var)
                period = parse_expression(params.get('period', '2*pi'))
                n_terms = int(params.get('terms', 5))
                result = fourier_series(expr, var_sym, period, n_terms)
                step_text = f"Fourier coefficients: {format_result(result)}"
                
            elif op_key == "laplace":
                t_var = params.get('t_var', 't')
                s_var = params.get('s_var', 's')
                t_sym = _get_var_symbol(expr, t_var)
                s_sym = sp.symbols(s_var)
                result = laplace_transform(expr, t_sym, s_sym)
                step_text = f"Laplace: {format_result(result)}"
                
            elif op_key == "inverse_laplace":
                s_var = params.get('s_var', 's')
                t_var = params.get('t_var', 't')
                s_sym = _get_var_symbol(expr, s_var)
                t_sym = sp.symbols(t_var)
                result = inverse_laplace_transform(expr, s_sym, t_sym)
                step_text = f"Inverse Laplace: {format_result(result)}"
                
            else:
                self.result_ready.emit(False, f"Unknown operation: {op_key}")
                return
            
            self.result_ready.emit(True, {
                'result': format_result(result),
                'latex': latex_result(result),
                'step': step_text,
                'raw': result,
                'graph_data': graph_data,
            })
            
        except Exception as e:
            import traceback
            self.result_ready.emit(False, f"Error: {str(e)}\n\n{traceback.format_exc()}")

# ============ OPERATION PANEL WIDGET ============

class OperationPanel(QWidget):
    """Widget for one operation: builds dynamic fields and examples."""
    
    def __init__(self, op_def: dict, parent=None):
        super().__init__(parent)
        self.op_def = op_def
        self.fields = {}
        self._build()
    
    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Expression or component input
        needs_expr = self.op_def.get('needs_expr', True)
        
        if self.op_def['key'] == 'divergence' or self.op_def['key'] == 'curl':
            label = QLabel("Vector Field Components (comma-separated):")
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
            layout.addWidget(label)
            self.comp_input = QLineEdit()
            self.comp_input.setPlaceholderText("e.g. x^2, y^2, z^2")
            self.comp_input.setFont(QFont("Consolas", 10))
            layout.addWidget(self.comp_input)
        elif needs_expr:
            label = QLabel("f(x) — Expression:")
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
            layout.addWidget(label)
            self.comp_input = QLineEdit()
            self.comp_input.setPlaceholderText("e.g. x^3*sin(2*x) + exp(-x^2)")
            self.comp_input.setFont(QFont("Consolas", 10))
            layout.addWidget(self.comp_input)
        else:
            label = QLabel("ODE Equation:")
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
            layout.addWidget(label)
            self.comp_input = QLineEdit()
            self.comp_input.setPlaceholderText("e.g. y' = y  or  y'' + y = 0")
            self.comp_input.setFont(QFont("Consolas", 10))
            layout.addWidget(self.comp_input)
        
        # Extra fields
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        for field_id, field_label, options, ftype, default in self.op_def['fields']:
            if ftype == "combo" and options:
                combo = QComboBox()
                for k, v in options.items():
                    combo.addItem(v, k)  # store key as item data
                # Find index for default
                for i in range(combo.count()):
                    if combo.itemData(i) == default:
                        combo.setCurrentIndex(i)
                        break
                self.fields[field_id] = combo
            elif ftype == "number":
                spin = QSpinBox()
                spin.setValue(int(default) if default else 1)
                spin.setMinimum(1)
                spin.setMaximum(30)
                self.fields[field_id] = spin
            else:
                le = QLineEdit()
                le.setFont(QFont("Consolas", 10))
                le.setText(str(default) if default else "")
                self.fields[field_id] = le
            form_layout.addRow(f"{field_label}:", self.fields[field_id])
        layout.addWidget(form_widget)
        
        # Examples
        if self.op_def.get('examples'):
            hbox = QHBoxLayout()
            label = QLabel("Examples:")
            label.setStyleSheet("font-weight: bold;")
            hbox.addWidget(label)
            self.ex_label = QLabel(", ".join(self.op_def['examples']))
            self.ex_label.setStyleSheet("color: #58a6ff; font-family: Consolas; font-size: 11px;")
            self.ex_label.setCursor(Qt.PointingHandCursor)
            hbox.addWidget(self.ex_label)
            layout.addLayout(hbox)
        
        layout.addStretch()
    
    def get_params(self) -> dict:
        params = {}
        # Main expression
        if hasattr(self, 'comp_input'):
            params['expression'] = self.comp_input.text().strip()
        for field_id, widget in self.fields.items():
            if isinstance(widget, QComboBox):
                params[field_id] = widget.currentData()
            elif hasattr(widget, 'value'):
                params[field_id] = widget.value()
            else:
                params[field_id] = widget.text().strip()
        return params


# ============ RESULT DISPLAY ============

class ResultWidget(QWidget):
    """Shows the computation result with LaTeX-like rendering and plot."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        self.lbl_title = QLabel("Result")
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #3fb950;")
        layout.addWidget(self.lbl_title)
        
        # Plot widget (shown for function-based ops)
        self.plot_widget = PlotWidget()
        layout.addWidget(self.plot_widget)
        
        # Result text (plain)
        self.txt_result = QLabel()
        self.txt_result.setFont(QFont("Consolas", 12))
        self.txt_result.setStyleSheet("""
            background: #1e2128;
            color: #e6edf3;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #30363d;
        """)
        self.txt_result.setWordWrap(True)
        self.txt_result.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.txt_result)
        
        # Step text
        self.txt_step = QLabel()
        self.txt_step.setFont(QFont("Consolas", 10))
        self.txt_step.setStyleSheet("""
            background: #161b22;
            color: #8b949e;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #21262d;
        """)
        self.txt_step.setWordWrap(True)
        self.txt_step.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.txt_step)
        
        # LaTeX
        self.txt_latex = QLabel()
        self.txt_latex.setFont(QFont("Consolas", 10))
        self.txt_latex.setStyleSheet("""
            background: #161b22;
            color: #6e7681;
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #21262d;
        """)
        self.txt_latex.setWordWrap(True)
        self.txt_latex.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.txt_latex.setVisible(True)
        layout.addWidget(self.txt_latex)
        
        self._has_plot = False
    
    def show_result(self, data: dict, expr_str: str = None, var_name: str = None):
        self.lbl_title.setText("Result")
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #3fb950;")
        self.txt_result.setText(data.get('result', 'No result'))
        self.txt_step.setText(data.get('step', ''))
        latex = data.get('latex', '')
        if latex:
            self.txt_latex.setText(f"LaTeX: {latex}")
            self.txt_latex.setVisible(True)
        
        # Show plot if we have an expression
        if expr_str and var_name:
            self.plot_widget.visible = True
            self.plot_widget.plot_function(expr_str, var_name)
            self._has_plot = True
        else:
            self.plot_widget.setVisible(False)
            self._has_plot = False
    
    def show_error(self, error_msg: str):
        self.lbl_title.setText("Error")
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #f85149;")
        self.txt_result.setText(error_msg[:500])
        self.txt_step.setText("")
        self.txt_latex.setVisible(False)
        self.plot_widget.setVisible(False)
        self._has_plot = False
    
    def clear(self):
        self.lbl_title.setText("Result")
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #8b949e;")
        self.txt_result.setText("Enter an expression and click Solve")
        self.txt_step.setText("")
        self.txt_latex.setVisible(False)
        self.plot_widget.setVisible(False)
        self._has_plot = False


class PlotWidget(QWidget):
    """Matplotlib-based plot widget for visualizing functions."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        
        # Create figure
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.fig.patch.set_facecolor('#0d1117')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet("background: #0d1117;")
        layout.addWidget(self.canvas)
        
        self.ax = self.fig.add_subplot(111)
        self._style_ax()
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        self.btn_plot = QPushButton("📊 Plot Function")
        self.btn_plot.setStyleSheet("""
            background: #21262d; color: #e6edf3; border: 1px solid #30363d;
            border-radius: 4px; padding: 4px 12px;
        """)
        self.btn_plot.clicked.connect(self.plot_function)
        toolbar_layout.addWidget(self.btn_plot)
        
        self.btn_clear = QPushButton("✕ Clear")
        self.btn_clear.setStyleSheet("""
            background: #21262d; color: #e6edf3; border: 1px solid #30363d;
            border-radius: 4px; padding: 4px 12px;
        """)
        self.btn_clear.clicked.connect(self.clear_plot)
        toolbar_layout.addWidget(self.btn_clear)
        
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)
        
        self.current_expr = None
        self.current_var = 'x'
    
    def _style_ax(self):
        """Style the matplotlib axes for dark theme."""
        self.ax.set_facecolor('#0d1117')
        self.ax.tick_params(colors='#e6edf3', labelsize=8)
        for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            label.set_color('#8b949e')
        self.ax.spines['bottom'].set_color('#30363d')
        self.ax.spines['top'].set_color('#30363d')
        self.ax.spines['left'].set_color('#30363d')
        self.ax.spines['right'].set_color('#30363d')
        self.ax.grid(True, color='#21262d', linestyle='-', alpha=0.5)
        self.ax.set_xlabel('x', color='#e6edf3')
        self.ax.set_ylabel('y', color='#e6edf3')
    
    def plot_function(self, expr_str=None, var_name=None, x_min=-10, x_max=10):
        """Plot a function given as string expression."""
        if expr_str is None and self.current_expr is None:
            return
        
        expr_str = expr_str or self.current_expr
        if not expr_str:
            return
        
        try:
            expr = parse_expression(expr_str)
            self.current_expr = expr_str
        except Exception as e:
            return
        
        # Generate x values
        x_vals = np.linspace(x_min, x_max, 1000)
        
        # Vectorize the expression
        try:
            f = sp.lambdify(_get_var_symbol(None, var_name or 'x'), expr, modules='numpy')
            y_vals = f(x_vals)
        except Exception:
            # Try numeric evaluation
            y_vals = []
            for val in x_vals:
                try:
                    y_vals.append(float(expr.subs('x', val)))
                except Exception:
                    y_vals.append(np.nan)
            y_vals = np.array(y_vals)
        
        # Check for complex values
        if np.iscomplexobj(y_vals) or np.any(np.isnan(y_vals)):
            return
        
        # Clear and plot
        self.ax.clear()
        self._style_ax()
        self.ax.plot(x_vals, y_vals, color='#58a6ff', linewidth=1.5, label=expr_str)
        self.ax.legend(loc='upper right', fontsize=8)
        self.ax.set_title(f"y = {expr_str}", color='#e6edf3', fontsize=9)
        
        # Add annotations if needed
        if hasattr(expr, 'free_symbols'):
            sym = list(expr.free_symbols)[0] if expr.free_symbols else None
            if sym:
                self.ax.set_xlabel(str(sym))
        
        self.canvas.draw()
    
    def clear_plot(self):
        """Clear the plot."""
        self.ax.clear()
        self._style_ax()
        self.ax.set_title("Plot", color='#8b949e')
        self.canvas.draw()


# ============ HISTORY TREE ITEM ============

class HistoryItem:
    def __init__(self, op_name: str, expr: str, result: str):
        self.op_name = op_name
        self.expr = expr
        self.result = result


# ============ MAIN WINDOW ============

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculas — University Calculus Solver")
        self.setMinimumSize(1200, 800)
        self.resize(1300, 900)
        
        # Dark theme palette
        self._apply_dark_theme()
        
        self.history = []
        self.compute_thread = None
        self.current_op_key = None
        
        self._build_ui()
    
    def _apply_dark_theme(self):
        """Apply dark theme palette."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#161b22"))
        palette.setColor(QPalette.WindowText, QColor("#e6edf3"))
        palette.setColor(QPalette.Base, QColor("#0d1117"))
        palette.setColor(QPalette.AlternateBase, QColor("#161b22"))
        palette.setColor(QPalette.ToolTipBase, QColor("#161b22"))
        palette.setColor(QPalette.ToolTipText, QColor("#e6edf3"))
        palette.setColor(QPalette.Text, QColor("#e6edf3"))
        palette.setColor(QPalette.Button, QColor("#21262d"))
        palette.setColor(QPalette.ButtonText, QColor("#e6edf3"))
        palette.setColor(QPalette.BrightText, QColor("#58a6ff"))
        palette.setColor(QPalette.Link, QColor("#58a6ff"))
        palette.setColor(QPalette.Highlight, QColor("#1f6feb"))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QMainWindow { background: #0d1117; }
            QTreeWidget {
                background: #161b22;
                color: #e6edf3;
                border: none;
                font-size: 13px;
                outline: none;
            }
            QTreeWidget::item {
                padding: 6px;
                border-radius: 4px;
            }
            QTreeWidget::item:selected {
                background: #1f6feb;
                color: white;
            }
            QTreeWidget::item:hover:!selected {
                background: #21262d;
            }
            QTreeWidget::branch {
                background: transparent;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #8b949e;
                text-transform: uppercase;
                letter-spacing: 1px;
                border: none;
                margin-top: 8px;
                padding-top: 4px;
            }
            QToolButton {
                background: #21262d;
                color: #e6edf3;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
            }
            QToolButton:hover {
                background: #30363d;
                border-color: #58a6ff;
            }
            QToolButton:pressed {
                background: #1f6feb;
            }
            QComboBox, QLineEdit {
                background: #0d1117;
                color: #e6edf3;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 6px 10px;
                font-family: Consolas;
                font-size: 11px;
            }
            QComboBox:hover, QLineEdit:hover {
                border-color: #58a6ff;
            }
            QSpinBox {
                background: #0d1117;
                color: #e6edf3;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 4px 8px;
            }
            QFormLayout {
                spacing: 6px;
            }
            QLabel {
                color: #e6edf3;
            }
        """)
    
    def _build_ui(self):
        """Build the main window UI."""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === SIDEBAR (left) ===
        sidebar = QWidget()
        sidebar.setMaximumWidth(260)
        sidebar.setMinimumWidth(200)
        sidebar.setStyleSheet("background: #161b22; border-right: 1px solid #30363d;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # App title
        title = QLabel()
        title.setText("∂ Calculas")
        title.setStyleSheet("""
            font-size: 24px; font-weight: bold; color: #58a6ff;
            padding: 16px 12px 4px;
        """)
        sidebar_layout.addWidget(title)
        
        subtitle = QLabel("University Calculus Solver")
        subtitle.setStyleSheet("font-size: 11px; color: #8b949e; padding: 0 12px 12px;")
        sidebar_layout.addWidget(subtitle)
        
        # Operation tree
        self.op_tree = QTreeWidget()
        self.op_tree.setHeaderHidden(True)
        self.op_tree.setAnimated(True)
        self.op_tree.setIndentation(12)
        
        for cat_name, cat_key in CATEGORIES:
            cat_item = QTreeWidgetItem(self.op_tree, [cat_name])
            cat_item.setExpanded(True)
            for op in OPERATIONS[cat_key]:
                op_item = QTreeWidgetItem(cat_item, [op['name']])
                op_item.setData(0, Qt.UserRole, op['key'])
        
        self.op_tree.currentItemChanged.connect(self._on_op_selected)
        sidebar_layout.addWidget(self.op_tree)
        
        sidebar_layout.addStretch()
        
        # === MAIN AREA (right) ===
        main_splitter = QSplitter(Qt.Vertical)
        
        # Top: operation panel + solve button
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(16, 12, 16, 12)
        
        # Op header
        self.lbl_op_header = QLabel("Select an operation")
        self.lbl_op_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #e6edf3;")
        top_layout.addWidget(self.lbl_op_header)
        
        self.lbl_op_desc = QLabel("")
        self.lbl_op_desc.setStyleSheet("font-size: 12px; color: #8b949e; margin-bottom: 8px;")
        top_layout.addWidget(self.lbl_op_desc)
        
        # Stacked widget for operation panels
        self.op_stack = QStackedWidget()
        # Add a placeholder
        placeholder = QWidget()
        ph_layout = QVBoxLayout(placeholder)
        ph_layout.addWidget(QLabel("← Select an operation from the sidebar"))
        self.op_stack.addWidget(placeholder)
        
        # Build all operation panels
        self.op_panels = {}
        for cat_key, ops in OPERATIONS.items():
            for op_def in ops:
                panel = OperationPanel(op_def)
                self.op_stack.addWidget(panel)
                self.op_panels[op_def['key']] = panel
        
        top_layout.addWidget(self.op_stack)
        
        # Action buttons
        btn_row = QHBoxLayout()
        self.btn_solve = QToolButton()
        self.btn_solve.setText("▶  Solve")
        self.btn_solve.setCheckable(True)
        self.btn_solve.clicked.connect(self._on_solve)
        btn_row.addWidget(self.btn_solve)
        
        self.btn_clear = QToolButton()
        self.btn_clear.setText("✕  Clear")
        self.btn_clear.clicked.connect(self._on_clear)
        btn_row.addWidget(self.btn_clear)
        
        btn_row.addStretch()
        
        self.btn_examples = QToolButton()
        self.btn_examples.setText("★  Fill Example")
        self.btn_examples.clicked.connect(self._on_fill_example)
        btn_row.addWidget(self.btn_examples)
        
        top_layout.addLayout(btn_row)
        main_splitter.addWidget(top_widget)
        
        # Bottom: result
        self.result_widget = ResultWidget()
        self.result_widget.clear()
        main_splitter.addWidget(self.result_widget)
        
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 1)
        
        # Right panel
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(16, 0, 16, 0)
        right_layout.addWidget(main_splitter)
        
        # Add to main
        main_layout.addWidget(sidebar)
        
        # Vertical separator
        sep = QFrame()
        sep.setFixedWidth(1)
        sep.setStyleSheet("background: #30363d;")
        main_layout.addWidget(sep)
        
        main_layout.addWidget(right_widget)
        
        # Select first operation
        self._select_first_op()
    
    def _select_first_op(self):
        """Select the first operation automatically."""
        first_cat = self.op_tree.topLevelItem(0)
        if first_cat and first_cat.childCount() > 0:
            first_op = first_cat.child(0)
            self.op_tree.setCurrentItem(first_op)
    
    def _on_op_selected(self, current, previous):
        if current is None:
            return
        op_key = current.data(0, Qt.UserRole)
        if op_key is None:
            return  # Category selected, not operation
        
        self.current_op_key = op_key
        panel = self.op_panels.get(op_key)
        if panel is None:
            return
        
        # Find op def
        op_def = None
        for ops in OPERATIONS.values():
            for op in ops:
                if op['key'] == op_key:
                    op_def = op
                    break
            if op_def:
                break
        
        self.lbl_op_header.setText(op_def['name'])
        self.lbl_op_desc.setText(op_def['desc'])
        
        # Find index in stack
        for i in range(self.op_stack.count()):
            w = self.op_stack.widget(i)
            if w is panel:
                self.op_stack.setCurrentIndex(i)
                break
        
        self.result_widget.clear()
    
    def _on_fill_example(self):
        """Fill the current panel with the first example."""
        if self.current_op_key is None:
            return
        op_def = None
        for ops in OPERATIONS.values():
            for op in ops:
                if op['key'] == self.current_op_key:
                    op_def = op
                    break
            if op_def:
                break
        if op_def is None or not op_def.get('examples'):
            return
        
        example = op_def['examples'][0]
        panel = self.op_panels[self.current_op_key]
        
        if hasattr(panel, 'comp_input'):
            if op_def.get('needs_expr', True) is False and self.current_op_key in ('divergence', 'curl'):
                # Split by comma for vector field
                parts = [p.strip() for p in example.split(',')]
                panel.comp_input.setText(example)
            else:
                panel.comp_input.setText(example)
    
    def _on_solve(self):
        """Start computation in background thread."""
        if self.current_op_key is None:
            QMessageBox.information(self, "Calculas", "Select an operation first.")
            return
        
        panel = self.op_panels.get(self.current_op_key)
        if panel is None:
            return
        
        self.params = panel.get_params()
        
        # Handle vector field components for divergence/curl
        if self.current_op_key in ('divergence', 'curl'):
            comp_str = self.params.get('expression', '')
            parts = [p.strip() for p in comp_str.split(',')]
            for i, p in enumerate(parts):
                self.params[f'component_{i}'] = p
            self.params['variables_list'] = 'x, y, z'
        
        # Validate expression
        needs_expr = self.current_op_key not in ('divergence', 'curl', 'ode')
        if needs_expr and not self.params.get('expression', '').strip():
            QMessageBox.warning(self, "Calculas", "Please enter an expression.")
            return
        
        # Disable button
        self.btn_solve.setChecked(False)
        self.btn_solve.setText("⏳  Computing...")
        self.btn_solve.setEnabled(False)
        self.result_widget.lbl_title.setText("Computing...")
        self.result_widget.lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #d29922;")
        self.result_widget.txt_result.setText("Working on it... This may take a moment for complex integrals.")
        
        # Start thread
        self.compute_thread = ComputeThread(self.current_op_key, self.params)
        self.compute_thread.result_ready.connect(self._on_result)
        self.compute_thread.start()
    
    def _on_result(self, success: bool, data):
        """Handle result from compute thread."""
        self.btn_solve.setText("▶  Solve")
        self.btn_solve.setEnabled(True)
        
        if success and isinstance(data, dict):
            # Get expression and variable for plotting
            expr_str = self.params.get('expression', '') if hasattr(self, 'params') else ''
            var_name = self.params.get('variable', 'x') if hasattr(self, 'params') else 'x'
            
            self.result_widget.show_result(data, expr_str, var_name)
            
            # Add to history
            op_name = ""
            for ops in OPERATIONS.values():
                for op in ops:
                    if op['key'] == self.current_op_key:
                        op_name = op['name']
                        break
            expr = data.get('step', '').split('=')[0].strip() if '=' in str(data.get('step', '')) else ""
            result = data.get('result', '')[:100]
            self.history.append(HistoryItem(op_name, expr, result))
            
        elif success and isinstance(data, str):
            self.result_widget.show_error(data)
        else:
            self.result_widget.show_error(str(data) if data else "Unknown error")
    
    def _on_clear(self):
        """Clear expression and result."""
        if self.current_op_key and self.current_op_key in self.op_panels:
            panel = self.op_panels[self.current_op_key]
            if hasattr(panel, 'comp_input'):
                panel.comp_input.clear()
        self.result_widget.clear()


# ============ ENTRY POINT ============

def main():
    # High DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Consistent across platforms
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()