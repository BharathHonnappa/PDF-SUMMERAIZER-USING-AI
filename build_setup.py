# build_setup_fixed.py - Python 3.13 Compatible Build Script
import subprocess
import sys
import os
import shutil
from pathlib import Path

def install_requirements():
    """Install Python 3.13 compatible packages"""
    print("📦 Installing Python 3.13 compatible packages...")
    
    # Updated packages for Python 3.13 compatibility
    packages = [
        "PyQt5>=5.15.9",
        "numpy>=1.26.0",  # Python 3.13 compatible
        "scikit-learn>=1.4.0",  # Python 3.13 compatible
        "networkx>=3.1",
        "PyPDF2>=3.0.1",
        "reportlab>=4.0.4",
        "pyinstaller>=6.0.0"  # Latest version for Python 3.13
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning: Failed to install {package}")
    
    print("✅ Package installation completed!")

def create_simple_build():
    """Create executable using simple PyInstaller command"""
    print("🔨 Building executable with PyInstaller...")
    
    try:
        # Simple build command that should work
        subprocess.run([
            "pyinstaller", 
            "--onefile",
            "--windowed",
            "--name=AI_Document_Summarizer",
            "--add-data=ui;ui",
            "--add-data=utils;utils", 
            "--hidden-import=sklearn.utils._cython_blas",
            "--hidden-import=sklearn.neighbors.typedefs",
            "--hidden-import=sklearn.tree._utils",
            "--hidden-import=PyQt5.sip",
            "main.py"
        ], check=True)
        
        print("✅ Executable built successfully!")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Build failed with detailed options. Trying minimal build...")
        
        # Fallback: minimal build
        try:
            subprocess.run([
                "pyinstaller", 
                "--onefile",
                "--windowed",
                "main.py"
            ], check=True)
            print("✅ Minimal build completed!")
            return True
        except subprocess.CalledProcessError:
            print("❌ All build attempts failed")
            return False

def create_distribution():
    """Create distribution folder"""
    print("📁 Creating distribution folder...")
    
    dist_folder = "AI_Document_Summarizer_Distribution"
    
    # Remove existing folder
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    
    # Create new folder
    os.makedirs(dist_folder)
    
    # Find and copy executable
    exe_files = [
        "dist/AI_Document_Summarizer.exe",
        "dist/main.exe"
    ]
    
    exe_copied = False
    for exe_file in exe_files:
        if os.path.exists(exe_file):
            shutil.copy2(exe_file, f"{dist_folder}/AI_Document_Summarizer.exe")
            exe_copied = True
            print(f"✅ Copied {exe_file}")
            break
    
    if not exe_copied:
        print("❌ No executable found to copy")
        return None
    
    # Create README
    create_readme(dist_folder)
    create_sample_files(dist_folder)
    
    return dist_folder

def create_readme(dist_folder):
    """Create README file"""
    readme_content = '''
# AI Document Summarizer

## 🚀 Quick Start
1. Double-click "AI_Document_Summarizer.exe"
2. Browse and select a PDF or text file
3. Adjust summary detail level (10% = brief, 90% = detailed)
4. Click "Generate Smart Summary"
5. Save as PDF if needed

## 💻 Requirements
- Windows 10/11 (64-bit)
- No additional software needed

## ⚠️ Security Note
If Windows shows a warning:
1. Click "More info"
2. Click "Run anyway"
This is normal for new applications.

## 🎯 Features
✨ Smart LexRank summarization
📄 PDF and text file support
🎛️ Adjustable detail levels
💾 PDF export functionality
🔒 100% offline processing

---
AI Document Summarizer v1.0
'''
    
    with open(f"{dist_folder}/README.txt", "w", encoding='utf-8') as f:
        f.write(readme_content)

def create_sample_files(dist_folder):
    """Create sample files for testing"""
    sample_folder = f"{dist_folder}/Sample_Documents"
    os.makedirs(sample_folder)
    
    sample_text = '''
Artificial Intelligence and Machine Learning Overview

Introduction
Artificial Intelligence (AI) represents a transformative technology that enables computers to perform tasks requiring human-like intelligence. This includes learning, reasoning, problem-solving, and natural language understanding.

Key Concepts
Machine Learning serves as a crucial subset of AI, allowing systems to learn from data without explicit programming. The three main types include supervised learning, unsupervised learning, and reinforcement learning.

Applications
AI applications span healthcare, finance, transportation, and entertainment. From medical diagnosis to autonomous vehicles, AI continues to revolutionize various industries and improve human capabilities.

Future Outlook
As AI technology advances, it promises to enhance productivity and solve complex global challenges while raising important questions about ethics and responsible development.
'''
    
    with open(f"{sample_folder}/AI_Overview.txt", "w", encoding='utf-8') as f:
        f.write(sample_text)

def main():
    """Main build process"""
    print("🏗️  AI Document Summarizer - Fixed Build Process")
    print("=" * 60)
    
    try:
        # Install compatible packages
        install_requirements()
        print()
        
        # Build executable
        if create_simple_build():
            print()
            
            # Create distribution
            dist_folder = create_distribution()
            
            if dist_folder:
                print(f"\n🎉 BUILD COMPLETED SUCCESSFULLY!")
                print("=" * 60)
                print(f"📦 Your application is ready in: {dist_folder}/")
                print("🚀 Users can run AI_Document_Summarizer.exe directly")
                print("\n📋 Next step: Run create_installer.py to create zip file")
            else:
                print("❌ Distribution creation failed")
                return False
        else:
            print("❌ Build process failed")
            return False
        
    except Exception as e:
        print(f"❌ Build failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()
