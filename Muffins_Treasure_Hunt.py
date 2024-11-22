import os
import platform
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet
import time

# Function to display intro with emojis
def display_intro():
    print("🔍 Welcome to Muffin's Treasure Hunting Tool!")
    print("🐾 Muffin is here to help sniff out crypto treasures!")
    print("\nWhat does this tool do?")
    print("🦴 Searches your drives for crypto wallets, keys, and related treasures.")
    print("📊 Exports results to both a text file and a spreadsheet.")
    print("\n🐶 Sniffing will start soon... Please be patient!")
    print("------------------------------------------------------------", flush=True)
    time.sleep(5)  # Pause to let the user read

# Get available drives
def get_drives():
    if platform.system() == "Windows":
        import string
        return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    elif platform.system() == "Darwin":  # macOS
        return ["/"]  # Start from root for macOS
    else:
        return ["/"]  # Generic fallback for Unix/Linux systems

# Define keywords, their icons, and ignored extensions
KEYWORDS_ICONS = {
    "crypto": "🪙", "wallet": "💰", "bitcoin": "₿", "ethereum": "Ξ", "doge": "🐕",
    "litecoin": "Ł", "key": "🔑", "phrase": "✍️", "secret": "🤫", "password": "🔒",
    "passphrase": "✏️", "xpub": "📜", "0x": "📬", "backup": "📂", "seed": "🌱", "private": "🕶️"
}
IGNORED_EXTENSIONS = [".exe", ".dll", ".sys", ".tmp", ".log", ".ini", ".dat"]

# Recursive search
def search_files(drive):
    found_items = []
    print(f"🔍 Searching drive {drive}...", flush=True)
    for root, dirs, files in os.walk(drive):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file)
            file_extension = os.path.splitext(file)[1].lower()

            # Skip ignored extensions
            if file_extension in IGNORED_EXTENSIONS:
                continue

            # Match keywords in file name
            keyword_matches = [kw for kw in KEYWORDS_ICONS if kw.lower() in file_name.lower()]
            if keyword_matches:
                icon = KEYWORDS_ICONS[keyword_matches[0]]  # Use the first matched keyword's icon
                main_folder = root.split(os.sep)[1] if platform.system() == "Windows" else root.split("/")[1]
                main_folder = main_folder if main_folder.lower() not in ["program files", "windows"] else root.split(os.sep)[2]
                found_items.append({
                    "Drive": drive[0],
                    "Main Folder": main_folder,
                    "Keyword Match": ", ".join(keyword_matches),
                    "File Extension": file_extension,
                    "File Name": file_name,
                    "File Path": root,
                })
                print(f"{icon} Found: {file_name}", flush=True)  # Display filename with an icon
    return found_items

# Write results to .txt and Excel
def export_results(found_items):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    text_file = os.path.join(desktop_path, "Muffins_Treasure_Hunt_Results.txt")
    excel_file = os.path.join(desktop_path, "Muffins_Treasure_Hunt_Results.xlsx")

    # Write to .txt
    with open(text_file, "w", encoding="utf-8") as txt:
        txt.write("🔍 Muffin's Treasure Hunt Results\n")
        txt.write(f"🏆 Total treasures found: {len(found_items)}\n\n")
        for item in found_items:
            txt.write(f"Drive: {item['Drive']} | Folder: {item['Main Folder']} | File: {item['File Name']} | Path: {item['File Path']}\n")

    # Write to Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Muffin's Results"

    # Define headers
    headers = ["Drive", "Main Folder", "Keyword Match", "File Extension", "File Name", "File Path"]
    for col, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    # Enable filters
    sheet.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"

    # Populate rows
    for row, item in enumerate(found_items, 2):
        sheet.cell(row=row, column=1, value=item["Drive"])
        sheet.cell(row=row, column=2, value=item["Main Folder"])
        sheet.cell(row=row, column=3, value=item["Keyword Match"])
        sheet.cell(row=row, column=4, value=item["File Extension"])
        sheet.cell(row=row, column=5, value=item["File Name"])
        path_cell = sheet.cell(row=row, column=6, value=item["File Path"])
        path_cell.hyperlink = f"file:///{item['File Path']}"  # Make the path clickable

    # Adjust column widths
    for col in range(1, len(headers) + 1):
        sheet.column_dimensions[get_column_letter(col)].width = 25

    # Save the spreadsheet
    workbook.save(excel_file)

    print("\n🎉 Export Complete!")
    print(f"📄 Text File: {text_file}")
    print(f"📊 Spreadsheet: {excel_file}")
    print(f"🏆 Total treasures found: {len(found_items)} 🐾", flush=True)

# Main Function
def muffins_treasure_hunt():
    display_intro()
    drives = get_drives()
    print(f"📂 Drives to be searched: {', '.join(drives)}\n", flush=True)
    all_found_items = []

    for drive in drives:
        found_items = search_files(drive)
        all_found_items.extend(found_items)

    export_results(all_found_items)
    print("\n🐶 Muffin's hunt is complete! Happy treasure hunting! 🦴", flush=True)

# Run the tool
if __name__ == "__main__":
    muffins_treasure_hunt()
