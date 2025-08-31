import re
from collections import Counter
import numpy as np
import torch
import warnings
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import os
import sys

# Suppress transformer warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# Set your READ-only token (replace with your actual token)
os.environ['HUGGINGFACEHUB_API_TOKEN'] = "  "    '''<----your api key here'''

# Robust transformers import with fallback
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
    print("✅ Transformers library loaded successfully")
except Exception as e:
    print(f"⚠️ Transformers import failed: {e}")
    TRANSFORMERS_AVAILABLE = False
    pipeline = None

class AIDocumentSummarizer:
    def __init__(self, model_type="t5-small", is_online=False):
        """Initialize with offline/online AI model"""
        self.model_type = model_type
        self.is_online = is_online
        self.summarizer = None
        
        if TRANSFORMERS_AVAILABLE and not is_online:
            self._load_offline_model()
        elif is_online:
            print("🌐 Online mode selected - will use HuggingFace API")
        else:
            print("⚠️ Running in extractive-only mode")
    
    def _load_offline_model(self):
        """Load the offline T5-Small model only"""
        try:
            print("Loading T5-Small model for offline summarization...")
            
            self.summarizer = pipeline(
                "summarization",
                model="t5-small",
                tokenizer="t5-small",
                framework="pt",
                device=-1,  # CPU usage
                clean_up_tokenization_spaces=True
            )
            
            print("✅ T5-Small model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading T5 model: {e}")
            print("Falling back to extractive summarization...")
            self.summarizer = None
    
    def _online_summarize(self, text, summary_ratio):
        """Use HuggingFace online API for summarization"""
        try:
            import requests
            
            # HuggingFace Inference API endpoint
            API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            
            headers = {
                "Authorization": f"Bearer {os.environ.get('HUGGINGFACEHUB_API_TOKEN')}",
                "Content-Type": "application/json"
            }
            
            # Privacy protection: limit text size
            safe_text = text[:1000]  # Truncate for privacy
            
            # Calculate target length
            input_words = len(safe_text.split())
            max_length = max(50, min(500, int(input_words * summary_ratio * 2)))
            min_length = max(20, int(max_length * 0.3))
            
            payload = {
                "inputs": safe_text,
                "parameters": {
                    "max_length": max_length,
                    "min_length": min_length,
                    "do_sample": False
                },
                "options": {
                    "wait_for_model": True,
                    "use_cache": False  # Privacy: don't cache
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result[0]['summary_text']
            else:
                print(f"⚠️ Online API failed: {response.status_code}")
                return self.fallback_extractive_summary(text, summary_ratio)
                
        except Exception as e:
            print(f"⚠️ Online summarization failed: {e}")
            return self.fallback_extractive_summary(text, summary_ratio)
    
    def clean_extracted_text(self, text):
        """Clean and preprocess text"""
        # Fix PDF extraction issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
        text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive whitespace and clean formatting
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if len(line) > 20:  # Filter out short fragments
                cleaned_lines.append(line)
        
        return ' '.join(cleaned_lines)
    
    def chunk_text(self, text, max_chunk_length=800):
        """Split text into manageable chunks for AI processing"""
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
                
            # Check if adding this sentence would exceed the limit
            if len(current_chunk) + len(sentence) > max_chunk_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    # Single sentence is too long, split it
                    chunks.append(sentence[:max_chunk_length])
            else:
                current_chunk += " " + sentence
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            
        return chunks

    def ai_summarize_chunk(self, text_chunk, summary_ratio=0.3):
        """Summarize a single chunk using AI model with optimized token handling"""
        # Use online API if online mode
        if self.is_online:
            return self._online_summarize(text_chunk, summary_ratio)
        
        # Use offline model if available
        if not self.summarizer:
            return self.fallback_extractive_summary(text_chunk, summary_ratio)
            
        try:
            # Calculate optimal token lengths based on input
            input_words = len(text_chunk.split())
            
            # ✅ IMPROVED: Dynamic token calculation based on actual input length
            if summary_ratio <= 0.3:  # Low detail (20%)
                target_ratio = 0.3
            elif summary_ratio <= 0.6:  # Medium detail (40%) 
                target_ratio = 0.5
            else:  # High detail (70%)
                target_ratio = 0.7
            
            # Calculate max tokens based on input length and desired ratio
            max_new_tokens = max(20, min(int(input_words * target_ratio), input_words - 10))
            
            # Ensure we don't exceed input length (fix the warnings)
            max_length = min(max_new_tokens, int(input_words * 0.8))
            min_length = max(10, int(max_length * 0.3))
            
            print(f"📊 Input: {input_words} words → Target: {max_length} tokens (ratio: {target_ratio})")
            
            # T5 requires "summarize:" prefix
            input_text = f"summarize: {text_chunk}"
            
            # ✅ FIXED: Use max_length and min_length instead of max_new_tokens
            summary = self.summarizer(
                input_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True,
                clean_up_tokenization_spaces=True
            )
            
            return summary[0]['summary_text']
            
        except Exception as e:
            print(f"❌ AI summarization failed for chunk: {e}")
            return self.fallback_extractive_summary(text_chunk, summary_ratio)
    
    def fallback_extractive_summary(self, text, summary_ratio=0.3):
        """Fallback extractive summarization if AI fails"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) <= 2:
            return text
            
        # Simple frequency-based extraction
        words = text.lower().split()
        word_freq = Counter(words)
        
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = sum(word_freq.get(word.lower(), 0) for word in sentence.split())
            sentence_scores.append((score, i, sentence))
        
        # Select top sentences
        num_sentences = max(1, int(len(sentences) * summary_ratio))
        top_sentences = sorted(sentence_scores, key=lambda x: x[0], reverse=True)[:num_sentences]
        
        # Sort by original order
        selected = sorted(top_sentences, key=lambda x: x[1])
        
        return ' '.join([s[1] for s in selected])
    
    def extract_key_phrases(self, text, top_n=6):
        """Extract key phrases from text"""
        text = self.clean_extracted_text(text)
        
        # Extract meaningful phrases
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        technical_terms = re.findall(r'\b[a-z]{6,}\b', text.lower())
        
        stop_words = {
            'the', 'this', 'that', 'these', 'those', 'and', 'but', 'or', 'for', 'nor', 
            'on', 'at', 'to', 'from', 'up', 'by', 'with', 'without', 'through', 'over', 
            'under', 'above', 'below', 'example', 'method', 'system', 'information'
        }
        
        all_phrases = capitalized_terms + technical_terms
        phrase_freq = Counter([phrase.lower().strip() for phrase in all_phrases 
                              if phrase.lower().strip() not in stop_words and len(phrase) > 3])
        
        key_phrases = []
        for phrase, freq in phrase_freq.most_common(top_n * 2):
            if freq >= 1 and len(phrase) > 4:
                key_phrases.append(phrase.title())
            if len(key_phrases) >= top_n:
                break
        
        return key_phrases[:top_n]
    
    def _structure_summary_content(self, text):
        """Structure the summary content into readable sections"""
        structured_parts = []
        structured_parts.append("SUMMARY:")
        structured_parts.append("")
        
        # Clean up the text first
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'([A-Z])\s+([A-Z])', r'\1\2', text)  # Fix spaced capitals
        
        # Try to identify different sections based on content
        sections = self._identify_content_sections(text)
        
        for i, section in enumerate(sections, 1):
            if section.strip():
                # Clean and format each section
                clean_section = self._clean_section_text(section)
                if clean_section:
                    structured_parts.append(f"{i}. {clean_section}")
                    structured_parts.append("")
        
        return structured_parts

    def _identify_content_sections(self, text):
        """Identify and separate different content sections"""
        # Try to split into logical sections
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Group sentences into sections (every 3-4 sentences)
        sections = []
        current_section = []
        
        for sentence in sentences:
            current_section.append(sentence)
            if len(current_section) >= 3:  # Create sections of 3 sentences
                sections.append('. '.join(current_section) + '.')
                current_section = []
        
        # Add remaining sentences
        if current_section:
            sections.append('. '.join(current_section) + '.')
        
        return sections[:8]  # Limit to 8 sections max

    def _clean_section_text(self, text):
        """Clean and format individual section text"""
        # Remove excessive spacing and clean up
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common formatting issues
        text = re.sub(r'([a-z])([A-Z])', r'\1. \2', text)  # Add periods between sentences
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)  # Fix spacing after periods
        text = re.sub(r'•\s*', '• ', text)  # Fix bullet points
        
        # Ensure proper capitalization
        if text and not text[0].isupper():
            text = text.upper() + text[1:]
        
        # Ensure proper ending
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def create_structured_summary(self, summary_text, key_phrases, summary_ratio, source_filename=""):
        """Create properly structured and readable summary"""
        summary_parts = []
        
        # Clean header
        model_name = "ONLINE HUGGINGFACE" if self.is_online else "T5-SMALL OFFLINE"
        summary_parts.append(f"AI DOCUMENT SUMMARY - {model_name}")
        summary_parts.append("=" * 60)
        summary_parts.append("")
        
        # Source document
        if source_filename:
            summary_parts.append(f"SOURCE DOCUMENT: {source_filename}")
            summary_parts.append("")
        
        # Key topics section
        if key_phrases:
            summary_parts.append("KEY TOPICS:")
            for phrase in key_phrases[:6]:
                summary_parts.append(f"  • {phrase}")
            summary_parts.append("")
        
        # Detail level
        level_descriptions = {
            0.2: "LOW DETAIL - Key Points Only",
            0.4: "MEDIUM DETAIL - Balanced Overview", 
            0.7: "HIGH DETAIL - Comprehensive Analysis"
        }
        level = level_descriptions.get(summary_ratio, f"DETAIL LEVEL: {int(summary_ratio * 100)}%")
        summary_parts.append(level)
        summary_parts.append("")
        
        # Process and structure the summary content
        if summary_text and summary_text.strip():
            structured_content = self._structure_summary_content(summary_text)
            summary_parts.extend(structured_content)
        else:
            summary_parts.append("SUMMARY:")
            summary_parts.append("Unable to generate summary from the provided document.")
        
        summary_parts.append("")
        summary_parts.append("-" * 50)
        mode_text = "Online HuggingFace API" if self.is_online else "Offline T5-Small Model"
        summary_parts.append(f"Generated using {mode_text}")
        
        return "\n".join(summary_parts)
    
    def summarize(self, text, summary_ratio=0.4, source_filename=""):
        """Main summarization method"""
        original_text = text
        cleaned_text = self.clean_extracted_text(text)
        
        if len(cleaned_text.strip()) < 100:
            return {
                'summary': "Document too short for meaningful AI summarization.",
                'original_sentences': 1,
                'summary_sentences': 1,
                'original_words': len(text.split()),
                'summary_words': 20,
                'compression_ratio': 0,
                'key_topics': [],
                'model_used': 'offline' if not self.is_online else 'online',
                'source_file': source_filename
            }
        
        # Extract key phrases
        key_phrases = self.extract_key_phrases(text)
        
        # Process based on online/offline mode
        mode_text = "ONLINE HUGGINGFACE" if self.is_online else "OFFLINE T5-SMALL"
        
        if self.is_online:
            print(f"🌐 Processing with {mode_text}...")
            final_summary = self._online_summarize(cleaned_text, summary_ratio)
        else:
            # Chunk text for offline processing
            chunks = self.chunk_text(cleaned_text, max_chunk_length=800)
            print(f"🏠 Processing {len(chunks)} chunks with {mode_text}...")
            
            chunk_summaries = []
            for i, chunk in enumerate(chunks):
                print(f"AI processing chunk {i+1}/{len(chunks)}...")
                chunk_summary = self.ai_summarize_chunk(chunk, summary_ratio)
                if chunk_summary and len(chunk_summary.strip()) > 10:
                    chunk_summaries.append(chunk_summary)
            
            # Combine chunk summaries
            if len(chunk_summaries) > 1:
                combined_summaries = " ".join(chunk_summaries)
                if len(combined_summaries.split()) > 500:
                    final_summary = self.ai_summarize_chunk(combined_summaries, summary_ratio)
                else:
                    final_summary = combined_summaries
            else:
                final_summary = chunk_summaries[0] if chunk_summaries else "Unable to generate summary."
        
        # Create structured output
        structured_summary = self.create_structured_summary(
            final_summary, key_phrases, summary_ratio, source_filename
        )
        
        # Calculate statistics
        original_sentences = len(re.split(r'[.!?]+', text))
        summary_sentences = len(re.split(r'[.!?]+', final_summary)) if final_summary else 0
        original_words = len(text.split())
        summary_words = len(final_summary.split()) if final_summary else 0
        
        compression_ratio = ((original_words - summary_words) / original_words) * 100 if original_words > 0 else 0
        compression_ratio = max(0, min(100, compression_ratio))
        
        return {
            'summary': structured_summary,
            'original_sentences': original_sentences,
            'summary_sentences': summary_sentences,
            'original_words': original_words,
            'summary_words': summary_words,
            'compression_ratio': compression_ratio,
            'key_topics': key_phrases,
            'model_used': 'online' if self.is_online else 'offline',
            'source_file': source_filename
        }

# Enhanced Online Summarizer Class
class OnlineTransformersSummarizer(AIDocumentSummarizer):
    """Online HuggingFace Transformers Summarizer with Privacy Protection"""
    def __init__(self):
        super().__init__(model_type="online-transformers", is_online=True)

# Keep compatibility
class LexRankSummarizer(AIDocumentSummarizer):
    """Wrapper for backward compatibility - Offline T5 only"""
    def __init__(self, model_type="t5-small"):
        super().__init__(model_type=model_type, is_online=False)

# File extraction functions
def extract_text_from_file(file_path):
    """Extract text from different file formats"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def extract_text_from_pdf(file_path):
    """Enhanced PDF text extraction"""
    try:
        import PyPDF2
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
    except ImportError:
        raise Exception("PyPDF2 is required for PDF processing.")
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

# Enhanced SummaryWorker for multiple files
class SummaryWorker(QThread):
    """Enhanced worker thread with online/offline support"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)  # For progress updates
    
    def __init__(self, file_path, summary_ratio, model_type="t5-small", is_online=False):
        super().__init__()
        self.file_path = file_path
        self.summary_ratio = summary_ratio
        self.model_type = model_type
        self.is_online = is_online
    
    def run(self):
        try:
            # Extract text from file
            filename = os.path.basename(self.file_path)
            self.progress.emit(f"📖 Extracting text from {filename}...")
            
            text = extract_text_from_file(self.file_path)
            
            if not text.strip():
                self.error.emit("The selected file appears to be empty or unreadable.")
                return
            
            # Create appropriate summarizer
            self.progress.emit(f"🤖 Initializing AI model...")
            
            if self.is_online:
                summarizer = OnlineTransformersSummarizer()
            else:
                summarizer = LexRankSummarizer(model_type=self.model_type)
            
            self.progress.emit(f"📝 Generating summary...")
            result = summarizer.summarize(text, self.summary_ratio, filename)
            
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(f"Error processing file: {str(e)}")

# PDF Export function - should be added to your main UI class
def export_to_pdf(self):
    """Export summary to PDF with proper functionality"""
    if not hasattr(self, 'all_summaries') or not self.all_summaries:
        QMessageBox.warning(self, "No Summary", "Please generate a summary first.")
        return

    # Get save location from user
    options = QFileDialog.Options()
    default_name = "AI_Summary.pdf"
    if hasattr(self, 'selected_files') and self.selected_files:
        default_name = f"Summary_{self.selected_files[0]['filename'].split('.')}.pdf"
    
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
        body {{ font-family: Georgia, serif; font-size: 12pt; line-height: 1.6; margin: 40px; }}
        h1 {{ color: #2c3e50; font-size: 18pt; margin-bottom: 20px; }}
        h2 {{ color: #34495e; font-size: 14pt; margin-top: 25px; margin-bottom: 10px; }}
        .stats {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .stat {{ display: inline-block; margin-right: 30px; font-weight: bold; }}
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
    <p>{summary_content.replace(chr(10), '</p><p>')}</p>
    
    <hr style="margin-top: 30px;">
    <p><em>Generated by AI Document Summarizer</em></p>
</body>
</html>
            """
            
            doc.setHtml(formatted_content)
            doc.print_(printer)
            
            QMessageBox.information(self, "Success", f"Summary successfully saved as:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "PDF Export Error", f"Failed to save PDF:\n{str(e)}")
