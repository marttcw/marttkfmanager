# MartTKfManager - Martin's File Manager (TK version)
version = "BETA v3.0"
cur_year = "2016"

from tkinter import *
import tkinter.ttk as ttk
from tkinter import tix
from tkinter import messagebox
from PIL import ImageTk, Image
from time import sleep
from functools import partial
import sys, os, time, pwd, grp, subprocess, re, fnmatch# g-streamer
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0') # GstVideo is Needed for set_window_handle():
gi.require_version('GstTag', '1.0')   # GstTag is needed for country tag matching for text
from gi.repository import GObject, Gst, GstVideo, GstTag

GObject.threads_init()
Gst.init(None)

project_dir = os.getcwd()
pos = 0
home = os.path.expanduser("~") # home directory
history = [home]
show_hidden_files = False
access_info = ''
file_list_clip = []
mus_dur = ''
is_playing = False
dir_changed = False
sub_ind = 0
aud_ind = 0
language = ''
sa_count = 0
tab_num = 0
min_tab = 0
tab_bg_colour_inactive = '#cccccc'
tab_bg_colour_active = '#99ccff'
viable_tabs = []
sort_type = 'Name Ascending'

def menu_l_add_command(menu_l):
    menu_l.add_command(label="Open", command=lambda: ext_prog(0))
    menu_l.add_command(label="Open with", command=lambda: ext_prog_alt())
    menu_l.add_command(label="Refresh Directory", command=lambda: dir_change_action(0, 0, 0))
    menu_l.add_command(label="Hide/Unhide hidden Files/Directory", command=lambda: toggle_hidden(0))
    menu_l.add_separator()
    menu_l.add_command(label="Cut", command=lambda: target_cut())
    menu_l.add_command(label="Copy", command=lambda: target_copy())
    menu_l.add_command(label="Paste", command=lambda: target_paste())
    menu_l.add_command(label="Make Directory", command=lambda: target_mkdir())
    menu_l.add_command(label="Duplicate", command=lambda: target_duplicate())
    menu_l.add_command(label="Rename", command=lambda: target_rename())
    menu_l.add_command(label="Delete", command=lambda: target_delete())

def tab_frame_label_changer(colour_new):
    global tab_frame_label, tab_num
    for itr in range(0, len(tab_frame_label)):
        tab_frame_label[itr][tab_num]['background']=colour_new
    
def conf_read():
    try:
        cf_file = open(home+'/.marttkfmanagerrc', 'r')
        cf_file = cf_file.readlines()
    except:                             # if the marttkfmanagerrc file is missing
        cf_file = open(project_dir+'/marttkfmanagerrc_DEFAULT', 'r')
        cf_file = cf_file.readlines()
    for itr in range(0, len(cf_file)):
        cf_file[itr] = cf_file[itr][:-1]
    cf_file.append('EXIT')
    return cf_file

def window_destroy(conf_win, base_conf_win):
    conf_win.destroy()
    base_conf_win.destroy()

def save_entry(editing_conf):
    new_file = []
    for itr in range(0, len(editing_conf)-1):
        if editing_conf[itr] =='TAG':
            new_file += ['[TAG]\n']
        elif editing_conf[itr] =='/TAG':
            new_file += ['[/TAG]\n']
        elif editing_conf[itr] =='EXTENTION':
            new_file += ['[EXTENTION]\n']
        elif editing_conf[itr] =='/EXTENTION':
            new_file += ['[/EXTENTION]\n']
        else:
            line_add = []
            for itr2 in range(0, len(editing_conf[itr])-1):
                line_add += [editing_conf[itr][itr2].get()]
            new_file += [':'.join(line_add)+'\n']
    new_file += ['\n']
    cf_file = open(home+'/.marttkfmanagerrc', 'w')
    for line in new_file:
        cf_file.write(line)
    cf_file.close()

def conf_file_update(conf_file, editing_conf):
    for itr in range(0, len(conf_file)-1):
        if conf_file[itr] == ':':
            conf_file[itr] = editing_conf[itr][0].get()+':'+editing_conf[itr][1].get()
        elif conf_file[itr] == '::':
            conf_file[itr] = editing_conf[itr][0].get()+':'+editing_conf[itr][1].get()+':'+editing_conf[itr][2].get()
    return conf_file

def remove_entry(get_itr, conf_win, conf_file, base_conf_win, editing_conf):
    conf_file = conf_file_update(conf_file, editing_conf)
    del conf_file[get_itr]
    conf_win.destroy()
    base_conf_win.destroy()
    list_entry(conf_file)

def add_entry(itr, tag_type, conf_file, conf_win, base_conf_win, editing_conf):
    conf_file = conf_file_update(conf_file, editing_conf)
    for itr in range(0, len(conf_file)-1):
        if conf_file[itr] == '[/TAG]' and tag_type == 'TAG':
            conf_file = conf_file[:itr] + [':'] + conf_file[itr:]
            break
        elif conf_file[itr] == '[/EXTENTION]' and tag_type == 'EXTENTION':
            conf_file = conf_file[:itr] + ['::'] + conf_file[itr:]
            break
    conf_win.destroy()
    base_conf_win.destroy()
    list_entry(conf_file)

