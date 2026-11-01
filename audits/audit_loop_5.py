#!/usr/bin/env python
"""
Audit Loop 5: Memory and Resource Leak Check
Looks for potential memory leaks and resource management issues
"""
import sys
import re

print("=" * 60)
print("AUDIT LOOP 5/10: Memory and Resource Leak Check")
print("=" * 60)

main_path = r'C:\1_SAJID\FreeBuff\Random apps\calculas\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

issues = []

# Check for potential memory leaks
for i, line in enumerate(lines, 1):
    # Check for infinite loops
    if 'while True' in line and 'break' not in line:
        issues.append((i, "Potential infinite loop without break", line.strip()))
    
    # Check for large list allocations
    if 'np.linspace' in line:
        issues.append((i, "Array allocation - check size", line.strip()))
    
    # Check for unbounded recursion
    if re.match(r'\s*def\s+\w+.*\(\s*\)', line.strip()):
        method_name = re.search(r'def\s+(\w+)', line.strip()).group(1)
        # Check if method calls itself
        for j in range(i, min(i+50, len(lines))):
            if re.search(rf'self\.{method_name}\(', lines[j]):
                issues.append((i, f"Possible recursion: {method_name}", lines[j].strip()))
                break

print("\nPotential issues found:")
if issues:
    for line_no, issue, context in issues[:20]:  # Show first 20
        print(f"  Line {line_no}: {issue}")
        print(f"    Context: {context}")
else:
    print("  ✓ No obvious memory leaks detected")

print("\n✓ Resource check complete")
print("\n" + "=" * 60)
print("AUDIT LOOP 5 COMPLETE")
print("=" * 60)