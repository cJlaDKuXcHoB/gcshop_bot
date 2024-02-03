@echo off

call %~dp0gcshop_bot\venv\Scripts\activate

cd %~dp0gcshop_bot

set TOKEN=5805237480:AAGvqKA0oQenOe3ffnlYjMhD5LXnzaM7Yrk

set ADMIN=1814848272

python bot.py 

pause