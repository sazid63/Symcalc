#!/usr/bin/env python
"""Quick test of the main app components"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel

app = QApplication(sys.argv)
app.setStyle("Fusion")

window = QMainWindow()
window.setWindowTitle("Test")
window.resize(800, 600)

central = QWidget()
layout = QVBoxLayout(central)
layout.addWidget(QLabel("Test window works"))
window.setCentralWidget(central)

window.show()
print("Window shown")
app.exec()
print("App exited")