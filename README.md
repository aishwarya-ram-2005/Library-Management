<img width="1915" height="907" alt="Screenshot 2026-11-11 192103" src="https://github.com/user-attachments/assets/c3079782-09ff-4e4a-ae2a-d55e9f24a7d9" />
<img width="1917" height="906" alt="Screenshot 2026-11-11 192055" src="https://github.com/user-attachments/assets/cb2dd69f-34b3-430a-aca5-9513f3dc2632" />
<img width="1912" height="907" alt="Screenshot 2026-11-11 192044" src="https://github.com/user-attachments/assets/0c397df3-f3f1-4597-bcaa-cf779fc7010d" />
<img width="1916" height="908" alt="Screenshot 2026-11-11 192036" src="https://github.com/user-attachments/assets/989637d7-79d9-423e-b72a-fe7aa3ba801b" />
<img width="1916" height="912" alt="Screenshot 2026-11-11 192025" src="https://github.com/user-attachments/assets/f1234e2a-dfcb-4280-8c37-ad6731642531" />
<img width="1917" height="910" alt="Screenshot 2026-11-11 192010" src="https://github.com/user-attachments/assets/e9b6ed3f-d732-4dae-9899-4bf0349c712d" />
<img width="1892" height="912" alt="Screenshot 2026-11-11 191400" src="https://github.com/user-attachments/assets/33140940-e725-40fc-bfa9-bb03af069ee3" />
<img width="1917" height="907" alt="Screenshot 2026-11-11 191337" src="https://github.com/user-attachments/assets/02fd2fee-b561-4c2f-85f1-8e0f20b3f6a2" />
# Library Management System (Django + MySQL)

## Features
- Librarian registration, login and logout
- Dashboard statistics and recent activity
- Book add, edit, delete, list and search by title/author/ISBN/category
- Category management
- Member registration, edit, delete and search
- Issue and return books with 14-day due date
- Overdue indicator and simple fine calculation (₹2 per overdue day)
- Reports for available, issued and returned books
- Django admin

## Requirements
- Python 3.10+
- MySQL Server running locally
- A MySQL database named `library_db`

## Setup on Windows (PowerShell or CMD)
1. Extract this folder.
2. Open a terminal in the extracted folder (the folder containing `manage.py`).
3. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   In Command Prompt use:
   ```bat
   .venv\Scripts\activate
   ```
4. Install packages:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
   If `mysqlclient` fails to install on Windows, install a compatible MySQL client build tool or use a Python version supported by the mysqlclient wheel.
5. Create the MySQL database:
   ```sql
   CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
6. Copy `.env.example` to `.env`. Update `DB_USER` and `DB_PASSWORD` with your own MySQL username/password. Do not share your password.
7. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
8. Open `http://127.0.0.1:8000/` and log in using the superuser credentials. You can also register a librarian account.

## Notes
- This starter is for local learning/development, not production deployment.
- The fine is a sample policy of ₹2 per overdue day. Change it in `library/models.py` if your institution specifies a different rule.
- Use the same folder name and app name (`config`, `library`) when integrating into an existing project. Back up your current files before replacing them.
