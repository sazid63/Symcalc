#!/usr/bin/env python
"""Test frontend access"""
import urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with urllib.request.urlopen('http://127.0.0.1:5000/', timeout=10) as r:
    html = r.read().decode('utf-8')
    if '<title>' in html:
        title = html.split('<title>')[1].split('</title>')[0]
        print('Frontend loads successfully:', title)
    else:
        print('Frontend may have issues')