def list_entry(conf_file):
    base_conf_win = tix.Tk()
    base_conf_win.title("MartTKfManager - Configuraton")
    base_conf_win.resizable(width=False, height=False)
    base_conf_win.geometry("%dx%d+%d+%d" % (600, 480, 0, 0))
    scrollwin = tix.ScrolledWindow(base_conf_win, width="600", height="480")
    scrollwin.pack()
    conf_win = scrollwin.window
    ttk.Button(conf_win, text="Close", command=lambda: window_destroy(conf_win, base_conf_win)).grid(column=0, row=0, pady=5)
    ttk.Button(conf_win, text="Save", command=lambda: save_entry(editing_conf)).grid(column=1, row=0, pady=5)
    editing_conf = []
    section = -1
    for itr in range(0, len(conf_file)-1):
        section += 1
        if conf_file[itr] == '[TAG]':
            Label(conf_win, text='TAG Configuration').grid(column=0, row=itr+1, columnspan=3)
            editing_conf += ['TAG']
        elif conf_file[itr] == '[EXTENTION]':
            Label(conf_win, text='EXTENTION Configuration').grid(column=0, row=itr+1, columnspan=3)
            editing_conf += ['EXTENTION']
        elif conf_file[itr] == '[/TAG]': 
            Button(conf_win, text='Add Tag', command=partial(add_entry, itr, 'TAG', conf_file, conf_win, base_conf_win, editing_conf)).grid(column=0, row=itr+1, columnspan=3)
            editing_conf += ['/TAG']
        elif conf_file[itr] == '[/EXTENTION]':
            Button(conf_win, text='Add Extention', command=partial(add_entry, itr, 'EXTENTION', conf_file, conf_win, base_conf_win, editing_conf)).grid(column=0, row=itr+1, columnspan=3)
            editing_conf += ['/EXTENTION']
        elif conf_file[itr] == 'EXIT':
            break
        else:
            editing_conf.append([])
            file_section = conf_file[itr].split(':')
            if len(file_section) != 1:
                for itr2 in range(0, len(file_section)):
                    editing_conf[section] += [Entry(conf_win)]
                    editing_conf[section][itr2].grid(column=itr2, row=itr+1)
                    editing_conf[section][itr2].delete(0, END)
                    editing_conf[section][itr2].insert(0, file_section[itr2])
                editing_conf[section] += [Button(conf_win, text='Remove', command=partial(remove_entry, itr, conf_win, conf_file, base_conf_win, editing_conf))] 
                editing_conf[section][itr2+1].grid(column=itr2+1, row=itr+1)
    base_conf_win.mainloop()

def conf_edit(): # GUI Configuration editor
    menu_l.unpost()
    conf_file = conf_read()
    list_entry(conf_file)

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
                tags_conf[str_part[0]] = str_part[1] # TAG LINKED TO PROGRAM
            elif tag_in == 'EXT':
                ext_conf[str_part[0]] = str_part[1] # EXT LINKED TO TAG
                ext_conf_n[str_part[0]] = str_part[2] # EXT_NAME LINKED TO NAME
    if fetch == 'TAG':
        return tags_conf
    elif fetch == 'EXT':
        return ext_conf
    elif fetch == 'EXT_NAME':
        return ext_conf_n

def dir_change_action(operation, to_dir, pos_ch): # operation = 0 = Normal, operation = 1 = Find
    global dir_info_01, tree, pos, access_info, playbin, is_playing, cur_dir_entry, video, find_win, dir_changed, tab_frame_label
    dir_changed = True
    side_destroyer()
    if operation == 'FIND' or operation == 'SEARCH':
        if pos_ch != '':
            find_list = ['*'+pos_ch+'*', '*'+pos_ch.upper()+'*', '*'+pos_ch.lower()+'*', '*'+pos_ch.capitalize()+'*'] # Find list algorithm 
            matching_list = []
            if operation == 'FIND':
                dir_ls = os.listdir(os.getcwd())                                                                      # might want a better algorithm
                dir_ls.sort()
                for find in find_list:
                    matching_list += fnmatch.filter(dir_ls, find)
                matching_list = list(set(matching_list))
            elif operation == 'SEARCH':
                search_count = 0
                searching_popup = Tk()
                searching_popup.resizable(width=False, height=False)
                searching_popup.geometry("%dx%d+%d+%d" % (400, 100, 0, 0))
                searching_popup.title("MartTkfManager - Searching... Found "+str(search_count)+" items")
                search_label = Label(searching_popup, text="Found "+str(search_count)+" items")
                search_label.pack()
                searching_popup.update()
                for root, dirs, files in os.walk("/"):
                    for file in files:
                        if pos_ch in file:
                            matching_list += [os.path.join(root, file)]
                            search_label.destroy()
                            search_count += 1
                            searching_popup.title("MartTkfManager - Searching... Found "+str(search_count)+" items")
                            search_label = Label(searching_popup, text="Found "+str(search_count)+" items")
                            search_label.pack()
                            searching_popup.update()
                searching_popup.destroy()
        else:
            matching_list = []
        find_win.destroy()
    else:
        pos += pos_ch
        matching_list = 0
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
    tab_frame_dir[tab_num] = os.getcwd()
    tab_frame_label[1][tab_num].destroy()
    tab_frame_label[1][tab_num] = Label(tab_frame_label[0][tab_num], text=os.getcwd())
    #if len(os.getcwd()) > 25:
    #    tab_frame_label[1][tab_num] = Label(tab_frame_label[0][tab_num], text='...'+os.getcwd()[-25:])
    tab_frame_label[2][tab_num].pack_forget()
    tab_frame_label[2][tab_num].pack(side=RIGHT)#.grid(row=0, column=1, sticky=E)
    tab_frame_label[1][tab_num].pack(side=RIGHT)#.grid(row=0, column=0, sticky=E)
    tab_num_goto = tab_num
    tab_frame_label[1][tab_num].bind('<Button-1>', lambda event: goto_tab(tab_num_goto, 'CHANGE'))
    tab_frame_label[1][tab_num]['background']=tab_bg_colour_active

    menu_l.unpost()
    tree.destroy()
    main_list_dir(matching_list)

def about():
    menu_l.unpost()
    about_win = Tk()
    about_win.title("MartTKfManager - About")
    about_win.resizable(width=False, height=False)
    about_win.geometry("%dx%d+%d+%d" % (400, 250, 0, 0))
    Label(about_win, text="MartTKfManager (Martin's File Manager (TK version))\nVersion: "+version+"\nCopyright (c) "+cur_year).pack(pady=15)
    about_img_render = ImageTk.PhotoImage(Image.open(project_dir+"/beta_logo_big.png"), master=about_win)
    about_img_label = Label(about_win, image=about_img_render)
    about_img_label.image = about_img_render
    about_img_label.pack(pady=0)
    ttk.Button(about_win, text="Close", command=about_win.destroy).pack(pady=15)
    about_win.mainloop()

