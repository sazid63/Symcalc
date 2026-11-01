#!/usr/bin/env python
"""
Test script for calculus operations
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\1_SAJID\FreeBuff\Random apps\calculas')

import sympy as sp
from app import (
    parse_expression, derivative, integral, limit_expr, series_expansion,
    solve_ode, gradient, divergence, curl, laplacian, critical_points,
    hessian_matrix, parse_ode_expression, multiple_integral,
    tangent_line, normal_line, arc_length, surface_area, volume_of_revolution,
    improper_integral, residue, fourier_series, laplace_transform, inverse_laplace_transform,
    partial_derivative
)

# Define symbols
x, y, z, t = sp.symbols('x y z t', real=True)

print("Testing Calculus Operations")
print("=" * 50)

# Test 1: Derivative
print("\n1. Derivative:")
expr = parse_expression('x**3 + 2*x**2 - 5*x + 1')
result = derivative(expr, x, 1)
print(f"  d/dx (x^3 + 2x^2 - 5x + 1) = {result}")

# Test 2: Integral (indefinite)
print("\n2. Indefinite Integral:")
expr = parse_expression('x**2*sin(x)')
result = integral(expr, x)
print(f"  int x^2*sin(x) dx = {result}")

# Test 3: Definite Integral
print("\n3. Definite Integral:")
expr = parse_expression('1/(x**2 + 1)')
result = integral(expr, x, 0, sp.oo)
print(f"  int[0,inf] 1/(x^2+1) dx = {result}")

# Test 4: Limit
print("\n4. Limit:")
expr = parse_expression('sin(x)/x')
result = limit_expr(expr, x, 0)
print(f"  lim[x->0] sin(x)/x = {result}")

# Test 5: Series
print("\n5. Series Expansion:")
expr = parse_expression('exp(x)')
result = series_expansion(expr, x, 0, 6)
print(f"  Series of e^x at x=0: {result}")

# Test 6: Partial Derivative
print("\n6. Partial Derivative:")
expr = parse_expression('x**2*y + y**3')
result = partial_derivative(expr, x, y)
print(f"  d^2/dxdy (x^2*y + y^3) = {result}")

# Test 7: Gradient
print("\n7. Gradient:")
expr = parse_expression('x**2 + y**2')
result = gradient(expr, x, y)
print(f"  grad(x^2 + y^2) = {result}")

# Test 8: Divergence
print("\n8. Divergence:")
F = [parse_expression('x**2'), parse_expression('y**2'), parse_expression('z**2')]
result = divergence(F, x, y, z)
print(f"  div(x^2, y^2, z^2) = {result}")

# Test 9: Curl
print("\n9. Curl:")
F = [parse_expression('-y'), parse_expression('x'), parse_expression('0')]
result = curl(F, (x, y, z))
print(f"  curl(-y, x, 0) = {result}")

# Test 10: Laplacian
print("\n10. Laplacian:")
expr = parse_expression('x**2 + y**2 + z**2')
result = laplacian(expr, x, y, z)
print(f"  Laplacian(x^2 + y^2 + z^2) = {result}")

# Test 11: Critical Points
print("\n11. Critical Points:")
expr = parse_expression('x**3 - 3*x + y**3 - 3*y')
result = critical_points(expr, x, y)
print(f"  Critical points of x^3 - 3x + y^3 - 3y = {result}")

# Test 12: Hessian
print("\n12. Hessian Matrix:")
expr = parse_expression('x**2*y + x*y**2')
result = hessian_matrix(expr, x, y)
print(f"  H(x^2*y + x*y^2) = {result}")

# Test 13: Multiple Integral
print("\n13. Multiple Integral:")
expr = parse_expression('x*y')
result = multiple_integral(expr, (x, 0, 1), (y, 0, 2))
print(f"  double int x*y dx dy over [0,1]x[0,2] = {result}")

# Test 14: Tangent Line
print("\n14. Tangent Line:")
expr = parse_expression('x**2')
result = tangent_line(expr, x, 2)
print(f"  Tangent to x^2 at x=2: y = {result}")

# Test 15: Arc Length
print("\n15. Arc Length:")
expr = parse_expression('sqrt(1 - x**2)')
result = arc_length(expr, x, -1, 1)
print(f"  Arc length of semicircle = {result}")

# Test 16: Volume of Revolution
print("\n16. Volume of Revolution:")
expr = parse_expression('sqrt(1 - x**2)')
result = volume_of_revolution(expr, x, -1, 1, 'x')
print(f"  Volume of sphere (disc method) = {result}")

# Test 17: Improper Integral
print("\n17. Improper Integral:")
expr = parse_expression('exp(-x)')
result = improper_integral(expr, x, 0, sp.oo)
print(f"  int[0,inf] e^(-x) dx = {result}")

# Test 18: Residue
print("\n18. Residue:")
z = sp.symbols('z')
expr = parse_expression('1/(z**2 + 1)')
result = residue(expr, z, sp.I)
print(f"  Residue of 1/(z^2+1) at z=i = {result}")

# Test 19: Fourier Series
print("\n19. Fourier Series:")
expr = parse_expression('x')
result = fourier_series(expr, x, 2*sp.pi, 3)
print(f"  Fourier of x on [-pi,pi]: a0={result['a0']}, b1={result['b1']}, b2={result['b2']}")

# Test 20: Laplace Transform
print("\n20. Laplace Transform:")
t, s = sp.symbols('t s', positive=True)
a, b = sp.symbols('a b', positive=True)
expr = parse_expression('exp(-a*t)*sin(b*t)', {'a': a, 'b': b})
result = laplace_transform(expr, t, s)
print(f"  Laplace of e^(-at)*sin(bt) = {result}")

# Test 21: Inverse Laplace
print("\n21. Inverse Laplace:")
expr = parse_expression('1/(s**2 + 1)')
result = inverse_laplace_transform(expr, s, t)
print(f"  Inverse Laplace of 1/(s^2+1) = {result}")

# Test 22: ODE (simple)
print("\n22. ODE:")
func = sp.Function('y')
eq = parse_ode_expression("y' = y", 'y', 'x')
print(f"  ODE: {eq}")
result = solve_ode(eq, func(x))
print(f"  Solution: {result}")

# Test 23: ODE second order
print("\n23. Second Order ODE:")
eq = parse_ode_expression("y'' + y = 0", 'y', 'x')
result = solve_ode(eq, func(x))
print(f"  Solution to y'' + y = 0: {result}")

print("\n" + "=" * 50)
print("All tests completed!")
