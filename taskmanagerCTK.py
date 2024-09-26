from customtkinter import *
import functools
import mysql.connector as sql
import sys, os

def auth():
    username = username_box.get()
    password = password_box.get()

    q = "SELECT * from userinfo"
    cursor.execute(q)
    data = cursor.fetchall()
    for rec in data:
        if rec[0] == username and rec[1] == password:
           tasks_win.tkraise()
           tasks_page_welctext.configure(text="Welcome back, {}!".format(rec[2]))
           usercontent(username)
           global current_user
           current_user = username
           break
    else:
        wrongpass_text.configure(text="Incorrect username or password, try again.")

def usercontent(username):
    q = "SELECT * from tasks where username = '{}'".format(username)
    cursor.execute(q)
    data = cursor.fetchall()
    row = pending_task_gen(data)
    done_task_gen(data, row)

def pending_task_gen(tasklist):

    r = 1
    i = 0
    tasklabel_list = []
    task_done_button_list = []
    task_del_button_list = []

    tasks_page_pendingtext = CTkLabel(tasks_page_taskframe, text="Pending tasks: ",font=("Microsoft Yahei UI", 20))
    tasks_page_pendingtext.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    for task in tasklist:

        if task[2] == "pending":
            tasklabel = CTkLabel(tasks_page_taskframe, text="• {}".format(task[1]), font=("Microsoft Yahei UI", 18))
            tasklabel.grid(row=r, column=0, padx=20, pady=10, sticky="w")
            tasklabel_list.append(tasklabel)

            task_done_button = CTkButton(tasks_page_taskframe, text="Done", font=("Microsoft Yahei UI", 15), width= 90, fg_color="green", command=functools.partial(task_done, tasklabel_list, i))
            task_done_button.grid(row=r, column=1, sticky="e", padx=10, pady=10)
            task_done_button_list.append(task_done_button)

            task_del_button = CTkButton(tasks_page_taskframe, text="Delete", font=("Microsoft Yahei UI", 15), width=90, fg_color="red", command=functools.partial(task_del, tasklabel_list, task_done_button_list, task_del_button_list, i))
            task_del_button.grid(row=r, column=2, padx=(0,10), pady=10, sticky="e")
            task_del_button_list.append(task_del_button)
        
            r += 1
            i += 1
        else:
            continue    

    if i == 0:
        nil_label = CTkLabel(tasks_page_taskframe, text="No Tasks available",font=("Microsoft Yahei UI", 20))
        nil_label.grid(row=r, column=0, padx=10, pady=10, sticky="w")
        r += 1
    
    return r
    

def done_task_gen(tasklist, r):
    i = 0
    tasklabel_list = []
    task_undone_button_list = []
    task_del_button_list = []

    tasks_page_donetext = CTkLabel(tasks_page_taskframe, text="Done tasks: ",font=("Microsoft Yahei UI", 20))
    tasks_page_donetext.grid(row=r, column=0, padx=10, pady=10, sticky="w")
    r += 1

    for task in tasklist:
        
        if task[2] == "done":
        
            tasklabel = CTkLabel(tasks_page_taskframe, text="• {}".format(task[1]), font=("Microsoft Yahei UI", 18))
            tasklabel.grid(row=r, column=0, padx=20, pady=10, sticky="w")
            tasklabel_list.append(tasklabel)

            task_undone_button = CTkButton(tasks_page_taskframe, text="Undo", font=("Microsoft Yahei UI", 15), width= 90, fg_color="green", command=functools.partial(task_undone, tasklabel_list, i))
            task_undone_button.grid(row=r, column=1, sticky="e", padx=10, pady=10)
            task_undone_button_list.append(task_undone_button)

            task_del_button = CTkButton(tasks_page_taskframe, text="Delete", font=("Microsoft Yahei UI", 15), width=90, fg_color="red", command=functools.partial(task_del, tasklabel_list, task_undone_button_list, task_del_button_list, i))
            task_del_button.grid(row=r, column=2, padx=(0,10), pady=10, sticky="e")
            task_del_button_list.append(task_del_button)
        
            r += 1
            i += 1
        else:
            continue

    if i == 0:
        nil_label = CTkLabel(tasks_page_taskframe, text="No Tasks available",font=("Microsoft Yahei UI", 20))
        nil_label.grid(row=r, column=0, padx=10, pady=10, sticky="w")

