"""
University-level Calculus Calculator Backend
Powered by SymPy for symbolic mathematics
"""
from flask import Flask, request, jsonify, send_from_directory
import sympy as sp
import numpy as np
import json
import traceback

app = Flask(__name__, static_folder='static')

# Define common symbols
x, y, z, t = sp.symbols('x y z t', real=True)
n, m, k = sp.symbols('n m k', integer=True, positive=True)
a, b, c = sp.symbols('a b c', real=True)

def parse_expression(expr_str, variables=None):
    """Parse a mathematical expression string into a SymPy expression."""
    if variables is None:
        variables = {}
    
    # Common replacements for user-friendly input
    replacements = {
        '^': '**',
        'e': 'E',
        'pi': 'pi',
        'inf': 'oo',
        'infty': 'oo',
        'infinty': 'oo',
        'ln': 'log',
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'cot': 'cot',
        'sec': 'sec',
        'csc': 'csc',
        'asin': 'asin',
        'acos': 'acos',
        'atan': 'atan',
        'sinh': 'sinh',
        'cosh': 'cosh',
        'tanh': 'tanh',
        'exp': 'exp',
        'sqrt': 'sqrt',
        'abs': 'Abs',
        'factorial': 'factorial',
        'gamma': 'gamma',
    }
    
    # Apply replacements carefully
    expr_str = expr_str.strip()
    
    # Parse with sympy
    local_dict = {
        'x': x, 'y': y, 'z': z, 't': t,
        'n': n, 'm': m, 'k': k,
        'a': a, 'b': b, 'c': c,
        'E': sp.E, 'pi': sp.pi, 'oo': sp.oo,
        'I': sp.I,
    }
    local_dict.update(variables)
    
    try:
        expr = sp.sympify(expr_str, locals=local_dict)
        return expr
    except Exception as e:
        # Try with replacements
        for old, new in replacements.items():
            expr_str = expr_str.replace(old, new)
        try:
            expr = sp.sympify(expr_str, locals=local_dict)
            return expr
        except Exception as e2:
            raise ValueError(f"Could not parse expression: {expr_str}. Error: {e2}")

def format_result(expr):
    """Format a SymPy expression for display."""
    if expr is None:
        return "undefined"
    try:
        # Try to simplify
        simplified = sp.simplify(expr)
        return str(simplified)
    except:
        return str(expr)

def latex_result(expr):
    """Get LaTeX representation of expression."""
    if expr is None:
        return "undefined"
    try:
        return sp.latex(expr)
    except:
        return str(expr)

# ============ CALCULUS OPERATIONS ============

def derivative(expr, var, order=1):
    """Compute derivative."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.diff(expr, var_sym, order)

def partial_derivative(expr, *vars):
    """Compute partial derivative."""
    return sp.diff(expr, *vars)

def integral(expr, var, lower=None, upper=None):
    """Compute integral (definite or indefinite)."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    if lower is not None and upper is not None:
        return sp.integrate(expr, (var_sym, lower, upper))
    return sp.integrate(expr, var_sym)

def multiple_integral(expr, *limits):
    """Compute multiple integral. limits = [(var, lower, upper), ...]"""
    return sp.integrate(expr, *limits)

def limit_expr(expr, var, point, dir='+-'):
    """Compute limit."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.limit(expr, var_sym, point, dir=dir)

def series_expansion(expr, var, point=0, n=6):
    """Compute series expansion."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.series(expr, var_sym, point, n).removeO()

