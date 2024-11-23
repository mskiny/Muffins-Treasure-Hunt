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

# Paths for results
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Muffins_Treasure_Hunt_Results")
CONSOLE_LOG_FILE = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Console_Log.txt")
ERROR_LOG_FILE = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Errors.txt")

# Global Variables
KEYWORDS_ICONS = {
    "crypto": "🪙", "wallet": "💰", "bitcoin": "₿", "ethereum": "Ξ", "doge": "🐕",
    "litecoin": "Ł", "key": "🔑", "phrase": "✍️", "secret": "🤫", "password": "🔒",
    "passphrase": "✏️", "xpub": "📜", "0x": "📬", "backup": "📂", "seed": "🌱",
    "private": "🕶️", "important": "⭐", "credentials": "📋", "blockchain": "⛓️",
    "coins": "💵", "hash": "🔗", "wallet.dat": "📄", "ripple": "🌊",
    "stellar": "🌟", "tron": "🚀", "bnb": "⚡", "solana": "☀️",
    "cardano": "🌌", "mnemonic": "🧠", "recovery": "📦", "restore": "🔄",
    "seed phrase": "🔐", "secret phrase": "🔓", "metamask": "🦊",
    "phantom": "👻", "keystore": "📁", "ledger": "📒", "trezor": "🔐",
    "cold storage": "❄️", "pk": "🗝️", "private_key": "🗝️", "xprv": "📜",
    "encrypted": "🔒", "kdfparams": "📑", "cipher": "🔐", "ciphertext": "🔏",
    "btc": "₿", "eth": "Ξ", "ltc": "Ł", "xrp": "🌊", "xlm": "🌟",
    "ada": "🌌", "trx": "🚀", "json": "📄", "dat": "📄", "ftx": "🚩",
    "mtgox": "⚠️", "quadrigacx": "❗", "bitconnect": "❌", "cryptopia": "⚡",
    "nicehash": "💻", "binance": "⚡", "kraken": "🐙", "gemini": "♊",
    "bitstamp": "📈", "okx": "📊", "huobi": "🔥", "bybit": "📉",
    "bitfinex": "🏦", "uniswap": "💱", "exodus": "📂", "trustwallet": "🔒",
    "atomic wallet": "💥", "bluewallet": "🔵", "safepal": "🔐", "guarda": "🔒"
}

# Adjust EXCLUDED_PATHS based on platform
if platform.system() == "Windows":
    EXCLUDED_PATHS = ["C:\\Windows", "C:\\Program Files", os.path.expanduser("~\\AppData")]
else:
    EXCLUDED_PATHS = ["/System", "/Library", "/Applications", "/bin", "/sbin", "/usr", "/var", "/dev", "/proc", "/run", "/sys"]

# File extensions to ignore
IGNORED_EXTENSIONS = [".exe", ".dll", ".sys", ".tmp", ".log", ".ini", ".dat", ".js", ".ts"]

# Folders to exclude
EXCLUDED_FOLDERS = ["images", "icons", "img16_16", "img24_24", "img32_32", "sketches"]

