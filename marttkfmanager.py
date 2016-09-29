# MartTKfManager - Martin's File Manager (TK version)
version = "ALPHA v0.2.0"
cur_year = "2016"

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sys, os, time, pwd, grp, subprocess, re

pos = 0
home = os.path.expanduser("~") # home directory
history = [home]
show_hidden_files = False
access_info = ''

def conf_read():
    try:
        cf_file = open(home+'/.marttkfmanagerrc', 'r')
        cf_file = cf_file.readlines()
    except:                             # if the marttkfmanagerrc file is missing
        cf_file = ['[TAG]\n', 'images:feh\n', 'videos:mpv\n', 'text:st -e vim\n', '[/TAG]\n', '\n', '[EXTENTION]\n', '*:text:Unknown File Type\n', 'rc:text:Configuration File\n', 'jpg:images:Joint Photographic Experts Group\n', 'jpeg:images:Joint Photographic Experts Group\n', 'png:images:Portable Network Graphic\n', 'mkv:videos:Matroska Multimedia Container\n', 'mp4:videos:MPEG-4\n', 'txt:text:Text File\n', 'c:text:C Source Code\n', 'py:text:Python Source Code\n', 'html:text:HTML File\n', 'htm:text:HTML File\n', 'php:text:PHP File\n', 'sh:text:Shell Script\n', '[/EXTENTION]\n', '\n', '\n']
    for itr in range(0, len(cf_file)):
        cf_file[itr] = cf_file[itr][:-1]
    cf_file.append('EXIT')
    return cf_file

def human_readable_size(new_size):
    for unit in ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']:
        if new_size < 1024:
            return str("%.2f" % new_size)+'\xa0'+unit
        new_size /= 1024
    return str("%.2f" % new_size)+'\xa0YiB'

def sort_file(fetch):                   # fetch == 'TAG': Returns the tags_conf | fetch == 'EXT': Returns the ext_conf | fetch == 'EXT_NAME': Returns the ext_conf_n
    conf_file = conf_read()
    tags_conf, ext_conf, ext_conf_n = {}, {}, {}
    tag_in = 'NONE'
    for itr in range(0, len(conf_file)):
        if conf_file[itr] == '[TAG]':
            tag_in = 'TAG'
        elif conf_file[itr] == '[/TAG]' or conf_file[itr] == '[/EXTENTION]':
            tag_in = 'NONE'
        elif conf_file[itr] == '[EXTENTION]':
            tag_in = 'EXT'
        elif conf_file[itr] == 'EXIT':
            break
        else:
            str_part = conf_file[itr].split(':')
            if tag_in == 'TAG':
                tags_conf[str_part[0]] = str_part[1]
            elif tag_in == 'EXT':
                ext_conf[str_part[0]] = str_part[1] 
                ext_conf_n[str_part[0]] = str_part[2]
    if fetch == 'TAG':
        return tags_conf
    elif fetch == 'EXT':
        return ext_conf
    elif fetch == 'EXT_NAME':
        return ext_conf_n

def dir_change_action(event, to_dir, pos_ch):
    global dir_info_01, tree, pos, access_info
    pos += pos_ch
    if type(to_dir) is list:
        if ((pos >= 0 and pos_ch == -1) or (pos <= len(history) - 1 and pos_ch == 1)):
            os.chdir(to_dir[pos])
        elif pos < 0:
            pos = 0
        elif pos > len(history) - 1:
            pos = len(history) - 1
    elif to_dir != 0: 
        history.append(os.getcwd())
        try:
            access_info=''
            os.chdir(to_dir)
        except:
            if os.path.isdir(to_dir) == True:
                access_info='     Access Denied'
            else:
                access_info='     Directory don\'t exist'
    main.title("MartTKfManager - "+os.getcwd())
    menu.unpost()
    dir_info_01.destroy()
    tree.destroy()
    main_list_dir()

def about():
    menu.unpost()
    about_win = Tk()
    about_win.title("MartTKfManager - About")
    about_win.resizable(width=False, height=False)
    about_win.geometry("%dx%d+%d+%d" % (400, 100, 0, 0))
    Label(about_win, text="MartTKfManager (Martin's File Manager (TK version))\nVersion: "+version+"\nCopyright (c) "+cur_year).pack()
    Button(about_win, text="Close", command=about_win.destroy).pack()
    about_win.mainloop()

