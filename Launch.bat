@ECHO OFF
net start MongoDB
start cmd.exe /C "C:\Users\scg\Documents\Cursus_env\Scripts\activate && cd C:\Users\scg\Documents\Rest_project\mainproject & python manage.py creationofsuperuser & python manage.py runserver 0.0.0.0:8000"
SLEEP 12
start "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "http://127.0.0.1:8000/mainapp/"