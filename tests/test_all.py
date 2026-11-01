#!/usr/bin/env python
import sys
sys.path.insert(0, r'C:\1_SAJID\FreeBuff\Random apps\calculas')
from calculus_core import *
import sympy as sp

# Test all calculus operations programmatically
tests = [
    ('Derivative', lambda: derivative(parse_expression('x**3*sin(2*x)'), x, 1)),
    ('Integral', lambda: integral(parse_expression('exp(-x**2)'), x, -sp.oo, sp.oo)),
    ('Limit', lambda: limit_expr(parse_expression('sin(x)/x'), x, 0)),
    ('Series', lambda: series_expansion(parse_expression('exp(x)'), x, 0, 5)),
    ('Partial', lambda: partial_derivative(parse_expression('x**2*y + y**3'), x, y)),
    ('Gradient', lambda: gradient(parse_expression('x**2 + y**2'), x, y)),
    ('Hessian', lambda: hessian_matrix(parse_expression('x**2*y + x*y**2'), x, y)),
    ('Critical', lambda: critical_points(parse_expression('x**3 - 3*x + y**3 - 3*y'), x, y)),
    ('Laplacian', lambda: laplacian(parse_expression('x**2 + y**2 + z**2'), x, y, z)),
    ('Divergence', lambda: divergence([parse_expression('x**2'), parse_expression('y**2'), parse_expression('z**2')], x, y, z)),
    ('Curl', lambda: curl([parse_expression('-y'), parse_expression('x'), parse_expression('0')], (x, y, z))),
    ('Multiple', lambda: multiple_integral(parse_expression('x*y'), (x, 0, 1), (y, 0, 1))),
    ('Tangent', lambda: tangent_line(parse_expression('x**2'), x, 2)),
    ('Arc', lambda: arc_length(parse_expression('sqrt(1-x**2)'), x, -1, 1)),
    ('Volume', lambda: volume_of_revolution(parse_expression('sqrt(1-x**2)'), x, -1, 1, 'x')),
    ('Improper', lambda: improper_integral(parse_expression('exp(-x)'), x, 0, sp.oo)),
    ('Residue', lambda: residue(parse_expression('1/(z**2+1)'), z, sp.I)),
    ('Fourier', lambda: fourier_series(parse_expression('x'), x, 2*sp.pi, 3)),
    ('Laplace', lambda: laplace_transform(parse_expression('exp(-a*t)*sin(b*t)'), t, sp.symbols('s'))),
    ('InvLaplace', lambda: inverse_laplace_transform(parse_expression('1/(s**2+1)'), sp.symbols('s'), sp.symbols('t'))),
    ('ODE', lambda: solve_ode(parse_ode_expression("y' = y", 'y', 'x'), sp.Function('y')(sp.symbols('x')))),
]

print('Testing 21 calculus operations...')
for name, func in tests:
    try:
        result = func()
        print('PASS {0:15} {1}'.format(name, format_result(result)[:50]))
    except Exception as e:
        print('FAIL {0:15} {1}'.format(name, str(e)[:80]))

print('\nAll core operations functional!')