def main_buttons():
    top_frame.grid(row=0, column=0, sticky=N+W)
    Button(top_frame, text="<-", command=lambda: dir_change_action(0, history, -1)).grid(row=0, column=1, sticky=N+W)
    Button(top_frame, text="->", command=lambda: dir_change_action(0, history, 1)).grid(row=0, column=2, sticky=N+W)
    Button(top_frame, text="~", command=lambda: dir_change_action(0, home, 1)).grid(row=0, column=3, sticky=N+W)
    Button(top_frame, text="About", command=about).grid(row=0, column=4, sticky=N+W)
    Button(top_frame, text="Exit", command=sys.exit).grid(row=0, column=5, sticky=N+W)

def file_sortout():
    menu.unpost()
    file_select, file_list = [], []
    for item_id in tree.selection():
        file_select += [tree.item(item_id)['text']]
    for item_n in file_select:
        file_list += [os.getcwd()+'/'+str(item_n)]
    return [file_list, file_select]

def ext_prog(event): # EXT_RUN
    list_of_list = file_sortout()
    file_list = list_of_list[0]
    if file_list != []:
        if file_list[0][-2:] == 'rc':
            file_ext = 'rc' 
        elif '.' not in file_list[0][1:]:
            file_ext = '*'
        else:
            file_ext = file_list[0].split('.')
            file_ext = file_ext[len(file_ext)-1]
        tags_conf = sort_file('TAG')
        ext_conf = sort_file('EXT')
        try:
            ext_bind = tags_conf[ext_conf[file_ext]].split(' ')
        except:
            ext_bind = tags_conf[ext_conf['*']].split(' ')
        ext_bind.extend(file_list)
        subprocess.Popen(ext_bind)                      # Popen: files open in another process (preferred) | call: files open within this process
    dir_change_action(event, 0, 0)

def ext_prog_alt(): # EXT_RUN ALTERNATIVE
    def alt_prog_open(open_command):
        subprocess.Popen(open_command)
        alt_win.destroy()
        dir_change_action(0, 0, 0)
    list_of_list = file_sortout()
    file_list = list_of_list[0]
    file_select = list_of_list[1]
    if file_list != []:
        alt_win = Tk()
        alt_win.title("MartTkfManager - Alternative Open")
        alt_win.resizable(width=False, height=False)
        alt_win.geometry("%dx%d+%d+%d" % (400, 100, 0, 0))
        Label(alt_win, text="Open "+str(' '.join(file_select))+" with...").pack()
        prog_entry = Entry(alt_win, width=100)
        prog_entry.pack()
        prog_entry.focus()
        prog_entry.bind('<Return>', lambda event: alt_prog_open(prog_entry.get().split(' ')+file_list))
        Button(alt_win, text="Go", width=10, command=lambda: alt_prog_open(prog_entry.get().split(' ')+file_list)).pack()
        alt_win.mainloop()

def toggle_hidden(event):
    global show_hidden_files
    show_hidden_files = not show_hidden_files
    menu.unpost()
    dir_change_action(event, 0, 0)

def target_duplicate():
    menu.unpost()
    list_of_list = file_sortout()
    file_list = list_of_list[0]
    for item_n in file_list:
        subprocess.Popen(['cp', '-r', item_n, item_n+'_copy']) 
    dir_change_action(0, 0, 0)

def rename_win_func(file_list, file_select, item_n):
    def rename_action(open_command):
        if open_command != 'NONE':
            subprocess.Popen(open_command)
        rename_win.destroy()
        dir_change_action(0, 0, 0)
        try:
            file_list[item_n + 1] # Only there to test (using try/except) on the IndexError
            rename_win_func(file_list, file_select, item_n + 1)
        except:
            pass
    rename_win = Tk()
    rename_win.title("MartTkfManager - Rename")
    rename_win.resizable(width=False, height=False)
    rename_win.geometry("%dx%d+%d+%d" % (400, 100, 0, 0))
    Label(rename_win, text="Rename "+file_select[item_n]+" to...").pack()
    newname_entry = Entry(rename_win, width=100)
    newname_entry.pack()
    newname_entry.delete(0, END)
    newname_entry.insert(0, file_select[item_n])
    newname_entry.focus()
    newname_entry.bind('<Return>', lambda event: rename_action(['mv', file_list[item_n], os.getcwd()+'/'+newname_entry.get()]))
    Button(rename_win, text="Rename", width=10, command=lambda: rename_action(['mv', file_list[item_n], os.getcwd()+'/'+newname_entry.get()])).pack()
    Button(rename_win, text="Cancel", width=10, command=lambda: rename_action('NONE')).pack()
    rename_win.update_idletasks()
    rename_win.update()

