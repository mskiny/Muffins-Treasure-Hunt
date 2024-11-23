# Muffin's Treasure Hunting Tool 🐾✨

Muffin is here to sniff out your crypto treasures!

---

## 🐶 What Does This Tool Do?

Muffin's Treasure Hunting Tool scans your computer for crypto-related files, such as wallet backups, recovery phrases, or sensitive keys. It searches through all storage drives (internal and external) for keywords and patterns related to cryptocurrency wallets, private keys, seed phrases, and other important crypto goodies.

---

## 🚀 Features

- **Search for Crypto Wallets and Keys**: Includes keywords like "crypto," "wallet," "bitcoin," "ethereum," "password," and more. Supports popular and legacy wallet names like MetaMask, Phantom, Electrum, and many others.

- **Seed Phrase Detection**: Muffin sniffs out potential seed phrases by looking for sequences of 12, 15, 18, 21, or 24 words from the BIP39 mnemonic wordlist, even in files without extensions!

- **Scans File Contents**: Dives deep into the contents of `.txt`, `.docx`, `.pdf`, `.csv`, `.xlsx`, and `.json` files for relevant keywords and seed phrases.

- **Handles Image Files Intelligently**: Scans `.png`, `.jpg`, `.jpeg`, and `.gif` files if their filenames match relevant keywords, catching those sneaky screenshots of private keys or seed phrases.

- **Includes Hidden Files**: Muffin doesn't miss a spot! Hidden files and folders are included in the hunt (unless blocked by your system).

- **Dynamic Drive Scanning**: Automatically detects and scans all available drives, including external flash drives. You choose which drives Muffin should explore.

- **Smart Filtering**: Skips common system and program folders to focus on where treasures are likely hidden.

- **Friendly Console Display**: Enjoy real-time progress updates with fun emojis and messages from Muffin.

- **Error Logging**: Any hiccups during the hunt are logged separately, so Muffin can focus on finding treasures.

- **Easy-to-Read Results**: Outputs results to both a detailed text file and a filterable spreadsheet with clickable paths.

- **Cross-Platform**: Compatible with Windows, macOS, and Linux.

---

## 🛠️ How to Use It

### **Step 1: Download the Tool**

Save the `muffins_treasure_hunt.py` script to a convenient location on your computer.

### **Step 2: Install Dependencies**

Open a terminal or command prompt and run:

```bash
pip install openpyxl PyPDF2 python-docx
```

### **Step 3: Run the Tool**

In the terminal or command prompt, navigate to the directory containing the script and run:

```bash
python muffins_treasure_hunt.py
```

### **Step 4: Let Muffin Work His Magic**

- **Welcome Screen**: Muffin greets you with a fun intro and instructions.

- **Drive Selection**: Choose which drives Muffin should sniff through. Type `ALL` to scan all detected drives or specify drive letters (e.g., `C`, `D`).

- **Real-Time Logging**: Watch as Muffin explores your files, displaying updates with fun icons and file names.

### **Step 5: View the Results**

After the hunt is complete, three files will be saved in a new folder on your Desktop named `Muffins_Treasure_Hunt_Results`:

1. **Muffins_Treasure_Hunt_Path_Log.txt**:

   - Captures all console logs, including welcome messages, progress updates, errors, and final results.

2. **Muffins_Treasure_Hunt_Results.xlsx**:

   - A detailed spreadsheet with:
     - **Drive**: Where the file was found.
     - **Main Folder**: The key folder (e.g., Documents, Desktop).
     - **Keyword Match**: What caught Muffin's attention.
     - **File Type**: The file extension (e.g., `.pdf`, `.txt`).
     - **File Name**: The name of the file.
     - **File Path**: A clickable link to the file's location.

3. **Muffins_Treasure_Hunt_Errors.txt**:

   - Logs any errors encountered during the hunt, such as unreadable files.

---

## 📝 Notes

- **Safety**: This tool **does not modify or delete files**; it only searches and records findings.

- **Performance**: Depending on the size of your drives, the scan may take some time. Muffin works hard to be thorough!

- **Privacy**: All results stay on your computer—nothing is sent online. Your secrets are safe with Muffin.

- **Hidden Treasures**: Muffin looks into hidden files and folders, leaving no stone unturned.

---

## 🐾 Muffin’s Mission

Muffin’s Treasure Hunting Tool is designed to help you uncover forgotten or lost crypto-related files on your computer. Whether you're rediscovering old wallets, backups, or recovery files, Muffin is here to help sniff them out!

Let Muffin help you uncover hidden crypto treasures! 🐶💎

---

**Happy hunting! If you have any questions or need assistance, feel free to reach out. Muffin is always ready to help!**

---

*Disclaimer: Use this tool responsibly. The developers are not responsible for any misuse or unintended consequences.*
