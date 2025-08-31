# components.py - Fixed and Integrated Version

from PyQt5.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFrame, QTextEdit, QComboBox, QCheckBox, QTabWidget, QWidget
)
class NoScrollComboBox(QComboBox):
    """QComboBox that ignores mouse wheel scrolling."""
    def wheelEvent(self, event):
        event.ignore()
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication
app = QApplication([])
app.setStyleSheet("QWidget { margin: 0; padding: 0; }")


# Unified styling constants
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

FRAME_STYLE = """
    QFrame {
        background-color: #ffffff;
        border: none;
        border-radius: 4px;
        margin: 10px 0px;
        padding: 8px;
    }
"""

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
"""

class HeaderComponent:
    """Component for creating the application header."""
    
    @staticmethod
    def create_header(layout):
        """Create and add header section to the layout."""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #00afef;
                border: none;
                border-radius: 4px;
                margin-bottom: 20px;
                padding: 8px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 8, 8, 8)
        header_layout.setSpacing(6)
        
        # Main title
        header = QLabel("AI Document Summarizer")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Georgia", 24, QFont.Bold))
        header.setStyleSheet("color: #ffffff; background: transparent; margin-bottom: 5px;")
        
        # Subtitle
        subtitle = QLabel("Transform lengthy documents into concise, meaningful summaries")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Georgia", 12))
        subtitle.setStyleSheet("color: #ffffff; background: transparent; margin-top: 5px;")
        
        header_layout.addWidget(header)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        return header, subtitle


class FileSelectionComponent:
    """Component for file selection functionality."""
    
    def __init__(self, parent):
        self.parent = parent
        
    def create_file_section(self, layout):
        """Create file selection section."""
        file_frame = QFrame()
        file_frame.setStyleSheet(FRAME_STYLE)
        
        file_layout = QVBoxLayout(file_frame)
        file_layout.setContentsMargins(8, 8, 8, 8)
        file_layout.setSpacing(6)
        
        # Section header
        file_label = QLabel("Select Documents")
        file_label.setFont(QFont("Georgia", 16, QFont.Bold))
        file_label.setAlignment(Qt.AlignCenter)
        file_label.setStyleSheet("color: #333333; margin-bottom: 15px; font-weight: bold;")
        
        # Browse button
        browse_btn = self._create_browse_button()
        button_layout = self._create_centered_layout(browse_btn)
        
        # File info display
        file_info = self._create_file_info_label()
        
        # Current processing file display (hidden by default)
        current_file_label, current_file_display = self._create_current_file_display()
        
        # Add widgets to layout
        file_layout.addWidget(file_label)
        file_layout.addLayout(button_layout)
        file_layout.addWidget(file_info)
        file_layout.addWidget(current_file_label)
        file_layout.addWidget(current_file_display)
        
        layout.addWidget(file_frame)
        
        return browse_btn, file_info, current_file_label, current_file_display
    
    def _create_browse_button(self):
        """Create the browse files button."""
        browse_btn = QPushButton("Browse Multiple Files")
        browse_btn.setMinimumHeight(45)
        browse_btn.setMinimumWidth(200)
        browse_btn.setStyleSheet(BUTTON_STYLE)
        return browse_btn
    
    def _create_centered_layout(self, widget):
        """Create a centered horizontal layout with the given widget."""
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(widget)
        layout.addStretch()
        return layout
    
    def _create_file_info_label(self):
        """Create the file information display label."""
        file_info = QLabel("No files selected")
        file_info.setAlignment(Qt.AlignCenter)
        file_info.setFont(QFont("Georgia", 10))
        file_info.setStyleSheet("""
            color: #333333;
            padding: 10px;
            font-style: italic;
            font-weight: normal;
        """)
        return file_info
    
    def _create_current_file_display(self):
        """Create labels for showing current processing file."""
        current_file_label = QLabel("Currently Processing:")
        current_file_label.setFont(QFont("Georgia", 11, QFont.Bold))
        current_file_label.setAlignment(Qt.AlignCenter)
        current_file_label.setStyleSheet("color: #e74c3c; margin-top: 10px;")
        current_file_label.setVisible(False)
        
        current_file_display = QLabel("")
        current_file_display.setAlignment(Qt.AlignCenter)
        current_file_display.setFont(QFont("Georgia", 10))
        current_file_display.setStyleSheet("""
            color: #e74c3c; 
            font-weight: bold; 
            background-color: #fdf2e9; 
            padding: 8px; 
            border-radius: 4px;
            border: 1px solid #f39c12;
            margin: 5px;
        """)
        current_file_display.setVisible(False)
        
        return current_file_label, current_file_display


class SettingsComponent:
    """Component for AI model and summary settings."""
    
    def __init__(self, parent):
        self.parent = parent
        
    def create_settings_section(self, layout):
        """Create settings configuration section."""
        settings_frame = QFrame()
        settings_frame.setStyleSheet(FRAME_STYLE)
        
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setContentsMargins(8, 8, 8, 8)
        settings_layout.setSpacing(6)   
        
        # Section header
        settings_label = QLabel("AI Model & Summary Configuration")
        settings_label.setFont(QFont("Georgia", 16, QFont.Bold))
        settings_label.setAlignment(Qt.AlignCenter)
        settings_label.setStyleSheet("color: #333333; margin: 0; font-weight: bold;")
        
        # Model selection
        model_selector, connection_status = self._create_model_selection()
        
        # Detail level selection
        detail_selector, detail_display = self._create_detail_selection()
        
        # Add all components to layout
        settings_layout.addWidget(settings_label)
        settings_layout.addWidget(self._create_section_label("AI Model Selection:"))
        settings_layout.addWidget(model_selector)
        settings_layout.addWidget(connection_status)
        settings_layout.addWidget(self._create_section_label("Summary Detail Level:", margin_top=8))
        settings_layout.addWidget(detail_selector)
        settings_layout.addWidget(detail_display)
        settings_layout.setSpacing(2)  # small gap between items
        settings_layout.setContentsMargins(5, 5, 5, 5)  # tiny padding around edges

        layout.addWidget(settings_frame)
        
        return detail_selector, detail_display, model_selector, connection_status
    
    def _create_section_label(self, text, margin_top=10):
        """Create a section label with consistent styling."""
        label = QLabel(text)
        label.setFont(QFont("Georgia", 12, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"color: #333333; margin: {margin_top}px 0 5px 0; font-weight: bold;")
        return label
    
    def _create_model_selection(self):
        """Create model selection dropdown and status."""
        model_selector = NoScrollComboBox()
        model_selector.addItems([
            "T5-Small (Offline - Fast & Reliable)",
            "HuggingFace Transformers (Online - Advanced)"
        ])
        model_selector.setCurrentIndex(0)
        model_selector.setFont(QFont("Georgia", 10))
        model_selector.setStyleSheet(COMBO_STYLE)
        
        connection_status = QLabel("Status: Offline Mode Active")
        connection_status.setAlignment(Qt.AlignCenter)
        connection_status.setFont(QFont("Georgia", 10))
        connection_status.setStyleSheet("""
            color: #27ae60; 
            font-weight: bold; 
            margin: 8px 0;
            padding: 5px;
            background-color: #d5f4e6;
            border-radius: 4px;
        """)
        
        return model_selector, connection_status
    
    def _create_detail_selection(self):
        """Create detail level selection dropdown and display."""
        detail_selector = NoScrollComboBox()
        detail_selector.addItems([
            "High Detail - Comprehensive Analysis",
            "Medium Detail - Balanced Overview",
            "Low Detail - Key Points Only"
        ])
        detail_selector.setCurrentIndex(1)  # Default to medium
        detail_selector.setFont(QFont("Georgia", 10))
        detail_selector.setStyleSheet(COMBO_STYLE)
        
        detail_display = QLabel("Medium Detail - Balanced Overview")
        detail_display.setAlignment(Qt.AlignCenter)
        detail_display.setFont(QFont("Georgia", 10))
        detail_display.setStyleSheet("""
            color: #333333; 
            font-style: italic; 
            margin-top: 8px;
            padding: 5px;
            font-weight: normal;
        """)
        
        return detail_selector, detail_display


class LimitationsComponent:
    """Component for displaying application limitations and notes."""
    
    @staticmethod
    def create_limitations_section(layout):
        """Create limitations/notes section."""
        limitations_frame = QFrame()
        limitations_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: none;
                border-radius: 4px;
                margin: 10px 0px;
                padding: 15px;
            }
        """)
        
        limitations_layout = QVBoxLayout(limitations_frame)
        limitations_layout.setContentsMargins(8, 8, 8, 8)
        limitations_layout.setSpacing(6)
        
        # Section header
        note_label = QLabel("Important Notes")
        note_label.setFont(QFont("Georgia", 14, QFont.Bold))
        note_label.setAlignment(Qt.AlignCenter)
        note_label.setStyleSheet("color: #333333; margin-bottom: 10px; font-weight: bold;")
        
        # Limitations text
        limitations_text = QLabel(
            "• Offline T5 model works best with files under 10MB\n"
            "• Processing may be slower for very large documents\n"
            "• Online mode requires internet connection and API key\n"
            "• Supported formats: PDF, TXT, and other text-based files"
        )
        limitations_text.setFont(QFont("Georgia", 10))
        limitations_text.setAlignment(Qt.AlignLeft)
        limitations_text.setStyleSheet("color: #333333; line-height: 1.4; font-weight: normal;")
        limitations_text.setWordWrap(True)
        
        limitations_layout.addWidget(note_label)
        limitations_layout.addWidget(limitations_text)
        
        layout.addWidget(limitations_frame)
        
        return limitations_frame


