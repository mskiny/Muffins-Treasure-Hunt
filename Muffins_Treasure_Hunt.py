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
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Paths for results
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Muffins_Treasure_Hunt_Results")
CONSOLE_LOG_FILE = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Console_Log.txt")
ERROR_LOG_FILE = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Errors.txt")

# Ensure the results directory exists
os.makedirs(DESKTOP_PATH, exist_ok=True)

# Configuration settings
CONFIG = {
    "include_paths": [],  # Directories to include (empty means include all)
    "exclude_paths": [],  # Additional directories to exclude
    "include_extensions": [],  # File extensions to include (empty means include all)
    "exclude_extensions": [
        ".exe", ".dll", ".sys", ".tmp", ".log", ".ini", ".js", ".ts",
        ".mp3", ".mp4", ".avi", ".mkv", ".flv", ".mov", ".wmv",
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".psd", ".ai", ".eps", ".svg",
        ".class", ".jar", ".war", ".ear", ".so", ".a", ".lib", ".o",
        ".apk", ".ipa", ".bin", ".pak", ".iso", ".plist",
        ".db", ".db3", ".sql", ".sqlite", ".sqlite3",
        ".pem", ".key"  # Added to exclude certificate and key files
    ],
    "log_level": "INFO",  # Set to "DEBUG" for more detailed logs
    "max_threads": 4  # Adjust based on your system's capabilities
}

