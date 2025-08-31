# styles.py - Unified Styling Configuration

# Main application theme - Clean Cyan & White
MAIN_STYLE = """
    QMainWindow {
        background-color: #ffffff;
        color: #333333;
    }
    QLabel {
        color: #333333;
        font-weight: normal;
        font-family: Georgia, serif;
    }
    QPushButton {
        background-color: #00afef;
        color: #ffffff;
        border: none;
        padding: 12px 24px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 14px;
        font-family: Georgia, serif;
    }
    QPushButton:hover {
        background-color: #0099d4;
    }
    QPushButton:pressed {
        background-color: #007bb8;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #666666;
    }
    QTextEdit {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 12px;
        color: #333333;
        font-size: 13px;
        font-family: Georgia, serif;
    }
    QTextEdit:focus {
        border-color: #00afef;
    }
    QComboBox {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 8px;
        background-color: white;
        color: #333333;
        min-height: 24px;
        font-family: Georgia, serif;
    }
    QComboBox:focus {
        border-color: #00afef;
    }
    QFrame {
        background-color: #ffffff;
        border: none;
        border-radius: 4px;
    }
    QScrollArea {
        border: none;
        background-color: #ffffff;
    }
    QScrollBar:vertical {
        background-color: #f5f5f5;
        width: 12px;
        border: none;
    }
    QScrollBar::handle:vertical {
        background-color: #00afef;
        border-radius: 6px;
        margin: 2px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #0099d4;
    }
"""

# Button styles
BUTTON_STYLE = """
    QPushButton {
        background-color: #00afef;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 14px;
        font-family: Georgia, serif;
    }
    QPushButton:hover {
        background-color: #0099d4;
    }
    QPushButton:pressed {
        background-color: #007bb8;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #666666;
    }
"""

PRIMARY_BUTTON_STYLE = """
    QPushButton {
        background-color: #00afef;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 15px 30px;
        font-weight: bold;
        font-size: 16px;
        font-family: Georgia, serif;
    }
    QPushButton:hover {
        background-color: #0099d4;
    }
    QPushButton:pressed {
        background-color: #007bb8;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #666666;
    }
"""

SECONDARY_BUTTON_STYLE = """
    QPushButton {
        background-color: #6c757d;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 12px;
        font-family: Georgia, serif;
    }
    QPushButton:hover {
        background-color: #5a6268;
    }
    QPushButton:pressed {
        background-color: #495057;
    }
"""

DANGER_BUTTON_STYLE = """
    QPushButton {
        background-color: #e74c3c;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 12px;
        font-family: Georgia, serif;
    }
    QPushButton:hover {
        background-color: #c0392b;
    }
    QPushButton:pressed {
        background-color: #a93226;
    }
"""

# Frame and container styles
FRAME_STYLE = """
    QFrame {
        background-color: #ffffff;
        border: none;
        border-radius: 4px;
        margin: 10px 0px;
        padding: 15px;
    }
"""

CARD_STYLE = """
    QFrame {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 4px;
        margin: 8px 4px;
        padding: 15px;
    }
"""

HEADER_CARD_STYLE = """
    QFrame {
        background-color: #00afef;
        border: none;
        border-radius: 4px;
        margin-bottom: 20px;
        padding: 20px;
    }
"""

NOTES_CARD_STYLE = """
    QFrame {
        background-color: #f8f9fa;
        border: none;
        border-radius: 4px;
        margin: 10px 0px;
        padding: 15px;
    }
"""

WARNING_CARD_STYLE = """
    QFrame {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 4px;
        margin: 10px 0px;
        padding: 15px;
    }
"""

# Text and label styles
HEADER_STYLE = """
    color: #ffffff; 
    margin-bottom: 15px; 
    font-weight: bold; 
    background: transparent;
    font-family: Georgia, serif;
"""

SUBTITLE_STYLE = """
    color: #ffffff; 
    margin-bottom: 20px; 
    font-size: 12px; 
    font-weight: normal;
    background: transparent;
    font-family: Georgia, serif;
"""

SECTION_HEADER_STYLE = """
    color: #333333; 
    margin-bottom: 15px; 
    font-weight: bold;
    background: transparent;
    font-family: Georgia, serif;
"""

BODY_TEXT_STYLE = """
    color: #333333; 
    font-weight: normal;
    background: transparent;
    font-family: Georgia, serif;
"""

FILE_INFO_DEFAULT_STYLE = """
    color: #333333; 
    font-style: italic; 
    font-weight: normal;
    padding: 10px;
    background: transparent;
    font-family: Georgia, serif;
"""

FILE_INFO_SELECTED_STYLE = """
    color: #27ae60;
    font-weight: bold;
    background-color: #d5f4e6;
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid #27ae60;
    font-family: Georgia, serif;
"""

