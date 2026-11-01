#!/usr/bin/env python
"""
Audit Loop 2: Class and Method Structure
Reads line by line to verify class definitions, method signatures, and structure
"""
import sys
import re

print("=" * 60)
print("AUDIT LOOP 2/10: Class and Method Structure")
print("=" * 60)

main_path = r'C:\1_SAJID\FreeBuff\Random apps\calculas\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

classes = []
methods = []
for i, line in enumerate(lines, 1):
    # Match class definitions
    match = re.match(r'^class\s+(\w+)', line.strip())
    if match:
        classes.append((i, match.group(1)))
    
    # Match method definitions
    match = re.match(r'^\s+def\s+(\w+)\(', line.strip())
    if match:
        methods.append((i, match.group(1)))

print(f"\nFound {len(classes)} classes:")
for line_no, name in classes:
    print(f"  Line {line_no}: {name}")

print(f"\nFound {len(methods)} methods:")
for line_no, name in methods:
    print(f"  Line {line_no}: {name}")

# Check for expected classes
expected_classes = ['OperationPanel', 'ResultWidget', 'PlotWidget', 'ComputeThread', 'MainWindow']
missing = [c for c in expected_classes if not any(c == name for _, name in classes)]
if missing:
    print(f"\n✗ Missing expected classes: {missing}")
else:
    print(f"\n✓ All expected classes found")

print("\n" + "=" * 60)
print("AUDIT LOOP 2 COMPLETE")
print("=" * 60)