import sys
sys.path.insert(0, r'C:\1_SAJID\FreeBuff\Random apps\calculas')
from app import parse_ode_expression
import sympy as sp

x = sp.symbols('x', real=True)

# Test 1: First order
eq = parse_ode_expression("y' = y", 'y', 'x')
print("Test 1 - First order:")
print(f"  Parsed ODE: {eq}")
print(f"  Type: {type(eq)}")
func = sp.Function('y')
result = sp.dsolve(eq, func(x))
print(f"  Solution: {result}")

# Test 2: Second order
eq2 = parse_ode_expression("y'' + y = 0", 'y', 'x')
print("\nTest 2 - Second order:")
print(f"  Parsed ODE: {eq2}")
print(f"  Type: {type(eq2)}")
result2 = sp.dsolve(eq2, func(x))
print(f"  Solution: {result2}")