def sort_type_set(sort_type_pass):
    global sort_type
    sort_type = sort_type_pass
    dir_change_action(0, 0, 0)

def extra_menu_add_command(extra_menu):
    extra_menu.add_command(label="About", command=about)
    extra_menu.add_command(label="Find", command=lambda: file_search('FIND'))
    extra_menu.add_command(label="Search", command=lambda: file_search('SEARCH'))
    extra_menu.add_command(label="Name Ascending", command=lambda: sort_type_set('Name Ascending'))
    extra_menu.add_command(label="Name Descending", command=lambda: sort_type_set('Name Descending'))
    extra_menu.add_command(label="Config", command=conf_edit)
    extra_menu.add_separator()
    extra_menu.add_command(label="Exit", command=sys.exit)
    return extra_menu

def extra_menu_pops(event, extra_menu):
    extra_menu.post(event.x_root, event.y_root)
    extra_menu.focus_set()

def main_buttons():
    extra_menu = Menu(main, tearoff=0)
    extra_menu = extra_menu_add_command(extra_menu)
    extra_menu.bind("<FocusOut>", lambda event: extra_menu.unpost())
    MultiButton = Button(top_frame, text="\u2261", width=1)
    MultiButton.pack(side=LEFT) # use optionmenu
    MultiButton.bind('<Button-1>', lambda event: extra_menu_pops(event, extra_menu))
    Button(top_frame, text="\u2190", width=1, command=lambda: dir_change_action(0, history, -1)).pack(side=LEFT)
    Button(top_frame, text="\u2192", width=1, command=lambda: dir_change_action(0, history, 1)).pack(side=LEFT)
    Button(top_frame, text="\u2302", width=1, command=lambda: dir_change_action(0, home, 1)).pack(side=LEFT)
    cur_dir_entry = ttk.Entry(top_frame) # Current Directory Entry
    cur_dir_entry.pack(side=LEFT, fill=X, expand=YES)
    Button(top_frame, text="\u21B5", width=1, command=lambda: dir_change_action(0, cur_dir_entry.get(), 1)).pack(side=LEFT)
    Button(top_frame, text="\u27F3", width=1, command=lambda: dir_change_action(0, 0, 0)).pack(side=LEFT)
    return (cur_dir_entry, extra_menu)

def file_sortout():
    menu_l.unpost()
    file_select, file_list = [], []
    for item_id in tree.selection():
        file_select += [tree.item(item_id)['text']]
    for item_n in file_select:
        if str(item_n)[0] != '/':
            media_path = os.getcwd()+'/'+str(item_n)
        elif str(item_n)[0] == '/':
            media_path = str(item_n)
        file_list += [media_path]
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
    dir_change_action(0, 0, 0)

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
        prog_entry = ttk.Entry(alt_win, width=100)
        prog_entry.pack()
        prog_entry.focus()
        prog_entry.bind('<Return>', lambda event: alt_prog_open(prog_entry.get().split(' ')+file_list))
        Button(alt_win, text="Go", width=10, command=lambda: alt_prog_open(prog_entry.get().split(' ')+file_list)).pack()
        alt_win.mainloop()

def toggle_hidden(event):
    global show_hidden_files
    show_hidden_files = not show_hidden_files
    menu_l.unpost()
    dir_change_action(0, 0, 0)

def target_duplicate():
    menu_l.unpost()
    list_of_list = file_sortout()
    file_list = list_of_list[0]
    for item_n in file_list:
        subprocess.Popen(['cp', '-r', item_n, item_n+'_copy']) 
    dir_change_action(0, 0, 0)

def rename_win_func(file_list, file_select, item_n):
    def rename_action(open_command):
        if open_command != 'SKIP':
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
    Label(rename_win, text="Rename "+file_select[item_n]+" to...").grid(row=0, column=0, rowspan=2, columnspan=2)
    newname_entry = ttk.Entry(rename_win)
    newname_entry.grid(row=0, column=2, columnspan=3, sticky=W+E)
    newname_entry.delete(0, END)
    newname_entry.insert(0, file_select[item_n])
    newname_entry.focus()
    newname_entry.bind('<Return>', lambda event: rename_action(['mv', file_list[item_n], os.getcwd()+'/'+newname_entry.get()]))
    newname_entry.bind('<Escape>', lambda event: rename_win.destroy())
    Button(rename_win, text="Rename", width=8, command=lambda: rename_action(['mv', file_list[item_n], os.getcwd()+'/'+newname_entry.get()])).grid(row=1, column=2)
    Button(rename_win, text="Skip", width=8, command=lambda: rename_action('SKIP')).grid(row=1, column=3)
    Button(rename_win, text="Cancel", width=8, command=lambda: rename_win.destroy()).grid(row=1, column=4)
    rename_win.update_idletasks()
    rename_win.update()

def target_rename():
    menu_l.unpost()
    list_of_list = file_sortout()
    if list_of_list[0] != []:
        rename_win_func(list_of_list[0], list_of_list[1], 0)

def target_delete():
    menu_l.unpost()
    list_of_list = file_sortout()
    file_list = list_of_list[0]
    file_select = list_of_list[1]
    if messagebox.askquestion("File Delete", "Delete these following files? "+str(', '.join(file_select))+"\nIt will be deleted forever.") == "yes":
        delete_popup = Tk()
        delete_popup.resizable(width=False, height=False)
        delete_popup.geometry("%dx%d+%d+%d" % (400, 100, 0, 0))
        for itr in range(0, len(file_list)):
            delete_popup.title("MartTkfManager - Deleting: "+file_list[itr])
            cur_del_text = Label(delete_popup, text="Deleting: "+file_list[itr])
            cur_del_text.pack()
            subprocess.call(['rm', '-fr']+[file_list[itr]])
            cur_del_text.destroy()
        delete_popup.destroy()
    dir_change_action(0, 0, 0)

