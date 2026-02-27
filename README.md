# Thuiswerkvergoeder
Script to parse export from shuttle to help fill in thuiswerkvergoeding declaration

## Use
- go to shuttelportal.nl
- set language in user settings to english
- export all transactions, place excel in this folder (script will prompt with selector for right file)
- `uv sync`
- `uv run working_home.py` 
- tool presents calendar with traveled days in terminal
