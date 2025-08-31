# PDF-SUMMERAIZER-USING-AI (Internship Project)

## 📖 Story Time
During my **5th semester internship at BEL (Bharat Electronics Limited)**, our team was assigned a project:  
➡️ Build a **Windows-based application** to summarize PDFs (**both offline and online**) for defence sector.  

We started with GUI first as it defines wch language we use:  
- After some brainstorming, a teammate’s father (a data engineer) suggested using **Python**.  
- Thinking he would mentor us, we went ahead with **PyQt5**.  
- For the backend, we integrated:
  - **Offline mode** → [t5-base](https://huggingface.co/t5-base)  
  - **Online mode** → [Hugging Face Transformers](https://huggingface.co/transformers)  

Everything worked… almost.  
✅ Summaries were generated.  
❌ But only up to the **3rd page of the PDF** — the rest were cut off.  
And sadly, the expected guidance never came, so the project was left unfinished before the deadline.  

---

## 🚧 Current Problem
- Summaries are truncated (only first 3 pages).  
- Need a fix to handle **full-document summarization**.  

---

## 💡 Open for Suggestions
I’m sharing this here because:
- I’d love **feedback, ideas, or fixes**.  
- Open to **pair programming** with anyone interested.  

If you have an idea to solve the "cut-off after 3rd page" issue, please feel free to:  
- Open an issue 📝  
- Create a pull request 🔧  
- Or just drop a suggestion! 💬

---

## 🔧 Tech Stack
- **Language**: Python  
- **Framework**: PyQt5  
- **Models**: T5-base (offline), Hugging Face Transformers (online)  

---

## 🙌 Contributing
Pull requests are welcome! If you have a better approach or want to collaborate, feel free to connect.  

---

## ✨ Closing Note
This was my first big step into **AI + desktop applications**.  
The project may be incomplete, but the journey was a huge learning experience. 🚀  

Let’s fix this together. 💻
