#!/usr/bin/env python
"""
Audit Loop 7: Thread Safety Check
Verifies thread-safe operations in ComputeThread
"""
import sys
import re

print("=" * 60)
print("AUDIT LOOP 7/10: Thread Safety Check")
print("=" * 60)

main_path = r'C:\1_SAJID\FreeBuff\Random apps\calculas\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Check ComputeThread class
in_thread_class = False
thread_issues = []

for i, line in enumerate(lines, 1):
    if 'class ComputeThread' in line:
        in_thread_class = True
    elif in_thread_class and line.strip().startswith('class '):
        in_thread_class = False
    
    if in_thread_class:
        # Check for GUI operations in thread (should not be done)
        if 'self.' in line and ('QLabel', 'setText', 'QMessageBox') in [l for l in ['QLabel', 'setText', 'QMessageBox'] if l in line]:
            thread_issues.append((i, "GUI operation in thread", line.strip()))

print(f"\nChecked ComputeThread for thread safety issues")
if thread_issues:
    print(f"⚠ Found {len(thread_issues)} potential issues:")
    for i, msg, ctx in thread_issues:
        print(f"  Line {i}: {msg}")
        print(f"    {ctx}")
else:
    print("✓ No obvious thread safety issues detected")

# Check signal usage
signal_count = content.count('Signal')
emit_count = content.count('emit')
connect_count = content.count('connect')

print(f"\nThreading primitives found:")
print(f"  Signal declarations: {signal_count}")
print(f"  emit() calls: {emit_count}")
print(f"  connect() calls: {connect_count}")

print("\n" + "=" * 60)
print("AUDIT LOOP 7 COMPLETE")
print("=" * 60)