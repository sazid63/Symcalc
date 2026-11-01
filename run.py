"""
Calculas - Native Windows Desktop Calculator
Startup wrapper
"""
import sys
import os

# Set UTF-8 mode for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def main():
    """Entry point for the desktop app."""
    try:
        # Quick smoke test
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance() or QApplication(sys.argv)
        app.setStyle("Fusion")
        
        # Import and run
        from main import MainWindow
        window = MainWindow()
        window.show()
        
        print("Calculas started successfully")
        sys.exit(app.exec())
        
    except Exception as e:
        import traceback
        print(f"Error starting Calculas:\n{e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
