# ⚕️ ECG File Visualizer

A simple web application designed for the rapid visualization of standard WFDB format electrocardiogram (ECG) files (`.hea` and `.dat`). Users can upload their files and receive high-quality graphical outputs in both SVG (vector) and PNG (raster) formats.

This project is built with Python and Streamlit, intended for researchers, students, and medical professionals who need a quick way to visually analyze ECG data without installing local software.

**[ ➡️ LIVE DEMO LINK ⬅️ ](https://ecg-visualizer.onrender.com)**


## 🚀 Features

-   **Multiple File Upload:** Upload multiple `.hea` and `.dat` files simultaneously.
-   **Automatic Processing:** Automatically processes 12-lead ECG signals and generates standard plots.
-   **Dual Format Output:** Results are generated in both high-quality SVG and PNG formats.
-   **Simple Interface:** A clean, minimalist, and intuitive user interface.
-   **Batch Download:** All processed files are bundled into a single ZIP archive for easy downloading.
-   **Open Source:** The project is fully open-source and available on GitHub.

---

## ⚙️ How to Use

1.  Navigate to the **Live Demo** link above.
2.  Click the **"Browse files"** button to select your `.hea` and `.dat` files.
3.  Once the files are selected, click the **"🚀 Start Processing"** button.
4.  Wait for the processing to complete.
5.  After processing, a **"📥 Download Results (ZIP)"** button will appear. Click it to download the archive to your computer.

---

## 💻 Local Installation

If you wish to run the project on your local machine:

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/ecg-webapp.git](https://github.com/YOUR_USERNAME/ecg-webapp.git)
cd ecg-webapp
```
*(Replace `YOUR_USERNAME/ecg-webapp.git` with your repository's URL)*

**2. (Recommended) Create and activate a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the Streamlit application:**
```bash
streamlit run app.py
```
The application will open in your web browser, typically at `http://localhost:8501`.

---

## 🛠️ Tech Stack

-   **Backend:** Python
-   **Web Framework:** Streamlit
-   **Data Processing:**
    -   `wfdb` - For reading WFDB database files.
    -   `numpy` - For numerical operations on data arrays.
    -   `matplotlib` & `ecg-plot` - For plotting ECG signals.
-   **Deployment:** Render.com

---

## 📄 License

This project is distributed under the MIT License.

**Copyright (c) 2025 Cordica Inc.**