# Set up logging
logging.basicConfig(
    level=getattr(logging, CONFIG.get("log_level", "INFO").upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(CONSOLE_LOG_FILE, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

# Global Variables
KEYWORDS_ICONS = {
    "crypto": "🪙",
    "wallet": "💰",
    "bitcoin": "₿",
    "ethereum": "Ξ",
    "doge": "🐕",
    "key": "🔑",
    "phrase": "✍️",
    "secret": "🤫",
    "password": "🔒",
    "passphrase": "✏️",
    "xpub": "📜",
    "0x": "📬",
    "backup": "📂",
    "seed": "🌱",
    "private": "🕶️",
    "credentials": "📋",
    "blockchain": "⛓️",
    "coins": "💵",
    "hash": "🔗",
    "wallet.dat": "📄",
    "mnemonic": "🧠",
    "recovery": "📦",
    "restore": "🔄",
    "seed phrase": "🔐",
    "secret phrase": "🔓",
    "metamask": "🦊",
    "phantom": "👻",
    "keystore": "📁",
    "ledger": "📒",
    "trezor": "🔐",
    "cold storage": "❄️",
    "private_key": "🗝️",
    "xprv": "📜",
    "encrypted": "🔒",
    "kdfparams": "📑",
    "cipher": "🔐",
    "ciphertext": "🔏",
    "btc": "₿",
    "eth": "Ξ",
    "exodus": "📂",
    "trustwallet": "🔒",
    "binance": "⚡",
    "kraken": "🐙"
}

# Folders to exclude (excluding unnecessary asset folders)
EXCLUDED_FOLDERS = [
    "node_modules", "__pycache__", ".git", ".svn", "build", "dist",
    "Library", "Logs", "Temp", "Cache", "Caches", "venv", "env",
    "VirtualEnv", "Anaconda3", "Miniconda3", "System Volume Information",
    "$Recycle.Bin",
    "Program Files\\Common Files",
    "Program Files\\Windows Defender",
    "Program Files\\WindowsApps",
    "Assets", "Images", "Resources"  # Exclude common asset folders
] + CONFIG.get("exclude_paths", [])

# File extensions to include or exclude
INCLUDED_EXTENSIONS = CONFIG.get("include_extensions", [])
IGNORED_EXTENSIONS = CONFIG.get("exclude_extensions", [])

SEED_WORD_COUNTS = [12, 15, 18, 21, 24]

# Load mnemonic wordlist
def load_mnemonic_wordlist():
    wordlist_file = os.path.join(os.path.dirname(__file__), "bip39_wordlist.txt")
    try:
        with open(wordlist_file, "r", encoding="utf-8") as f:
            words = f.read().splitlines()
            return set(words)
    except Exception as e:
        logger.error(f"Error loading mnemonic wordlist: {e}")
        sys.exit(1)

MNEMONIC_WORDLIST = load_mnemonic_wordlist()

def get_drives():
    """
    Detect available drives to scan.
    """
    if platform.system() == "Windows":
        import string
        return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    else:
        return ["/"]

def display_intro_and_select_drives():
    """
    Display introductory text and prompt the user to select drives to scan.
    """
    print("🔍 Welcome to Muffin's Treasure Hunting Tool!")
    print("🐾 Muffin is here to help sniff out crypto treasures!")
    print("\nWhat does this tool do?")
    print("🦴 Searches your drives for crypto wallets, keys, and related treasures.")
    print("📄 Scans files for sensitive data, including text, spreadsheets, and more.")
    print("📊 Exports results to both a text file and a spreadsheet.")
    print("\n🐶 Let’s get started! Muffin is ready to sniff out hidden treasures!")
    print("\n------------------------------------------------------------\n")

    # Detect drives
    drives = get_drives()
    if not drives:
        logger.error("No drives detected. Exiting...")
        sys.exit(0)

    if platform.system() == "Windows":
        print(f"1. Type ALL to scan all of the 📂 Detected Drives: {' '.join(drives)}")
        print("2. Or type only drive letters you want to scan separated by spaces (e.g., C or C D or E).")
    else:
        print(f"📂 On this system, the following drives are detected: {' '.join(drives)}")
        print("1. Type ALL to scan all detected drives.")
        print("2. Or type the paths you want to scan separated by spaces (e.g., / or / /mnt/data).")

    print()  # Adds a blank line for better readability
    print("✨Type your answer and press Enter to continue:", flush=True)  # Ensures immediate display

    # User input for drive selection
    response = input().strip().upper()
    if response == "ALL":
        return drives
    else:
        selected_drives = []
        if platform.system() == "Windows":
            for d in response.split():
                drive = f"{d.upper()}:\\" if not d.endswith(":\\") else d.upper()
                if drive in drives:
                    selected_drives.append(drive)
                else:
                    logger.warning(f"Drive {d} is not a valid drive.")
        else:
            for d in response.split():
                if os.path.exists(d):
                    selected_drives.append(d)
                else:
                    logger.warning(f"Path {d} is not a valid path.")
        if not selected_drives:
            logger.error("No valid drives selected. Exiting...")
            sys.exit(0)
        return selected_drives

def is_valid_ethereum_address(address):
    """
    Check if a string is a valid Ethereum address.
    """
    match = re.fullmatch(r"0x[a-fA-F0-9]{40}", address)
    return bool(match)

def is_valid_bitcoin_address(address):
    """
    Check if a string is a valid Bitcoin address.
    """
    btc_regex = r"^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,39}$"
    return bool(re.match(btc_regex, address))

def contains_json_wallet_structure(file_path):
    """
    Check if a JSON file contains wallet structure indicators.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return any(key in content for key in ["ciphertext", "cipherparams", "kdfparams", "mac", "address", "version"])
    except Exception as e:
        logger.debug(f"Error reading JSON file {file_path}: {e}")
    return False

def scan_spreadsheet(file_path):
    """
    Scan a spreadsheet file for crypto-related keywords.
    Returns a list of matched keywords.
    """
    matched_keywords = []
    try:
        if file_path.endswith(".csv"):
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    for cell in row:
                        for keyword in KEYWORDS_ICONS:
                            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                            if re.search(pattern, str(cell).lower()):
                                matched_keywords.append(keyword)
        else:
            workbook = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
            for sheet in workbook.sheetnames:
                ws = workbook[sheet]
                for row in ws.iter_rows(values_only=True):
                    for cell in row:
                        if cell:
                            cell_str = str(cell).lower()
                            for keyword in KEYWORDS_ICONS:
                                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                                if re.search(pattern, cell_str):
                                    matched_keywords.append(keyword)
    except Exception as e:
        logger.debug(f"Error reading spreadsheet {file_path}: {e}")
    return list(set(matched_keywords))  # Remove duplicates

def detect_seed_phrase(content):
    """
    Detect potential seed phrases in the content.
    Returns a tuple (found: bool, words: list)
    """
    words = re.findall(r'\b\w+\b', content.lower())
    for count in SEED_WORD_COUNTS:
        for i in range(len(words) - count + 1):
            word_sequence = words[i:i+count]
            if all(word in MNEMONIC_WORDLIST for word in word_sequence):
                return True, word_sequence  # Return the matching sequence
    return False, []

def search_file_content(file_path):
    """
    Search the content of a file for crypto-related keywords and seed phrases.
    Returns a list of matched keywords.
    """
    matched_keywords = []
    try:
        if file_path.endswith(".txt") or '.' not in os.path.basename(file_path):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            content = "\n".join(para.text for para in doc.paragraphs)
        elif file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            content = "\n".join(page.extract_text() or '' for page in reader.pages)
        else:
            return matched_keywords

        for keyword in KEYWORDS_ICONS:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, content.lower()):
                matched_keywords.append(keyword)

        seed_phrase_found, seed_phrase_words = detect_seed_phrase(content)
        if seed_phrase_found:
            matched_keywords.append("seed_phrase")

    except Exception as e:
        logger.debug(f"Error processing file {file_path}: {e}")
    return list(set(matched_keywords))  # Remove duplicates

def process_file(file_path):
    """
    Process a single file to check for crypto-related content.
    Returns a dictionary with file details if a match is found, else None.
    """
    try:
        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1].lower()

        if IGNORED_EXTENSIONS and file_extension in IGNORED_EXTENSIONS:
            return None

        if INCLUDED_EXTENSIONS and file_extension not in INCLUDED_EXTENSIONS:
            return None

        matched_keywords = [kw for kw in KEYWORDS_ICONS if kw.lower() in file_name.lower()]

        # Validate Ethereum address if '0x' is present
        if "0x" in matched_keywords and not is_valid_ethereum_address(file_name):
            matched_keywords.remove("0x")
        # Validate Bitcoin address
        if is_valid_bitcoin_address(file_name):
            matched_keywords.append("bitcoin_address")
        # Check for JSON wallet structure
        if file_extension == ".json" and contains_json_wallet_structure(file_path):
            matched_keywords.append("json_wallet")
        # Scan spreadsheets
        if file_extension in [".xlsx", ".xls", ".csv"]:
            spreadsheet_keywords = scan_spreadsheet(file_path)
            matched_keywords.extend(spreadsheet_keywords)
        # Scan file content for other file types
        if not matched_keywords and file_extension in [".txt", ".docx", ".pdf"]:
            content_keywords = search_file_content(file_path)
            matched_keywords.extend(content_keywords)

        # Contextual Validation: Skip if file is in a known safe directory
        # (Add any directories you consider safe here)
        safe_directories = [
            os.path.join(os.environ.get('ProgramFiles', ''), 'SomeKnownSafeDir'),
            # Add other safe directories as needed
        ]
        if any(file_path.startswith(safe_dir) for safe_dir in safe_directories):
            return None

        if matched_keywords:
            icon = KEYWORDS_ICONS.get(matched_keywords[0], "📄")
            main_folder = os.path.basename(os.path.dirname(file_path))

            result = {
                "Drive": os.path.splitdrive(file_path)[0],
                "Main Folder": main_folder,
                "Keyword Match": ", ".join(set(matched_keywords)),
                "File Extension": file_extension,
                "File Name": file_name,
                "Folder Path": os.path.dirname(file_path),
            }
            logger.info(f"{icon} Found: {file_name}")
            return result
    except Exception as e:
        logger.debug(f"Error processing file {file_path}: {e}")
    return None

def search_files(drive):
    """
    Recursively searches the specified drive for files matching crypto-related keywords.
    Returns a list of found items.
    """
    found_items = []
    file_paths = []

    logger.info(f"🔍 Searching drive {drive}...")
    for root, dirs, files in os.walk(drive, topdown=True):
        # Exclude irrelevant folders
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    # Use multithreading to process files
    with ThreadPoolExecutor(max_workers=CONFIG.get("max_threads", 4)) as executor:
        futures = {executor.submit(process_file, fp): fp for fp in file_paths}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning files"):
            result = future.result()
            if result:
                found_items.append(result)

    return found_items

def export_results(found_items):
    """
    Export the search results to a text file and an Excel spreadsheet.
    """
    text_file = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Path_Log.txt")
    excel_file = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Results.xlsx")

    # Export to Text File
    try:
        with open(text_file, "w", encoding="utf-8") as txt:
            txt.write("🔍 Muffin's Treasure Hunt Results\n")
            txt.write(f"🏆 Total treasures found: {len(found_items)}\n\n")
            for item in found_items:
                txt.write(f"Drive: {item['Drive']} | Folder: {item['Main Folder']} | File: {item['File Name']} | Path: {item['Folder Path']}\n")
        logger.info(f"📄 Text File: {text_file}")
    except Exception as e:
        logger.error(f"Failed to write text file: {e}")

    # Export to Excel Spreadsheet
    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Muffin's Results"

        headers = ["Drive", "Main Folder", "Keyword Match", "File Extension", "File Name", "Folder Path"]
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
            folder_path_cell = sheet.cell(row=row_num, column=6)
            folder_path_cell.value = item["Folder Path"]

        for col in range(1, len(headers) + 1):
            sheet.column_dimensions[get_column_letter(col)].width = 25

        workbook.save(excel_file)
        logger.info(f"📊 Spreadsheet: {excel_file}")
    except Exception as e:
        logger.error(f"Failed to write Excel file: {e}")

    logger.info(f"🏆 Total treasures found: {len(found_items)} 🐾")

def muffins_treasure_hunt():
    """
    Main function to run Muffin's Treasure Hunt.
    """
    start_time = time.time()
    selected_drives = display_intro_and_select_drives()
    all_found_items = []
    for drive in selected_drives:
        found_items = search_files(drive)
        all_found_items.extend(found_items)
    export_results(all_found_items)
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"\n⏰ Total time taken: {total_time:.2f} seconds")
    logger.info("\n🐶 Muffin's hunt is complete! Happy treasure hunting! 🦴")

if __name__ == "__main__":
    try:
        muffins_treasure_hunt()
    except KeyboardInterrupt:
        logger.warning("\n🛑 Scan interrupted by user. Exiting gracefully.")
