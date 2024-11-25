import os
import platform
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
import time
import re
from PyPDF2 import PdfReader
from docx import Document
import csv
import sys
import msvcrt  # For Windows keyboard input handling

DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Muffins_Treasure_Hunt_Results")
CONSOLE_LOG_FILE = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Console_Log.txt")
ERROR_LOG_FILE = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Errors.txt")

class Logger:
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log_file = open(log_file, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        pass

os.makedirs(DESKTOP_PATH, exist_ok=True)
sys.stdout = Logger(CONSOLE_LOG_FILE)

def display_intro():
    print("🔍 Welcome to Muffin's Treasure Hunting Tool!")
    print("🐾 Muffin is here to help sniff out crypto treasures!")
    print("\nWhat does this tool do?")
    print("🦴 Searches your drives for crypto wallets, keys, and related treasures.")
    print("📄 Scans the content of .docx, .pdf, .txt, .csv, .xlsx, and .json files for deeper insights.")
    print("📊 Exports results to both a text file and a spreadsheet.")
    print("\n🐶 Let's select the drives you want Muffin to hunt through!")
    print("------------------------------------------------------------")

def select_drives(drives):
    print("\nAvailable Drives:")
    for idx, drive in enumerate(drives, 1):
        print(f"{idx}. {drive}")
    print("\nEnter the numbers of the drives you want to scan, separated by commas (e.g., 1,3): ", end="", flush=True)
    
    selected = []
    while True:
        user_input = sys.stdin.readline().strip()
        if not user_input:
            print("Please enter at least one number corresponding to the drives you want to scan.", flush=True)
            continue
        try:
            indices = [int(x.strip()) for x in user_input.split(",")]
            selected = [drives[i-1] for i in indices if 1 <= i <= len(drives)]
            if not selected:
                raise ValueError
            break
        except:
            print("Invalid input. Please enter valid numbers separated by commas (e.g., 1,3): ", end="", flush=True)
    
    print(f"\n🚀 Starting search on drives: {', '.join(selected)}\n", flush=True)
    return selected

def get_drives():
    if platform.system() == "Windows":
        import string
        return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    elif platform.system() == "Darwin":
        return ["/"]
    else:
        return ["/"]

KEYWORDS_ICONS = {
    "crypto": "🪙", "wallet": "💰", "bitcoin": "₿", "ethereum": "Ξ", "doge": "🐕",
    "litecoin": "Ł", "key": "🔑", "phrase": "✍️", "secret": "🤫", "password": "🔒",
    "passphrase": "✏️", "xpub": "📜", "0x": "📬", "backup": "📂", "seed": "🌱",
    "private": "🕶️", "account": "🧾", "credentials": "📋", "2FA": "🔑"
}
IGNORED_EXTENSIONS = [".exe", ".dll", ".sys", ".tmp", ".log", ".ini", ".dat", ".js", ".ts"]
EXCLUDED_FOLDERS = ["images", "icons", "img16_16", "img24_24", "img32_32", "sketches"]
EXCLUDED_PATHS = ["C:\\Windows", "Program Files", "AppData", "Local", "Cache"]

def log_error(message):
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as error_log:
        error_log.write(f"{message}\n")

def is_valid_ethereum_address(file_name):
    return bool(re.search(r"\b0x[a-fA-F0-9]{40}\b", file_name))

def is_valid_bitcoin_key(file_name):
    btc_regex = r"\b(5[HJK][1-9A-HJ-NP-Za-km-z]{49,50}|[13][1-9A-HJ-NP-Za-km-z]{26,35})\b"
    return bool(re.search(btc_regex, file_name))

def contains_json_wallet_structure(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return any(key in content for key in ["ciphertext", "cipherparams", "kdfparams", "mac", "address"])
    except Exception as e:
        log_error(f"Error reading JSON file {file_path}: {e}")
    return False

def scan_spreadsheet(file_path):
    try:
        if file_path.endswith(".csv"):
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if any(cell and any(keyword.lower() in str(cell).lower() for keyword in KEYWORDS_ICONS) for cell in row):
                        return True
        else:
            workbook = openpyxl.load_workbook(file_path, read_only=True)
            for sheet in workbook.sheetnames:
                ws = workbook[sheet]
                for row in ws.iter_rows(values_only=True):
                    if any(cell and any(keyword.lower() in str(cell).lower() for keyword in KEYWORDS_ICONS) for cell in row):
                        return True
    except Exception as e:
        log_error(f"Error reading spreadsheet {file_path}: {e}")
    return False

def search_file_content(file_path, keywords):
    try:
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                return any(keyword.lower() in content.lower() for keyword in keywords)
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])
            return any(keyword.lower() in content.lower() for keyword in keywords)
        elif file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            content = "\n".join([page.extract_text() for page in reader.pages])
            return any(keyword.lower() in content.lower() for keyword in keywords)
    except Exception as e:
        log_error(f"Error processing file {file_path}: {e}")
    return False