CURRENT_FILE_STYLE = """
    color: #e74c3c;
    font-weight: bold;
    background-color: #fdf2e9;
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid #f39c12;
    text-align: center;
    font-family: Georgia, serif;
"""

STATUS_SUCCESS_STYLE = """
    color: #27ae60; 
    font-weight: bold; 
    margin: 8px 0;
    padding: 5px 8px;
    background-color: #d5f4e6;
    border-radius: 4px;
    font-family: Georgia, serif;
"""

STATUS_WARNING_STYLE = """
    color: #e74c3c; 
    font-weight: bold; 
    margin: 8px 0;
    padding: 5px 8px;
    background-color: #fdf2e9;
    border-radius: 4px;
    font-family: Georgia, serif;
"""

STATUS_INFO_STYLE = """
    color: #00afef; 
    font-weight: bold; 
    margin: 8px 0;
    padding: 5px 8px;
    background-color: #e3f2fd;
    border-radius: 4px;
    font-family: Georgia, serif;
"""

# Input and control styles
COMBO_STYLE = """
    QComboBox {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 8px;
        background-color: white;
        color: #333333;
        min-height: 24px;
        font-family: Georgia, serif;
    }
    QComboBox:focus {
        border-color: #00afef;
    }
    QComboBox::drop-down {
        width: 30px;
        border: none;
    }
    QComboBox::down-arrow {
        width: 12px;
        height: 12px;
    }
    QComboBox::item {
        color: #333333;
        background-color: white;
        padding: 8px;
    }
    QComboBox::item:selected {
        background-color: #e3f2fd;
        color: #00afef;
    }
"""

TEXT_EDIT_STYLE = """
    QTextEdit {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 12px;
        color: #333333;
        font-size: 13px;
        font-family: Georgia, serif;
        line-height: 1.6;
    }
    QTextEdit:focus {
        border-color: #00afef;
    }
"""

# Progress and loading styles
PROGRESS_BAR_STYLE = """
    QProgressBar {
        border: none;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 4px;
        text-align: center;
        color: white;
        min-height: 25px;
        font-weight: bold;
        font-family: Georgia, serif;
    }
    QProgressBar::chunk {
        background-color: white;
        border-radius: 4px;
    }
"""

OVERLAY_STYLE = """
    QFrame {
        background-color: rgba(0, 175, 239, 0.9);
        border: none;
        border-radius: 8px;
    }
"""

# Summary and statistics styles
SUMMARY_FRAME_STYLE = """
    QFrame {
        background-color: #ffffff;
        border: none;
        border-radius: 4px;
        margin: 10px 0px;
        min-height: 400px;
        padding: 15px;
    }
"""

SUMMARY_HEADER_STYLE = """
    color: #ffffff; 
    margin-bottom: 8px;
    padding: 12px;
    background-color: #00afef;
    border-radius: 4px;
    font-weight: bold;
    font-family: Georgia, serif;
"""

STATS_FRAME_STYLE = """
    QFrame {
        background-color: #f8f9fa;
        border: none;
        border-radius: 4px;
        padding: 10px;
        margin-top: 10px;
    }
"""

STAT_LABEL_STYLE = """
    color: #333333; 
    padding: 8px; 
    font-weight: bold;
    background: transparent;
    font-family: Georgia, serif;
"""

# Tab styles
TAB_WIDGET_STYLE = """
    QTabWidget::pane {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        background-color: #ffffff;
        margin-top: 10px;
    }
    QTabWidget::tab-bar {
        alignment: center;
    }
    QTabBar::tab {
        background-color: #f8f9fa;
        color: #333333;
        border: 1px solid #e0e0e0;
        padding: 12px 20px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        font-family: Georgia, serif;
        font-weight: bold;
        font-size: 11pt;
        min-width: 120px;
    }
    QTabBar::tab:selected {
        background-color: #00afef;
        color: white;
        border-color: #00afef;
    }
    QTabBar::tab:hover {
        background-color: #0099d4;
        color: white;
    }
"""

# Scrollbar styles
SCROLLBAR_STYLE = """
    QScrollBar:vertical {
        background-color: #f5f5f5;
        width: 12px;
        border: none;
    }
    QScrollBar::handle:vertical {
        background-color: #00afef;
        border-radius: 6px;
        margin: 2px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #0099d4;
    }
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
"""

# Color constants
COLORS = {
    'primary': '#00afef',
    'primary_hover': '#0099d4',
    'primary_pressed': '#007bb8',
    'success': '#27ae60',
    'success_bg': '#d5f4e6',
    'warning': '#f39c12',
    'warning_bg': '#fdf2e9',
    'danger': '#e74c3c',
    'danger_bg': '#fdf2e9',
    'info': '#00afef',
    'info_bg': '#e3f2fd',
    'text': '#333333',
    'text_light': '#6c757d',
    'background': '#ffffff',
    'surface': '#f8f9fa',
    'border': '#e0e0e0',
    'border_light': '#e9ecef'
}