class SummaryComponent:
    @staticmethod
    def create_summary_section():
        """Create visible and properly sized summary section"""
        summary_widget = QFrame()
        summary_widget.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: none;
                border-radius: 4px;
                margin: 10px 0px;
                min-height: 400px;
                padding: 15px;
            }
        """)
        summary_layout = QVBoxLayout(summary_widget)
        summary_layout.setContentsMargins(8, 8, 8, 8)
        summary_layout.setSpacing(6)
        
        # Summary header (thin underline style)
        summary_header = QLabel("Generated Summary")
        summary_header.setFont(QFont("Georgia", 16, QFont.Bold))
        summary_header.setAlignment(Qt.AlignLeft)  # left aligned looks cleaner
        summary_header.setStyleSheet("""
            color: #00afef;
            margin-bottom: 8px;
            padding-bottom: 4px;
            border-bottom: 2px solid #00afef;
        """)
        summary_layout.addWidget(summary_header)
        
        # Summary text area
        summary_text = QTextEdit()
        summary_text.setMinimumHeight(150)   # reduced height
        summary_text.setMaximumHeight(300)   # cap height
        summary_text.setPlaceholderText("Your structured summary will appear here...")
        summary_text.setFont(QFont("Georgia", 12))
        summary_text.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #00afef;   /* blue border */
                border-radius: 4px;
                padding: 8px;
                color: #333333;
                font-size: 13px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border: 1px solid #0077aa;   /* darker blue on focus */
            }
        """)
        summary_layout.addWidget(summary_text)

        summary_widget.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
                margin: 0;
                padding: 0;
            }
        """)


        # Summary statistics (compact row style)
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 3px;
                padding: 6px;
                margin-top: 10px;
            }
        """)
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(8, 8, 8, 8)
        stats_layout.setSpacing(6)
        
        compression_stat = QLabel("Compression: 0%")
        compression_stat.setFont(QFont("Georgia", 10))
        compression_stat.setStyleSheet("color: #555555;")
        
        word_count_stat = QLabel("Words: 0 → 0")
        word_count_stat.setFont(QFont("Georgia", 10))
        word_count_stat.setStyleSheet("color: #555555;")
        
        key_topics_stat = QLabel("Topics: None")
        key_topics_stat.setFont(QFont("Georgia", 10))
        key_topics_stat.setStyleSheet("color: #555555;")
        
        stats_layout.addWidget(compression_stat)
        stats_layout.addStretch()
        stats_layout.addWidget(word_count_stat)
        stats_layout.addStretch()
        stats_layout.addWidget(key_topics_stat)
        
        summary_layout.addWidget(stats_frame)
        
        return summary_widget, summary_text, compression_stat, word_count_stat, key_topics_stat



