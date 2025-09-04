import requests
import datetime

PRINTER_IP = "http://172.16.10.87:53230/print"  # replace with your actual endpoint

def sendPrintRequest(entries: list[str]):
    """
    entries = [lot, tote_id, gross_weight, tare_weight, production_date]
    """

    lot, tote_id, gross_wgt, tare_wgt, prod_date = entries

    # convert numeric fields safely
    try:
        tote_id = int(tote_id)
    except ValueError:
        tote_id = 0

    try:
        gross_wgt = int(gross_wgt)
    except ValueError:
        gross_wgt = 0

    try:
        tare_wgt = int(tare_wgt)
    except ValueError:
        tare_wgt = 0

    net_wgt = gross_wgt - tare_wgt

    # Use prod_date for both ProdDate and ExpDate (example: +1 year)
    try:
        prod_dt = datetime.datetime.strptime(prod_date, "%Y-%m-%d")
        exp_dt = prod_dt.replace(year=prod_dt.year + 1)
    except ValueError:
        prod_dt = datetime.datetime.today()
        exp_dt = prod_dt.replace(year=prod_dt.year + 1)

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
            "Barcode": f"NLHA{lot}09{net_wgt:04}{prod_dt.strftime('%y%m%d')}{tote_id:07}"
        }
    }

    try:
        response = requests.post(PRINTER_IP, json=payload, timeout=5)
        response.raise_for_status()
        print("✅ Print request sent successfully:", response.text)
    except requests.RequestException as e:
        print("❌ Failed to send print request:", e)