# Logger class with flush method
class Logger:
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log_file = open(log_file, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

os.makedirs(DESKTOP_PATH, exist_ok=True)
sys.stdout = Logger(CONSOLE_LOG_FILE)

def get_drives():
    """
    Detect available drives to scan.
    """
    if platform.system() == "Windows":
        import string
        return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    else:
        return [os.path.expanduser("~")]

def display_intro_and_select_drives():
    """
    Display introductory text and prompt the user to select drives to scan.
    """
    print("🔍 Welcome to Muffin's Treasure Hunting Tool!")
    print("🐾 Muffin is here to help sniff out crypto treasures!")
    print("\nWhat does this tool do?")
    print("🦴 Searches your drives for crypto wallets, keys, and related treasures.")
    print("📄 Scans files for sensitive data, including text, spreadsheets, images, and more.")
    print("📊 Exports results to both a text file and a spreadsheet.")
    print("\n🐶 Let’s get started! Muffin is ready to sniff out hidden treasures!")
    print("\n------------------------------------------------------------\n")

    # Detect drives
    drives = get_drives()
    if not drives:
        print("🚫 No drives detected. Exiting...")
        sys.exit(0)

    if platform.system() == "Windows":
        print(f"1. Type ALL to scan all of the 📂 Detected Drives: {' '.join(drives)}")
        print("2. Or type only drive letters you want to scan separated by spaces (e.g., C or C D or E).")
    else:
        print(f"📂 On this system, only the home directory can be scanned: {drives[0]}")

    print()  # Adds a blank line for better readability
    print("✨Type your answer and press Enter to continue:", flush=True)  # Ensures immediate display

    # User input for drive selection
    response = input().strip().upper()
    if platform.system() != "Windows":
        # For non-Windows systems, only home directory is scanned
        print("⚠️ On non-Windows systems, only the home directory is available for scanning.")
        return drives

    if response == "ALL":
        return drives
    else:
        selected_drives = []
        for d in response.split():
            drive = f"{d.upper()}:\\" if not d.endswith(":\\") else d.upper()
            if drive in drives:
                selected_drives.append(drive)
            else:
                print(f"🚫 Drive {d} is not a valid drive.")
        if not selected_drives:
            print("🚫 No valid drives selected. Exiting...")
            sys.exit(0)
        return selected_drives

def log_error(message):
    """
    Log errors to the error log file and print them to the console.
    """
    print(f"❌ {message}", flush=True)
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as error_log:
        error_log.write(f"{message}\n")

def is_valid_ethereum_address(file_name):
    """
    Check if a string in the file name is a valid Ethereum address.
    """
    return bool(re.search(r"\b0x[a-fA-F0-9]{40}\b", file_name))

def is_valid_bitcoin_key(file_name):
    """
    Check if a string in the file name is a valid Bitcoin address or key.
    """
    btc_regex = r"\b(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,62}\b"
    return bool(re.search(btc_regex, file_name))

def contains_json_wallet_structure(file_path):
    """
    Check if a JSON file contains wallet structure indicators.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return any(key in content for key in ["ciphertext", "cipherparams", "kdfparams", "mac", "address"])
    except Exception as e:
        log_error(f"Error reading JSON file {file_path}: {e}")
    return False

def scan_spreadsheet(file_path):
    """
    Scan a spreadsheet file for crypto-related keywords.
    """
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

def search_file_content(file_path):
    """
    Search the content of a file for crypto-related keywords.
    """
    try:
        if file_path.endswith(".txt") or '.' not in os.path.basename(file_path):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if any(keyword.lower() in content.lower() for keyword in KEYWORDS_ICONS):
                    return True
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            for para in doc.paragraphs:
                if any(keyword.lower() in para.text.lower() for keyword in KEYWORDS_ICONS):
                    return True
        elif file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()
                if text and any(keyword.lower() in text.lower() for keyword in KEYWORDS_ICONS):
                    return True
    except Exception as e:
        log_error(f"Error processing file {file_path}: {e}")
    return False

def search_files(drive):
    """
    Recursively searches the specified drive for files matching crypto-related keywords.
    """
    found_items = []
    print(f"🔍 Searching drive {drive}...", flush=True)

    # Normalize the drive letter to lower case for consistent comparison
    drive_letter = os.path.splitdrive(drive)[0].lower()

    # Filter EXCLUDED_PATHS to include only those on the same drive
    excluded_paths_on_same_drive = [
        os.path.abspath(excluded) for excluded in EXCLUDED_PATHS
        if os.path.splitdrive(excluded)[0].lower() == drive_letter
    ]

    for root, dirs, files in os.walk(drive):
        normalized_root = os.path.abspath(root)

        # Exclude specified folders
        if any(excluded_folder.lower() in root.lower() for excluded_folder in EXCLUDED_FOLDERS):
            continue

        # Check if the current root is within any excluded paths
        exclude = False
        for excluded in excluded_paths_on_same_drive:
            if normalized_root.lower().startswith(excluded.lower()):
                exclude = True
                break
        if exclude:
            continue

        print(f"📂 Scanning directory: {root}", flush=True)
        for file in files:
            file_path = os.path.join(root, file)
            file_name = file
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in IGNORED_EXTENSIONS:
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
            if (not keyword_matches and file_extension in [".txt", ".docx", ".pdf"]) or (not file_extension):
                if search_file_content(file_path):
                    keyword_matches.append("content_match")

            # Include images with keywords in filenames
            if file_extension in [".png", ".jpg", ".jpeg", ".gif"]:
                if any(kw.lower() in file_name.lower() for kw in KEYWORDS_ICONS):
                    keyword_matches.append("image_keyword_match")

            if keyword_matches:
                icon = KEYWORDS_ICONS.get(keyword_matches[0], "📄")
                main_folder = (
                    normalized_root.split(os.sep)[2] if normalized_root.startswith(f"{drive}Users") and len(normalized_root.split(os.sep)) > 2
                    else normalized_root.split(os.sep)[1] if len(normalized_root.split(os.sep)) > 1 else normalized_root
                )
                main_folder = main_folder if main_folder.lower() not in ["program files", "windows"] else normalized_root.split(os.sep)[2] if len(normalized_root.split(os.sep)) > 2 else normalized_root

                found_items.append({
                    "Drive": drive[0],
                    "Main Folder": main_folder,
                    "Keyword Match": ", ".join(keyword_matches),
                    "File Extension": file_extension,
                    "File Name": file_name,
                    "File Path": normalized_root,
                })
                print(f"{icon} Found: {file_name}", flush=True)
    return found_items

def export_results(found_items):
    """
    Export the search results to a text file and an Excel spreadsheet.
    """
    text_file = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Path_Log.txt")
    excel_file = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Results.xlsx")

    with open(text_file, "w", encoding="utf-8") as txt:
        txt.write("🔍 Muffin's Treasure Hunt Results\n")
        txt.write(f"🏆 Total treasures found: {len(found_items)}\n\n")
        for item in found_items:
            txt.write(f"Drive: {item['Drive']} | Folder: {item['Main Folder']} | File: {item['File Name']} | Path: {item['File Path']}\n")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Muffin's Results"

    headers = ["Drive", "Main Folder", "Keyword Match", "File Extension", "File Name", "File Path"]
    for col, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    sheet.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"

    for row_num, item in enumerate(found_items, start=2):
        sheet.cell(row=row_num, column=1, value=item["Drive"])
        sheet.cell(row=row_num, column=2, value=item["Main Folder"])
        sheet.cell(row=row_num, column=3, value=item["Keyword Match"])
        sheet.cell(row=row_num, column=4, value=item["File Extension"])
        sheet.cell(row=row_num, column=5, value=item["File Name"])
        path_cell = sheet.cell(row=row_num, column=6, value=item["File Path"])
        # Create hyperlink to the file path
        if platform.system() == "Windows":
            path_cell.hyperlink = f"file:///{item['File Path'].replace(os.sep, '/')}"
        else:
            path_cell.hyperlink = f"file://{item['File Path']}"

    for col in range(1, len(headers) + 1):
        sheet.column_dimensions[get_column_letter(col)].width = 25

    workbook.save(excel_file)

    print("\n🎉 Export Complete!")
    print(f"📄 Text File: {text_file}")
    print(f"📊 Spreadsheet: {excel_file}")
    print(f"🏆 Total treasures found: {len(found_items)} 🐾", flush=True)

def muffins_treasure_hunt():
    """
    Main function to run Muffin's Treasure Hunt.
    """
    selected_drives = display_intro_and_select_drives()
    all_found_items = []
    for drive in selected_drives:
        found_items = search_files(drive)
        all_found_items.extend(found_items)
    export_results(all_found_items)
    print("\n🐶 Muffin's hunt is complete! Happy treasure hunting! 🦴", flush=True)

if __name__ == "__main__":
    try:
        muffins_treasure_hunt()
    except KeyboardInterrupt:
        print("\n🛑 Scan interrupted by user. Exiting gracefully.", flush=True)
