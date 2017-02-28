# marttkfmanager
A file manager made with tk

![BETA v5.0 - Video player screenshot](screenshot_01.png)

## Keyboard bindings:

 Keybind's Actions                          | Binds
 -------------------------------------------|-------------
 Toggle Showing Hidden Files:               | `Ctrl-h`
 Toggle fullscreen:                         | `F11`
 Refresh:                                   | `Ctrl-r`
 Find:                                      | `Ctrl-f`
 Search:                                    | `Ctrl-s`
 Directory Input Bar:                       | `Ctrl-l`
 Up Directory:                              | `Left`
 Change Directory/Open File:                | `Right`
 Move between Directory/Files:              | `Up/Down`
 Move between Directory/Files in 10 steps:  | `Ctrl-Up/Down`
 Beginning/End file of the directory:       | `Home/End`
 Move scrollbar up/down:                    | `Pageup/Pagedown`
 Stop Media:                                | `Ctrl-1`
 Rewind Media by 5 seconds:                 | `Ctrl-2`
 Play/Pause Media:                          | `Ctrl-3`
 Forward Media by 5 seconds:                | `Ctrl-4`
 Toggle Subtitle of Video:                  | `Ctrl-5`
 Toggle Audio of Video:                     | `Ctrl-6`
 New Tab:                                   | `Ctrl-t`
 Switch up a tab                            | `Ctrl-Tab`
 Exit Tab:                                  | `Ctrl-q`
 Quit Program:                              | `Ctrl-Q`

## Mouse bindings:

* Left click on `ExD` brings menu of mounted external devices
* Right click on `ExD` brings menu of mountable/unmountable mounted external devices
 
## Dependencies

Based on Debian package names, these may differ in other distros.

* python3
* python3-dev 
* tkinter
* tix
* tix-dev
* python-pil
* udisks2

In Debian/Ubuntu, install those gstreamer1.0 dependencies as follow:

```
sudo apt install python-gi python3-gi \
    gstreamer1.0-tools \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-libav
```

To cover over these dependencies:

* python-gobject
* python-gst-1.0
* python-gstvideo

## Configuration

It's important to put the "marttkfmanagerrc" file in your home directory as ".marttkfmanagerrc" if you want to have a proper configuration file.

## To-Do; Plans for later releases:

* Custom execution buttons
* Better GUI configuration
* (Maybe) drop-down for address entry
* Bookmarks
* Extra information on bottom about selected files
* (Unlikely) icons/thumbnails per files
* Gallery preview
* Better tabs (buttons to move between tabs) 

## Changelog - BETA

### 2017 FEB 23 BETA v5.0 - Changelog:
* Text preview height size improved
* Fix bug where resize gets less than 0 and unable to resize
* Changed how labels are updated
* Images gets updated/resized via window height
* Text line does not add a `\n` any-more so it looks fine to read now
* Increased volume from 0.5 to 1
* Prevented the forward button to go pass the total media duration
* Improved UI to resize adjustments
* File Properties Window
 * With ability to change permission (chmod, chgrp, chown)
 * User can now see the file's/folder's properties

### 2016 DEC 15 BETA v4.0 - Changelog:
* **Automounting and external storage devices support**
 * Basic interface for going to external storage devices
 * Automounting when new storage device detected
 * Can unmount and mount with right click menu on `ExD`
* Added localization, language mostly done:
 * Russian/русский
 * Chinese Tradition/中國傳統的 (Taiwan (RoC), Hong Kong)
 * Chinese Simplified/简体中文 (Mainland China (PRoC))
 * Japanese/日本語
* Language will only go by your system, the default and fallback is English
* Added the ability to toggle fullscreen
* Single click on item makes sense now: From Button-1 to ButtonRelease-1
 * Side frame disappears when clicked on a directory
* Changed the colour of the tabs
* Text preview responsive to window resize
* Fixed directory history to support multi-tabs and expected directory when forward/backward
* Different and improve sorting list toggle
 * Name, Time, Size, and File Type sorting
* No longer give lambda error after playlist to other directory change
 * Used partial instead of lambda (effected in the use of .unpost(), changed to call `unposter` function instead)

### 2016 NOV 28 BETA v3.0 - Changelog:
* **User Interface refinement update**
* New user interface
 * Navigation bar and buttons now in one row
 * Uses unicode symbols
* Fixed the side frame overriding the top 2 navigation frames
 * Having the top 2 frames set to main instead of inside tab_frame
* tab_frame no longer an array, no need for it to be one
* Fixing the directory not changing after the music/video player playing to change tab bug
* Auto-updates player more by 10 times
 * Allows for a slightly faster video/music load
* Slider resolution reduced from 0.5 to 0.1 - now more accurate/on point when using the slider
* Closing configuration button no longer refresh directory
* side_frame mainloop turned to update to fix the rare bug crash
* Images over the height of the tree/directory list get set to the size of the tree/directory list
* Auto-Image resize now smooth (No longer flickers a lot when resizing)
 * No longer destroy then create, but rather just change the configuration of image 
* bottom_frame/Information frame does not get overlapped by image viewer/side_frame
* Without the .marttkfmanagerrc file now reads for the marttkfmanagerrc_DEFAULT file
* Menu, list_frame, and side_frame no longer an array
* Added the ability to change between ascending and descending name

