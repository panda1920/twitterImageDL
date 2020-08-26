[![panda1920](https://circleci.com/gh/panda1920/twitterImageDL.svg?style=shield)](https://app.circleci.com/pipelines/github/panda1920/twitterImageDL)

## Project overview
This simple python application allows easy collection of media files on twitter.  
No more repetitive right click-and-save!  
Intended to be used on Windows system.

## TODO
- Setup CI/CD to automatically build/distribute executable
- Brush up GUI
- Add functionality to create/delete task scheduler entry
- Adapt to new twitter APIv2.0
- Create executable for other systems (maybe)

## Building the app locally
#### Prerequisites
- Since pyinstaller is not cross-platform, you must be on windows system
- python >=3.7
- pipenv

#### Instructions
1. Clone this repo and cd into it
2. Install dependencies with command `pipenv install`
3. Execute build script build/build.bat

Built files would be located at dist/gui and dist/twitter_image_dl.  
twitter_image_dl.exe is a standalone executable that does download tasks only.

## Using the app
#### Prerequisites
- Access to twitter API
- Only works for windows system

#### Instructions
Create a file called `users.txt`.
Fill out `users.txt` with usernames you wish to collect media files from in the following way:
```
username01
username02
username03
```

Execute gui.exe.  
From the settings page, fill out your twitter API related info and your desired save location of media files.  
Make sure you hit the apply change button.  
Place `users.txt` file in the save location you specified earlier.  
Navigate back to main page and hit download button.
