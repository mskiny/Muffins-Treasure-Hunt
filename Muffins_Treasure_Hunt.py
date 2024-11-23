import os
import platform
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
import time
import re
from PyPDF2 import PdfReader
from docx import Document
import msvcrt  # For Windows keyboard input handling

# Function to display intro with countdown and skip option
def display_intro():
    countdown = 30
    print("🔍 Welcome to Muffin's Treasure Hunting Tool!")
    print("🐾 Muffin is here to help sniff out crypto treasures!")
    print("\nWhat does this tool do?")
    print("🦴 Searches your drives for crypto wallets, keys, and related treasures.")
    print("📄 Scans the content of .docx, .pdf, and .txt files for deeper insights.")
    print("📊 Exports results to both a text file and a spreadsheet.")
    print("\n🐶 Sniffing will start soon... Please be patient!")
    print("------------------------------------------------------------")
    print("⏳ Starting in 30 seconds. Press any key to start immediately.", flush=True)

    while countdown > 0:
        print(f"\r⏳ Starting in {countdown} seconds...", end="", flush=True)
        if msvcrt.kbhit():  # Check if a key is pressed
            msvcrt.getch()  # Consume the keypress
            print("\r🚀 Skipping countdown and starting immediately!          ", flush=True)
            break
        time.sleep(1)
        countdown -= 1

    print("\n🚀 Starting search now!", flush=True)

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
    "passphrase": "✏️", "xpub": "📜", "0x": "📬", "backup": "📂", "seed": "🌱", 
    "private": "🕶️", "account": "🧾", "credentials": "📋", "2FA": "🔑"
}
IGNORED_EXTENSIONS = [".exe", ".dll", ".sys", ".tmp", ".log", ".ini", ".dat"]

# Validate Ethereum addresses
def is_valid_ethereum_address(file_name):
    return bool(re.search(r"\b0x[a-fA-F0-9]{40}\b", file_name))

# Validate Bitcoin public or private keys
def is_valid_bitcoin_key(file_name):
    btc_regex = r"\b(5[HJK][1-9A-HJ-NP-Za-km-z]{49,50}|[13][1-9A-HJ-NP-Za-km-z]{26,35})\b"
    return bool(re.search(btc_regex, file_name))

# Search for JSON wallet structures
def contains_json_wallet_structure(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return any(key in content for key in ["ciphertext", "cipherparams", "kdfparams", "mac", "address"])
    except Exception as e:
        print(f"⚠️ Error reading file {file_path}: {e}", flush=True)
    return False

# Search file content for keywords
def search_file_content(file_path, keywords):
    try:
        # TXT file
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if any(keyword.lower() in content.lower() for keyword in keywords):
                    return True
        # DOCX file
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])
            if any(keyword.lower() in content.lower() for keyword in keywords):
                return True
        # PDF file
        elif file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            content = "\n".join([page.extract_text() for page in reader.pages])
            if any(keyword.lower() in content.lower() for keyword in keywords):
                return True
    except Exception as e:
        print(f"⚠️ Error processing file {file_path}: {e}", flush=True)
    return False

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

            # Special handling for "0x" and Ethereum addresses
            if "0x" in keyword_matches and not is_valid_ethereum_address(file_name):
                keyword_matches.remove("0x")

            # Check for Bitcoin public/private keys
            if is_valid_bitcoin_key(file_name):
                keyword_matches.append("bitcoin_key")

            # Check for JSON wallet structure
            if file_extension == ".json" and contains_json_wallet_structure(file_path):
                keyword_matches.append("json_wallet")

            # Deep content search for specific file types
            if not keyword_matches and file_extension in [".txt", ".docx", ".pdf"]:
                print(f"📄 Scanning content of {file_path}...", flush=True)
                if search_file_content(file_path, KEYWORDS_ICONS.keys()):
                    keyword_matches = ["content_match"]

            if keyword_matches:
                icon = KEYWORDS_ICONS.get(keyword_matches[0], "📄")  # Use first matched keyword's icon

                # Determine Main Folder
                if root.startswith(f"{drive}Users"):
                    parts = root.split(os.sep)
                    main_folder = parts[2] if len(parts) > 2 else "Unknown"
                else:
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
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Muffins_Treasure_Hunt_Results")
    os.makedirs(desktop_path, exist_ok=True)
    text_file = os.path.join(desktop_path, "Muffins_Treasure_Hunt_Path_Log.txt")
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
