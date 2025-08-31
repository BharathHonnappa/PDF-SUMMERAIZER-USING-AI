# main_window.py - Integrated with Fixed Components

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QMessageBox, QFrame, QPushButton, QLabel, QProgressBar, QFileDialog,
    QTextEdit, QComboBox, QApplication
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
import os
import sys

# Import your components and summarizer
from .components import (
    HeaderComponent, FileSelectionComponent, SettingsComponent,
    LimitationsComponent, SummaryComponent, ExportComponent, UIUtils
)
from utils.summarizer import SummaryWorker, export_to_pdf



class ModernSummarizerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_properties()
        self._init_window()
        self.setup_ui()

    def _init_properties(self):
        """Initialize application properties"""
        self.is_processing = False
        self.worker = None
        self.selected_files = []
        self.current_file_index = 0
        self.all_summaries = []
        self.selected_detail_ratio = 0.8
        self.is_online_mode = False
        self.selected_model = "t5-small"

    def _init_window(self):
        """Initialize window properties"""
        self.setWindowTitle("AI Document Summarizer")
        self.setGeometry(150, 150, 900, 800)
        self.setMinimumSize(800, 600)

        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')))

        
        # Set main window styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
                color: #333333;
            }
        """)

    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
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
                background-color: #a0c9d9;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0c9d9;
            }
        """)

        
        # Content frame
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background-color: #ffffff; border: none;")
        
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(10)
        
        self._setup_components()
        scroll_area.setWidget(self.content_frame)
        main_layout.addWidget(scroll_area)
       
        self._setup_processing_overlay()

    def _setup_components(self):
        """Setup all UI components using the component classes"""
        # Header
        self.header, self.subtitle = HeaderComponent.create_header(self.content_layout)
        
        # File selection
        file_component = FileSelectionComponent(self)
        file_result = file_component.create_file_section(self.content_layout)
        self.browse_btn, self.file_info, self.current_file_label, self.current_file_display = file_result
        self.browse_btn.clicked.connect(self.browse_files)
        
        # Settings
        settings_component = SettingsComponent(self)
        settings_result = settings_component.create_settings_section(self.content_layout)
        self.detail_selector, self.detail_display, self.model_selector, self.connection_status = settings_result
        
        # Connect settings signals
        self.model_selector.currentTextChanged.connect(self.on_model_changed)
        self.detail_selector.currentTextChanged.connect(self.on_detail_level_changed)
        
        # Limitations/Notes
        LimitationsComponent.create_limitations_section(self.content_layout)
        
        # Generate button
        generate_container = QHBoxLayout()
        self.generate_btn = QPushButton("Generate Smart Summary")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #00afef;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
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
        """)
        self.generate_btn.setFont(QFont("Georgia", 14, QFont.Bold))
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.setMinimumWidth(250)
        self.generate_btn.clicked.connect(self.generate_summary)
        
        generate_container.addStretch()
        generate_container.addWidget(self.generate_btn)
        generate_container.addStretch()
        self.content_layout.addLayout(generate_container)
        
        # Summary section
        summary_result = SummaryComponent.create_summary_section()
        self.summary_widget, self.summary_text, self.compression_stat, self.word_count_stat, self.key_topics_stat = summary_result
        self.summary_widget.setVisible(False)
        self.content_layout.addWidget(self.summary_widget)
        
        # Export button
        export_container, self.export_btn = ExportComponent.create_export_section()
        self.export_btn.clicked.connect(self.export_to_pdf)
        self.content_layout.addLayout(export_container)

    def _setup_processing_overlay(self):
        """Setup processing overlay for visual feedback"""
        self.processing_overlay = QFrame(self)
        self.processing_overlay.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 175, 239, 0.9);
                border: none;
                border-radius: 8px;
            }
        """)
        self.processing_overlay.setVisible(False)
        
        overlay_layout = QVBoxLayout(self.processing_overlay)
        overlay_layout.setAlignment(Qt.AlignCenter)
        
        self.processing_label = QLabel("Processing Document...")
        self.processing_label.setFont(QFont("Georgia", 16, QFont.Bold))
        self.processing_label.setStyleSheet("color: white; background: transparent;")
        self.processing_label.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                text-align: center;
                color: white;
                min-height: 25px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: white;
                border-radius: 4px;
            }
        """)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.cancel_btn.clicked.connect(self.cancel_processing)
        
        overlay_layout.addWidget(self.processing_label)
        overlay_layout.addWidget(self.progress_bar)
        overlay_layout.addWidget(self.cancel_btn)

    # Event handlers
    def browse_files(self):
        """Handle file browsing"""
        if self.is_processing:
            return
            
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Documents", "", 
            "PDF files (*.pdf);;Text files (*.txt);;All files (*.*)"
        )
        
        if file_paths:
            self._process_selected_files(file_paths)

    def _process_selected_files(self, file_paths):
        """Process the selected files and update UI"""
        self.selected_files = []
        total_size = 0
        
        for file_path in file_paths:
            try:
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                file_name = os.path.basename(file_path)
                total_size += file_size
                
                self.selected_files.append({
                    'filename': file_name,
                    'size_mb': file_size,
                    'path': file_path
                })
            except OSError:
                continue
        
        if self.selected_files:
            self._update_file_display(total_size)

    def _update_file_display(self, total_size):
        """Update the file display information"""
        if len(self.selected_files) == 1:
            file_info = self.selected_files[0]
            text = f"Selected: {file_info['filename']} ({file_info['size_mb']:.1f} MB)"
        else:
            text = f"Selected: {len(self.selected_files)} files ({total_size:.1f} MB total)"
        
        self.file_info.setText(text)
        self.file_info.setStyleSheet("""
            color: #27ae60;
            font-weight: bold;
            background-color: #d5f4e6;
            padding: 8px 12px;
            border-radius: 4px;
            border: 1px solid #27ae60;
        """)

    def on_model_changed(self, model_text):
        """Handle model selection change"""
        if "T5-Small" in model_text:
            self.is_online_mode = False
            self.selected_model = "t5-small"
            self.connection_status.setText("Status: Offline Mode Active")
            self.connection_status.setStyleSheet("""
                color: #27ae60; 
                font-weight: bold; 
                margin: 8px 0;
                padding: 5px;
                background-color: #d5f4e6;
                border-radius: 4px;
            """)
        else:
            self.is_online_mode = True
            self.selected_model = "online"
            self.connection_status.setText("Status: Online Mode - Internet Required")
            self.connection_status.setStyleSheet("""
                color: #e74c3c; 
                font-weight: bold; 
                margin: 8px 0;
                padding: 5px;
                background-color: #fdf2e9;
                border-radius: 4px;
            """)

    def on_detail_level_changed(self, level_text):
        """Handle detail level change"""
        level_mapping = {
            "High Detail - Comprehensive Analysis": 0.7,
            "Medium Detail - Balanced Overview": 0.4,
            "Low Detail - Key Points Only": 0.2
        }
        self.selected_detail_ratio = level_mapping.get(level_text, 0.4)
        self.detail_display.setText(level_text)

    def generate_summary(self):
        """Start the summary generation process"""
        if self.is_processing or not self.selected_files:
            if not self.selected_files:
                QMessageBox.warning(self, "No Files", "Please select files to summarize first.")
            return
        
        self.all_summaries = []
        self.current_file_index = 0
        self._set_processing_state(True)
        self._process_current_file()

    def _process_current_file(self):
        """Process the current file in the queue"""
        if self.current_file_index >= len(self.selected_files):
            self._on_all_files_completed()
            return
        
        current_file = self.selected_files[self.current_file_index]
        self.processing_label.setText(f"Processing: {current_file['filename']}")
        
        # Show current file being processed
        self.current_file_label.setVisible(True)
        self.current_file_display.setVisible(True)
        self.current_file_display.setText(current_file['filename'])
        
        # Create and start worker
        self.worker = SummaryWorker(
            current_file['path'], 
            self.selected_detail_ratio,
            self.selected_model,
            self.is_online_mode
        )
        
        self.worker.finished.connect(self._on_file_finished)
        self.worker.error.connect(self._on_error)
        self.worker.progress.connect(self._on_progress_update)
        self.worker.start()

    def _on_progress_update(self, message):
        """Handle progress updates from worker"""
        self.processing_label.setText(message)

    def _on_file_finished(self, summary_data):
        """Handle completion of a single file"""
        current_file = self.selected_files[self.current_file_index]
        summary_data['source_file'] = current_file
        self.all_summaries.append(summary_data)
        
        self.current_file_index += 1
        
        if self.current_file_index < len(self.selected_files):
            self._process_current_file()
        else:
            self._on_all_files_completed()

    def _on_all_files_completed(self):
        """Handle completion of all files"""
        self._set_processing_state(False)
        
        # Hide current file display
        self.current_file_label.setVisible(False)
        self.current_file_display.setVisible(False)
        
        if self.all_summaries:
            self.summary_widget.setVisible(True)
            self.export_btn.setVisible(True)
            self._display_summary(self.all_summaries[0])
            QTimer.singleShot(300, self._scroll_to_summary)
        else:
            QMessageBox.warning(self, "No Summaries", "No summaries were generated.")

    def _on_error(self, error_message):
        """Handle processing errors"""
        self._set_processing_state(False)
        
        # Hide current file display
        self.current_file_label.setVisible(False)
        self.current_file_display.setVisible(False)
        
        QMessageBox.critical(self, "Processing Error", f"An error occurred:\n{error_message}")

    def _display_summary(self, summary_data):
        """Display the summary results"""
        self.summary_text.setPlainText(summary_data['summary'])
        print(f"Displaying summary of length: {len(summary_data['summary'])}")
        self.compression_stat.setText(f"Compression: {summary_data['compression_ratio']:.1f}%")
        self.word_count_stat.setText(f"Words: {summary_data['original_words']} → {summary_data['summary_words']}")
        
        topics = summary_data.get('key_topics', [])
        if topics:
            self.key_topics_stat.setText(f"Topics: {', '.join(topics[:3])}")
        else:
            self.key_topics_stat.setText("Topics: None identified")

    def _scroll_to_summary(self):
        """Scroll to the summary section"""
        scroll_area = self.centralWidget().findChild(QScrollArea)
        if scroll_area:
            scroll_bar = scroll_area.verticalScrollBar()
            # Scroll to near the bottom to show summary
            scroll_bar.setValue(int(scroll_bar.maximum() * 0.8))

    def cancel_processing(self):
        """Cancel the current processing"""
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
        self._set_processing_state(False)
        
        # Hide current file display
        self.current_file_label.setVisible(False)
        self.current_file_display.setVisible(False)

    def export_to_pdf(self):
        """Export summary to PDF"""
        if not hasattr(self, 'all_summaries') or not self.all_summaries:
            QMessageBox.warning(self, "No Summary", "Please generate a summary first.")
            return

        # Get save location from user
        options = QFileDialog.Options()
        default_name = "AI_Summary.pdf"
        if hasattr(self, 'selected_files') and self.selected_files:
            base_name = os.path.splitext(self.selected_files[0]['filename'])[0]
            default_name = f"Summary_{base_name}.pdf"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Summary as PDF", 
            default_name, 
            "PDF Files (*.pdf)", 
            options=options
        )

        if file_path:
            try:
                # Create printer object
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(file_path)
                printer.setPageSize(QPrinter.A4)
                
                # Create document with formatted content
                doc = QTextDocument()
                
                # Get the summary content and format it nicely
                summary_content = self.summary_text.toPlainText()
                
                # Add some basic formatting
                formatted_content = f"""
