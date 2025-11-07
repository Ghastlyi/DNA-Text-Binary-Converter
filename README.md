# DNA Text-Binary Converter (Flask Web App)

## Project Overview

This project is a Flask-based web application that allows users to convert data between text, binary, and DNA base sequences (A, T, G, C). It serves as an illustration of how binary data can be encoded using DNA nucleotides — a concept inspired by bioinformatics and DNA data storage systems. The application provides a simple and intuitive web interface to perform conversions instantly.

---

## How It Works

Each DNA base represents two binary bits.  
The conversion logic is based on mapping binary pairs to DNA bases as follows:  
00 → A  
01 → T  
10 → G  
11 → C  

For example:  
Text “A” → Binary “01000001” → DNA “TAAT”  
DNA “TAAT” → Binary “01000001” → Text “A”

This simple model demonstrates how computers can mimic biological information encoding systems.

---

## Features

- Converts Text ↔ Binary ↔ DNA  
- Works through a Flask web interface  
- Accurate and consistent encoding/decoding logic  
- Lightweight and easy to deploy  
- Ideal for learning bioinformatics or data encoding concepts  

---

## Installation and Setup
Open terminal and follow...


1.Clone the repository
```bash
git clone https://github.com/Ghastlyi/DNA-Text-Binary-Converter.git
cd DNA-Text-Binary-Converter
```

2.Create and activate a virtual environment

For Windows (PowerShell):
```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3.Install dependencies
```bash
pip install -r requirements.txt
```

4.Run the program
```bash
python main.py
```

## Notes on Limitations

-This project is a digital simulation only it does not perform real DNA synthesis or molecular storage.

-The mapping is simplistic (2-bit → 1 base) and lacks redundancy and advanced error correction that real DNA storage solutions require.

-Not optimized for very large files or binary streams without modifications.
