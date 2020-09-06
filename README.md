[![panda1920](https://circleci.com/gh/panda1920/twitterImageDL.svg?style=shield)](https://app.circleci.com/pipelines/github/panda1920/twitterImageDL)

## Project overview
This simple python application allows easy collection of media files on twitter.  
No more repetitive right click-and-save!  
Intended to be used on Windows system.

## Features
- Automates download of images/videos/gifs based on a list of users
- Simple GUI which requires no knowledge of python/programming to use

## Obtaining the app
You may either (a) download the executable or (b) build the app yourself.

### a) Download the app
Download the app [here](https://twitter-image-dl.kamigama.dev).

### b) Building the app locally
#### Prerequisites
- Since pyinstaller is not cross-platform, you must be on windows system
- python >=3.7
- pipenv

#### Instructions
1. Clone this repo and cd into it
2. Install dependencies with command `pipenv install`
3. Execute build script build/build.bat

Built files would be located dist/twitter_image_dl.  
twitter_image_dl.exe is a standalone executable that does download tasks only.

## Usage
#### Prerequisites
- Access to twitter API
- Only works for windows system

#### Instructions
Create a file called `users.txt`.
List out twitter usernames you wish to collect media files from in `users.txt`:
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

#### Precautions
Directory structure of the app is important.  
Pulling files/folders out of its original location may cause the app to break.

## TODO checklist
- [x] Properly generate twitter API authorization header
- [x] Implement basic download capability
- [x] Rewrite code to utilize multithreading because download is slow
- [x] Implement mechanism to prevent excessive API calls by keeping track of download history
- [x] Replace environment variables with textfile for app configuration
- [x] Implement a class that create/delete task scheduler entry
- [x] Setup a GUI to consolidate all functionality in one place
- [x] Convert the entire app into windows executable to make it distributable
- [x] Set up CI/CD to automate test/build/distribution of app
- [ ] Brush up GUI
- [ ] Better logging and message output
- [ ] Integrate task scheduler functionality to the GUI
- [ ] Adapt to new twitter APIv2.0
- [ ] Create executable for other systems (maybe)
