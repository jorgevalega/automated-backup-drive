import os
import datetime
import logging
import smtplib
from email.message import EmailMessage
import pyminizip
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Config
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SOURCE_DIR = os.getenv("SOURCE_DIR")
GENERAL_DIR = os.getenv("GENERAL_DIR")
GDRIVE_FOLDER_NAME = "000-backups"

# Logger
logging.basicConfig(filename="backup.log", level=logging.INFO)

def get_password(date_str):
    return f"{date_str}-qW"

def zip_folder(source_folder, output_zip, password):
    file_list, rel_paths = [], []
    for root, _, files in os.walk(source_folder):
        for f in files:
            abs_path = os.path.join(root, f)
            rel_path = os.path.relpath(abs_path, source_folder)
            file_list.append(abs_path)
            rel_paths.append(rel_path)
    pyminizip.compress_multiple(file_list, rel_paths, output_zip, password, 5)

def upload_to_drive(file_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    folder_list = drive.ListFile({
        "q": f"title='{GDRIVE_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder'"
    }).GetList()
    folder_id = folder_list[0]['id'] if folder_list else None

    if not folder_id:
        folder = drive.CreateFile({
            "title": GDRIVE_FOLDER_NAME,
            "mimeType": "application/vnd.google-apps.folder"
        })
        folder.Upload()
        folder_id = folder['id']

    f = drive.CreateFile({'title': os.path.basename(file_path), 'parents': [{'id': folder_id}]})
    f.SetContentFile(file_path)
    f.Upload()

def send_email(subject, body):
    msg = EmailMessage()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.set_content(body)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

def perform_partial_backup():
    today = datetime.date.today().isoformat()
    src_folder = os.path.join(SOURCE_DIR, today)
    zip_name = f"{today}.zip"
    zip_path = os.path.join(SOURCE_DIR, zip_name)
    password = get_password(today)

    try:
        if not os.path.exists(src_folder):
            raise Exception(f"Source folder not found: {src_folder}")
        zip_folder(src_folder, zip_path, password)
        upload_to_drive(zip_path)
        send_email("Partial Backup Success", f"File: {zip_name}\nUploaded to: {GDRIVE_FOLDER_NAME}")
        logging.info(f"Partial backup completed: {zip_name}")
    except Exception as e:
        logging.error(str(e))
        send_email("Partial Backup Failed", str(e))

def perform_general_backup():
    today = datetime.date.today().isoformat()
    zip_name = f"g-{today}.zip"
    zip_path = os.path.join(SOURCE_DIR, zip_name)
    password = get_password(today)

    try:
        if not os.path.exists(GENERAL_DIR):
            raise Exception(f"General folder not found: {GENERAL_DIR}")
        zip_folder(GENERAL_DIR, zip_path, password)
        upload_to_drive(zip_path)
        send_email("General Backup Success", f"File: {zip_name}\nUploaded to: {GDRIVE_FOLDER_NAME}")
        logging.info(f"General backup completed: {zip_name}")
    except Exception as e:
        logging.error(str(e))
        send_email("General Backup Failed", str(e))
