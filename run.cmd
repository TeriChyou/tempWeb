@echo off
set FLASK_APP=app.py
rem 切換工作目錄至批次檔所在目錄
cd /d "%~dp0"
if not defined _OLD_VIRTUAL_PROMPT (
	call env\Scripts\activate
)
flask --debug run -h 0.0.0.0 -p 80
