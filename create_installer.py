# create_installer.py - Creates a zip file for easy distribution
import os
import zipfile
from pathlib import Path
from datetime import datetime

def create_installer_zip():
    """Create a zip file for easy distribution"""
    print("📦 Creating distribution package...")
    
    dist_folder = "AI_Document_Summarizer_Distribution"
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"AI_Document_Summarizer_v1.0_{timestamp}_Windows.zip"
    
    if not os.path.exists(dist_folder):
        print("❌ Distribution folder not found. Run build_setup.py first.")
        return False
    
    # Create zip file with compression
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(dist_folder):
            for file in files:
                file_path = os.path.join(root, file)
                # Get relative path from distribution folder
                arc_name = os.path.relpath(file_path, dist_folder)
                zipf.write(file_path, arc_name)
                print(f"  Added: {arc_name}")
    
    file_size = os.path.getsize(zip_name) / (1024 * 1024)  # MB
    print(f"\n✅ Created: {zip_name}")
    print(f"📏 Size: {file_size:.1f} MB")
    print("📤 Ready for Google Drive upload!")
    
    # Create sharing instructions
    create_sharing_instructions(zip_name)
    
    return True

def create_sharing_instructions(zip_name):
    """Create instructions for sharing via Google Drive"""
    instructions = f'''
🌐 Google Drive Sharing Instructions

📁 File to Upload: {zip_name}

🔗 Sharing Steps:
1. Upload {zip_name} to your Google Drive
2. Right-click the file → "Share"
3. Change access to "Anyone with the link can view"
4. Copy the sharing link
5. Share this link with your recipients

💬 Message Template for Recipients:
---
🤖 AI Document Summarizer - Free Download

Transform your documents into intelligent summaries with this easy-to-use tool!

📥 Download: [YOUR_GOOGLE_DRIVE_LINK_HERE]

✅ Features:
• Smart PDF and text summarization
• Adjustable detail levels (10% - 90%)
• Export summaries as professional PDFs
• Completely offline - your documents stay private
• No installation required - just download and run!

🚀 Instructions:
1. Download and extract the zip file
2. Run AI_Document_Summarizer.exe
3. Select your document and start summarizing!

💻 Requirements: Windows 10/11 (64-bit)
📏 Download Size: ~150-200MB
---

📋 Google Drive Link Format:
• Share link: https://drive.google.com/file/d/FILE_ID/view
• Direct download: https://drive.google.com/uc?export=download&id=FILE_ID

Replace FILE_ID with the actual ID from your Google Drive link.
'''
    
    with open("Google_Drive_Sharing_Instructions.txt", "w", encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"📋 Created: Google_Drive_Sharing_Instructions.txt")

if __name__ == "__main__":
    create_installer_zip()
