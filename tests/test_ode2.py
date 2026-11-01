import sys
sys.path.insert(0, r'C:\1_SAJID\FreeBuff\Random apps\calculas')
from app import parse_ode_expression
import sympy as sp

x = sp.symbols('x', real=True)
y = sp.Function('y')

# Test 1: First order ODE
eq_str = "y' = y"
eq = parse_ode_expression(eq_str, 'y', 'x')
print(f"Test 1: '{eq_str}'")
print(f"  Parsed: {eq}")
print(f"  Type: {type(eq)}")
print(f"  Is Eq?: {isinstance(eq, sp.Eq)}")
result = sp.dsolve(eq, y(x))
print(f"  Solution: {result}")

# Test 2: Second order ODE  
eq_str2 = "y'' + y = 0"
eq2 = parse_ode_expression(eq_str2, 'y', 'x')
print(f"\nTest 2: '{eq_str2}'")
print(f"  Parsed: {eq2}")
print(f"  Type: {type(eq2)}")
result2 = sp.dsolve(eq2, y(x))
print(f"  Solution: {result2}")

# Test 3: First order linear
eq_str3 = "y' + 2*y = exp(x)"
eq3 = parse_ode_expression(eq_str3, 'y', 'x')
print(f"\nTest 3: '{eq_str3}'")
print(f"  Parsed: {eq3}")
result3 = sp.dsolve(eq3, y(x))
print(f"  Solution: {result3}")