def target_cut(): # 0 - Cut
    global file_list_clip
    menu_l.unpost()
    list_of_list = file_sortout()
    file_list_clip = list_of_list[0] + [0]

def target_copy(): # 1 - Copy
    global file_list_clip
    menu_l.unpost()
    list_of_list = file_sortout()
    file_list_clip = list_of_list[0] + [1]

def target_paste():
    menu_l.unpost()
    if file_list_clip[len(file_list_clip)-1] == 0: # Cut -> Paste acts like move
        subprocess.Popen(['mv']+file_list_clip[:-1]+[os.getcwd()+'/.'])
    elif file_list_clip[len(file_list_clip)-1] == 1: # Copy -> Paste acts like copy
        subprocess.Popen(['cp', '-r']+file_list_clip[:-1]+[os.getcwd()+'/.'])
    sleep(0.5)
    dir_change_action(0, 0, 0)

def target_mkdir():
    def mkdir_action(open_command):
        subprocess.Popen(open_command)
        mkdir_win.destroy()
        dir_change_action(0, 0, 0)
    menu_l.unpost()
    mkdir_win = Tk()
    mkdir_win.title("MartTkfManager - Make Directory")
    mkdir_win.resizable(width=False, height=False)
    Label(mkdir_win, text="New Directory's name...").grid(row=0, column=0)
    newdir_entry = ttk.Entry(mkdir_win)
    newdir_entry.grid(row=0, column=1, columnspan=3, sticky=W+E)
    newdir_entry.focus()
    newdir_entry.bind('<Return>', lambda event: mkdir_action(['mkdir', os.getcwd()+'/'+newdir_entry.get()]))
    newdir_entry.bind('<Escape>', lambda event: mkdir_win.destroy())
    ttk.Button(mkdir_win, text="Create", width=10, command=lambda: mkdir_action(['mkdir', os.getcwd()+'/'+newdir_entry.get()])).grid(row=1, column=1)
    ttk.Button(mkdir_win, text="Cancel", width=10, command=lambda: mkdir_win.destroy()).grid(row=1, column=2)
    mkdir_win.update_idletasks()
    mkdir_win.update()

def time_convert(time):
    s, ns = divmod(time, 1000000000) # 9 zeros
    m, s = divmod(s, 60)
    if m < 60:
        return "{:02d}:{:02d}".format(m,s)
    else:
        h,m  = divmod(m, 60)
        return "{:d}:{:02d}:{:02d}".format(h,m,s)

def mus_info_update(info_type, item_media):
    global mus_disp, playbin, side_frame, slider, mus_info, sa_show, sa_count, main
    if 'playbin' in globals() and info_type == 'INFO':
        mus_dur = time_convert(playbin.query_duration(Gst.Format.TIME)[1])
        mus_pos = time_convert(playbin.query_position(Gst.Format.TIME)[1]) 
        mus_time = mus_pos+' / '+mus_dur
        mus_disp.configure(text=mus_time)
        side_frame.after(100, lambda: mus_info_update('INFO', item_media))
    elif 'playbin' in globals() and info_type == 'INFO NAME':                                    # PLAYER INFORMATION FORMATTING
        mus_info_text = 'Playing: '+item_media
        if len(mus_info_text) > 40 and ('sa_show' in globals() and sa_show != None) :
            mus_info['text'] = mus_info_text[:int(0.0185 * main.winfo_width())]+'...'+sa_show
            sa_count += 1
        elif len(mus_info_text) > 40:
            mus_info['text'] = mus_info_text[:int(0.0370 * main.winfo_width())]+'...' 
        elif len(mus_info_text) <= 40 and ('sa_show' in globals() and sa_show != None):
            mus_info['text'] = mus_info_text[:int(0.0097 * main.winfo_width())]+' '+sa_show
            sa_count += 1
        else:
            mus_info['text'] = mus_info_text
        if sa_count >= 20:
            sa_count = 0
            sa_show = None
        side_frame.after(100, lambda: mus_info_update('INFO NAME', item_media))
    elif 'playbin' in globals() and info_type == 'SCALE TOTAL':
        slider['to'] = playbin.query_duration(Gst.Format.TIME)[1]
        if slider['to'] == 0:
            side_frame.after(100, lambda: mus_info_update('SCALE TOTAL', item_media))
    elif 'playbin' in globals() and info_type == 'SCALE':
        if slider.get() - playbin.query_position(Gst.Format.TIME)[1] > 1000000000 or slider.get() - playbin.query_position(Gst.Format.TIME)[1] < -1000000000 :
            playbin.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, slider.get())
    elif 'playbin' in globals() and info_type == 'SCALE UPDATE':
        slider.set(playbin.query_position(Gst.Format.TIME)[1])
        side_frame.after(100, lambda: mus_info_update('SCALE UPDATE', item_media))

def side_destroyer(): # destroys the side_frame and its contents
    global side_frame, playbin, mus_info, video, img_label, text_render, is_playing, img_load, tab_frame
    if 'img_label' in globals() or 'text_render' in globals():    # Checks if image been displayed
        if 'img_label' in globals(): # Image
            img_label.destroy()
            img_load = None
        elif 'text_render' in globals(): # Text
            text_render.destroy()
    if 'playbin' in globals() and playbin is not None: # Audio/Video
        playbin.set_state(Gst.State.NULL)
        playbin = None
        is_playing = False
    if 'video' in globals():
        video.destroy()
    if side_frame != None:
        side_frame.destroy()
        side_frame = Frame(tab_frame, width=0, height=0)
    mus_info = ''

