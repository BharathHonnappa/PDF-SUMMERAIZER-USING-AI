from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime
import re
import os

class StructuredSummaryPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom styles for structured PDF"""
        
        # Title Style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Section Header Style
        self.section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=16,
            textColor=colors.HexColor('#3498db'),
            fontName='Helvetica-Bold',
            leftIndent=0
        )
        
        # Key Topics Style
        self.key_topic_style = ParagraphStyle(
            'KeyTopic',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            leftIndent=20,
            bulletIndent=10,
            textColor=colors.HexColor('#2c3e50'),
            fontName='Helvetica'
        )
        
        # Main Content Style
        self.content_style = ParagraphStyle(
            'MainContent',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            spaceBefore=6,
            textColor=colors.HexColor('#34495e'),
            fontName='Helvetica',
            alignment=TA_JUSTIFY,
            leftIndent=0,
            rightIndent=0
        )
        
        # Statistics Style
        self.stats_style = ParagraphStyle(
            'Statistics',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.HexColor('#7f8c8d'),
            fontName='Helvetica',
            alignment=TA_LEFT
        )
        
        # Footer Style
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#95a5a6'),
            fontName='Helvetica-Oblique',
            alignment=TA_CENTER
        )

    def parse_structured_summary(self, summary_text):
        """Parse the structured summary text into components"""
        lines = summary_text.split('\n')
        
        parsed_summary = {
            'title': '',
            'key_topics': [],
            'content_header': '',
            'main_content': [],
            'footer': ''
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect title (usually the first substantial line)
            if 'AI DOCUMENT SUMMARY' in line:
                parsed_summary['title'] = line.replace('', '').replace('=', '').strip()
                current_section = 'title'
            
            # Detect key topics section
            elif 'KEY TOPICS:' in line:
                current_section = 'key_topics'
                continue
            
            # Detect footer
            elif 'Generated using' in line:
                parsed_summary['footer'] = line
                current_section = 'footer'
            
            # Parse content based on current section
            elif current_section == 'key_topics' and line.startswith('•'):
                topic = line.replace('•', '').strip()
                parsed_summary['key_topics'].append(topic)
            
            elif current_section == 'main_content' and line:
                # Clean up content lines
                clean_line = line.strip()
                if len(clean_line) > 10:  # Filter out very short lines
                    parsed_summary['main_content'].append(clean_line)
        
        return parsed_summary

    def clean_filename_for_display(self, filename):
        """Clean filename for better display in PDF"""
        # Remove URL encoding
        import urllib.parse
        clean_name = urllib.parse.unquote(filename)
        
        # Remove path if present
        clean_name = os.path.basename(clean_name)
        
        return clean_name

    def create_structured_pdf(self, summary_data, file_info, output_path):
        """Create a beautifully structured PDF"""
        
        try:
            # Create document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72,
                title="AI Document Summary",
                author="AI Document Summarizer Pro"
            )
            
            # Parse the summary text
            parsed_summary = self.parse_structured_summary(summary_data['summary'])
            
            # Build story (content elements)
            story = []
            
            # Title
            if parsed_summary['title']:
                title = Paragraph(parsed_summary['title'], self.title_style)
                story.append(title)
                story.append(Spacer(1, 20))
            
            # Document Information Table
            clean_filename = self.clean_filename_for_display(file_info['filename'])
            
            doc_info_data = [
                ['Source Document:', clean_filename],
                ['File Size:', f"{file_info['size_mb']:.1f} MB"],
                ['Generated:', datetime.now().strftime("%B %d, %Y at %I:%M %p")],
                ['AI Model:', summary_data.get('model_used', 'T5-Small').upper()]
            ]
            
            doc_info_table = Table(doc_info_data, colWidths=[2*inch, 4*inch])
            doc_info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(doc_info_table)
            story.append(Spacer(1, 20))
            
            # Key Topics Section
            if parsed_summary['key_topics']:
                topics_header = Paragraph(" KEY TOPICS", self.section_header_style)
                story.append(topics_header)
                
                for topic in parsed_summary['key_topics']:
                    topic_para = Paragraph(f"• {topic}", self.key_topic_style)
                    story.append(topic_para)
                
                story.append(Spacer(1, 16))
            
            # Content Header
            if parsed_summary['content_header']:
                content_header = Paragraph(parsed_summary['content_header'], self.section_header_style)
                story.append(content_header)
                story.append(Spacer(1, 12))
            
            # Main Content
            for i, content_line in enumerate(parsed_summary['main_content']):
                # Skip very short lines or separators
                if len(content_line.strip()) < 10:
                    continue
                    
                # Format content with proper paragraph structure
                if content_line.strip():
                    # Escape special HTML characters for ReportLab
                    escaped_content = content_line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    content_para = Paragraph(escaped_content, self.content_style)
                    story.append(content_para)
            
            story.append(Spacer(1, 20))
            
            # Statistics Section
            stats_header = Paragraph("SUMMARY STATISTICS", self.section_header_style)
            story.append(stats_header)
            
            stats_data = [
                ['Original Words:', f"{summary_data['original_words']:,}"],
                ['Summary Words:', f"{summary_data['summary_words']:,}"],
                ['Compression Ratio:', f"{summary_data['compression_ratio']:.1f}%"],
                ['Original Sentences:', f"{summary_data['original_sentences']}"],
                ['Summary Sentences:', f"{summary_data['summary_sentences']}"]
            ]
            
            stats_table = Table(stats_data, colWidths=[2*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e3f2fd')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1976d2')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbdefb')),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # Key Topics Statistics (if available)
            if 'key_topics' in summary_data and summary_data['key_topics']:
                topics_stats_header = Paragraph("🔍 IDENTIFIED TOPICS", self.section_header_style)
                story.append(topics_stats_header)
                
                topics_text = ", ".join(summary_data['key_topics'][:10])  # Show up to 10 topics
                topics_para = Paragraph(topics_text, self.content_style)
                story.append(topics_para)
                story.append(Spacer(1, 16))
            
            # Footer
            if parsed_summary['footer']:
                footer_para = Paragraph(parsed_summary['footer'], self.footer_style)
                story.append(footer_para)
            
            # Add generation timestamp
            timestamp_para = Paragraph(
                f"Generated on {datetime.now().strftime('%A, %B %d, %Y at %I:%M:%S %p')}", 
                self.footer_style
            )
            story.append(Spacer(1, 10))
            story.append(timestamp_para)
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error creating structured PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

def save_summary_as_pdf(summary_data, file_info, output_path):
    """Enhanced function to save structured summary as PDF"""
    try:
        generator = StructuredSummaryPDFGenerator()
        return generator.create_structured_pdf(summary_data, file_info, output_path)
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Please install reportlab: pip install reportlab")
        return False
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

# Backward compatibility
class SummaryPDFGenerator:
    """Backward compatibility class"""
    def __init__(self):
        self.generator = StructuredSummaryPDFGenerator()
    
    def create_pdf(self, summary_data, file_info, output_path):
        return self.generator.create_structured_pdf(summary_data, file_info, output_path)

def test_pdf_generation():
    """Test function to verify PDF generation works"""
    test_summary_data = {
        'summary': '''T5-SMALL AI DOCUMENT SUMMARY
========================================

KEY TOPICS:
   • Artificial Intelligence
   • Machine Learning
   • Neural Networks
   • Deep Learning

COMPREHENSIVE SUMMARY

This document covers the fundamentals of artificial intelligence and machine learning. The content explores various neural network architectures and their applications in modern AI systems.

Machine learning algorithms are presented with detailed explanations of supervised, unsupervised, and reinforcement learning approaches. The document also discusses the mathematical foundations underlying these techniques.

     Generated using T5-Small AI Model (100% Offline)''',
        'original_words': 1000,
        'summary_words': 150,
        'compression_ratio': 85.0,
        'original_sentences': 45,
        'summary_sentences': 8,
        'key_topics': ['Artificial Intelligence', 'Machine Learning', 'Neural Networks', 'Deep Learning'],
        'model_used': 't5-small'
    }
    
    test_file_info = {
        'filename': 'test_document.pdf',
        'size_mb': 2.5
    }
    
    return save_summary_as_pdf(test_summary_data, test_file_info, 'test_output.pdf')

# Run test if executed directly
if __name__ == "__main__":
    print("Testing PDF generation...")
    if test_pdf_generation():
        print("PDF generation test successful!")
    else:
        print("PDF generation test failed!")
