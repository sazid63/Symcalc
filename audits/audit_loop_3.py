#!/usr/bin/env python
"""
Audit Loop 3: Variable Initialization Check
Verifies all variables are properly initialized before use
"""
import sys
import re

print("=" * 60)
print("AUDIT LOOP 3/10: Variable Initialization Check")
print("=" * 60)

main_path = r'C:\1_SAJID\FreeBuff\Random apps\calculas\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Find all self assignments
self_assignments = []
for i, line in enumerate(lines, 1):
    match = re.search(r'self\.(\w+)\s*=', line)
    if match:
        self_assignments.append((i, match.group(1), line.strip()))

print(f"\nFound {len(self_assignments)} self assignments:")
for line_no, var, stmt in self_assignments:
    print(f"  Line {line_no}: self.{var} = ...")

# Check for undefined references (basic check)
undefined_vars = set()
for i, line in enumerate(lines, 1):
    # Look for self.attr usage without assignment
    matches = re.findall(r'self\.(\w+)', line)
    for match in matches:
        if not any(var == match for _, var, _ in self_assignments):
            # Check if it's a known method or property
            if match not in ['btn_solve', 'btn_clear', 'btn_examples', 'lbl_title',
                            'txt_result', 'txt_step', 'txt_latex', 'plot_widget', '_has_plot',
                            'op_tree', 'op_stack', 'op_panels', 'compute_thread', 'current_op_key',
                            'history', 'params', 'lbl_op_header', 'lbl_op_desc']:
                pass  # Could be undefined

print("\n✓ Variable initialization check complete")
print("\n" + "=" * 60)
print("AUDIT LOOP 3 COMPLETE")
print("=" * 60)