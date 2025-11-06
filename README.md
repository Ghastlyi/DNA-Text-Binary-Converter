# DNA-Text-Binary-Converter
An easy to use Flask web app for translating tools to and from DNA, binary and text.  This project serves as an illustration of DNA data encoding, covering for informational encoding by using nucleotide bases (A,T,G,C).  

# 🧬 DNA Text-Binary Converter (Flask Web App)

## Overview
This project is a Flask-based web application that lets users convert data between **Text**, **Binary**, and **DNA sequence** formats.  
It’s inspired by the concept of **DNA data storage**, an emerging technology that uses genetic molecules to store digital data.  
The app provides an easy-to-use interface for encoding and decoding, allowing students and researchers to explore how biological systems can inspire data storage models.

---

##  How It Works
1. **Text → Binary → DNA:**  
   Each character is converted to binary, and then each binary pair is mapped to a DNA base (A, T, G, C).  
2. **DNA → Binary → Text:**  
   The sequence is decoded back to binary and then converted to readable text.  
3. **Binary ↔ DNA ↔ Text:**  
   The app allows free conversion between these three layers to demonstrate reversibility and accuracy.

---

## Technologies Used
- **Python 3.10+**
- **Flask (Web Framework)**
- **HTML, CSS (Frontend UI)**
- **Jinja2 Templating**
- **Bootstrap (for layout)**

---

## Features
- Convert **Text ↔ Binary ↔ DNA**
- Real-time results with a clean web interface
- Lightweight Flask backend, easy to run locally
- Educational demonstration of DNA-based information encoding
- Extendable for encryption or compression research

---

# clone the repo
git clone https://github.com/yourusername/DNA-Text-Binary-Converter.git
cd DNA-Text-Binary-Converter

# create and activate virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the app
python dna_converter.py

# open in browser
http://127.0.0.1:5000