<html>
<head>
    <style>
        body {{ 
            font-family: Georgia, serif; 
            font-size: 12pt; 
            line-height: 1.6; 
            margin: 40px; 
            color: #333333;
        }}
        h1 {{ 
            color: #00afef; 
            font-size: 18pt; 
            margin-bottom: 20px; 
            text-align: center;
        }}
        h2 {{ 
            color: #333333; 
            font-size: 14pt; 
            margin-top: 25px; 
            margin-bottom: 10px; 
        }}
        .stats {{ 
            background-color: #f8f9fa; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 20px 0; 
            border: 1px solid #e0e0e0;
        }}
        .stat {{ 
            display: inline-block; 
            margin-right: 30px; 
            font-weight: bold; 
            color: #333333;
        }}
        .content {{
            white-space: pre-line;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <h1>AI Document Summary</h1>
    
    <div class="stats">
        <span class="stat">{self.compression_stat.text()}</span>
        <span class="stat">{self.word_count_stat.text()}</span>
        <span class="stat">{self.key_topics_stat.text()}</span>
    </div>
    
    <h2>Summary Content</h2>
    <div class="content">{summary_content}</div>
    
    <hr style="margin-top: 30px; border: none; border-top: 1px solid #e0e0e0;">
    <p style="text-align: center; font-style: italic; color: #666666;">
        Generated by AI Document Summarizer
    </p>
</body>
</html>
                """
                
                doc.setHtml(formatted_content)
                doc.print_(printer)
                
                QMessageBox.information(self, "Success", f"Summary successfully saved as:\n{file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "PDF Export Error", f"Failed to save PDF:\n{str(e)}")

    def _set_processing_state(self, processing):
        """Set the processing state and update UI accordingly"""
        self.is_processing = processing
        
        # Disable/enable controls
        controls = [self.browse_btn, self.model_selector, self.detail_selector, self.generate_btn]
        for control in controls:
            control.setEnabled(not processing)
        
        if processing:
            self.processing_overlay.setVisible(True)
            self.processing_overlay.resize(self.size())
            self.generate_btn.setText("Processing...")
        else:
            self.processing_overlay.setVisible(False)
            self.generate_btn.setText("Generate Smart Summary")

    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        if hasattr(self, 'processing_overlay'):
            self.processing_overlay.resize(self.size())


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Georgia", 10)
    app.setFont(font)
    
    window = ModernSummarizerUI()
    window.show()
    sys.exit(app.exec_())