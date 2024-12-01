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

### 🛠️ Installation Steps

#### 1. **Clone the Repository**

Open your terminal or command prompt and navigate to the directory where you want to place the project. Then, clone the repository:

```bash
git clone https://github.com/mskiny/muffins-treasure-hunt.git
```

*Replace `yourusername` with your actual GitHub username.*

#### 2. **Navigate to the Project Directory**

```bash
cd muffins-treasure-hunt
```

#### 3. **Set Up a Virtual Environment**

It's a good practice to use a virtual environment to manage dependencies.

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

With the virtual environment activated, install the necessary Python packages:

```bash
pip install -r requirements.txt
```

*If you don't have a `requirements.txt`, you can install them manually:*

```bash
pip install openpyxl PyPDF2 python-docx pytesseract pillow tqdm
```

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

### 🐾 Running the Script

Now that everything is set up, it's time to let Muffin hunt for treasures!

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

   - Select the drives you want Muffin to search.
   - Let Muffin do the magic! 🪄
   - Review the generated reports on your Desktop in the `Muffins_Treasure_Hunt_Results` folder.

---

## 📂 Results

After the hunt, Muffin will generate two reports:

- **Text File:** `Muffins_Treasure_Hunt_Path_Log.txt`
- **Excel Spreadsheet:** `Muffins_Treasure_Hunt_Results.xlsx`

Find them on your Desktop in the `Muffins_Treasure_Hunt_Results` folder. Dive in and see what treasures Muffin uncovered! 🎉

---

## 🐾 Contributing

Muffin's Treasure Hunt is a community-driven project. If you'd like to contribute:

1. Fork the repository.
2. Create your feature branch:

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add some feature"
   ```

4. Push to the branch:

   ```bash
   git push origin feature/YourFeatureName
   ```

5. Open a pull request! 🐕

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Happy Hunting! May your drives be treasure-filled and your crypto safe! 🐾🔒*
