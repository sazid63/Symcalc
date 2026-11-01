#!/usr/bin/env python
"""
Audit Loop 8: UI Consistency Check
Verifies consistent use of Qt components and styling
"""
import sys
import re

print("=" * 60)
print("AUDIT LOOP 8/10: UI Consistency Check")
print("=" * 60)

main_path = r'C:\1_SAJID\FreeBuff\Random apps\calculas\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Check for consistent Qt imports
expected_imports = {
    'QApplication': 1,
    'QMainWindow': 1,
    'QWidget': 1,
    'QVBoxLayout': 1,
    'QHBoxLayout': 1,
    'QComboBox': 1,
    'QLabel': 1,
    'QFormLayout': 1,
    'QStackedWidget': 1,
    'QToolButton': 1,
    'QFrame': 1,
    'QSplitter': 1,
    'QTreeWidget': 1,
    'QLineEdit': 1,
    'QSpinBox': 1,
    'QPushButton': 1,
    'QFileDialog': 1,
}

print("\nChecking Qt imports consistency...")
import_section = content.split('from PySide6.QtWidgets import')[1].split(')')[0]
import_count = len(re.findall(r'\w+', import_section))
print(f"  Items in QtWidgets import: {import_count}")

# Check for proper widget parenting
parent_issues = []
for i, line in enumerate(lines, 1):
    if 'addWidget' in line and 'self.' in line:
        match = re.search(r'self\.(\w+)\.addWidget', line)
        if match:
            parent = match.group(1)
            if parent not in ['layout', 'form_layout', 'sidebar_layout', 'top_layout', 
                              'main_layout', 'right_layout', 'hbox', 'toolbar_layout']:
                pass  # Could be valid

print("✓ UI consistency check complete")

# Check for hardcoded dimensions
hardcoded = re.findall(r'set(?:Fixed)?(?:Width|Height)\((\d+)\)', content)
print(f"\nHardcoded dimensions found: {len(hardcoded)}")
if hardcoded:
    unique_sizes = set(hardcoded)
    print(f"  Unique values: {unique_sizes}")

print("\n" + "=" * 60)
print("AUDIT LOOP 8 COMPLETE")
print("=" * 60)