def taylor_series(expr, var, point=0, n=6):
    """Compute Taylor series."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.series(expr, var_sym, point, n).removeO()

def solve_ode(eq, func, ics=None):
    """Solve ordinary differential equation."""
    try:
        if ics:
            return sp.dsolve(eq, func, ics=ics)
        return sp.dsolve(eq, func)
    except Exception as e:
        return f"Could not solve ODE: {str(e)}"


def parse_ode_expression(eq_str, func_name, var_name, variables=None):
    """
    Parse a user-friendly ODE expression.
    Supports formats like:
      - "y' = y" or "y'' + y = 0" or "y' + 2*y = exp(x)"
      - "Eq(Derivative(y(x), x), y(x))" (SymPy native)
      - "D(y(x), x) = x*y(x)" (shorthand)
    """
    if variables is None:
        variables = {}
    
    # Use global symbols to ensure compatibility with dsolve
    # Map var_name to the global symbol
    global_symbols = {'x': x, 'y': y, 'z': z, 't': t}
    var_sym = global_symbols.get(var_name, sp.symbols(var_name))
    func = sp.Function(func_name)
    
    # Try native SymPy format first
    local_dict = {
        'x': x, 'y': y, 'z': z, 't': t,
        'Eq': sp.Eq, 'Derivative': sp.Derivative, 'D': sp.Derivative,
        func_name: func,
        'u': sp.Function('u'), 'f': sp.Function('f'),
    }
    local_dict.update(variables)
    
    try:
        eq = sp.sympify(eq_str, locals=local_dict)
        if isinstance(eq, sp.Eq):
            return eq
    except:
        pass
    
    # Try user-friendly format: "y' = f(x, y)" or "y'' + y = 0"
    eq_str = eq_str.strip()
    
    # Replace prime notation with Derivative
    # y' -> D(y(x), x)
    # y'' -> D(y(x), x, 2)
    # y''' -> D(y(x), x, 3)
    # y'''' -> D(y(x), x, 4)
    
    # Handle up to 4 primes
    for n in range(4, 0, -1):
        primes = "'" * n
        pattern = f"{func_name}{primes}"
        replacement = f"Derivative({func_name}({var_name}), {var_name}, {n})"
        eq_str = eq_str.replace(pattern, replacement)
    
    # Handle y(x) notation - replace standalone func_name with func_name(var_name)
    import re
    # Replace "y" at word boundaries with "y(x)" when it looks like a function call
    # But don't replace if already followed by (
    eq_str = re.sub(rf'\b{func_name}\b(?!\s*\()', f'{func_name}({var_name})', eq_str)
    
    # Parse as equation
    local_dict = {
        'x': x, 'y': y, 'z': z, 't': t,
        'Eq': sp.Eq, 'Derivative': sp.Derivative, 'D': sp.Derivative,
        func_name: func,
        'u': sp.Function('u'), 'f': sp.Function('f'),
    }
    local_dict.update(variables)
    
    try:
        eq = sp.sympify(eq_str, locals=local_dict)
        if isinstance(eq, sp.Eq):
            return eq
    except:
        pass
    
    # Last resort: try to split on = and create Eq
    if '=' in eq_str:
        left, right = eq_str.split('=', 1)
        try:
            left_expr = sp.sympify(left.strip(), locals=local_dict)
            right_expr = sp.sympify(right.strip(), locals=local_dict)
            return sp.Eq(left_expr, right_expr)
        except Exception as e:
            raise ValueError(f"Could not parse ODE: {eq_str}. Error: {str(e)}")
    
    raise ValueError(f"Could not parse ODE: {eq_str}")

def solve_pde(eq, func):
    """Solve partial differential equation (limited support)."""
    try:
        return sp.pdsolve(eq, func)
    except Exception as e:
        return f"Could not solve PDE: {str(e)}"

def gradient(expr, *vars):
    """Compute gradient."""
    return [sp.diff(expr, v) for v in vars]

def divergence(vector_field, *vars):
    """Compute divergence of vector field."""
    if len(vector_field) != len(vars):
        raise ValueError("Vector field dimension must match variables")
    return sum(sp.diff(vector_field[i], vars[i]) for i in range(len(vars)))

def curl(vector_field, vars):
    """Compute curl in 3D."""
    if len(vector_field) != 3 or len(vars) != 3:
        raise ValueError("Curl requires 3D vector field and 3 variables")
    x, y, z = vars
    P, Q, R = vector_field
    return [
        sp.diff(R, y) - sp.diff(Q, z),
        sp.diff(P, z) - sp.diff(R, x),
        sp.diff(Q, x) - sp.diff(P, y)
    ]

def laplacian(expr, *vars):
    """Compute Laplacian."""
    return sum(sp.diff(expr, v, 2) for v in vars)

def critical_points(expr, *vars):
    """Find critical points."""
    grad = gradient(expr, *vars)
    sols = sp.solve(grad, vars, dict=True)
    return sols

def hessian_matrix(expr, *vars):
    """Compute Hessian matrix."""
    n = len(vars)
    H = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            H[i, j] = sp.diff(expr, vars[i], vars[j])
    return H

def tangent_line(expr, var, point):
    """Find tangent line at a point."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    f_prime = sp.diff(expr, var_sym)
    slope = f_prime.subs(var_sym, point)
    y0 = expr.subs(var_sym, point)
    tangent = slope * (var_sym - point) + y0
    return sp.simplify(tangent)

