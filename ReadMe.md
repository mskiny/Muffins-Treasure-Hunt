# Muffin's Treasure Hunting Tool 🐾✨

**Muffin is here to sniff out your crypto treasures!**  

---
## 🐶 What Does This Tool Do?

Muffin's Treasure Hunting Tool scans your computer for crypto-related files, such as wallet backups, recovery phrases, or sensitive keys. It searches through all storage drives (internal and external) for keywords related to cryptocurrency wallets, private keys, and other important crypto-related information.

The results are saved in:

1. **A text file** for easy viewing, which includes all console logs and messages.
2. **A spreadsheet** with advanced filtering, sorting, and clickable paths.
3. **An error log** to capture any processing issues for review.

---
## 🚀 Features:

- **Search for Crypto Wallets and Keys:** Includes keywords like "crypto," "wallet," "bitcoin," "ethereum," "password," and more. Supports popular and legacy wallet names like MetaMask, Phantom, and Electrum.
- **Scans File Contents:** Searches the contents of `.txt`, `.docx`, `.pdf`, `.csv`, `.xlsx`, and `.json` files for relevant keywords.
- **Handles Image Files Intelligently:** Scans `.png`, `.jpg`, `.jpeg`, and `.gif` files **only if their filenames** match relevant keywords, to detect potential screenshots of private keys or seed phrases.
- **Dynamic Drive Scanning:** Automatically detects and scans all available drives, including external flash drives.
- **Smart Filtering for Program Assets:** Excludes common paths and folders containing program assets, such as `images`, `icons`, and `AppData`.
- **Friendly Console Display:** Real-time progress updates, emojis, and drive selection prompts.
- **Error Logging:** Captures any file-reading or processing errors in a dedicated log file.
- **Easy-to-Read Results:** Outputs results to both a detailed text file and a filterable spreadsheet with clickable paths.
- **Cross-Platform:** Compatible with Windows and macOS.

---
## 🛠️ How to Use It  

### Step 1: Download the Tool  

1. Visit the GitHub repository hosting Muffin's Treasure Hunting Tool.  
2. Download the correct file for your operating system:  
   - **Windows:** `Muffins_Treasure_Hunt_Windows.zip`  
   - **Mac:** `Muffins_Treasure_Hunt_Mac.zip`  

---
### Step 2: Extract the Files  

- **Windows:**  
   1. Right-click the `.zip` file and select "Extract All."  
   2. Open the extracted folder.  

- **Mac:**  
   1. Double-click the `.zip` file to extract it.  
   2. Open the extracted folder.  

---
### Step 3: Run the Tool  

- **Windows:**  
   1. Double-click the file named `Muffins_Treasure_Hunt_Windows.exe`.  
   2. If Windows blocks the program, click **More Info > Run Anyway**.  

- **Mac:**  
   1. Double-click the file named `Muffins_Treasure_Hunt_Mac`.  
   2. If macOS blocks the program:  
      - Go to **System Preferences > Security & Privacy > Open Anyway**.  
      - Alternatively, run the following command in Terminal:  
        ```bash
        xattr -d com.apple.quarantine /path/to/Muffins_Treasure_Hunt_Mac
        ```

---
### Step 4: Select Drives and Watch the Magic  

1. **Welcome Screen:** The program will display an intro screen with information about its functionality.  
2. **Drive Selection:** You'll be prompted to select the drives you want Muffin to scan by entering the corresponding numbers.  
3. **Real-Time Logging:** As Muffin sniffs through your files, you'll see updates in the console with fun icons and file names.  

---
### Step 5: View the Results  

After the hunt is complete, three files will be saved in a new folder on your Desktop named **Muffins_Treasure_Hunt_Results**:

1. **`Muffins_Treasure_Hunt_Path_Log.txt`:**  
   - Captures all console logs, including welcome messages, progress updates, errors, and final results.  

2. **`Muffins_Treasure_Hunt_Results.xlsx`:**  
   - A detailed spreadsheet with:  
     - **Drive**: The drive where the file was found.  
     - **Top Folder**: The highest folder after the drive.  
     - **Bottom Folder**: The immediate folder containing the file.  
     - **Keyword Match**: The matched keyword(s) triggering the result.  
     - **File Extension**: The file extension (e.g., `.pdf`, `.txt`).  
     - **File Name**: The name of the file.  
     - **File Path**: A clickable link to the file's folder (not the file itself).  

3. **`Muffins_Treasure_Hunt_Errors.txt`:**  
   - Logs any errors encountered during processing, such as unreadable files or unsupported formats.  

---
## 📝 Notes:

- **Safety:** This tool does not modify or delete files; it only searches and records.  
- **Performance:** Depending on the size of your drives, the scan may take some time.  
- **Privacy:** Results stay on your computer—nothing is sent online.  

---
## 🐾 Muffin’s Mission:

Muffin’s Treasure Hunting Tool is designed to uncover forgotten or lost crypto-related files from your computer. It’s perfect for anyone looking to rediscover hidden treasures from old wallets, backups, and recovery files.  

Let Muffin help you uncover hidden crypto treasures! 🐶💎  

For any questions, reach out via the GitHub repository's **Issues** section.  

🐾✨