def frame_refresh():
    global tasks_page_taskframe
    tasks_page_taskframe.destroy()
    tasks_page_taskframe = CTkScrollableFrame(tasks_page_taskframe_wrapper)
    tasks_page_taskframe.grid(row=0, column=0, sticky="nsew")
    tasks_page_taskframe.columnconfigure(0, weight=100)
    tasks_page_taskframe.columnconfigure((1,2), weight=1)
    usercontent(current_user)

def task_del(label_list, done_button_list, del_button_list, idx):
    raw = label_list[idx].cget("text")
    task = raw[2:]
    q = "DELETE from tasks WHERE task = '{}'".format(task)
    cursor.execute(q)
    con.commit()
    label_list[idx].destroy()
    done_button_list[idx].destroy()
    del_button_list[idx].destroy()
    frame_refresh()

def task_done(label_list, idx):
    raw = label_list[idx].cget("text")
    task = raw[2:]
    q = "UPDATE tasks SET status = '{}' WHERE task = '{}'".format("done", task)
    cursor.execute(q)
    con.commit()
    frame_refresh()
            
def task_undone(label_list, idx):
    raw = label_list[idx].cget("text")
    task = raw[2:]
    q = "UPDATE tasks SET status = '{}' WHERE task = '{}'".format("pending", task)
    cursor.execute(q)
    con.commit()
    frame_refresh()

def actual_addtask():
    new_task = add_task_entry.get()
    if new_task == "":
        notask_label.configure(text="Please enter a task.", text_color="red")
    else:
        status = "pending"
        q = "INSERT INTO tasks VALUES('{}', '{}', '{}')".format(current_user, new_task, status)
        cursor.execute(q)
        con.commit()
        add_task_entry.delete(0, END)
        notask_label.configure(text="Task added.", text_color="#16c71f")
        frame_refresh()

def add_new_task(button):
    tasks_page_addtaskframe.tkraise()
    button.destroy()
    back_button = CTkButton(tasks_win, text="back", font=("Microsoft Yahei UI", 18), command=lambda : add_newtask_back(back_button))
    back_button.grid(row=2, column=0, padx=20, pady=20, sticky="e")

def add_newtask_back(button):
    tasks_page_taskframe_wrapper.tkraise()
    button.destroy()
    tasks_page_add_task_button = CTkButton(tasks_win, text="add new task", font=("Microsoft Yahei UI", 18), command=lambda : add_new_task(tasks_page_add_task_button))
    tasks_page_add_task_button.grid(row=2, column=0, padx=20, pady=20, sticky="e")

def signup_data_collect():
    username = signup_page_usernamebox.get()
    password = signup_page_passwordbox.get()
    name = signup_page_namebox.get()
    age = signup_page_agebox.get()
    address = signup_page_addressbox.get()

    for data in (username, password, name, age, address):
        if data == "":
            signup_page_nodatatext.configure(text="Please enter all the details.", text_color="red")
            break
    else:
        q = "INSERT INTO userinfo VALUES('{}', '{}', '{}', {}, '{}')".format(username, password, name, age, address)
        cursor.execute(q)
        con.commit()
        signup_page_nodatatext.configure(text="Account created successfully.", text_color="#16c71f")
        global signup_page_signupbutton
        signup_page_signupbutton.destroy()
        signup_page_signupbutton = CTkButton(signup_win, text="continue", font=("Microsoft Yahei UI", 18), command=lambda : login_win.tkraise())
        signup_page_signupbutton.grid(row=8, column=0, columnspan=2, pady=(0,20))


#sql connectivity
con = sql.connect(user = "root", host = "localhost", passwd = "sarvesh123", database = "taskmanager")
cursor = con.cursor()

current_user = ""

