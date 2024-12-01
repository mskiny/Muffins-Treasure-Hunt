# 🐶 Muffin's Treasure Hunt 🐾


## 🏆 Sniffing Out Crypto Treasures! 🏆

Welcome to **Muffin's Treasure Hunt**! 🐾🐶 Your friendly neighborhood doggo here, ready to help you sniff out those elusive crypto treasures hiding in the nooks and crannies of your computer. Whether it's wallets, keys, recovery phrases, or other sensitive information, Muffin's got your back!

---

## 🔍 What Does Muffin's Treasure Hunt Do?

- **🦴 Searches Files:** Scans files like `.txt`, `.docx`, `.pdf`, and more for crypto-related keywords.
- **🐕 Performs OCR:** Extracts text from image files to find hidden information.
- **📂 Excludes System Directories:** Skips directories and folders that are unlikely to contain relevant data to reduce noise.
- **💼 Generates Reports:** Outputs results to both a text file and an Excel spreadsheet for easy review.

---

## 🚀 Getting Started

Ready to embark on this treasure hunt? Follow the steps below to set up Muffin's Treasure Hunt on your machine. It's paws-itively easy! 🐾

### 🐱‍👤 Prerequisites

Before you begin, ensure you have the following installed on your computer:

- **Python 3.8 or higher** 🐍
  - [Download Python](https://www.python.org/downloads/)
- **Visual Studio Code (VS Code)** 💻
  - [Download VS Code](https://code.visualstudio.com/download)

---

## 🛠️ Installation Steps

#### 1. **Clone the Repository**

Open your terminal or command prompt and navigate to the directory where you want to place the project. Then, clone the repository:

```bash
git clone https://github.com/mskiny/muffins-treasure-hunt.git
```
#### 2. **Navigate to the Project Directory**

```bash
cd muffins-treasure-hunt
```

#### 3. **Set Up a Virtual Environment**

It's best to use a virtual environment to manage dependencies without affecting your global Python setup.

- **Windows:**

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **Mac:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### 4. **Install Required Libraries**

With your virtual environment activated, install the necessary Python packages:

```bash
pip install -r requirements.txt
```

📝 **Package Descriptions:**

- **`tqdm`** 🐢: Adds a stylish progress bar to your loops, making your treasure hunt feel even more dynamic!
- **`openpyxl`** 📊: Handles Excel file creation and manipulation, perfect for those detailed treasure reports.
- **`PyPDF2`** 📄: Reads and extracts text from PDF files, ensuring no treasure goes unnoticed.
- **`python-docx`** 📑: Interacts with Word documents, keeping an eye out for crypto clues.
- **`pytesseract`** 🖼️: Integrates OCR capabilities to extract text from images—because treasures can be hidden in pictures too!
- **`Pillow`** 🖌️: Enhances image processing, making sure your OCR hunts are spot-on.

#### 5. **Install Tesseract OCR**

**Muffin's Treasure Hunt** uses Tesseract for OCR to extract text from images.

- **Windows:**
  1. [Download Tesseract OCR](https://github.com/tesseract-ocr/tesseract/releases/latest)
  2. Run the installer and follow the prompts.
  3. **Important:** After installation, add Tesseract to your system's PATH or specify its path in the script by uncommenting and updating the following line in `Muffins_Treasure_Hunt.py`:

     ```python
     # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
     ```

- **Mac:**

  Install via Homebrew:

  ```bash
  brew install tesseract
  ```

---

## 🐾 Running Muffin's Treasure Hunt

1. **Open the Project in VS Code**

   ```bash
   code .
   ```

2. **Ensure Virtual Environment is Activated**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **Mac:**

     ```bash
     source venv/bin/activate
     ```

3. **Run the Script**

   ```bash
   python Muffins_Treasure_Hunt.py
   ```

4. **Follow the On-Screen Prompts**

   - **Select Drives:** Choose the drives you want Muffin to search or type `ALL` to scan all available drives.
   - **Sit Back & Relax:** Let Muffin do the magic! 🪄
   - **Review Reports:** After the hunt, check the generated reports on your Desktop in the `Muffins_Treasure_Hunt_Results` folder.

---

## 📂 Results

After the hunt, Muffin will generate two reports:

- **Text File:** `Muffins_Treasure_Hunt_Path_Log.txt` – A plain text summary of all findings.
- **Excel Spreadsheet:** `Muffins_Treasure_Hunt_Results.xlsx` – A detailed, organized spreadsheet with all the treasures Muffin uncovered.

Both files will be located in the `Muffins_Treasure_Hunt_Results` folder on your Desktop. Dive in and see what treasures await! 🎉

---

## 📚 Additional Notes

- **BIP39 Wordlist:** Ensure that the `bip39_wordlist.txt` file is present in the same directory as `Muffins_Treasure_Hunt.py`. This file is essential for detecting valid seed phrases.

- **Tesseract Configuration:** If Tesseract OCR is not added to your system's PATH, make sure to specify its path in the script by uncommenting and updating the relevant line as mentioned in the installation steps.

- **Operating System Compatibility:** The script is compatible with both Windows and Mac. Adjust the installation steps accordingly based on your operating system.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Happy Hunting! May your drives be treasure-filled and your crypto safe! 🐾🔒*