def search_files(drive):
    found_items = []
    print(f"🔍 Searching drive {drive}...", flush=True)
    for root, dirs, files in os.walk(drive):
        if any(excluded.lower() in root.lower() for excluded in EXCLUDED_PATHS + EXCLUDED_FOLDERS):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in IGNORED_EXTENSIONS and not file_extension in [".png", ".jpg", ".jpeg", ".gif"]:
                continue

            keyword_matches = [kw for kw in KEYWORDS_ICONS if kw.lower() in file_name.lower()]

            if "0x" in keyword_matches and not is_valid_ethereum_address(file_name):
                keyword_matches.remove("0x")
            if is_valid_bitcoin_key(file_name):
                keyword_matches.append("bitcoin_key")
            if file_extension == ".json" and contains_json_wallet_structure(file_path):
                keyword_matches.append("json_wallet")
            if file_extension in [".xlsx", ".xls", ".csv"] and scan_spreadsheet(file_path):
                keyword_matches.append("spreadsheet_content")
            if not keyword_matches and file_extension in [".txt", ".docx", ".pdf"]:
                if search_file_content(file_path, KEYWORDS_ICONS.keys()):
                    keyword_matches.append("content_match")

            if keyword_matches:
                icon = KEYWORDS_ICONS.get(keyword_matches[0], "📄")
                
                # Determine Top Folder (highest folder after the drive)
                path_parts = os.path.normpath(root).split(os.sep)
                if platform.system() == "Windows":
                    # Remove the drive letter
                    path_parts = path_parts[1:]
                else:
                    # For Unix-like systems, first part is root '/'
                    path_parts = path_parts[1:]
                
                top_folder = path_parts[0] if path_parts else "Root"
                
                # Determine Bottom Folder (immediate folder containing the file)
                bottom_folder = os.path.basename(root) if root else "Root"
                
                found_items.append({
                    "Drive": drive[0],
                    "Top Folder": top_folder,
                    "Bottom Folder": bottom_folder,
                    "Keyword Match": ", ".join(keyword_matches),
                    "File Extension": file_extension,
                    "File Name": file_name,
                    "File Path": root,
                })
                print(f"{icon} Found: {file_name}", flush=True)
    return found_items

def export_results(found_items):
    text_file = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Path_Log.txt")
    excel_file = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Results.xlsx")

    with open(text_file, "w", encoding="utf-8") as txt:
        txt.write("🔍 Muffin's Treasure Hunt Results\n")
        txt.write(f"🏆 Total treasures found: {len(found_items)}\n\n")
        for item in found_items:
            txt.write(f"Drive: {item['Drive']} | Top Folder: {item['Top Folder']} | Bottom Folder: {item['Bottom Folder']} | File: {item['File Name']} | Path: {item['File Path']}\n")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Muffin's Results"

    headers = ["Drive", "Top Folder", "Bottom Folder", "Keyword Match", "File Extension", "File Name", "File Path"]
    for col, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    sheet.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"

    for row, item in enumerate(found_items, 2):
        sheet.cell(row=row, column=1, value=item["Drive"])
        sheet.cell(row=row, column=2, value=item["Top Folder"])
        sheet.cell(row=row, column=3, value=item["Bottom Folder"])
        sheet.cell(row=row, column=4, value=item["Keyword Match"])
        sheet.cell(row=row, column=5, value=item["File Extension"])
        sheet.cell(row=row, column=6, value=item["File Name"])
        path_cell = sheet.cell(row=row, column=7, value=item["File Path"])
        path_cell.hyperlink = f"file:///{item['File Path']}"

    for col in range(1, len(headers) + 1):
        sheet.column_dimensions[get_column_letter(col)].width = 25

    workbook.save(excel_file)

    print("\n🎉 Export Complete!")
    print(f"📄 Text File: {text_file}")
    print(f"📊 Spreadsheet: {excel_file}")
    print(f"🏆 Total treasures found: {len(found_items)} 🐾", flush=True)

def muffins_treasure_hunt():
    display_intro()
    drives = get_drives()
    selected_drives = select_drives(drives)
    print(f"📂 Drives to be searched: {', '.join(selected_drives)}\n", flush=True)
    all_found_items = []

    for drive in selected_drives:
        found_items = search_files(drive)
        all_found_items.extend(found_items)

    export_results(all_found_items)
    print("\n🐶 Muffin's hunt is complete! Happy treasure hunting! 🦴", flush=True)

if __name__ == "__main__":
    muffins_treasure_hunt()
