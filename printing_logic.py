import requests
import datetime
import tkinter as tk
from tkinter import messagebox
PRINTER_IP = "http://172.16.10.87:53230/print"  # replace with your actual endpoint

def sendPrintRequest(entries: list[tk.Entry]):
    """
    entries = [lot_entry, tote_entry, gross_entry, tare_entry, prod_date_entry]
    """

    # Grab raw values
    lot = entries[0].get()
    tote_id = entries[1].get()
    gross_wgt = entries[2].get()
    tare_wgt = entries[3].get()
    prod_date = entries[4].get()

    # Validate numeric fields
    try:
        tote_id = int(tote_id)
    except ValueError:
        messagebox.showerror("Invalid Data", "Tote ID must be a number.")
        entries[1].delete(0, tk.END)
        return

    try:
        gross_wgt = int(gross_wgt)
    except ValueError:
        messagebox.showerror("Invalid Data", "Gross Weight must be a number.")
        entries[2].delete(0, tk.END)
        return

    try:
        tare_wgt = int(tare_wgt)
    except ValueError:
        messagebox.showerror("Invalid Data", "Tare Weight must be a number.")
        entries[3].delete(0, tk.END)
        return

    net_wgt = gross_wgt - tare_wgt

    # Validate production date
    try:
        prod_dt = datetime.datetime.strptime(prod_date, "%Y-%m-%d")
        exp_dt = prod_dt.replace(year=prod_dt.year + 2)
    except ValueError:
        messagebox.showerror("Invalid Data", "Production Date must be in YYYY-MM-DD format.")
        entries[4].delete(0, tk.END)
        return

    prod_time = prod_dt.strftime("%H:%M")

    payload = {
        "TemplatePath": "alaska_salmon.btw",
        "PrinterName": "ZDesigner GX420d",
        "labelData": {
            "ToteNumber": tote_id,
            "LotNumber": lot,
            "ProductName": "Round Sockeye Salmon IQF O/R",
            "SpeciesName": "Sockeye Salmon",
            "ScientificName": "Oncorhynchus nerka",
            "GrossWgt": gross_wgt,
            "TareWgt": tare_wgt,
            "NetWgt": net_wgt,
            "ProdDate": prod_dt.strftime("%Y-%m-%d"),
            "ProdTime": prod_time,
            "ExpDate": exp_dt.strftime("%Y-%m-%d"),
            "FAO": 67,
            "ADEC": 15972,
            "FEI": 3031121070,
            "GearType": "Gillnet and Setnet",
            "Barcode": f"NLHA{lot}09{net_wgt:04}{prod_dt.strftime('%y%m%d')}{tote_id:06}"
        }
    }

    try:
        response = requests.post(PRINTER_IP, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Print request sent successfully:", response.text)
    except requests.RequestException as e:
        print("❌ Failed to send print request:", e)
