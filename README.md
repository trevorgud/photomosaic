# photomosaic
Tool for creation of photo mosaic from a directory of photos

### Install and run
```powershell
python3 -m venv .venv
# May need to update execution policy in order to run the activate script:
# Set-ExecutionPolicy RemoteSigned
.\.venv\Scripts\activate.ps1
python3 -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python ./src/main.py
```

```powershell
# To auto detect and prompt for rotation, iterating over each photo:
.\.venv\Scripts\python ./src/rotation.py
# Will prompt twice when detecting a suspicious photo. It will also open the unrotated photo in view mode.
# Will once prompt for rotation angle, where you put a number of degrees for rotation (90, -90, 180).
# After putting in the angle, it will open another photo that is the original, rotated by that amount.
# Then a second prompt to confirm, and only valid answer is a single character 'y'.
```
