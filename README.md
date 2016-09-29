# marttkfmanager
A file manager made with tk

## Keyboard bindings:

 Keybind's Actions                          | Binds
 -------------------------------------------|-------------
 Toggle Showing Hidden Files:               | `Ctrl-h`
 Refresh:                                   | `Ctrl-r`
 Up Directory:                              | `Left`
 Change Directory/Open File:                | `Right`
 Move between Directory/Files:              | `Up/Down`
 Move between Directory/Files in 10 steps:  | `Ctrl-Up/Down`
 Beginning/End file of the directory:       | `Home/End`
 Move scrollbar up/down:                    | `Pageup/Pagedown`
 Quit program:                              | `Ctrl-q`

## Dependencies

Based on Debian package names, these may differ in other distros.

* python3
* tkinter
* python-pil

## Configuration

It's important to put the "marttkfmanagerrc" file in your home directory as ".marttkfmanagerrc" if you want to have a proper configuration file.

## Changelog

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

## To-Do; Plans for later releases:

* Add find/search entrybox
* Right click menu future features
 * Ability to delete file 
 * Ability to move file 
 * Ability to copy file 
* Add configuration button and window
* About window style change

### Future Dependencies

* python-gstreamer
* python-gobject