def target_rename():
    menu.unpost()
    list_of_list = file_sortout()
    if list_of_list[0] != []:
        rename_win_func(list_of_list[0], list_of_list[1], 0)

def target_delete():
    menu.unpost()
    list_of_list = file_sortout()
    file_list = list_of_list[0]
    file_select = list_of_list[1]
    if messagebox.askquestion("File Delete", "Delete these following files? "+str(', '.join(file_select))+"\nIt will be deleted forever.") == "yes":
        subprocess.Popen(['rm', '-r']+file_list)
    dir_change_action(0, 0, 0)

def main_list_dir():
    global history, dir_info_01, show_hidden_files, tree, access_info, id_pos
    def r_click(event): # RIGHT CLICK MENU
        menu.post(event.x_root, event.y_root)

    def bind_cur_dir_entry(event):
        menu.unpost()
        cur_dir_entry.focus_set()

    def row_change(event, pos_change, id_list):
        global id_pos
        menu.unpost()
        tree.focus_set()
        id_pos += pos_change
        if id_pos < 0 or pos_change == 0:
            id_pos = 0
        elif id_pos > len(id_list) - 1 or pos_change == 2:
            id_pos = len(id_list) - 1
        tree.focus(id_list[id_pos])

    cur_dir_entry = Entry(top_frame, width=40)
    cur_dir_entry.grid(row=0, column=6, columnspan=4, sticky=N+W)
    cur_dir_entry.delete(0, 'end') 
    cur_dir_entry.insert(0, os.getcwd())
    cur_dir_entry.bind('<Return>', lambda event: dir_change_action(event, cur_dir_entry.get(), 1))
    Button(top_frame, text="Go", width=10, command=lambda: dir_change_action(0, cur_dir_entry.get(), 1)).grid(row=0, column=10, sticky=N+W)

    row_place, col_place = 2, 0
    dir_ls = os.listdir(os.getcwd())
    dir_ls.sort()

    list_frame.grid(row=1, column=0, sticky=N+W+E)
    scrollbar = Scrollbar(list_frame, orient=VERTICAL)
    scrollbar.grid(row=0, column=20, rowspan=15, sticky=N+S)
    tree = Treeview(list_frame, height=21, columns=('size', 'last_mod', 'uid_gid', 'ext'), yscrollcommand=scrollbar.set)
    tree.grid(row=0, column=0, columnspan=20, sticky=W+E)
    tree.column('#0', width=300, anchor='w')
    tree.heading('#0', text='Filename')
    tree.column('size', width=120, anchor='w')
    tree.heading('size', text='Size')
    tree.column('last_mod', width=200, anchor='w')
    tree.heading('last_mod', text='Last Modified')
    tree.column('uid_gid', width=140, anchor='w')
    tree.heading('uid_gid', text='Owner/Group')
    tree.column('ext', width=140, anchor='w')
    tree.heading('ext', text='File type')
    total_dir, total_file, id_pos = 0, 0, 0
    id_list = []
    up_id = tree.insert('', 'end', text='..', tag=('up'), values=('UP\xa0DIRECTORY '))
    id_list.append(up_id)
    tree.focus_set()
    tree.focus(id_list[id_pos])
    for itr in range(0, len(dir_ls)):
        if (show_hidden_files == False and dir_ls[itr][0] != '.') or (show_hidden_files == True):
            las_mod_time = str(time.ctime(os.stat(dir_ls[itr]).st_mtime))
            las_mod_time = re.sub(r"\s+", '\xa0', las_mod_time)
            try:
                uid_gid_get = str(pwd.getpwuid(os.stat(dir_ls[itr]).st_uid)[0]+'\xa0'+grp.getgrgid(os.stat(dir_ls[itr]).st_gid)[0]) # gets the uid/gid of the file, then convert that to the name of the uid/gid
                uid_gid_get = re.sub(r"\s+", '\xa0', uid_gid_get)
            except:
                uid_gid_get = str(os.stat(dir_ls[itr]).st_uid)+'\xa0'+str(os.stat(dir_ls[itr]).st_gid) # if uid/gid is not found
            if os.path.isdir(dir_ls[itr]) == True:
                r_id = tree.insert('', 'end', text=dir_ls[itr], tag=('dir'), values=('DIRECTORY '+las_mod_time+' '+uid_gid_get+' DIRECTORY')) 
                id_list.append(r_id)
                total_dir += 1
            else:   # EXT_NAME
                if dir_ls[itr][-2:] == 'rc':
                    file_ext = 'rc'
                elif '.' not in dir_ls[itr][1:]:
                    file_ext = '*'
                else:
                    file_ext = dir_ls[itr].split('.')
                    file_ext = file_ext[len(file_ext)-1]
                ext_conf_n = sort_file('EXT_NAME')
                try:
                    file_ext_n = ext_conf_n[file_ext] 
                except:
                    file_ext_n = ext_conf_n['*']
                file_ext_n = re.sub(r"\s+", '\xa0', file_ext_n)
                r_id = tree.insert('', 'end', text=dir_ls[itr], tag=('file'), values=(human_readable_size(os.stat(dir_ls[itr]).st_size)+' '+las_mod_time+' '+uid_gid_get+' '+file_ext_n))
                id_list.append(r_id)
                total_file += 1
    tree.tag_configure('dir', background='#94bff3')
    tree.tag_configure('up', background='#d9d9d9')
    tree.tag_bind('dir', '<Double-Button-1>', lambda event: dir_change_action(event, tree.item(tree.focus())['text'], 1))
    tree.tag_bind('file', '<Double-Button-1>', ext_prog)
    tree.tag_bind('up', '<Double-Button-1>', lambda event: dir_change_action(event, '..', 1))
    tree.tag_bind('dir', '<Right>', lambda event: dir_change_action(event, tree.item(tree.focus())['text'], 1))
    tree.tag_bind('file', '<Right>', ext_prog)
    tree.tag_bind('up', '<Right>', lambda event: dir_change_action(event, '..', 1))
    tree.tag_bind('dir', '<Button-3>', r_click)
    tree.tag_bind('file', '<Button-3>', r_click)
    scrollbar.config(command=tree.yview)

    sizestat = os.statvfs('/')
    lower_info_text = 'Total overall/directories/files: '+str(total_dir+total_file)+'/'+str(total_dir)+'/'+str(total_file)+'    Hidden files shown: '+str(show_hidden_files)+'    Free Space: '+str(human_readable_size(sizestat.f_frsize * sizestat.f_bfree))+'    Total Space: '+str(human_readable_size(sizestat.f_frsize * sizestat.f_blocks))+access_info
    dir_info_01 = Label(list_frame, text=lower_info_text)
    dir_info_01.grid(row=20, column=0, columnspan=8, sticky='w')

    main.bind('<Control-h>', toggle_hidden)
    main.bind('<Control-r>', lambda event: dir_change_action(event, 0, 0))
    main.bind('<Control-l>', bind_cur_dir_entry)
    main.bind('<Left>', lambda event: dir_change_action(event, '..', 1))
    main.bind('<Up>', lambda event: row_change(event, -1, id_list))
    main.bind('<Down>', lambda event: row_change(event, 1, id_list))
    main.bind('<Control-Up>', lambda event: row_change(event, -10, id_list)) 
    main.bind('<Control-Down>', lambda event: row_change(event, 10, id_list))
    main.bind('<Home>', lambda event: row_change(event, 0, id_list))
    main.bind('<End>', lambda event: row_change(event, 2, id_list))
    main.bind('<Control-q>', sys.exit)

def ttk_style():
    Style().configure("TButton", xpad=12, relief="flat", background="#ccc")
    main.configure(background="#EEE")

os.chdir(home) 
main = Tk()
main.title("MartTKfManager - "+os.getcwd())
main.geometry("%dx%d+%d+%d" % (970, 490, 0, 0))
main.grid_columnconfigure(0, weight=1, minsize = 480)
main.grid_rowconfigure(0, minsize = 40)
top_frame = Frame(main)
list_frame = Frame(main)
list_frame.columnconfigure(0, weight=1)

menu = Menu(main, tearoff=0)
menu.add_command(label="Open", command=lambda: ext_prog(0))
menu.add_command(label="Open with", command=lambda: ext_prog_alt())
menu.add_command(label="Refresh Directory", command=lambda: dir_change_action(0, 0, 0))
menu.add_command(label="Hide/Unhide hidden Files/Directory", command=lambda: toggle_hidden(0))
menu.add_separator()
menu.add_command(label="Duplicate", command=lambda: target_duplicate())
menu.add_command(label="Rename", command=lambda: target_rename())
menu.add_command(label="Delete", command=lambda: target_delete())

main_buttons()
main_list_dir()
ttk_style()
main.update()

main.mainloop()