#setting up root window
root = CTk()
root.title("Personalized Task Manager")
root.geometry("900x500")
set_appearance_mode("dark")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#declaring windows
login_win = CTkFrame(root)
login_win.grid(row=0, column=0, sticky="nsew")

tasks_win = CTkFrame(root)
tasks_win.grid(row=0, column=0, sticky="nsew")

signup_win = CTkFrame(root)
signup_win.grid(row=0, column=0, sticky="nsew")

login_win.tkraise() #putting login page on top

# --- Login Page Start ---

title = CTkLabel(login_win, text="Personalized Task Manger", font=("Microsoft YaHei UI", 40))
title.pack(pady=20)

login_frame = CTkFrame(login_win, width=300, height = 300, fg_color="#48484a")
login_frame.pack(pady=20)
login_frame.columnconfigure((0, 1), weight=1)

login_text = CTkLabel(login_frame, text="Login", font=("Microsoft YaHei UI", 25), width=250, height=40, corner_radius= 7, text_color="#FFFFFF")
login_text.grid(row=0, column=0, pady=10, padx=25, columnspan=2)

user_text = CTkLabel(login_frame, text="Username:", font=("Microsoft YaHei UI", 20))
user_text.grid(row=1, column=0, sticky="w", padx=25)

username_box = CTkEntry(login_frame, width=250, height=40)
username_box.grid(row=2, column=0, pady=(0,5), columnspan=2)

pass_text = CTkLabel(login_frame, text="Password:", font=("Microsoft YaHei UI", 20))
pass_text.grid(row=3, column=0, sticky="w", padx=25)

password_box = CTkEntry(login_frame, width=250, height=40)
password_box.grid(row=4, column=0, pady=(0,5), columnspan=2)

wrongpass_text =CTkLabel(login_frame, text="", font=("Microsoft YaHei UI", 12), text_color="red")
wrongpass_text.grid(row=5, column=0, padx=25, pady=(0,15), columnspan=2)

login_button = CTkButton(login_frame, text="Login", font=("Microsoft YaHei UI", 16), width=120, command=auth)
login_button.grid(row=6, column=0, pady=(0,20), sticky="ew", padx=20)

signup_button = CTkButton(login_frame, text="Sign-Up", font=("Microsoft YaHei UI", 16), width=120,command=lambda : signup_win.tkraise())
signup_button.grid(row=6, column=1, pady=(0,20), sticky="ew", padx=(0,20))

# --- Login Page end --- 


# --- Sign up Page start ---

signup_win.columnconfigure(0, weight=1)
signup_win.columnconfigure(1, weight=5)

signup_page_text = CTkLabel(signup_win, text="Sign-up", font=("Microsoft Yahei UI", 30))
signup_page_text.grid(row=0, column=0, padx=20, pady=(20,0), columnspan=2)

signup_page_lb1 = CTkLabel(signup_win, text="Enter the following details: ", font=("Microsoft Yahei UI", 25))
signup_page_lb1.grid(row=1, column=0, padx=20, pady=(0,20), sticky="w", columnspan=2)

signup_page_usernametext = CTkLabel(signup_win, text="Username: ", font=("Microsoft Yahei UI", 20))
signup_page_usernametext.grid(row=2, column=0, padx=20, pady=(0,20), sticky="w")

signup_page_usernamebox = CTkEntry(signup_win, width=250, height=40)
signup_page_usernamebox.grid(row=2, column=1, pady=(0,20), sticky="w")

signup_page_passwordtext = CTkLabel(signup_win, text="Password: ", font=("Microsoft Yahei UI", 20))
signup_page_passwordtext.grid(row=3, column=0, padx=20, pady=(0,20), sticky="w")

signup_page_passwordbox = CTkEntry(signup_win, width=250, height=40)
signup_page_passwordbox.grid(row=3, column=1, pady=(0,20), sticky="w")

signup_page_nametext = CTkLabel(signup_win, text="Name: ", font=("Microsoft Yahei UI", 20))
signup_page_nametext.grid(row=4, column=0, padx=20, pady=(0,20), sticky="w")

signup_page_namebox = CTkEntry(signup_win, width=250, height=40)
signup_page_namebox.grid(row=4, column=1, pady=(0,20), sticky="w")

