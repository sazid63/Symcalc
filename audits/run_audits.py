#!/usr/bin/env python
"""
Run all 10 audit loops - Windows UTF-8 compatible version
"""
import sys
import subprocess
import io
import os

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Project root is the parent of the audits/ directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("CALCAS AUDIT SYSTEM - Running 10 Audit Loops")
print("=" * 70)

audit_scripts = [
    'audit_loop_1.py',
    'audit_loop_2.py',
    'audit_loop_3.py',
    'audit_loop_4.py',
    'audit_loop_5.py',
    'audit_loop_6.py',
    'audit_loop_7.py',
    'audit_loop_8.py',
    'audit_loop_9.py',
    'audit_loop_10.py',
]

passed = 0
failed = 0

for i, script in enumerate(audit_scripts, 1):
    script_path = os.path.join(PROJECT_ROOT, 'audits', script)
    print(f"\n{'='*70}")
    print(f"Starting Audit Loop {i}/10: {script}")
    print('='*70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=PROJECT_ROOT,
            env={**subprocess.os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONPATH': PROJECT_ROOT}
        )
        print(result.stdout)
        if result.returncode != 0:
            if result.stderr:
                print(f"STDERR: {result.stderr[:500]}")
            failed += 1
        else:
            passed += 1
    except Exception as e:
        print(f"Error running {script}: {e}")
        failed += 1

print("\n" + "=" * 70)
print(f"AUDIT SUMMARY: {passed} passed, {failed} failed out of 10 loops")
print("=" * 70)

if failed == 0:
    print("\n[OK] ALL AUDITS PASSED - Calculas is ready for use!")
else:
    print(f"\n[WARN] {failed} audit(s) failed - review output above")