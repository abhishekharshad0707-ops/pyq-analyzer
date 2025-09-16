import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pdfplumber
import re

# --- Extract text from PDF ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# --- Split questions using regex (Q.1, Q1, etc.) ---
def extract_questions(text):
    questions = re.split(r"(?:Q\.?\s?\d+[:.)-])", text)
    cleaned = [q.strip() for q in questions if q.strip()]
    return cleaned

# --- Upload and Analyze PDF ---
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return
    
    try:
        raw_text = extract_text_from_pdf(file_path)
        questions = extract_questions(raw_text)

        # Show in Text Box
        output_box.delete(1.0, tk.END)
        for i, q in enumerate(questions, 1):
            output_box.insert(tk.END, f"Q{i}: {q}\n\n")

        messagebox.showinfo("Success", f"Extracted {len(questions)} questions.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Save Results ---
def save_results():
    data = output_box.get(1.0, tk.END)
    if not data.strip():
        messagebox.showwarning("Warning", "No data to save!")
        return
    
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(data)
        messagebox.showinfo("Saved", f"Results saved at {save_path}")

# --- GUI Setup ---
root = tk.Tk()
root.title("PYQ Analyzer App")
root.geometry("800x600")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

upload_btn = tk.Button(btn_frame, text="Upload PDF", command=upload_pdf)
upload_btn.pack(side=tk.LEFT, padx=10)

save_btn = tk.Button(btn_frame, text="Save Results", command=save_results)
save_btn.pack(side=tk.LEFT, padx=10)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
output_box.pack(pady=10)

root.mainloop()
