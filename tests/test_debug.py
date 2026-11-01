#!/usr/bin/env python
"""Debug failing API calls"""
import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def calc(op, params):
    data = json.dumps({'operation': op, 'params': params}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:5000/api/calculate', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return json.loads(body)

# Test gradient
r = calc('gradient', {'expression': 'x**2 + y**2', 'variables_list': ['x', 'y']})
print(f"gradient: {r}")

# Test divergence
r = calc('divergence', {'expression': '', 'vector_field': ['x**2', 'y**2', 'z**2'], 'variables_list': ['x', 'y', 'z']})
print(f"divergence: {r}")

# Test curl
r = calc('curl', {'expression': '', 'vector_field': ['-y', 'x', '0'], 'variables_list': ['x', 'y', 'z']})
print(f"curl: {r}")

# Test laplacian
r = calc('laplacian', {'expression': 'x**2 + y**2 + z**2', 'variables_list': ['x', 'y', 'z']})
print(f"laplacian: {r}")

# Test critical_points
r = calc('critical_points', {'expression': 'x**3 - 3*x + y**3 - 3*y', 'variables_list': ['x', 'y']})
print(f"critical_points: {r}")

# Test ode
r = calc('ode', {'expression': "y' = y", 'function': 'y'})
print(f"ode: {r}")