def side_file_preview(event):       # SIDE PREVIEW DEVELOPMENT
    global img_label, side_frame, is_playing, playbin, mus_info, video, text_render, slider, img_load, media_path, control, tab_frame
    def on_sync_message(bus, message, window_id):
        if not message.get_structure() is None:
            if message.get_structure().get_name() == 'prepare-window-handle':
                image_sink = message.src
                image_sink.set_property('force-aspect-ratio', True)
                image_sink.set_window_handle(window_id)
    def on_player(state, player_type, media_path):
        global playbin, is_playing, side_frame, mus_disp, slider, sub_ind, aud_ind, sa_show, control, mus_info
        if state == 'PLAY' and is_playing == False:
            if player_type == 'MUSIC':
                playbin = Gst.ElementFactory.make("playbin", "player")
            elif player_type == 'VIDEO':
                playbin = Gst.ElementFactory.make("playbin", None)
            playbin.set_property('uri', 'file://'+media_path)
            playbin.set_property('volume', 0.5)
            playbin.set_property('subtitle-font-desc', 'Sans, 18')
            playbin.set_state(Gst.State.PLAYING)
            if player_type == 'VIDEO':
                bus = playbin.get_bus()
                bus.enable_sync_message_emission()
                bus.connect('sync-message::element', on_sync_message, window_id)
            mus_disp = Label(side_frame)
            mus_disp.pack(side=LEFT)
            mus_info_update('INFO', item_media)
            if player_type == 'VIDEO':
                mus_info = Label(control)
            elif player_type == 'MUSIC':
                mus_info = Label(side_frame)
            mus_info.pack(side=LEFT)
            mus_info_update('INFO NAME', item_media)
            slider = Scale(side_frame, from_=0, showvalue=0, orient=HORIZONTAL, resolution=0.1, command=lambda event: mus_info_update('SCALE', item_media))
            mus_info_update('SCALE TOTAL', item_media)
            slider.pack(fill=X, padx=5)
            is_playing = True
            mus_info_update('SCALE UPDATE', item_media)
            side_frame.update()                # RARE CRASH for .mainloop()
        elif state == 'PLAY' and is_playing == True:
            if playbin == None:
                is_playing = False
                on_player('PLAY', 'MUSIC', media_path)
            else:
                playbin.set_state(Gst.State.PLAYING)

        elif state == 'PAUSE':
            try:
                playbin.set_state(Gst.State.PAUSED)
            except:
                is_playing = False
        elif state == 'REWIND' and is_playing == True:
            rc, pos_int = playbin.query_position(Gst.Format.TIME)
            seek_ns = pos_int - 5 * 1000000000 # seek rewind/backward by 5 seconds
            if seek_ns < 0:
                seek_ns = 0
            playbin.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, seek_ns)
        elif state == 'FORWARD' and is_playing == True:
            rc, pos_int = playbin.query_position(Gst.Format.TIME)
            seek_ns = pos_int + 5 * 1000000000 # seek forward by 5 seconds
            playbin.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, seek_ns)
        elif (state == 'SUB' or state == 'AUD') and is_playing == True:
            current_code = None
            if state == 'SUB':
                sub_ind += 1
                if sub_ind >= playbin.get_property('n-text'):        # Amount of subtitles
                    sub_ind = 0
                playbin.set_property('current-text', sub_ind)
                tags = playbin.emit("get-text-tags", sub_ind)
            elif state == 'AUD':
                aud_ind += 1
                if aud_ind >= playbin.get_property('n-audio'):       # Amount of audios
                    aud_ind = 0
                playbin.set_property('current-audio', aud_ind)
                tags = playbin.emit("get-audio-tags", aud_ind)
            for itr in range(0, 4):
                try:
                    name = tags.nth_tag_name(itr)
                except:
                    break
                if name == "language-code":
                    current_code = tags.get_string(name)[1]
                    language = GstTag.tag_get_language_name(current_code)
                    break
            if current_code == None:
                current_code = 'null'
                language = 'null'
            if 'sa_show' in globals() and sa_show != None:
                sa_show = None
            if state == 'SUB':
                sa_show = 'Subtitle: '+str(sub_ind)+' ['+str(current_code).upper()+'] '+str(language)
            elif state == 'AUD':
                sa_show = 'Audio: '+str(aud_ind)+' ['+str(current_code).upper()+'] '+str(language)
        elif state == 'STOP':
            if playbin == None:
                is_playing = False
            else:
                playbin.set_state(Gst.State.NULL)
    item_media = tree.item(tree.focus())['text']

    if '.' not in item_media[1:]:   # Gets the item's tag to be matched
        file_ext = '*'
    else:
        file_ext = item_media.split('.')
        file_ext = file_ext[len(file_ext)-1]
    ext_conf = sort_file('EXT')
    try:
        tag_get = ext_conf[file_ext]
    except:
        tag_get = ext_conf['*']
    if item_media[0] != '/':
        media_path = os.getcwd()+'/'+item_media
    elif item_media[0] == '/':
        media_path = item_media
    if tag_get == 'images' and os.path.isdir(item_media) == False and main.winfo_width() >= 800:         # Per tags go with each proper instruction
        side_frame.grid(row=0, column=1, rowspan=2, sticky=N+S+W+E)
        try:
            img_load = Image.open(media_path)
            img_width, img_height = img_load.size
            new_img_width = int(main.winfo_width() / 2.4)
            new_img_height = int((img_height / img_width) * new_img_width)
            if new_img_height >= tree.winfo_height():
                new_img_height = tree.winfo_height()
                new_img_width = int((img_width / img_height) * new_img_height)
            img_load = img_load.resize((new_img_width, new_img_height), Image.ANTIALIAS)
            img_render = ImageTk.PhotoImage(img_load)
            img_label = Label(side_frame, image=img_render)
            img_label.image = img_render
            img_label.grid(row=0, column=0)
        except:
            side_frame.destroy()
    elif tag_get == 'text' and os.path.isdir(item_media) == False and file_ext == 'txt' and main.winfo_width() >= 800:
        side_frame.destroy()
        side_frame = Frame(tab_frame, width=150, height=250)
        text_scrollbar = ttk.Scrollbar(side_frame, orient=VERTICAL)
        text_scrollbar.grid(row=0, column=1, rowspan=15, sticky=N+S)
        side_frame.grid(row=0, column=1, rowspan=2, sticky=N+S+W+E)
        text_load = open(media_path, 'r', encoding="ISO-8859-1").readlines()
        text_render = Text(side_frame, width=80, height=30, wrap=WORD, yscrollcommand=text_scrollbar.set)
        for text_line in text_load:
            text_render.insert(END, text_line + '\n')
        text_render.grid(row=0, column=0)
        text_scrollbar.config(command=text_render.yview)
    elif (tag_get == 'music' or tag_get == 'midi') and os.path.isdir(item_media) == False: # MUSIC PLAYER
        side_frame.destroy()
        side_frame = Frame(tab_frame, width=150, height=50)
        side_frame.grid(row=1, column=0, rowspan=2, sticky=N+S+W+E) # under the list
        play_button = Button(side_frame, text='\u23F4', width=1, command=lambda: on_player('PLAY', 'MUSIC', media_path))          # NOTED DURING RARE CRASH
        pause_button = Button(side_frame, text='\u23F8', width=1, command=lambda: on_player('PAUSE', 'MUSIC', media_path))
        rewind_button = Button(side_frame, text='\u23EA', width=1, command=lambda: on_player('REWIND', 'MUSIC', media_path))
        forward_button = Button(side_frame, text='\u23E9', width=1, command=lambda: on_player('FORWARD', 'MUSIC', media_path))
        stop_button = Button(side_frame, text='\u23F9', width=1, command=lambda: on_player('STOP', 'MUSIC', media_path))
        rewind_button.pack(side=LEFT)
        play_button.pack(side=LEFT)
        pause_button.pack(side=LEFT)
        forward_button.pack(side=LEFT)
        stop_button.pack(side=RIGHT)
    elif tag_get == 'videos' and os.path.isdir(item_media) == False and main.winfo_width() >= 800: # VIDEO PLAYER
        side_frame.destroy()
        side_frame = Frame(tab_frame)
        side_frame.grid(row=0, column=1, columnspan=50, rowspan=2, sticky=N+S+W+E)
        video = Frame(side_frame, bg="#000000", width=int(main.winfo_width() / 2.4))
        video.pack(expand=YES, fill=BOTH)
        window_id = video.winfo_id()
        control = Frame(side_frame)
        control.pack(fill=X)
        play_button = Button(control, text='\u23F4', width=1, command=lambda: on_player('PLAY', 'VIDEO', media_path))
        pause_button = Button(control, text='\u23F8', width=1, command=lambda: on_player('PAUSE', 'VIDEO', media_path))
        rewind_button = Button(control, text='\u23EA', width=1, command=lambda: on_player('REWIND', 'VIDEO', media_path))
        forward_button = Button(control, text='\u23E9', width=1, command=lambda: on_player('FORWARD', 'VIDEO', media_path))
        sub_tog_button = Button(control, text='SUB', width=1, command=lambda: on_player('SUB', 'VIDEO', media_path))
        aud_tog_button = Button(control, text='AUD', width=1, command=lambda: on_player('AUD', 'VIDEO', media_path))
        stop_button = Button(control, text='\u23F9', width=1, command=lambda: on_player('STOP', 'VIDEO', media_path))
        rewind_button.pack(side=LEFT)
        play_button.pack(side=LEFT)
        pause_button.pack(side=LEFT)
        forward_button.pack(side=LEFT)
        stop_button.pack(side=RIGHT, padx=5)
        sub_tog_button.pack(side=RIGHT)
        aud_tog_button.pack(side=RIGHT)
    elif side_frame in globals():
        side_destroyer()

