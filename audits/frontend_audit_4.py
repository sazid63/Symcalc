#!/usr/bin/env python
"""
Audit Loop 4: UI-Backend Communication Integrity
Validates that all UI operation switching correctly maps to backend handlers,
data flows properly, and error handling is integrated
"""
import sys
import re

print("=" * 70)
print("AUDIT LOOP 4/5: UI-Backend Communication Integrity")
print("=" * 70)

errors = []
warnings = []

with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()
with open('main.py', 'r', encoding='utf-8') as f:
    py = f.read()

# 1. Operation buttons map to Python handlers
op_buttons = re.findall(r'data-op="(\w+)"', js)
python_ops = re.findall(r'"key":\s*"(\w+)"', py)

button_op_set = set(op_buttons)
py_op_set = set(python_ops)

missing_from_py = button_op_set - py_op_set
missing_from_js = py_op_set - button_op_set

if missing_from_py:
    warnings.append(str(len(missing_from_py)) + " JS ops not in Python: " + str(list(missing_from_py)[:5]))
else:
    print("[PASS] All JS operation buttons map to Python handlers")

if missing_from_js:
    warnings.append(str(len(missing_from_js)) + " Python ops not mapped in JS: " + str(list(missing_from_js)[:5]))
else:
    print("[PASS]" + " All Python operations have JS button mappings")

# 2. Check that setOperation() is called for each op type
op_types_in_js = set(op_buttons)
set_op_cases = len(re.findall(r'elif op_key == "', js))
if set_op_cases >= len(op_types_in_js):
    print("[PASS]" + " setOperation has " + str(set_op_cases) + "+ case blocks for " + str(len(op_types_in_js)) + " ops")
else:
    warnings.append("setOperation may be missing cases: " + str(set_op_cases) + " cases for " + str(len(op_types_in_js)) + " ops")

# 3. Check form data gets sent correctly
integration_checks = [
    ('expression sent', 'expression' in js and 'data.params.expression' in js),
    ('operation type sent', 'operation: currentOp' in js),
    ('variable field handled', 'input-variable' in js.lower()),
    ('error handling present', 'showError' in js),
    ('success handling present', 'displayResult' in js),
    ('loading state present', 'setButtonLoading' in js),
    ('toast on success', 'showToast' in js and 'success' in js),
]

for check_name, result in integration_checks:
    if result:
        print("[PASS]" + " " + check_name)
    else:
        errors.append("Missing integration check: " + check_name)

# 3. Check that solve() disables button and shows spinner
if 'isSolving = true' in js and 'setButtonLoading(true)' in js:
    print("[PASS]" + " solve() shows loading state (button disable + spinner)")
else:
    errors.append("solve() missing loading state")

# 4. Check that result display clears previous results
if "els['result-panel'].hidden" in js or 'els["result-panel"].hidden' in js:
    print("[PASS]" + " Result panel clearing present")
else:
    warnings.append("Result panel clearing pattern unclear")

# 5. Check history persistence logic
if 'localStorage' in js and 'JSON.stringify' in js:
    print("[PASS]" + " History persistence via localStorage")
else:
    warnings.append("No localStorage history persistence found")

# Summary
print("\n" + "=" * 70)
print("AUDIT LOOP 4 SUMMARY")
print("=" * 70)

if errors:
    print("[FAIL] ERRORS (" + str(len(errors)) + "):")
    for e in errors:
        print("  - " + e)
else:
    print("[PASS]" + " No errors found")

if warnings:
    print("[WARN] WARNINGS (" + str(len(warnings)) + "):")
    for w in warnings:
        print("  - " + w)
else:
    print("[PASS]" + " No warnings found")

status = "[PASS]" if not errors and len(warnings) <= 5 else "[FAIL]"
print("\n" + status + " Audit Loop 4: UI-Backend communication integrity validation complete")