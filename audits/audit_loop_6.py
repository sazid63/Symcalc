#!/usr/bin/env python
"""
Audit Loop 6: Error Handling Check
Verifies try/except blocks and error handling patterns
"""
import sys
import re

print("=" * 60)
print("AUDIT LOOP 6/10: Error Handling Check")
print("=" * 60)

main_path = r'C:\1_SAJID\FreeBuff\Random apps\calculas\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Find all try/except blocks
try_blocks = []
except_blocks = []
for i, line in enumerate(lines, 1):
    if 'try:' in line:
        try_blocks.append(i)
    if 'except' in line:
        except_blocks.append(i)

print(f"\nFound {len(try_blocks)} try blocks:")
for i in try_blocks:
    print(f"  Line {i}: {lines[i-1].strip()}")

print(f"\nFound {len(except_blocks)} except blocks:")
for i in except_blocks:
    print(f"  Line {i}: {lines[i-1].strip()}")

# Check for bare except
bare_except = []
for i, line in enumerate(lines, 1):
    if re.match(r'\s*except\s*:', line.strip()):
        bare_except.append(i)

if bare_except:
    print(f"\n⚠ Found {len(bare_except)} bare 'except' (should specify exception type):")
    for i in bare_except:
        print(f"  Line {i}: {lines[i-1].strip()}")
else:
    print("\n✓ No bare except clauses found")

# Check for error messages
error_msgs = re.findall(r'"Error.*?"', content)
print(f"\nFound {len(error_msgs)} error messages")

print("\n" + "=" * 60)
print("AUDIT LOOP 6 COMPLETE")
print("=" * 60)