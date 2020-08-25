## Project overview
This simple python application allows easy collection of media files on twitter.  
No more repetitive right click-and-save!  
Intended to be used on Windows system.

## TODO
- Setup CI/CD to automatically build/distribute executable
- Brush up GUI
- Add functionality to create/delete task scheduler entry

## Building the app locally
#### Prerequisites
- Since pyinstaller is not cross-platform, you must be on windows system
- python >=3.7
- pipenv

#### Instructions
1. Install dependencies with command `pipenv install`
2. Execute build script build/build.bat

Built files would be located at dist/gui and dist/twitter_image_dl.  
twitter_image_dl.exe is a standalone executable that does download tasks only.

## Using the app
#### Prerequisites
- You must have access to twitter API

#### Instructions
Execute GUI.exe.  
From the settings page, fill out your twitter API related info and your desired save location of media files.  
Make sure you hit the apply change button.
Back to main page and hit download button.