### 2016 NOV 24 BETA v2.2 - Changelog:
* Version number changed from vX.X.X system to vX.X
 * vX.X.X system does not make sense in the way I decided on the version numbers
* Add configuration button and window
 * Partial used over lambda due to the way variable passing was handled

### 2016 NOV 23 BETA v0.2.1 - Changelog:
* Tabs bug fixes
* Buttons no longer uses flat relief/style
* Added logo on window decoration

### 2016 NOV 21 BETA v0.2.0 - Changelog:
* **Added tab support** (Big update)
* Auto-updates resizes more by 100 times
* Added midi support for music player
* Added audio and subtitle change toggle button (Not all subtitles can works and change)
* Audio/Video player style and text formatting changed slightly
* Added logo in about page

### 2016 NOV 18 BETA v0.1.7 - Changelog:
* Added slider for both music and video player
* Now autoplays when you select a different row if you set the music/video to play
* Fixed some bugs (side viewer not destroyed after row change, music play refresh bug)
* Auto-updates with the height of treeview/list of directories/files relative to directory change or window height change or directory refresh
 * Also auto-updates width of images and videos
* Rewind/Forward seeker buttons jumps 5 seconds instead of 10

### 2016 NOV 14 BETA v0.1.6 - Changelog:
* Find function implemented - Binded as: `Ctrl-f`
* Search function implemented - Binded as: `Ctrl-s`
* Added 'Find' and 'Refresh' button on top frame
* Fixed text side preview stuck bug 
* Fixed up directory/change row error when video not a variable/as a NoneType
* Prevents the side preview to be viewed when resolution is lower than the lower limit
 * Less than 800 in width means no preview
 * Only exception is the music preview which can be at any resolution
* Make directory and Rename window redesigned
* Deleting files now forced and one by one with each having per window opened then closed

### 2016 NOV 13 BETA v0.1.5 - Changelog:
* Position of the Music Player changed from right-side to bottom
* Added music info, position, and duration
* Top button and Entry re-style/position
* Partial Fix for the opening video program via Button 1 while side-video player is playing (can still crash in some circumstances)
* Added rewind (<<) and forward (>>) seeker buttons 
* Added stop button

### 2016 NOV 12 BETA v0.1.4 - Changelog:
* Video player width fix
* Fixed Video player crash
* Text viewer only open on .txt files now

### 2016 NOV 10 BETA v0.1.3 - Changelog:
* Audio devices limited to 1
* Video player added

### 2016 OCT 25 BETA v0.1.2 - Changelog:
* Gstreamer - First time audio/basic music player implimentation

### 2016 OCT 05 BETA v0.1.1 - Changelog:
* Added for reading text files
* Tried to impliment audio (currently not working)

### 2016 OCT 04 BETA v0.1.0 - Changelog:
* Added side media preview for first time
 * Currently only for previewing pictures
 * BUG: Single-Click would be delayed by one image

## Changelog - ALPHA

### 2016 SEP 30 ALPHA v0.2.1 - Changelog:
* Added cut, copy, and paste feature in menu
* Added make directory feature in menu
* Empty directory can now right click: Moved from tag bind right click to whole of treeview/list
* Menu should unpost when click out of menu

### 2016 SEP 29 ALPHA v0.2.0 - Changelog:
* It can now do multiple selection of items (files/directories)
 * Used selection instead of focus
* Added duplication feature in menu
* Added renaming feature in menu
* Added delete feature in menu
* Widgets are inside either the 2 frames
* Resizeable directory list
* Layout change

### 2016 SEP 28 ALPHA v0.1.5 - Changelog:
* Added the ability to refresh and show/hide hidden files on right click menu

### 2016 SEP 21 ALPHA v0.1.4 - Changelog:
* Add right click menu
 * Ability to use alternative program/commands

### 2016 SEP 18 ALPHA v0.1.3 - Changelog:
* Fixed pos variable going out of range of history list
* Fixed mistake where history is set at current directory and not home
* Reduced LOC from 261 LOC to 252 LOC - No more variable assignment on top buttons and about label and button
* Renamed tkfmanager.py to marttkfmanager.py

### 2016 SEP 17 ALPHA v0.1.2 - Changelog:

* Less redundent code - Cut down of around ~40 SLOC (From 310 to 261 LOC/238 SLOC (including removing of 9 lined dependency comment))
 * Uses lambda instead in replace of simpler functions
* Display 'Directory don\'t exist' if user tries to enter a non-existent directory

### 2016 SEP 16 ALPHA v0.1.1 - Changelog:

* Use arrow keys to quickly navigate through directories and files
* Control-up/down for 10 steps
* Display 'Access Denied' if user cannot enter directory
* About window fixed

### From 2016 SEP 15 v00 to 2016 SEP 15 ALPHA v0.1.0 - Changelog:

* Turn it from a file browser to a basic file manager
* Change from release click to double click 
* Add more information on bottom: Free space V Total space
* Hide hidden files - Toggles with 'CTRL + H'
* Ability to refresh directory - Toggles with 'CTRL + R'
* Files ends with 'rc' are recognised
* Changed from PRE-ALPHA to ALPHA stage
* Change how up directory works
* Directory entrybox binded to keyboard-enter 
* Flexably uses between units (Bytes to YiB) on file sizes
* \xa0 used instead of _


