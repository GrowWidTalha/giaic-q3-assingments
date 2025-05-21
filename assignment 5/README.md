# 🔒 Secure Data Encryption System

A Streamlit-based secure data storage and retrieval system that allows users to store sensitive data with unique passkeys and retrieve it securely.

## Features

- 🔐 **Secure Data Storage**: Store sensitive data with unique passkeys
- 🔑 **Passkey Protection**: Data is encrypted using Fernet symmetric encryption
- 🔒 **Enhanced Security**: 
  - PBKDF2 password hashing
  - Three-attempt limit before lockout
  - 15-minute lockout period
  - Master password authentication
- 💾 **Data Persistence**: Data is stored in a JSON file
- 🎨 **User-Friendly Interface**: Clean and intuitive Streamlit UI

## Prerequisites

- Python 3.7+
- Required packages (install using `pip install -r requirements.txt`):
  - streamlit
  - cryptography
  - python-dotenv

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd secure-data-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the application in your web browser (typically at http://localhost:8501)

3. Use the application:
   - **Store Data**: Enter your data and create a passkey
   - **Retrieve Data**: Use your Data ID and passkey to retrieve stored data
   - **Security**: After 3 failed attempts, you'll need to authenticate with the master password

## Security Notes

- The master password is set to "admin123" for demonstration purposes
- In a production environment:
  - Use a secure master password
  - Store the encryption key securely
  - Implement proper user authentication
  - Use environment variables for sensitive data

## Project Structure

```
secure-data-system/
├── app.py              # Main Streamlit application
├── encryption.py       # Encryption utilities
├── storage.py          # Data storage management
├── secure_data.json    # Encrypted data storage
└── README.md          # Project documentation
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 