def normal_line(expr, var, point):
    """Find normal line at a point."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    f_prime = sp.diff(expr, var_sym)
    slope = f_prime.subs(var_sym, point)
    if slope == 0:
        return f"x = {point}"
    normal_slope = -1/slope
    y0 = expr.subs(var_sym, point)
    normal = normal_slope * (var_sym - point) + y0
    return sp.simplify(normal)

def arc_length(expr, var, a, b):
    """Compute arc length."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    deriv = sp.diff(expr, var_sym)
    integrand = sp.sqrt(1 + deriv**2)
    return sp.integrate(integrand, (var_sym, a, b))

def surface_area(expr, var, a, b, axis='x'):
    """Compute surface area of revolution."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    deriv = sp.diff(expr, var_sym)
    if axis == 'x':
        integrand = 2 * sp.pi * expr * sp.sqrt(1 + deriv**2)
    else:
        integrand = 2 * sp.pi * var_sym * sp.sqrt(1 + deriv**2)
    return sp.integrate(integrand, (var_sym, a, b))

def volume_of_revolution(expr, var, a, b, axis='x'):
    """Compute volume of revolution."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    if axis == 'x':
        integrand = sp.pi * expr**2
    else:
        integrand = 2 * sp.pi * var_sym * expr
    return sp.integrate(integrand, (var_sym, a, b))

def improper_integral(expr, var, lower, upper):
    """Compute improper integral."""
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.integrate(expr, (var_sym, lower, upper))

def _to_symbol(var):
    """Convert string or symbol to sympy symbol."""
    if isinstance(var, str):
        return sp.symbols(var)
    return var

# Global symbol table - must match what parse_expression uses
GLOBAL_SYMBOLS = {'x': x, 'y': y, 'z': z, 't': t, 'n': n, 'm': m, 'k': k, 'a': a, 'b': b, 'c': c}

def _get_var_symbol(expr, var_name):
    """
    Get the correct symbol from the expression's free symbols.
    This ensures we use the same symbol object that was used during parsing.
    Falls back to the global symbol table (same symbols parse_expression uses).
    """
    if not isinstance(var_name, str):
        return var_name
    # Look for a matching symbol in the expression's free symbols
    if expr is not None:
        for sym in expr.free_symbols:
            if str(sym) == var_name:
                return sym
    # Fallback: use the module-level symbol (same instance parse_expression uses)
    return GLOBAL_SYMBOLS.get(var_name, sp.symbols(var_name))

def residue(expr, var, point):
    """Compute residue at a point."""
    var_sym = _to_symbol(var)
    return sp.residue(expr, var_sym, point)

def fourier_series(expr, var, period=2*sp.pi, n_terms=5):
    """Compute Fourier series coefficients."""
    var_sym = _to_symbol(var)
    L = period / 2
    
    a0 = (1/L) * sp.integrate(expr, (var_sym, -L, L))
    an = lambda n: (1/L) * sp.integrate(expr * sp.cos(n * sp.pi * var_sym / L), (var_sym, -L, L))
    bn = lambda n: (1/L) * sp.integrate(expr * sp.sin(n * sp.pi * var_sym / L), (var_sym, -L, L))
    
    coeffs = {'a0': a0}
    for i in range(1, n_terms + 1):
        coeffs[f'a{i}'] = an(i)
        coeffs[f'b{i}'] = bn(i)
    return coeffs

def laplace_transform(expr, t, s):
    """Compute Laplace transform."""
    t_sym = _to_symbol(t)
    s_sym = _to_symbol(s)
    return sp.laplace_transform(expr, t_sym, s_sym, noconds=True)

def inverse_laplace_transform(expr, s, t):
    """Compute inverse Laplace transform."""
    s_sym = _to_symbol(s)
    t_sym = _to_symbol(t)
    return sp.inverse_laplace_transform(expr, s_sym, t_sym)

