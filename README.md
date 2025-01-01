Note for Windows Users:
When you first run the game, Windows might show a security message saying "Windows protected your PC". 
This is normal for indie games that aren't digitally signed.
To run the game:
1. Click "More info"
2. Click "Run anyway"

The message appears because the game isn't signed with a digital certificate, which is expensive and usually only used by large software companies.

[Space Shooter]
-----------------

Windows Users:
1. Extract all files
2. Double-click YourGameName.exe to play

Linux Users:
1. Extract all files
2. Install Wine if you haven't' already:
sudo apt install wine
3. Open terminal in the game directory
4. Run: wine YourGameName.exe

Controls:
WASD for movement
space bar to shoot

Credits:
Andrew Vreeland



-----------------

to create more copies

cp dist/main "dist/SpaceShooter.exe"

Run commands
pyinstaller --add-data "assets:assets" --onefile main.py
wine ./dist/main