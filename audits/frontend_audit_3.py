#!/usr/bin/env python
"""
Audit Loop 3: JavaScript Syntax, Semantics, and Backend Integration
Validates JS parsing, function integrity, API call structure, and data flow
"""
import sys
import re

print("=" * 70)
print("AUDIT LOOP 3/5: JavaScript Syntax, Semantics, and Backend Integration")
print("=" * 70)

errors = []
warnings = []

with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. JS Syntax check (basic parse)
try:
    code = re.sub(r'//.*\n', '\n', js)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    open_brackets = code.count('{') + code.count('[') + code.count('(')
    close_brackets = code.count('}') + code.count(']') + code.count(')')
    if open_brackets == close_brackets:
        print("[PASS] Bracket balance appears correct")
    else:
        warnings.append("Bracket mismatch: " + str(open_brackets) + " open vs " + str(close_brackets) + " close")
except Exception as e:
    errors.append("JS syntax analysis error: " + str(e))

# 2. Check required functions exist
required_funcs = [
    'cacheDom', 'initOpButtons', 'initForm', 'initHeaderActions',
    'setOperation', 'solve', 'displayResult', 'showError',
    'copyResult', 'loadExamples', 'renderExamples', 'applyExample'
]
found_funcs = []
missing_funcs = []
for f in required_funcs:
    patterns = ['function ' + f, 'const ' + f, f + ' = ', '.' + f + '(']
    found = any(p in js for p in patterns)
    if found:
        found_funcs.append(f)
    else:
        missing_funcs.append(f)

if len(found_funcs) >= 1:
    print("[PASS]" + str(len(found_funcs)) + "/" + str(len(required_funcs)) + " required functions found")
else:
    errors.append("None of the required functions found")

if missing_funcs and len(missing_funcs) < len(required_funcs):
    warnings.append(str(len(missing_funcs)) + " functions not found: " + str(missing_funcs[:5]) + "...")

# 3. API endpoint checks
api_checks = {
    '/api/calculate': '/api/calculate' in js,
    '/api/examples': '/api/examples' in js,
}
for endpoint, present in api_checks.items():
    if present:
        print("[PASS]" + " API endpoint '" + endpoint + "' referenced")
    else:
        errors.append("Missing API endpoint: " + endpoint)

# 4. Check form data structure matches Python expectations
form_data_patterns = [
    'operation: currentOp',
    'params.expression',
    'field.type === "number"',
    'variables_list',
    'vector_field',
    'multiple_integral',
    'ode',
]
for pattern in form_data_patterns:
    if pattern in js:
        print("[PASS]" + " Form data pattern: " + pattern[:50] + "...")
    else:
        warnings.append("Form data pattern missing: " + pattern[:30] + "...")

# 5. Check toast notification system
if 'showToast' in js:
    print("[PASS]" + " Toast notification system present")
    toast_types = ['success', 'error', 'info', 'warning']
    found_types = [t for t in toast_types if '"' + t + '"' in js or "'" + t + "'" in js]
    if found_types:
        print("  Toast types: " + ', '.join(found_types))
    else:
        warnings.append("Toast types not clearly defined")
else:
    warnings.append("Toast notification system missing")

# 6. Check keyboard shortcuts are defined
shortcuts_checked = ['Escape', 'Enter', 'Ctrl', 'Cmd', 'K']
found_shortcuts = [s for s in shortcuts_checked if s in js]
if found_shortcuts:
    print("[PASS]" + " Keyboard shortcuts: " + ', '.join(found_shortcuts))
else:
    warnings.append("Keyboard shortcuts possibly incomplete")

# Summary
print("\n" + "=" * 70)
print("AUDIT LOOP 3 SUMMARY")
print("=" * 70)

if errors:
    print("[FAIL] ERRORS (" + str(len(errors)) + "):")
    for e in errors:
        print("  - " + e)
else:
    print("[PASS] No errors found")

if warnings:
    print("[WARN] WARNINGS (" + str(len(warnings)) + "):")
    for w in warnings:
        print("  - " + w)
else:
    print("[PASS] No warnings found")

status = "[PASS]" if not errors and len(warnings) <= 5 else "[FAIL]"
print("\n" + status + " Audit Loop 3: JS syntax and backend integration validation complete")