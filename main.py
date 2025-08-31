import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import ModernSummarizerUI

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("AI Document Summarizer Pro")
    app.setApplicationVersion("1.0")
    
    window = ModernSummarizerUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