def file_search(search_type): # File find and search function
    global find_win
    find_win = Tk()
    find_win.resizable(width=False, height=False)
    find_win.title("MartTkfManager - "+search_type.capitalize())
    Label(find_win, text=search_type.capitalize()+": ").grid(row=0, column=0)
    find_input = ttk.Entry(find_win)
    find_input.grid(row=0, column=1, columnspan=3, sticky=W+E)
    find_input.bind('<Return>', lambda event: dir_change_action(search_type, 0, find_input.get()))
    find_input.bind('<Escape>', lambda event: find_win.destroy())
    ttk.Button(find_win, text=search_type.capitalize(), command=lambda: dir_change_action(search_type, 0, find_input.get())).grid(row=1, column=1)
    ttk.Button(find_win, text="Cancel", command=lambda: find_win.destroy()).grid(row=1, column=2)
    find_input.focus_set()

def tree_height_updater(old_height, old_width, old_dir, height, width, cwd, old_num):
    global tree, side_frame, img_load, img_label, media_path, video, dir_changed, tab_frame, tab_num
    if 'tree' in globals() and tree != None and (height != old_height or cwd != old_dir or dir_changed == True or tab_num != old_num):
        try:
            if height >= 800:
                tree['height'] = int(height * 0.04459)
            elif height >= 700:
                tree['height'] = int(height * 0.04259)
            elif height >= 600:
                tree['height'] = int(height * 0.04059)
            else:
                tree['height'] = int(height * 0.03459)
            old_height = height
            old_dir = cwd
            dir_changed = False
            old_num = tab_num
        except:
            pass
    if 'side_frame' in globals() and (width != old_width):
        if 'img_label' in globals() and 'img_load' in globals() and img_label != None and img_load != None:
            img_load = Image.open(media_path)
            img_width, img_height = img_load.size
            new_img_width = int(width / 2.4)
            new_img_height = int((img_height / img_width) * new_img_width)
            if new_img_height >= tree.winfo_height():
                new_img_height = tree.winfo_height()
                new_img_width = int((img_width / img_height) * new_img_height)
            img_load = img_load.resize((new_img_width, new_img_height), Image.ANTIALIAS)
            img_render = ImageTk.PhotoImage(img_load)
            img_label.configure(image=img_render)
            img_label.image = img_render
            img_label.grid(row=0, column=0)
        elif 'video' in globals() and video != None:
            try:
                video['width'] = int(width / 2.4)
            except:
                pass
        old_width = width
    main.after(10, lambda: tree_height_updater(old_height, old_width, old_dir, main.winfo_height() - 20, main.winfo_width(), os.getcwd(), old_num))

