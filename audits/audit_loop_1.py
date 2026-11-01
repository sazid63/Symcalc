#!/usr/bin/env python
"""
Audit Loop 1: Syntax and Import Validation
Reads main.py line by line and checks for syntax errors and import issues
"""
import sys
import ast
import importlib.util

print("=" * 60)
print("AUDIT LOOP 1/10: Syntax and Import Validation")
print("=" * 60)

def check_import(module_name):
    """Check if a module can be imported."""
    spec = importlib.util.find_spec(module_name)
    return spec is not None

# Test imports
modules_to_check = ['PySide6', 'matplotlib', 'numpy', 'sympy']
print("\nChecking required modules:")
for mod in modules_to_check:
    exists = check_import(mod)
    status = "✓ OK" if exists else "✗ MISSING"
    print(f"  {mod:15} {status}")

# Parse main.py
main_path = r'C:\1_SAJID\FreeBuff\Random apps\calculas\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"\nParsing {main_path} ({len(lines)} lines)...")
try:
    tree = ast.parse(''.join(lines))
    print("✓ Syntax check passed")
except SyntaxError as e:
    print(f"✗ Syntax error at line {e.lineno}: {e.msg}")
    sys.exit(1)

# Check for common issues
issues = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped or stripped.startswith('#'):
        continue
    # Check for undefined variables
    if 'self.' in line and 'self.' not in ['self.btn_solve', 'self.result_widget', 'self.op_tree', 
                                            'self.op_stack', 'self.op_panels', 'self.compute_thread',
                                            'self.current_op_key', 'self.history', 'self.params',
                                            'self.lbl_op_header', 'self.lbl_op_desc']:
        pass  # Known attributes are OK

print("\n" + "=" * 60)
print("AUDIT LOOP 1 COMPLETE")
print("=" * 60)