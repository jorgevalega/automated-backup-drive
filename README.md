# automated-backup-drive

A silent Python-based backup automation system that creates encrypted ZIP archives and uploads them to Google Drive. Designed to run in the background with no user interface and send email reports upon completion.

---

## 🌍 Available Languages

- 🇬🇧 English – *You are here*
- 🇧🇷 [Versão em Português](https://github.com/jorgevalega/conversor-de-texto-para-ipa)
- 🇪🇸 [Versión en Español](https://github.com/jorgevalega/convertidor-de-texto-a-ipa)

---

## 🔧 Features

- 📦 Daily (partial) and weekly (general) backups
- 🔐 Encrypted ZIP files with date-based passwords
- ☁️ Automatic upload to a specific Google Drive folder
- 📧 Email report after each operation (success or failure)
- ⚙️ Designed for scheduled execution (cron, Task Scheduler, etc.)
- 🧩 Modular structure with reusable utilities

---

## 🗂️ Repository Structure

```bash
automated-backup-drive/
├── partial_backup.py         # Daily backup script
├── general_backup.py         # Weekly backup script
├── utils_backup.py           # Shared functions (zip, email, Drive upload)
├── requirements.txt
└── README.md
```
## 🛠️ Installation

### Requirements

Make sure you have **Python 3.8+** installed.

### 1. Clone the repository

```bash
git clone https://github.com/jorgevalega/automated-backup-drive.git
cd automated-backup-drive
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```
---

## ⚙️ Configuration

### Google Drive API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the **Google Drive API**
3. Create credentials and download `client_secrets.json`
4. Place the file in the project root folder

### Environment Variables

Use a `.env` file or set these directly in `utils_backup.py`:

```env
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

SOURCE_DIR=/absolute/path/to/daily/folders
GENERAL_DIR=/absolute/path/to/general/folder
```

> 💡 For Gmail accounts with 2FA, use [App Passwords](https://support.google.com/accounts/answer/185833)

---

## ▶️ Usage

### Daily Partial Backup

This script looks for a folder named like today’s date (e.g. `2025-05-06`), zips it with encryption, uploads it, and sends a report.

```bash
python partial_backup.py
```

### Weekly General Backup

This script zips the full general directory, uploads it, and sends a report. It should be run weekly.

```bash
python general_backup.py
```
---

## 🧾 Dependencies

- `pyminizip`
- `pydrive`
- `python-dotenv`

All dependencies are listed in [`requirements.txt`](requirements.txt).

---

## 🧑‍💻 Author

Developed by [Jorge Valega](https://github.com/jorgevalega) – passionate about automation and data protection with Python.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## ☕ Support

If you find this project useful, feel free to give it a ⭐️ on GitHub or share it with others!
