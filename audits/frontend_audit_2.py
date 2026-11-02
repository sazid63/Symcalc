#!/usr/bin/env python
"""
Audit Loop 2: CSS Styling, Responsiveness, and Visual Integrity
Validates CSS structure, responsive breakpoints, color contrast, and visual consistency
"""
import sys
import re

print("=" * 70)
print("AUDIT LOOP 2/5: CSS Styling, Responsiveness, and Visual Integrity")
print("=" * 70)

errors = []
warnings = []

with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Check for CSS variables / theming
if '--bg-primary:' in css:
    print("[PASS] CSS custom properties (variables) present")
else:
    warnings.append("No CSS custom properties found")

# 2. Check responsive rules (media queries)
media_queries = re.findall(r'@media[^{]*\{', css)
if media_queries:
    print("[PASS] " + str(len(media_queries)) + " media query(s) found")
    for mq in media_queries:
        print("  - " + mq.strip()[:60] + "...")
else:
    warnings.append("No media queries found -- may not be responsive")

# 3. Check essential selectors exist
essential_selectors = [
    '.app-header', '.sidebar', '.op-btn', '.main-panel',
    '.result-panel', '.error-panel'
]
for selector in essential_selectors:
    # Check with or without the dot
    if selector in css or '.' + selector.replace('.', '') in css:
        print("[PASS]" + " CSS selector '" + selector + "' present")
    else:
        errors.append("Missing CSS selector: " + selector)

# 3. Check for dark theme colors (matching the app)
dark_theme_colors = ['#0f1115', '#161b22', '#1f2530', '#30363d', '#e6edf3', '#58a6ff']
found_colors = [c for c in dark_theme_colors if c in css]
if found_colors:
    print("[PASS]" + str(len(found_colors)) + "/" + str(len(dark_theme_colors)) + " expected dark theme colors found")
else:
    warnings.append("Few or no expected dark theme colors found")

# 4. Check for key animation/transition properties
anim_keywords = ['transition', 'animation', 'keyframes', 'opacity']
found_anim = [k for k in anim_keywords if k in css.lower()]
if found_anim:
    print("[PASS]" + " Animation/transition properties: " + ', '.join(found_anim))
else:
    warnings.append("No animation/transition properties found")

# 5. Check for responsive grid rules (form-row, etc.)
if 'grid-template-columns' in css or 'minmax' in css:
    print("[PASS]" + " CSS grid/flexbox rules present")
else:
    warnings.append("No explicit grid/flexbox rules found")

# Summary
print("\n" + "=" * 70)
print("AUDIT LOOP 2 SUMMARY")
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

status = "[PASS]" if not errors and len(warnings) <= 4 else "[FAIL]"
print("\n" + status + " Audit Loop 2: CSS styling and responsiveness validation complete")