def bind_cur_dir_entry(event):
    global menu_l, cur_dir_entry
    menu_l.unpost()
    cur_dir_entry.focus_set()

def row_change(event, pos_change):
    global id_pos, is_playing, playbin, tree, id_list
    side_destroyer()
    side_file_preview(event)
    menu_l.unpost()
    tree.focus_set()
    id_pos += pos_change
    if id_pos < 0 or pos_change == 0:
        id_pos = 0
    elif id_pos > len(id_list) - 1 or pos_change == 2:
        id_pos = len(id_list) - 1
    tree.focus(id_list[id_pos])

def r_click(event): # RIGHT CLICK MENU
    menu_l.post(event.x_root, event.y_root)

def main_list_dir(matching_list):
    global history, dir_info_01, show_hidden_files, tree, access_info, id_pos, mus_info, cur_dir_entry, tab_frame, id_list
            
    cur_dir_entry.delete(0, 'end') 
    cur_dir_entry.insert(0, os.getcwd())
    cur_dir_entry.bind('<Return>', lambda event: dir_change_action(0, cur_dir_entry.get(), 1))
    
    row_place, col_place = 2, 0
    dir_ls = os.listdir(os.getcwd())

    if sort_type == 'Name Ascending':
        dir_ls.sort()
    elif sort_type == 'Name Descending':
        dir_ls.sort(reverse=True)

    list_frame.grid(row=0, column=0, sticky=N+W+E)
    scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL)
    scrollbar.grid(row=0, column=20, rowspan=15, sticky=N+S)
    tree = ttk.Treeview(list_frame, columns=('size', 'last_mod', 'uid_gid', 'ext'), yscrollcommand=scrollbar.set) #  height=46,  when 1080px height
    tree.grid(row=0, column=0, columnspan=20, sticky=W+E+N+S)
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
    if matching_list != 0: # Find/Search
        dir_ls = matching_list
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
    tree.tag_bind('file', '<Button-1>', side_file_preview)
    tree.tag_bind('dir', '<Double-Button-1>', lambda event: dir_change_action(0, tree.item(tree.focus())['text'], 1))
    tree.tag_bind('file', '<Double-Button-1>', ext_prog)
    tree.tag_bind('up', '<Double-Button-1>', lambda event: dir_change_action(0, '..', 1))
    tree.tag_bind('dir', '<Right>', lambda event: dir_change_action(0, tree.item(tree.focus())['text'], 1))
    tree.tag_bind('file', '<Right>', ext_prog)
    tree.tag_bind('up', '<Right>', lambda event: dir_change_action(0, '..', 1))
    tree.bind('<Button-3>', r_click)
    scrollbar.config(command=tree.yview)

    bottom_frame.grid(row=3, column=0, columnspan=2, sticky=N+W+E)
    sizestat = os.statvfs('/')
    lower_info_text = 'Total overall/directories/files: '+str(total_dir+total_file)+'/'+str(total_dir)+'/'+str(total_file)+'    Hidden files shown: '+str(show_hidden_files)+'    Free Space: '+str(human_readable_size(sizestat.f_frsize * sizestat.f_bfree))+'    Total Space: '+str(human_readable_size(sizestat.f_frsize * sizestat.f_blocks))+access_info
    if 'dir_info_01' not in globals():
        dir_info_01 = Label(bottom_frame, text=lower_info_text)
        dir_info_01.grid(row=0, column=0, columnspan=8, sticky='w')
    else:
        dir_info_01.configure(text=lower_info_text)

def add_button(itr_tab):
    global tab_frame, tab_num, tab_frame_label, tab_frame_title, tab_show_frame, tab_frame_label_exit
    if 'tab_frame_label_exit' in globals():
        tab_frame_label_exit.destroy()
    tab_frame_label[0].append(Frame(tab_show_frame))
    tab_frame_label_exit = Button(tab_frame_label[0][itr_tab+1], text='+', command=lambda: add_tab(False))
    tab_frame_label_exit.pack(side=RIGHT)
    tab_frame_label[0][itr_tab+1].pack(side=LEFT)

def add_tab(new):
    global tab_frame, tab_num, tab_frame_label, tab_frame_title, tab_show_frame, list_frame, side_frame, tab_frame_dir, viable_tabs, menu_l
    if new == False:
        side_destroyer()
        tab_frame.destroy()
        tab_frame_label_changer(tab_bg_colour_inactive)
        tab_frame = Frame(main)
        tab_frame_title += [home]
        tab_frame_dir += [home]
        tab_num = len(tab_frame_title) - 1
        viable_tabs += [tab_num]
    else:
        tab_frame = Frame(main)
        tab_frame_title = [home]
        tab_frame_dir = [os.getcwd()]
        viable_tabs += [0]
    os.chdir(home) 
    
    tab_frame.grid_columnconfigure(0, weight=1, minsize = 480)
    tab_frame.grid_rowconfigure(0, minsize = 40)
    tab_frame.grid(row=2, column=0, sticky=N+S+W+E)
    tab_frame.grid_propagate(True)
    
    if new == False:
        side_frame.destroy()
        list_frame.destroy()
        menu_l.destroy()

    side_frame = Frame(tab_frame)
    list_frame = Frame(tab_frame)
    list_frame.columnconfigure(0, weight=1)
    menu_l = Menu(tab_frame, tearoff=0)
    menu_l_add_command(menu_l)

    tab_frame_label[0].append(Frame(tab_show_frame))
    tab_frame_label[1].append(Label(tab_frame_label[0][tab_num], text=tab_frame_title[tab_num]))
    tab_num_local = tab_num
    tab_frame_label[2].append(Button(tab_frame_label[0][tab_num], text='x', command=lambda: exit_tab(tab_num_local)))
    tab_frame_label[2][tab_num].pack(side=RIGHT)#.grid(row=0, column=1, sticky=E)
    tab_frame_label[1][tab_num].pack(side=RIGHT)#.grid(row=0, column=0, sticky=E)
    tab_frame_label[0][tab_num].pack(side=LEFT, fill=X, expand=YES)
    tab_frame_label[0][tab_num].bind('<Button-1>', lambda event: goto_tab(tab_num_local, 'CHANGE'))
    tab_frame_label[1][tab_num].bind('<Button-1>', lambda event: goto_tab(tab_num_local, 'CHANGE'))
    tab_frame_label_changer(tab_bg_colour_active)
    add_button(tab_num)
        
    main_list_dir(0)
    if new == False:
        tab_frame.update()

