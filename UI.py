import tkinter as tk
from tkinter import ttk
from printing_logic import sendPrintRequest

def on_print():
    values = [e.get() for e in entries]
    print("Values:", values)
    sendPrintRequest(values)

root = tk.Tk()
root.title("Label Printing")

main = ttk.Frame(root, padding=12)
main.grid()

entries = []
labels = ["Lot Number", "Tote ID", "Gross Weight", "Tare Weight", "Production Date (YYYY-MM-DD)"]

for i, label in enumerate(labels):
    ttk.Label(main, text=label).grid(row=i, column=0, sticky="e", padx=(0,8), pady=4)
    entry = ttk.Entry(main, width=40)
    entry.grid(row=i, column=1, pady=4)
    entries.append(entry)

ttk.Button(main, text="Print", command=on_print).grid(row=5, column=0, columnspan=2, pady=(10,0))

root.mainloop()
