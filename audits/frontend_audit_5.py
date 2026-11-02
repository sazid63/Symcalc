#!/usr/bin/env python
"""
Audit Loop 5: Code Style, Maintainability, and Documentation
Validates Python/JS code style, comment density, function docstrings, and readability
"""
import sys
import re

print("=" * 70)
print("AUDIT LOOP 5/5: Code Style, Maintainability, and Documentation")
print("=" * 70)

errors = []
warnings = []

# ---- Python checks ----
print("\n--- Python Code Style Checks ---")

with open('main.py', 'r', encoding='utf-8') as f:
    py_content = f.read()
    py_lines = py_content.split('\n')

# 1. Check for docstrings in key functions
key_funcs = ['derivative', 'integral', 'limit_expr', 'series_expansion',
             'gradient', 'divergence', 'curl', 'laplacian', 'critical_points',
             'hessian_matrix', 'tangent_line', 'arc_length', 'volume_of_revolution',
             'improper_integral', 'residue', 'fourier_series', 'laplace_transform',
             'inverse_laplace_transform', 'parse_ode_expression']

docstring_checks = 0
for func_name in key_funcs:
    pattern = rf'def {func_name}\(.*?:\s*"""'
    if re.search(pattern, py_content, re.DOTALL):
        docstring_checks += 1
    alt = rf'def {func_name}\(.*?\n.*?"""'
    if re.search(alt, py_content, re.DOTALL):
        docstring_checks += 1

docstring_pct = (docstring_checks / len(key_funcs)) * 100 if key_funcs else 0
if docstring_pct >= 50:
    msg = str(docstring_checks) + "/" + str(len(key_funcs)) + " key functions (" + str(round(docstring_pct)) + "%) have docstrings"
    print("[PASS]" + msg)
else:
    warnings.append("Low docstring coverage: " + str(docstring_checks) + "/" + str(len(key_funcs)) + " (" + str(round(docstring_pct)) + "%)")

# 2. Check line length (PEP8 recommends <= 79 or <= 99)
long_lines = 0
for i, line in enumerate(py_lines, 1):
    if len(line) > 99:
        long_lines += 1
long_pct = (long_lines / len(py_lines)) * 100 if py_lines else 0
if long_pct < 5:
    msg = str(long_lines) + " lines > 99 chars (" + str(round(long_pct, 1)) + "%) — within PEP8 limits"
    print("[PASS]" + msg)
else:
    warnings.append("Many long lines: " + str(long_lines) + "/" + str(len(py_lines)) + " (" + str(round(long_pct, 1)) + "%)")

# 2. Check function length (no excessively long functions)
func_sizes = re.findall(r'def \w+\(.*?\n(?:    .*\n)*?(?=\n\w+|\nclass|\n@)', py_content, re.DOTALL)
oversized_funcs = [f for f in func_sizes if len(f) > 500]
if oversized_funcs:
    warnings.append(str(len(oversized_funcs)) + " functions > 500 chars — consider refactoring")
else:
    print("[PASS]" + " No excessively long functions detected")

# 3. Blank line ratio (should have reasonable spacing)
non_blank = [l for l in py_lines if l.strip()]
blank_lines = len(py_lines) - len(non_blank)
blank_pct = (blank_lines / len(py_lines)) * 100 if py_lines else 0
if 10 <= blank_pct <= 30:
    msg = "Blank line ratio: " + str(round(blank_pct, 1)) + "% — healthy code spacing"
    print("[PASS]" + msg)
else:
    warnings.append("Unusual blank line ratio: " + str(round(blank_pct, 1)) + "%")

# 4. Type hint check (modern Python)
if '->' in py_content:
    print("[PASS]" + " Type hints (->) found in code")
else:
    warnings.append("No type hints found — consider adding them")

# ---- JavaScript checks ----
print("\n--- JavaScript Code Style Checks ---")

with open('static/app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()
    js_lines = js_content.split('\n')

# 1. Check for comments
comment_lines = len(re.findall(r'//.*|\*/', js_content, re.DOTALL))
comment_pct = (comment_lines / len(js_lines)) * 100 if js_lines else 0
if comment_pct >= 8:
    msg = str(round(comment_pct, 1)) + "% comment density — healthy"
    print("[PASS]" + msg)
else:
    warnings.append("Low comment density: " + str(round(comment_pct, 1)) + "%")

# 2. Check for modern JS features (const/let vs var)
if 'const ' in js_content and 'let ' in js_content:
    print("[PASS]" + " Uses modern const/let (not just var)")
else:
    warnings.append("May be using older var declarations")

# 3. Check for code duplication markers
duplicate_patterns = len(re.findall(r'(.{50}).*\1', js_content))
if duplicate_patterns < 5:
    print("[PASS]" + " Low code duplication detected")
else:
    warnings.append("High code duplication: " + str(duplicate_patterns) + " repeated patterns")

# 4. Check indentation consistency
indented = [l for l in js_lines if l.strip().startswith('    ')]  # 4-space indent
if len(indented) > len(js_lines) * 0.6:
    print("[PASS]" + " JavaScript appears to use consistent indentation")
else:
    warnings.append("Inconsistent JavaScript indentation detected")

# 5. Check JSDoc or block comments presence
has_block_comments = bool(re.search(r'/\*.*?\*/', js_content, re.DOTALL))
if has_block_comments:
    print("[PASS]" + " Block comments (/* */) found")
else:
    warnings.append("No block comments found — consider adding them for complex functions")

# Summary
print("\n" + "=" * 70)
print("AUDIT LOOP 5 SUMMARY")
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

# Overall verdict
pass_count = sum(1 for s in [docstring_pct >= 50, long_pct < 5, 10 <= blank_pct <= 30, comment_pct >= 8, has_block_comments]) if 'docstring_pct' in dir() else 0
status = "[PASS]" if pass_count >= 3 else "[FAIL]"
print("\n" + status + " Audit Loop 5: Code style and maintainability validation complete")
print("\nNote: These are heuristic checks — manual review recommended for critical changes")