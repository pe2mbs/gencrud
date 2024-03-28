@echo off
python -m build --wheel
copy /Y dist\*.* E:\var\pypi
