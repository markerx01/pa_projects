import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib, requests, os

API_KEY = "d9f7c9becd7a6147622a2c343205b8f66311bae70f74d555ca507de7268f1981"  # put key here or set VT_API_KEY env var

def sha256(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def scan():
    if not API_KEY:
        messagebox.showerror("No API key", "Set API_KEY variable or VT_API_KEY env var.")
        return
    p = filedialog.askopenfilename()
    if not p: return
    h = sha256(p)
    r = requests.get(f"https://www.virustotal.com/api/v3/files/{h}", headers={"x-apikey":API_KEY})
    if r.status_code == 200:
        stats = r.json()["data"]["attributes"]["last_analysis_stats"]
        mal = stats.get("malicious", 0)
        messagebox.showinfo("Result", f"{os.path.basename(p)}\nmalicious: {mal}")
    elif r.status_code == 404:
        messagebox.showwarning("Not found", "File not in VirusTotal database.")
    else:
        messagebox.showerror("Error", f"VT error {r.status_code}")

root = tk.Tk()
root.title("Mini Real AV")
tk.Button(root, text="Scan File (VirusTotal)", command=scan, width=30).pack(padx=30, pady=30)
root.mainloop()
