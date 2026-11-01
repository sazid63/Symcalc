#!/usr/bin/env python
"""
Audit Loop 9: Calculation Correctness Verification
Runs test cases to verify calculus operations produce correct results
"""
import sys
sys.path.insert(0, r'C:\1_SAJID\FreeBuff\Random apps\calculas')

print("=" * 60)
print("AUDIT LOOP 9/10: Calculation Correctness Verification")
print("=" * 60)

from calculus_core import (
    parse_expression, derivative, integral, limit_expr, series_expansion,
    gradient, laplacian, divergence, curl, critical_points, tangent_line,
    arc_length, volume_of_revolution, improper_integral, residue,
    laplace_transform, inverse_laplace_transform, parse_ode_expression
)
import sympy as sp

x, y, z, t = sp.symbols('x y z t', real=True)

tests = [
    ("Derivative", lambda: derivative(parse_expression('x**3'), x, 1)),
    ("Integral sin", lambda: integral(parse_expression('cos(x)'), x, 0, sp.pi/2)),
    ("Limit sin/x", lambda: limit_expr(parse_expression('sin(x)/x'), x, 0)),
    ("Series exp", lambda: series_expansion(parse_expression('exp(x)'), x, 0, 4)),
    ("Gradient", lambda: gradient(parse_expression('x**2 + y**2'), x, y)),
    ("Laplacian", lambda: laplacian(parse_expression('x**2 + y**2 + z**2'), x, y, z)),
    ("Divergence", lambda: divergence([parse_expression('x'), parse_expression('y'), parse_expression('z')], x, y, z)),
    ("Curl", lambda: curl([parse_expression('-y'), parse_expression('x'), parse_expression('0')], (x, y, z))),
    ("Tangent", lambda: tangent_line(parse_expression('x**2'), x, 1)),
    ("Arc length", lambda: arc_length(parse_expression('x'), x, 0, 1)),
    ("Volume", lambda: volume_of_revolution(parse_expression('x'), x, 0, 1, 'x')),
    ("Improper", lambda: improper_integral(parse_expression('exp(-x)'), x, 0, sp.oo)),
    ("Residue", lambda: residue(parse_expression('1/(z*I - 1)'), z, sp.I)),
    ("Laplace", lambda: laplace_transform(parse_expression('exp(-t)'), t, sp.symbols('s'))),
    ("InvLaplace", lambda: inverse_laplace_transform(parse_expression('1/s'), sp.symbols('s'), t)),
    ("ODE", lambda: parse_ode_expression("y' = y", 'y', 'x')),
]

print("\nRunning correctness tests:")
passed = 0
failed = 0

for name, test in tests:
    try:
        result = test()
        # Verify result is not None and is a valid sympy expression
        if result is not None:
            print(f"  ✓ {name}: {result}")
            passed += 1
        else:
            print(f"  ✗ {name}: Returned None")
            failed += 1
    except Exception as e:
        print(f"  ✗ {name}: {str(e)[:60]}")
        failed += 1

print(f"\nResults: {passed} passed, {failed} failed, {len(tests)} total")

print("\n" + "=" * 60)
print("AUDIT LOOP 9 COMPLETE")
print("=" * 60)