def goto_tab(goto_num, go_type): # go_type - EXIT (from exit_tab) or CHANGE
    global tab_frame, tab_num, tab_frame_label, tab_frame_title, tab_show_frame, list_frame, side_frame, tab_frame_dir, playbin, min_tab, menu_l
    if goto_num > viable_tabs[-1]:
        goto_num = viable_tabs[0]
    if tab_frame_title[goto_num] == None and go_type == 'BINDING':
        original_goto = goto_num
        try:
            while tab_frame_title[goto_num] == None:
                goto_num += 1
        except IndexError:
            goto_num = original_goto
            while tab_frame_title[goto_num] == None:
                goto_num += 1
    if go_type == 'CHANGE' or go_type == 'BINDING':
        side_destroyer()
        tab_frame.destroy()
        tab_frame_label_changer(tab_bg_colour_inactive)
        tab_num = goto_num
        tab_frame_label_changer(tab_bg_colour_active)
    elif go_type == 'EXIT':
        for itr in range(0, len(tab_frame_title)):
            if (itr != min_tab or itr != goto_num) and tab_frame_title[itr] != None:
                min_tab = itr
        tab_num = min_tab
        try:
            tab_frame_label_changer(tab_bg_colour_active)
        except:
            sys.exit()
    os.chdir(tab_frame_dir[tab_num])
    tab_frame = Frame(main)
    main.title("MartTKfManager - "+tab_frame_dir[tab_num])

    tab_frame.grid_columnconfigure(0, weight=1, minsize = 480)
    tab_frame.grid_rowconfigure(0, minsize = 40)
    tab_frame.grid(row=2, column=0, sticky=N+S+W+E)
    tab_frame.grid_propagate(True)

    side_frame.destroy()
    list_frame.destroy()
    menu_l.destroy()

    side_frame = Frame(tab_frame)
    list_frame = Frame(tab_frame)
    list_frame.columnconfigure(0, weight=1)
    menu_l = Menu(tab_frame, tearoff=0)
    menu_l_add_command(menu_l)

    dir_change_action(0,0,0)
    main_list_dir(0)
    tab_frame.update()

def exit_tab(itr_tab): # Still does not work
    global tab_num, tab_frame, tab_frame_label, tab_show_frame, tab_frame_title, viable_tabs
    side_destroyer()
    tab_visible = 1
    for itr in range(0, len(viable_tabs)):
        try:
            if viable_tabs[itr] == itr_tab:
                del viable_tabs[itr]
        except:
            break
    if viable_tabs == []:
        sys.exit()
    else:
        tab_frame.destroy()
        tab_frame_label[0][itr_tab].destroy()
        tab_frame_label[0][itr_tab] = None
        tab_frame_title[itr_tab] = None
        goto_tab(itr_tab, 'EXIT')
    
os.chdir(home) 
main = Tk()
main.title("MartTKfManager - "+os.getcwd())
icon = PhotoImage(file=project_dir+'/beta_logo.png')
main.call('wm', 'iconphoto', main._w, icon)
main.geometry("%dx%d+%d+%d" % (970, 490, 0, 0))
#main.grid_rowconfigure(0, weight=1)
main.grid_columnconfigure(0, weight=1)
tab_frame_label = []
for g_itr in range(0, 3):
    tab_frame_label.append([])
tab_show_frame = Frame(main, height=10)
tab_show_frame.grid(row=0, column=0, sticky=W+E)
top_frame = Frame(main)
bottom_frame = Frame(main)
top_frame.columnconfigure(0, weight=1)
top_frame.grid(row=1, column=0, sticky=N+S+W+E)
cur_dir_entry, extra_menu = main_buttons()
add_tab(True)
tree_height_updater(0,0,'', main.winfo_height() - 20, main.winfo_width(), os.getcwd(), 0)

main.bind('<Control-h>', toggle_hidden)
main.bind('<Control-r>', lambda event: dir_change_action(0, 0, 0))
main.bind('<Control-l>', bind_cur_dir_entry)
main.bind('<Left>', lambda event: dir_change_action(0, '..', 1))
main.bind('<Up>', lambda event: row_change(event, -1))
main.bind('<Down>', lambda event: row_change(event, 1))
main.bind('<Control-Up>', lambda event: row_change(event, -10)) 
main.bind('<Control-Down>', lambda event: row_change(event, 10))
main.bind('<Home>', lambda event: row_change(event, 0))
main.bind('<End>', lambda event: row_change(event, 2))
main.bind('<Control-Q>', sys.exit)
main.bind('<Button-1>', lambda event: menu_l.unpost())
main.bind('<Control-f>', lambda event: file_search('FIND'))
main.bind('<Control-s>', lambda event: file_search('SEARCH'))
main.bind('<Control-t>', lambda event: add_tab(False))
main.bind('<Control-q>', lambda event: exit_tab(tab_num))
main.bind('<Control-Tab>', lambda event: goto_tab(tab_num+1, 'BINDING'))

tab_frame.configure(background="#EEE")
ttk.Style().layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

main.mainloop()

