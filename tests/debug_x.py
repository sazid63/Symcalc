import sys
sys.path.insert(0, r'C:\1_SAJID\FreeBuff\Random apps\calculas')
import app
import sympy as sp

# Use the same x as the module
print('Module x:', app.x, id(app.x))

x = app.x
y_func = sp.Function('y')
direct_eq = sp.Eq(sp.Derivative(y_func(x), x), y_func(x))
print(f'Direct: {direct_eq}')

# Now parse
input_str = 'y' + chr(39) + ' = y'
eq = app.parse_ode_expression(input_str, 'y', 'x')
print(f'Parsed: {eq}')

# Compare
print(f'equal: {eq == direct_eq}')

# Try solving direct_eq with module x
result = sp.dsolve(direct_eq, y_func(x))
print(f'Direct solution: {result}')

# Try solving parsed
try:
    result2 = sp.dsolve(eq, y_func(x))
    print(f'Parsed solution: {result2}')
except Exception as e:
    print(f'Parsed error: {e}')

# What is the x in parsed?
print(f'Parsed x in args: {eq.args[0].args[1]}')
print(f'Module x: {x}')
print(f'x equal: {eq.args[0].args[1] == x}')
