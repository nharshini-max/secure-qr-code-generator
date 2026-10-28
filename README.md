# Secure QR Code Generator 🔐

A Python-based application that encrypts confidential information before encoding it into a QR code.

## Features
- AES-256-GCM authenticated encryption
- QR code generation using Python
- QR detection and data extraction using OpenCV
- Decryption through a Streamlit interface
- Authentication checks to detect modified encrypted data

## Technologies
Python, Streamlit, Cryptography, OpenCV, NumPy, Pillow, QRCode.

## How It Works
1. Enter a sample message.
2. Encrypt the message using AES-256-GCM.
3. Encode the encrypted data into a QR code.
4. Upload the QR image to the application.
5. Extract the encrypted data and decrypt it using the corresponding key.

## Run Locally
Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal.

## Security
The QR code stores encrypted data rather than the original plaintext. Decryption requires the corresponding secret key. The key must be stored securely and must never be committed to a public repository.

This is an academic learning prototype, not a production security service.

## Project Outcome
The application demonstrated successful QR generation, QR detection, encrypted-data extraction, and decryption with the corresponding key.
