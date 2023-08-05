# Melee-YouTube-Uploader
A YouTube Uploader for my Melee recordings

A modified version of FRC-YouTube-Uploader for Super Smash Bros. Melee.

**IMPORTANT NOTE**

This application **DOES NOT** support enabling monetization at the moment. I highly suggest you upload videos as unlisted and set monetization settings before making them public or monitor your uploads and update monetization settings as they are uploaded (you can adjust the settings while the files are being uploaded without breaking anything). If you see the YouTube ContentID API in your Google Developer Console and are willing to help me test updates to fix the issue DM me on twitter at @xMetonym.

## To Do
* Automate creation of thumbnails
* Automate file picking
* Update this README even more

## Contributing
PRs are appreciated and will be reviewed quickly, the only code quality standard I have is to follow PEP8 standard except for the line length. If you have trouble understanding my code just ask me.

## Current Feature Set:
* Upload videos
* Queue and dequeue Videos to upload
* Adds a lot of relevant tags
* Adds to a YouTube playlist
* Saves and loads form values
* Loading values from history

## How to Setup
1. Install [Python 3.7.1](https://www.python.org/downloads/release/python-371/) for your OS with the PATH added and make sure there are no other versions of Python 3.
2. Install the program with `pip3 install -U meleeuploader`. If you want untested features you can download the repo and install with `pip3 install -U /path/to/repo`
3. Start the program by running `meleeuploader` in terminal.
4. Add in the necessary info in the Event Values and Match Values tabs
5. Hit submit every time a match finishes.
6. Update forms with the next match's info.
7. Enjoy not having to deal with YouTube's front end 🎉.

### Create Your Own Credentials
In the future I will not be including YouTube API credentials with this project. So here is a guide to create your own credentials.

1. Open the [Google Developer Console](https://console.developers.google.com/)
2. Hit the `Select Project` button near the top and create a new project.
3. Once the project is created, select the project.
4. Hit the `Enable APIs and Services` button and enable the YouTube Data API V3.
5. Once the API is enabled it will tell you to create credentials and there will be a button to press.
6. Follow the steps laid out in the credential creation wizard and make sure to select `Other UI` for `Where will you be calling the API from?` and `User Data` for `What data will you be accessing?`.
7. Once you have downloaded your credentails remember to rename them `client_secrets.json` (if you don't see the `.json` when renaming the file just use `client_secrets`) and put the file in `C:\Users\[Your Username]\` or, if you are on macOS or Unix, whatever `echo ~` returns in terminal. macOS users can also just do `open ~` to open a Finder window at that directory.
8. If you already created YouTube Account credentials for the program, open the program and select `Settings -> Remove YouTube Credentials`

### Additional Setup Options
#### Windows
If you want to launch the application easily, you can find the exe by hitting the Windows key and typing `meleeuploader`, if that doesn't show the option to run the command then you can probably find the exe at `C:\Users\[Your Username]\AppData\Local\Programs\Python\Python37\Scripts\`. Pinning the exe to the taskbar allows quick access to the program.

#### Mac and Unix
`meleeuploader &` if you want to hide the terminal window. There are probably ways to launch the program quicker, but I don't use macOS/Unix for uploading usually.

## How to use fields
### Required
`Event Name`, `File`, `Video Privacy`, `Match Type`, and `Player Tags` are the only required fields for uploading any file.

### Optional
#### Match Type Prefix and Suffix
These are fairly self explanatory, you can add a bit of text before and after the `Match Type`. When submitting the video the `Prefix` is kept while the `Suffix` is cleared.

#### Sponsor Tag
This field will be added to the player tag like so `{sponsor} | {player}` resulting in names like `TSM | Leffen`.

#### Characters
If you ignore this field on either player than both player will not have characters.  
Characters that are selected will be in the order they are shown in the list, not the selected order (unfortunate issue with the GUI framework).  
You can swap the character list using the menu bar option. Currently the Ultimate character list will only load if the last saved form used a character that was not in Melee, however switching between the two sets will keep your selection, assuming the selection exists in the other set (Melee -> Ult is guaranteed, but the inverse isn't).

#### YouTube PlaylistID
The URL of the playlist after creation can be put here, the program will trim it to just the part it needs. The URL should look like `https://www.youtube.com/playlist?list=PLSCJwgNAP2cXdlHlwbZr38JDHuuc8vx_s`, if the address has a string with `PL` at the start, it should work.

#### Bracket Link
Any URL will work here, just make sure to include `https://` so YouTube users can click on the link in the description.

#### Tags
If you want to add additional tags, for a specific event or your channel, add them here. Separate the tags with commas and don't worry about leading or trailing spaces.  
Also multiple tags about Melee and the players are added by the program so don't add any related to those in this field.

#### Description
Additional text can be added to the description here, it will go between the bracket link and the credit text.

#### Submit
The submit button does a lot, it adds submission to queue, clears fields in match values that aren't generally needed for consecutive matches, and prevents you from adding submissions that don't meet the minimum criteria.

## How to use advanced features

### History - Fixing an upload that didn't work
History was built so I could fix uploads that exceeded the title limit on YouTube (100 characters). 

By loading the history window from the menubar, you can double click any row in the list to reload the form with the values you inputted for that submission. Every submission will create a new entry, but the history window is only updated on load, you will need to close and reopen it to see new entries.

### Queue - Saving uploads for later
Queue was built so I could upload VODs after an event because the venue didn't have the bandwidth to support streaming and uploading simultaneously. 

Queue refers to the list of upcoming uploads in the status tab. By selecting `Toggle Uploads` you can toggle the uploading function, but continue to add entries to the queue. Once you have finished adding all the VODs you want to upload, selecting `Save Queue` will write the entire queue to your disk to be loaded later on. Finally, using `Load Queue` will load the entire queue file and start uploading immediately.
