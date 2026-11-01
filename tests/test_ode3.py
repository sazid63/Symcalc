import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\1_SAJID\FreeBuff\Random apps\calculas')
from app import parse_ode_expression
import sympy as sp

x = sp.symbols('x', real=True)
y_func = sp.Function('y')

# Test 1: First order ODE
print("Test 1: First order ODE")
eq_str = "y' = y"
print(f"  Input string: '{eq_str}'")
eq = parse_ode_expression(eq_str, 'y', 'x')
print(f"  Parsed: {eq}")
print(f"  Type: {type(eq)}")
result = sp.dsolve(eq, y_func(x))
print(f"  Solution: {result}")

# Test 2: Second order ODE
print("\nTest 2: Second order ODE")
eq_str2 = "y'' + y = 0"
print(f"  Input string: '{eq_str2}'")
eq2 = parse_ode_expression(eq_str2, 'y', 'x')
print(f"  Parsed: {eq2}")
result2 = sp.dsolve(eq2, y_func(x))
print(f"  Solution: {result2}")

# Test 3: First order linear
print("\nTest 3: First order linear ODE")
eq_str3 = "y' + 2*y = exp(x)"
print(f"  Input string: '{eq_str3}'")
eq3 = parse_ode_expression(eq_str3, 'y', 'x')
print(f"  Parsed: {eq3}")
result3 = sp.dsolve(eq3, y_func(x))
print(f"  Solution: {result3}")
