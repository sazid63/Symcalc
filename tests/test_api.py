#!/usr/bin/env python
"""Test API endpoints"""
import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def calc(op, params, timeout=60):
    data = json.dumps({'operation': op, 'params': params}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:5000/api/calculate', data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))

tests = [
    ('derivative', {'expression': 'sin(x)*cos(x)', 'variable': 'x', 'order': 1}),
    ('derivative', {'expression': 'exp(x**2)', 'variable': 'x', 'order': 2}),
    ('integral', {'expression': '1/(x**2+1)', 'variable': 'x', 'lower': '0', 'upper': 'oo'}),
    ('integral', {'expression': 'x**2*sin(x)', 'variable': 'x'}),
    ('limit', {'expression': 'sin(x)/x', 'variable': 'x', 'point': '0'}),
    ('limit', {'expression': '(1 + 1/x)**x', 'variable': 'x', 'point': 'oo'}),
    ('series', {'expression': 'exp(x)', 'variable': 'x', 'point': '0', 'terms': '6'}),
    ('series', {'expression': 'log(1+x)', 'variable': 'x', 'point': '0', 'terms': '6'}),
    ('partial_derivative', {'expression': 'x**2*y + y**3', 'variables_list': ['x', 'y']}),
    ('gradient', {'expression': 'x**2 + y**2', 'variables_list': ['x', 'y']}),
    ('divergence', {'expression': '', 'vector_field': ['x**2', 'y**2', 'z**2'], 'variables_list': ['x', 'y', 'z']}),
    ('curl', {'expression': '', 'vector_field': ['-y', 'x', '0'], 'variables_list': ['x', 'y', 'z']}),
    ('laplacian', {'expression': 'x**2 + y**2 + z**2', 'variables_list': ['x', 'y', 'z']}),
    ('critical_points', {'expression': 'x**3 - 3*x + y**3 - 3*y', 'variables_list': ['x', 'y']}),
    ('tangent_line', {'expression': 'x**2', 'variable': 'x', 'point': '2'}),
    ('arc_length', {'expression': 'sqrt(1 - x**2)', 'variable': 'x', 'a': '-1', 'b': '1'}),
    ('volume_revolution', {'expression': 'sqrt(1 - x**2)', 'variable': 'x', 'a': '-1', 'b': '1', 'axis': 'x'}),
    ('improper_integral', {'expression': 'exp(-x)', 'variable': 'x', 'lower': '0', 'upper': 'oo'}),
    ('residue', {'expression': '1/(z**2+1)', 'variable': 'z', 'point': 'I'}),
    ('fourier_series', {'expression': 'x', 'variable': 'x', 'period': '2*pi', 'terms': '5'}),
    ('laplace', {'expression': 'exp(-a*t)*sin(b*t)', 't_var': 't', 's_var': 's'}),
    ('laplace', {'expression': 't**2', 't_var': 't', 's_var': 's'}),
    ('inverse_laplace', {'expression': '1/(s**2+1)', 's_var': 's', 't_var': 't'}),
    ('inverse_laplace', {'expression': 's/(s**2+4)', 's_var': 's', 't_var': 't'}),
    ('ode', {'expression': "y' = y", 'function': 'y'}),
    ('ode', {'expression': "y'' + y = 0", 'function': 'y'}),
    ('ode', {'expression': "y' + 2*y = exp(x)", 'function': 'y'}),
]

pass_count = 0
fail_count = 0
for op, params in tests:
    try:
        r = calc(op, params)
        if r.get('success'):
            print(f"PASS {op:22} {str(params.get('expression'))[:30]:32} -> {str(r['result'])[:60]}")
            pass_count += 1
        else:
            print(f"FAIL {op:22} {str(params.get('expression'))[:30]:32} ERR: {r.get('error', '')[:100]}")
            fail_count += 1
    except Exception as e:
        print(f"EXC  {op:22} {str(params.get('expression'))[:30]:32} EXC: {str(e)[:100]}")
        fail_count += 1

print(f"\n{pass_count} passed, {fail_count} failed, {len(tests)} total")