"""
Core calculus operations using SymPy - extracted from web backend
for use in native desktop app
"""
import sympy as sp
import re

# Define global symbols (must be module-level for identity consistency)
x, y, z, t = sp.symbols('x y z t', real=True)
n, m, k = sp.symbols('n m k', integer=True, positive=True)
a, b, c = sp.symbols('a b c', real=True)

GLOBAL_SYMBOLS = {'x': x, 'y': y, 'z': z, 't': t, 'n': n, 'm': m, 'k': k, 'a': a, 'b': b, 'c': c}

# ============ PARSING ============

def parse_expression(expr_str, variables=None):
    """Parse a mathematical expression string into a SymPy expression."""
    if variables is None:
        variables = {}
    
    replacements = {
        '^': '**',
        'e': 'E',
        'pi': 'pi',
        'inf': 'oo',
        'infty': 'oo',
        'infinty': 'oo',
        'ln': 'log',
    }
    
    expr_str = expr_str.strip()
    
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
        for old, new in replacements.items():
            expr_str = expr_str.replace(old, new)
        try:
            expr = sp.sympify(expr_str, locals=local_dict)
            return expr
        except Exception as e2:
            raise ValueError(f"Could not parse expression: {expr_str}. Error: {e2}")

def _get_var_symbol(expr, var_name):
    """Get the correct symbol from the expression's free symbols."""
    if not isinstance(var_name, str):
        return var_name
    if expr is not None:
        for sym in expr.free_symbols:
            if str(sym) == var_name:
                return sym
    return GLOBAL_SYMBOLS.get(var_name, sp.symbols(var_name))

# ============ CALCULUS OPERATIONS ============

def derivative(expr, var, order=1):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.diff(expr, var_sym, order)

def partial_derivative(expr, *vars):
    return sp.diff(expr, *vars)

def integral(expr, var, lower=None, upper=None):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    if lower is not None and upper is not None:
        return sp.integrate(expr, (var_sym, lower, upper))
    return sp.integrate(expr, var_sym)

def multiple_integral(expr, *limits):
    return sp.integrate(expr, *limits)

def limit_expr(expr, var, point, dir='+-'):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.limit(expr, var_sym, point, dir=dir)

def series_expansion(expr, var, point=0, n=6):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.series(expr, var_sym, point, n).removeO()

def solve_ode(eq, func, ics=None):
    try:
        if ics:
            return sp.dsolve(eq, func, ics=ics)
        return sp.dsolve(eq, func)
    except Exception as e:
        return f"Could not solve ODE: {str(e)}"

def gradient(expr, *vars):
    return [sp.diff(expr, v) for v in vars]

def divergence(vector_field, *vars):
    if len(vector_field) != len(vars):
        raise ValueError("Vector field dimension must match variables")
    return sum(sp.diff(vector_field[i], vars[i]) for i in range(len(vars)))

def curl(vector_field, vars):
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
    return sum(sp.diff(expr, v, 2) for v in vars)

def critical_points(expr, *vars):
    grad = gradient(expr, *vars)
    sols = sp.solve(grad, vars, dict=True)
    return sols

def hessian_matrix(expr, *vars):
    n = len(vars)
    H = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            H[i, j] = sp.diff(expr, vars[i], vars[j])
    return H

def tangent_line(expr, var, point):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    f_prime = sp.diff(expr, var_sym)
    slope = f_prime.subs(var_sym, point)
    y0 = expr.subs(var_sym, point)
    tangent = slope * (var_sym - point) + y0
    return sp.simplify(tangent)

def arc_length(expr, var, a, b):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    deriv = sp.diff(expr, var_sym)
    integrand = sp.sqrt(1 + deriv**2)
    return sp.integrate(integrand, (var_sym, a, b))

def surface_area(expr, var, a, b, axis='x'):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    deriv = sp.diff(expr, var_sym)
    if axis == 'x':
        integrand = 2 * sp.pi * expr * sp.sqrt(1 + deriv**2)
    else:
        integrand = 2 * sp.pi * var_sym * sp.sqrt(1 + deriv**2)
    return sp.integrate(integrand, (var_sym, a, b))

def volume_of_revolution(expr, var, a, b, axis='x'):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    if axis == 'x':
        integrand = sp.pi * expr**2
    else:
        integrand = 2 * sp.pi * var_sym * expr
    return sp.integrate(integrand, (var_sym, a, b))

def improper_integral(expr, var, lower, upper):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.integrate(expr, (var_sym, lower, upper))

def residue(expr, var, point):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
    return sp.residue(expr, var_sym, point)

def fourier_series(expr, var, period=2*sp.pi, n_terms=5):
    var_sym = sp.symbols(var) if isinstance(var, str) else var
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
    t_sym = sp.symbols(t) if isinstance(t, str) else t
    s_sym = sp.symbols(s) if isinstance(s, str) else s
    return sp.laplace_transform(expr, t_sym, s_sym, noconds=True)

def inverse_laplace_transform(expr, s, t):
    s_sym = sp.symbols(s) if isinstance(s, str) else s
    t_sym = sp.symbols(t) if isinstance(t, str) else t
    return sp.inverse_laplace_transform(expr, s_sym, t_sym)

def parse_ode_expression(eq_str, func_name, var_name, variables=None):
    """Parse a user-friendly ODE expression."""
    if variables is None:
        variables = {}
    
    var_sym = GLOBAL_SYMBOLS.get(var_name, sp.symbols(var_name))
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
    
    # Try user-friendly format
    eq_str = eq_str.strip()
    
    # Replace prime notation with Derivative
    for n in range(4, 0, -1):
        primes = "'" * n
        pattern = f"{func_name}{primes}"
        replacement = f"Derivative({func_name}({var_name}), {var_name}, {n})"
        eq_str = eq_str.replace(pattern, replacement)
    
    # Handle y(x) notation
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
    
    # Last resort: split on = and create Eq
    if '=' in eq_str:
        left, right = eq_str.split('=', 1)
        try:
            left_expr = sp.sympify(left.strip(), locals=local_dict)
            right_expr = sp.sympify(right.strip(), locals=local_dict)
            return sp.Eq(left_expr, right_expr)
        except Exception as e:
            raise ValueError(f"Could not parse ODE: {eq_str}. Error: {str(e)}")
    
    raise ValueError(f"Could not parse ODE: {eq_str}")

# ============ FORMATTING ============

def format_result(expr):
    """Format a SymPy expression for display."""
    if expr is None:
        return "undefined"
    try:
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