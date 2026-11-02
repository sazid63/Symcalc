#!/usr/bin/env python
"""
Audit Loop 1: Web Frontend Structure and Accessibility
Validates HTML5 structure, ARIA labels, semantic elements, and accessibility
"""
import sys
import re

print("=" * 70)
print("AUDIT LOOP 1/5: Web Frontend Structure and Accessibility")
print("=" * 70)

errors = []
warnings = []

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Doctype and lang
if not html.startswith('<!DOCTYPE html>'):
    errors.append("Missing HTML5 doctype")
else:
    print("[PASS] HTML5 doctype present")

if 'lang="en"' not in html:
    errors.append("Missing lang='en' attribute")
else:
    print("[PASS] lang='en' present")

# 2. Required meta tags
checks = {
    'viewport': 'width=device-width, initial-scale=1' in html,
    'theme-color': '#08090d' in html,
    'description': 'University-level calculus problem solver' in html,
}
for tag, present in checks.items():
    if present:
        print("[PASS] <meta " + tag + "> present")
    else:
        warnings.append("Missing <meta " + tag + ">")

# 3. ARIA labels on interactive elements
aria_checks = {
    'mobile-menu-btn': 'aria-label' in html.split('mobile-menu-btn')[1][:80] if 'mobile-menu-btn' in html else False,
    'history-toggle': 'aria-label' in html.split('history-toggle')[1][:80] if 'history-toggle' in html else False,
    'help-toggle': 'aria-label' in html.split('help-toggle')[1][:80] if 'help-toggle' in html else False,
    'copy-btn': 'aria-label' in html.split('copy-btn')[1][:80] if 'copy-btn' in html else False,
    'copy-latex-btn': 'aria-label' in html.split('copy-latex-btn')[1][:80] if 'copy-latex-btn' in html else False,
    'history-clear': 'aria-label' in html.split('history-clear')[1][:80] if 'history-clear' in html else False,
}
for elem, present in aria_checks.items():
    if present:
        print("[PASS]" + elem + " has aria-label")
    else:
        warnings.append(elem + " missing aria-label")

# 3. Landmark regions
if '<header' in html:
    print("[PASS] <header> landmark present")
else:
    errors.append("Missing <header> landmark")

if '<main' in html:
    print("[PASS] <main> landmark present")
else:
    errors.append("Missing <main> landmark")

# 4. Form accessibility
form_checks = {
    'expression textarea has label': 'for="input-expression"' in html or 'aria-label' in html.split('input-expression')[1][:50] if 'input-expression' in html else False,
    'form has autocomplete="off"': 'autocomplete="off"' in html,
}
for check, present in form_checks.items():
    if present:
        print("[PASS]" + check)
    else:
        warnings.append("Missing: " + check)

# 5. Skip links / focus indicators
if 'focus' in html.lower() or 'sr-only' in html.lower():
    print("[PASS] Focus-related content present")
else:
    warnings.append("No visible focus indicators or skip links found")

# Summary
print("\n" + "=" * 70)
print("AUDIT LOOP 1 SUMMARY")
print("=" * 70)

if errors:
    print("\n[FAIL] ERRORS (" + str(len(errors)) + "):")
    for e in errors:
        print("  - " + e)
else:
    print("\n[PASS] No errors found")

if warnings:
    print("\n[WARN] WARNINGS (" + str(len(warnings)) + "):")
    for w in warnings:
        print("  - " + w)
else:
    print("[PASS] No warnings found")

status = "[PASS]" if not errors and len(warnings) <= 3 else "[FAIL]"
print("\n" + status + " Audit Loop 1: Structural and accessibility validation complete")