# ============ API ROUTES ============

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    operation = data.get('operation')
    params = data.get('params', {})
    
    try:
        # Parse expression
        expr_str = params.get('expression', '')
        variables = params.get('variables', {})
        # Some operations (divergence, curl) don't need an expression
        needs_expr = operation not in ('divergence', 'curl', 'ode')
        if needs_expr and not expr_str.strip():
            return jsonify({'success': False, 'error': 'Expression is required for this operation'}), 400
        
        expr = None
        if needs_expr:
            expr = parse_expression(expr_str, variables)
        
        var = params.get('variable', 'x')
        var_sym = _get_var_symbol(expr, var)
        
        result = None
        steps = []
        
        if operation == 'derivative':
            order = params.get('order', 1)
            result = derivative(expr, var_sym, order)
            steps.append(f"d/d{var} ({expr_str}) = {format_result(result)}")
            
        elif operation == 'partial_derivative':
            vars_list = params.get('variables_list', [var])
            var_symbols = [_get_var_symbol(expr, v) if isinstance(v, str) else v for v in vars_list]
            result = partial_derivative(expr, *var_symbols)
            steps.append(f"∂/∂{''.join(vars_list)} ({expr_str}) = {format_result(result)}")
            
        elif operation == 'integral':
            lower = params.get('lower')
            upper = params.get('upper')
            if lower is not None:
                lower = parse_expression(str(lower), variables)
            if upper is not None:
                upper = parse_expression(str(upper), variables)
            result = integral(expr, var_sym, lower, upper)
            if lower is not None:
                steps.append(f"∫[{lower}]^[{upper}] ({expr_str}) d{var} = {format_result(result)}")
            else:
                steps.append(f"∫ ({expr_str}) d{var} = {format_result(result)} + C")
                
        elif operation == 'multiple_integral':
            limits = params.get('limits', [])
            parsed_limits = []
            for lim in limits:
                v = _get_var_symbol(expr, lim['variable']) if isinstance(lim['variable'], str) else lim['variable']
                low = parse_expression(str(lim['lower']), variables) if lim.get('lower') is not None else None
                up = parse_expression(str(lim['upper']), variables) if lim.get('upper') is not None else None
                if low is not None and up is not None:
                    parsed_limits.append((v, low, up))
                elif low is not None:
                    parsed_limits.append((v, low))
                else:
                    parsed_limits.append(v)
            result = multiple_integral(expr, *parsed_limits)
            steps.append(f"Multiple integral = {format_result(result)}")
            
        elif operation == 'limit':
            point = params.get('point', 0)
            point = parse_expression(str(point), variables)
            direction = params.get('direction', '+-')
            result = limit_expr(expr, var_sym, point, direction)
            dir_str = {'+': '+', '-': '-', '+-': ''}.get(direction, '')
            steps.append(f"lim_{{x→{point}{dir_str}}} ({expr_str}) = {format_result(result)}")
            
        elif operation == 'series':
            point = params.get('point', 0)
            n_terms = params.get('terms', 6)
            point = parse_expression(str(point), variables)
            result = series_expansion(expr, var_sym, point, n_terms)
            steps.append(f"Series of ({expr_str}) at {var}={point}: {format_result(result)}")
            
        elif operation == 'taylor':
            point = params.get('point', 0)
            n_terms = params.get('terms', 6)
            point = parse_expression(str(point), variables)
            result = taylor_series(expr, var_sym, point, n_terms)
            steps.append(f"Taylor series of ({expr_str}) at {var}={point}: {format_result(result)}")
            
        elif operation == 'ode':
            # Parse ODE expression
            func_str = params.get('function', 'y')
            func = sp.Function(func_str)
            try:
                eq = parse_ode_expression(str(expr_str), func_str, var, variables)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
            ics = params.get('initial_conditions')
            if ics:
                ics_parsed = {}
                for k, v in ics.items():
                    ics_parsed[sp.symbols(k)] = parse_expression(str(v), variables)
                ics = ics_parsed
            result = solve_ode(eq, func(var_sym), ics)
            steps.append(f"ODE solution: {format_result(result)}")

        elif operation == 'gradient':
            vars_list = params.get('variables_list', ['x', 'y'])
            var_symbols = [_get_var_symbol(expr, v) if isinstance(v, str) else v for v in vars_list]
            result = gradient(expr, *var_symbols)
            steps.append(f"∇({expr_str}) = {format_result(result)}")

        elif operation == 'divergence':
            vector_field = params.get('vector_field', [])
            vars_list = params.get('variables_list', ['x', 'y', 'z'])
            var_symbols = [_get_var_symbol(expr, v) if isinstance(v, str) else v for v in vars_list]
            vec_parsed = [parse_expression(v, variables) for v in vector_field]
            result = divergence(vec_parsed, *var_symbols)
            steps.append(f"∇·F = {format_result(result)}")

        elif operation == 'curl':
            vector_field = params.get('vector_field', [])
            vars_list = params.get('variables_list', ['x', 'y', 'z'])
            var_symbols = [_get_var_symbol(expr, v) if isinstance(v, str) else v for v in vars_list]
            vec_parsed = [parse_expression(v, variables) for v in vector_field]
            result = curl(vec_parsed, var_symbols)
            steps.append(f"∇×F = {format_result(result)}")

        elif operation == 'laplacian':
            vars_list = params.get('variables_list', ['x', 'y'])
            var_symbols = [_get_var_symbol(expr, v) if isinstance(v, str) else v for v in vars_list]
            result = laplacian(expr, *var_symbols)
            steps.append(f"∇²({expr_str}) = {format_result(result)}")

        elif operation == 'critical_points':
            vars_list = params.get('variables_list', ['x', 'y'])
            var_symbols = [_get_var_symbol(expr, v) if isinstance(v, str) else v for v in vars_list]
            result = critical_points(expr, *var_symbols)
            steps.append(f"Critical points: {format_result(result)}")

        elif operation == 'hessian':
            vars_list = params.get('variables_list', ['x', 'y'])
            var_symbols = [_get_var_symbol(expr, v) if isinstance(v, str) else v for v in vars_list]
            result = hessian_matrix(expr, *var_symbols)
            steps.append(f"Hessian matrix:\n{format_result(result)}")
            
        elif operation == 'tangent_line':
            point = params.get('point', 0)
            point = parse_expression(str(point), variables)
            result = tangent_line(expr, var_sym, point)
            steps.append(f"Tangent line at {var}={point}: y = {format_result(result)}")
            
        elif operation == 'normal_line':
            point = params.get('point', 0)
            point = parse_expression(str(point), variables)
            result = normal_line(expr, var_sym, point)
            steps.append(f"Normal line at {var}={point}: {format_result(result)}")
            
        elif operation == 'arc_length':
            a = parse_expression(str(params.get('a', 0)), variables)
            b = parse_expression(str(params.get('b', 1)), variables)
            result = arc_length(expr, var_sym, a, b)
            steps.append(f"Arc length from {a} to {b}: {format_result(result)}")
            
        elif operation == 'surface_area':
            a = parse_expression(str(params.get('a', 0)), variables)
            b = parse_expression(str(params.get('b', 1)), variables)
            axis = params.get('axis', 'x')
            result = surface_area(expr, var_sym, a, b, axis)
            steps.append(f"Surface area (axis={axis}) from {a} to {b}: {format_result(result)}")
            
        elif operation == 'volume_revolution':
            a = parse_expression(str(params.get('a', 0)), variables)
            b = parse_expression(str(params.get('b', 1)), variables)
            axis = params.get('axis', 'x')
            result = volume_of_revolution(expr, var_sym, a, b, axis)
            steps.append(f"Volume (axis={axis}) from {a} to {b}: {format_result(result)}")
            
        elif operation == 'improper_integral':
            lower = params.get('lower')
            upper = params.get('upper')
            lower = parse_expression(str(lower), variables) if lower is not None else -sp.oo
            upper = parse_expression(str(upper), variables) if upper is not None else sp.oo
            result = improper_integral(expr, var_sym, lower, upper)
            steps.append(f"Improper integral = {format_result(result)}")
            
        elif operation == 'residue':
            point = params.get('point', 0)
            point = parse_expression(str(point), variables)
            # Get the correct variable symbol from the expression
            z_var = _get_var_symbol(expr, var)
            result = residue(expr, z_var, point)
            steps.append(f"Residue at {var}={point}: {format_result(result)}")
            
        elif operation == 'fourier_series':
            period = params.get('period', 2*sp.pi)
            n_terms = params.get('terms', 5)
            if isinstance(period, str):
                period = parse_expression(period, variables)
            if isinstance(n_terms, str):
                n_terms = int(n_terms)
            result = fourier_series(expr, var_sym, period, n_terms)
            steps.append(f"Fourier series coefficients: {format_result(result)}")
            
        elif operation == 'laplace':
            t_var = params.get('t_var', 't')
            s_var = params.get('s_var', 's')
            # Get the correct variable symbol from the expression
            t_sym = _get_var_symbol(expr, t_var)
            s_sym = sp.symbols(s_var) if isinstance(s_var, str) else s_var
            result = laplace_transform(expr, t_sym, s_sym)
            steps.append(f"Laplace transform: {format_result(result)}")
            
        elif operation == 'inverse_laplace':
            s_var = params.get('s_var', 's')
            t_var = params.get('t_var', 't')
            s_sym = _get_var_symbol(expr, s_var)
            t_sym = sp.symbols(t_var) if isinstance(t_var, str) else t_var
            result = inverse_laplace_transform(expr, s_sym, t_sym)
            steps.append(f"Inverse Laplace transform: {format_result(result)}")
            
        else:
            return jsonify({'error': f'Unknown operation: {operation}'}), 400
        
        return jsonify({
            'success': True,
            'result': format_result(result),
            'latex': latex_result(result),
            'steps': steps,
            'operation': operation
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/examples')
def get_examples():
    """Return example problems for each operation."""
    examples = {
        'derivative': [
            {'expression': 'x**3 + 2*x**2 - 5*x + 1', 'variable': 'x', 'order': 1, 'description': 'Basic polynomial derivative'},
            {'expression': 'sin(x)*cos(x)', 'variable': 'x', 'order': 1, 'description': 'Trigonometric derivative'},
            {'expression': 'exp(x**2)', 'variable': 'x', 'order': 2, 'description': 'Second derivative of e^(x^2)'},
            {'expression': 'log(x**2 + 1)', 'variable': 'x', 'order': 1, 'description': 'Logarithmic derivative'},
        ],
        'partial_derivative': [
            {'expression': 'x**2*y + y**3', 'variables_list': ['x', 'y'], 'description': 'Mixed partial derivative'},
            {'expression': 'exp(x*y)*sin(z)', 'variables_list': ['x', 'y', 'z'], 'description': 'Three-variable partial'},
        ],
        'integral': [
            {'expression': 'x**2*sin(x)', 'variable': 'x', 'description': 'Indefinite integral'},
            {'expression': '1/(x**2 + 1)', 'variable': 'x', 'lower': 0, 'upper': 'oo', 'description': 'Definite integral to infinity'},
            {'expression': 'exp(-x**2)', 'variable': 'x', 'lower': '-oo', 'upper': 'oo', 'description': 'Gaussian integral'},
            {'expression': 'sin(x)/x', 'variable': 'x', 'lower': 0, 'upper': 'oo', 'description': 'Sinc integral'},
        ],
        'multiple_integral': [
            {'expression': 'x*y', 'limits': [{'variable': 'x', 'lower': 0, 'upper': 1}, {'variable': 'y', 'lower': 0, 'upper': 2}], 'description': 'Double integral over rectangle'},
            {'expression': 'x**2 + y**2', 'limits': [{'variable': 'x', 'lower': -1, 'upper': 1}, {'variable': 'y', 'lower': -1, 'upper': 1}], 'description': 'Double integral over square'},
        ],
        'limit': [
            {'expression': 'sin(x)/x', 'variable': 'x', 'point': 0, 'description': 'Classic limit sin(x)/x'},
            {'expression': '(1 + 1/x)**x', 'variable': 'x', 'point': 'oo', 'description': 'Limit definition of e'},
            {'expression': 'log(x)/x', 'variable': 'x', 'point': 'oo', 'description': 'Logarithmic growth'},
            {'expression': '(x**2 - 1)/(x - 1)', 'variable': 'x', 'point': 1, 'description': 'Removable discontinuity'},
        ],
        'series': [
            {'expression': 'exp(x)', 'variable': 'x', 'point': 0, 'terms': 6, 'description': 'Maclaurin series of e^x'},
            {'expression': 'sin(x)', 'variable': 'x', 'point': 0, 'terms': 7, 'description': 'Maclaurin series of sin(x)'},
            {'expression': 'log(1+x)', 'variable': 'x', 'point': 0, 'terms': 6, 'description': 'Maclaurin series of ln(1+x)'},
            {'expression': '1/(1-x)', 'variable': 'x', 'point': 0, 'terms': 6, 'description': 'Geometric series'},
        ],
        'ode': [
            {'expression': 'Eq(Derivative(y(x), x), y(x))', 'function': 'y', 'description': 'y\' = y'},
            {'expression': 'Eq(Derivative(y(x), x, 2) + y(x), 0)', 'function': 'y', 'description': 'y\'\' + y = 0 (harmonic oscillator)'},
            {'expression': 'Eq(Derivative(y(x), x) + 2*y(x), exp(x))', 'function': 'y', 'description': 'First order linear ODE'},
        ],
        'gradient': [
            {'expression': 'x**2 + y**2', 'variables_list': ['x', 'y'], 'description': 'Gradient of paraboloid'},
            {'expression': 'x*y*z', 'variables_list': ['x', 'y', 'z'], 'description': '3D gradient'},
        ],
        'divergence': [
            {'vector_field': ['x**2', 'y**2', 'z**2'], 'variables_list': ['x', 'y', 'z'], 'description': 'Divergence of (x², y², z²)'},
        ],
        'curl': [
            {'vector_field': ['-y', 'x', '0'], 'variables_list': ['x', 'y', 'z'], 'description': 'Curl of 2D rotation field'},
        ],
        'laplacian': [
            {'expression': 'x**2 + y**2 + z**2', 'variables_list': ['x', 'y', 'z'], 'description': 'Laplacian of r²'},
            {'expression': 'sin(x)*cos(y)', 'variables_list': ['x', 'y'], 'description': '2D Laplacian'},
        ],
        'critical_points': [
            {'expression': 'x**3 - 3*x + y**3 - 3*y', 'variables_list': ['x', 'y'], 'description': 'Critical points of cubic function'},
        ],
        'tangent_line': [
            {'expression': 'x**2', 'variable': 'x', 'point': 2, 'description': 'Tangent to parabola at x=2'},
        ],
        'arc_length': [
            {'expression': 'sqrt(1 - x**2)', 'variable': 'x', 'a': -1, 'b': 1, 'description': 'Arc length of semicircle'},
        ],
        'surface_area': [
            {'expression': 'sqrt(1 - x**2)', 'variable': 'x', 'a': -1, 'b': 1, 'axis': 'x', 'description': 'Surface area of sphere'},
        ],
        'volume_revolution': [
            {'expression': 'sqrt(1 - x**2)', 'variable': 'x', 'a': -1, 'b': 1, 'axis': 'x', 'description': 'Volume of sphere'},
        ],
        'improper_integral': [
            {'expression': 'exp(-x)', 'variable': 'x', 'lower': 0, 'upper': 'oo', 'description': 'Exponential decay integral'},
            {'expression': '1/x**2', 'variable': 'x', 'lower': 1, 'upper': 'oo', 'description': 'p-integral with p=2'},
        ],
        'residue': [
            {'expression': '1/(z**2 + 1)', 'variable': 'z', 'point': 'I', 'description': 'Residue at z=i'},
        ],
        'fourier_series': [
            {'expression': 'x', 'variable': 'x', 'period': '2*pi', 'terms': 5, 'description': 'Fourier series of f(x)=x'},
            {'expression': 'x**2', 'variable': 'x', 'period': '2*pi', 'terms': 5, 'description': 'Fourier series of f(x)=x²'},
        ],
        'laplace': [
            {'expression': 'exp(-a*t)*sin(b*t)', 't_var': 't', 's_var': 's', 'description': 'Laplace of damped sine'},
            {'expression': 't**2', 't_var': 't', 's_var': 's', 'description': 'Laplace of t²'},
        ],
        'inverse_laplace': [
            {'expression': '1/(s**2 + 1)', 's_var': 's', 't_var': 't', 'description': 'Inverse Laplace of 1/(s²+1)'},
            {'expression': 's/(s**2 + 4)', 's_var': 's', 't_var': 't', 'description': 'Inverse Laplace of s/(s²+4)'},
        ],
    }
    return jsonify(examples)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)