class TabbedSummaryComponent:
    """Component for tabbed summary display with multiple models."""
    
    @staticmethod
    def create_tabbed_summary():
        """Create tabbed interface for multiple model summaries."""
        tabs_widget = QTabWidget()
        tabs_widget.setStyleSheet("""
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
        """)
        tabs_widget.setVisible(False)  # Hidden by default
        
        return tabs_widget

    @staticmethod
    def create_summary_tab(title="Summary"):
        """Create individual summary tab content."""
        tab_widget = QWidget()
        tab_layout = QVBoxLayout(tab_widget)
        tab_layout.setContentsMargins(8, 8, 8, 8)
        tab_layout.setSpacing(6)
        
        # Summary text area
        summary_text = QTextEdit()
        summary_text.setMinimumHeight(400)
        summary_text.setPlaceholderText("Summary will appear here...")
        summary_text.setFont(QFont("Georgia", 11))
        summary_text.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 12px;
                color: #333333;
                font-size: 13px;
                line-height: 1.6;
            }
            QTextEdit:focus {
                border-color: #00afef;
            }
        """)
        
        # Statistics layout
        stats_result = TabbedSummaryComponent._create_tab_stats()
        stats_layout = stats_result['layout']
        compression_stat, word_count_stat, topics_stat = stats_result['widgets']
        
        # Export button
        export_layout = QHBoxLayout()
        export_btn = QPushButton(f"Export {title} to PDF")
        export_btn.setStyleSheet(BUTTON_STYLE)
        export_btn.setFont(QFont("Georgia", 10, QFont.Bold))
        export_btn.setMinimumHeight(35)
        
        export_layout.addStretch()
        export_layout.addWidget(export_btn)
        export_layout.addStretch()
        
        # Add to tab layout
        tab_layout.addWidget(summary_text)
        tab_layout.addLayout(stats_layout)
        tab_layout.addLayout(export_layout)
        
        return tab_widget, summary_text, compression_stat, word_count_stat, topics_stat, export_btn
    
    @staticmethod
    def _create_tab_stats():
        """Create statistics layout for tab content."""
        stats_layout = QHBoxLayout()
        
        compression_stat = QLabel("Compression: 0%")
        compression_stat.setFont(QFont("Georgia", 10, QFont.Bold))
        compression_stat.setStyleSheet("color: #333333; padding: 5px; font-weight: bold;")
        
        word_count_stat = QLabel("Words: 0 → 0")
        word_count_stat.setFont(QFont("Georgia", 10, QFont.Bold))
        word_count_stat.setStyleSheet("color: #333333; padding: 5px; font-weight: bold;")
        
        topics_stat = QLabel("Topics: None")
        topics_stat.setFont(QFont("Georgia", 10, QFont.Bold))
        topics_stat.setStyleSheet("color: #333333; padding: 5px; font-weight: bold;")
        
        stats_layout.addWidget(compression_stat)
        stats_layout.addStretch()
        stats_layout.addWidget(word_count_stat)
        stats_layout.addStretch()
        stats_layout.addWidget(topics_stat)
        
        return {
            'layout': stats_layout,
            'widgets': (compression_stat, word_count_stat, topics_stat)
        }


class ExportComponent:
    """Component for export functionality."""
    
    @staticmethod
    def create_export_section():
        """Create export button section."""
        export_container = QHBoxLayout()
        
        export_btn = QPushButton("Save as PDF")
        export_btn.setStyleSheet(BUTTON_STYLE)
        export_btn.setFont(QFont("Georgia", 12, QFont.Bold))
        export_btn.setMinimumHeight(40)
        export_btn.setVisible(False)  # Hidden until summary is generated
        
        export_container.addStretch()
        export_container.addWidget(export_btn)
        export_container.addStretch()
        
        return export_container, export_btn


# Utility functions for common UI operations
class UIUtils:
    """Utility functions for common UI operations."""
    
    @staticmethod
    def create_centered_button(text, style=BUTTON_STYLE, min_height=45, min_width=200):
        """Create a centered button with consistent styling."""
        button = QPushButton(text)
        button.setStyleSheet(style)
        button.setMinimumHeight(min_height)
        button.setMinimumWidth(min_width)
        
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(button)
        layout.addStretch()
        
        return button, layout
    
    @staticmethod
    def create_info_label(text, color="#333333", font_size=10, italic=True):
        """Create an info label with consistent styling."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Georgia", font_size))
        
        style = f"color: {color}; padding: 10px; font-weight: normal;"
        if italic:
            style += " font-style: italic;"
        
        label.setStyleSheet(style)
        return label
    
    @staticmethod
    def create_section_header(text, font_size=16):
        """Create a section header with consistent styling."""
        header = QLabel(text)
        header.setFont(QFont("Georgia", font_size, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #333333; margin-bottom: 15px; font-weight: bold;")
        return header