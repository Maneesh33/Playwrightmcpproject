from openpyxl import Workbook
import os


def save_to_excel(jobs, role, location):
    folder = "output"
    os.makedirs(folder, exist_ok=True)

    filename = f"{role.replace(' ', '_')}_{location}.xlsx"
    filepath = os.path.join(folder, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "Jobs"

    ws.append(["Title", "Company", "Location", "Link", "Source"])

    for job in jobs:
        ws.append([
            job["title"],
            job["company"],
            job["location"],
            job["link"],
            job["source"]
        ])

    wb.save(filepath)

    print(f"\n📁 Saved to: {filepath}")