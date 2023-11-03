@echo off
python -m build
copy /Y dist\*.* E:\var\pypi
