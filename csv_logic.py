import datetime
import tkinter as tk
import csv
import os

def export_print_data_to_csv(entries: list[tk.Entry]):
    """
    entries = [lot_entry, tote_entry, gross_entry, tare_entry, prod_date_entry]
    Writes values to ~/Desktop/sockeye_<today>.csv
    """

    # Get values
    lot = entries[0].get()
    tote_id = entries[1].get()
    gross_wgt = entries[2].get()
    tare_wgt = entries[3].get()
    prod_date = entries[4].get()

    # Determine Desktop path (cross-platform)
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    # Ensure Desktop exists
    if not os.path.exists(desktop):
        os.makedirs(desktop, exist_ok=True)

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    filename = os.path.join(desktop, f"sockeye_{today_str}.csv")

    file_exists = os.path.isfile(filename)

    # Open CSV and append
    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header if new file
        if not file_exists:
            writer.writerow(["LotNumber", "ToteID", "GrossWeight", "TareWeight", "ProductionDate"])

        # Write row
        writer.writerow([lot, tote_id, gross_wgt, tare_wgt, prod_date])

    print(f"✅ Data exported to {filename}")
