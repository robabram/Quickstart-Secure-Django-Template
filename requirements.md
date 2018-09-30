
Remember to update setup.py (install_requires) when changing this list

Note: In requirements.in leave an extra line below the last package, pip-compile
       sometimes skips the last package if there is not a new line after
       the last package.

Note: Steps to update local VE packages before running pip-compile on this file

1. run: `pip freeze > tmp_req.txt`
2. change all '==' in tmp_req.txt to '>='. Check for django package max version and set it
3. run: `pip install -r tmp_req.txt --upgrade`
4. run: `pip-compile -r -U -o requirements.txt requirements.in`

!!! This may cause App breakages, test well before sending to production !!!