signup_page_agetext = CTkLabel(signup_win, text="Age: ", font=("Microsoft Yahei UI", 20))
signup_page_agetext.grid(row=5, column=0, padx=20, pady=(0,20), sticky="w")

signup_page_agebox = CTkEntry(signup_win, width=250, height=40)
signup_page_agebox.grid(row=5, column=1, pady=(0,20), sticky="w")

signup_page_addresstext = CTkLabel(signup_win, text="Address: ", font=("Microsoft Yahei UI", 20))
signup_page_addresstext.grid(row=6, column=0, padx=20, pady=(0,20), sticky="w")

signup_page_addressbox = CTkEntry(signup_win, width=250, height=40)
signup_page_addressbox.grid(row=6, column=1, pady=(0,30), sticky="w")

signup_page_nodatatext = CTkLabel(signup_win, text="", text_color="red", font=("Microsoft Yahei UI", 16))
signup_page_nodatatext.grid(row=7, column=0, columnspan=2, padx=20, sticky="w")

signup_page_signupbutton = CTkButton(signup_win, text="sign-up", font=("Microsoft Yahei UI", 18), command=signup_data_collect)
signup_page_signupbutton.grid(row=8, column=0, columnspan=2, pady=(0,20))

# --- Sign up Page end ---

# --- task page start ---

tasks_win.columnconfigure((0,1), weight=1)
tasks_win.rowconfigure(1, weight=1)

tasks_page_welctext = CTkLabel(tasks_win, text="Welcome back _____!",font=("Microsoft Yahei UI", 25))
tasks_page_welctext.grid(row=0, column=0, padx=20, pady=20, sticky="w", columnspan=2)

# making sub pages

tasks_page_taskframe_wrapper = CTkFrame(tasks_win)
tasks_page_taskframe_wrapper.grid(row=1, column=0, sticky="nsew", padx=10, columnspan=2)
tasks_page_taskframe_wrapper.columnconfigure(0, weight=1)
tasks_page_taskframe_wrapper.rowconfigure(0, weight=1)

tasks_page_taskframe = CTkScrollableFrame(tasks_page_taskframe_wrapper)
tasks_page_taskframe.grid(row=0, column=0, sticky="nsew")
tasks_page_taskframe.columnconfigure(0, weight=100)
tasks_page_taskframe.columnconfigure((1,2), weight=1)

tasks_page_addtaskframe = CTkFrame(tasks_win)
tasks_page_addtaskframe.grid(row=1, column=0, sticky="nsew", padx=10, columnspan=2)

tasks_page_taskframe_wrapper.tkraise()

# main tasklist page

tasks_page_add_task_button = CTkButton(tasks_win, text="add new task", font=("Microsoft Yahei UI", 18), command=lambda : add_new_task(tasks_page_add_task_button))
tasks_page_add_task_button.grid(row=2, column=0, padx=20, pady=20, sticky="e")

logout_button = CTkButton(tasks_win, text="logout", font=("Microsoft Yahei UI", 18), command=lambda : os.execv(sys.executable, ['python'] + sys.argv))
logout_button.grid(row=2, column=1, padx=20, pady=20, sticky="w")

# add new tasks page
add_task_text = CTkLabel(tasks_page_addtaskframe, text="Add new task:" , font=("Microsoft Yahei UI", 20))
add_task_text.pack(padx= 20, pady=20, anchor="w" )

add_task_entry = CTkEntry(tasks_page_addtaskframe, font=("Microsoft Yahei UI", 16), width=400)
add_task_entry.pack(padx=20, anchor="w")

notask_label = CTkLabel(tasks_page_addtaskframe, text="", font=("Microsoft Yahei UI", 14), text_color="red")
notask_label.pack(padx=20, pady=(5,0), anchor="w")


add_newtask_button = CTkButton(tasks_page_addtaskframe, text="Add Task", font=("Microsoft Yahei UI", 16), command=actual_addtask)
add_newtask_button.pack(padx=20, pady=20, anchor="w")

# --- tasks page end ---



root.mainloop()