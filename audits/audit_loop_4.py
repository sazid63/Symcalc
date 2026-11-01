#!/usr/bin/env python
"""
Audit Loop 4: Operation Coverage Check
Verifies all operations in OPERATIONS dict have corresponding handlers
"""
import sys
import re

print("=" * 60)
print("AUDIT LOOP 4/10: Operation Coverage Check")
print("=" * 60)

main_path = r'C:\1_SAJID\FreeBuff\Random apps\calculas\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all operation keys in OPERATIONS dict
op_keys = re.findall(r'"key":\s*"(\w+)"', content)
unique_ops = list(set(op_keys))
print(f"\nFound {len(unique_ops)} unique operations:")
for op in sorted(unique_ops):
    print(f"  - {op}")

# Find all handler blocks in ComputeThread.run()
handlers = re.findall(r'(?:elif|if) op_key == "(\w+)"', content)
unique_handlers = list(set(handlers))
print(f"\nFound {len(unique_handlers)} handler blocks:")
for op in sorted(unique_handlers):
    print(f"  - {op}")

# Check coverage
missing_handlers = [op for op in unique_ops if op not in unique_handlers]
extra_handlers = [op for op in unique_handlers if op not in unique_ops]

if missing_handlers:
    print(f"\n✗ Operations missing handlers: {missing_handlers}")
else:
    print(f"\n✓ All operations have handlers")

if extra_handlers:
    print(f"⚠ Extra handlers not in OPERATIONS: {extra_handlers}")

print("\n" + "=" * 60)
print("AUDIT LOOP 4 COMPLETE")
print("=" * 60)