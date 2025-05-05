import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import os
import datetime
import webbrowser

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

all_tasks = []
chat_data = {}
file_list = []

#----------------------------------------------------------------
def open_dashboard():
    login_window.destroy()

    dashboard = ctk.CTk()
    screen_width = dashboard.winfo_screenwidth()
    screen_height = dashboard.winfo_screenheight()
    dashboard.geometry(f"{screen_width}x{screen_height}+0+0")
    dashboard.title("WorkNet - Dashboard")

    main_frame = ctk.CTkFrame(dashboard)
    main_frame.pack(fill="both", expand=True)

    sidebar_frame = ctk.CTkFrame(main_frame, width=100, fg_color="#e0e0e0")
    sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)

    content_area = ctk.CTkFrame(main_frame)
    content_area.pack(side="left", fill="both", expand=True)

    def show_home_page():
        for widget in content_area.winfo_children():
            widget.destroy()

        summary_card = ctk.CTkFrame(content_area, fg_color="white", width=1000, height=550, corner_radius=15)
        summary_card.place(relx=0.5, rely=0.4, anchor="center")
        summary_card.pack_propagate(False)

        logo_image = ctk.CTkImage(light_image=Image.open("icons/logo.png"), size=(150, 150))
        ctk.CTkLabel(summary_card, image=logo_image, text="").pack(pady=(5, 10))

        ctk.CTkLabel(summary_card, text="Welcome to WorkNet!", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="black").pack(pady=(20, 10))
        ctk.CTkLabel(summary_card, text="Here's a quick summary of your workspace:", font=ctk.CTkFont(size=14),
                     text_color="black").pack(pady=(0, 15))

        completed = sum(t['done'] for t in all_tasks)
        ctk.CTkLabel(summary_card, text=f"✔ Completed Tasks: {completed}", font=ctk.CTkFont(size=16),
                     text_color="black").pack(pady=(0, 10))

        uploaded = len(file_list)
        ctk.CTkLabel(summary_card, text=f"✔ Uploaded Files: {uploaded}", font=ctk.CTkFont(size=16),
                     text_color="black").pack(pady=(0, 20))

        ctk.CTkButton(summary_card, text="Go to Tasks", width=170, height=40, fg_color="#007BFF", text_color="white",
                      command=show_tasks_page).pack(pady=(10, 0))

#----------------------------------------------------------------
    def show_tasks_page():
        for widget in content_area.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(content_area, text="Tasks", font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(pady=20)

        tasks_container = ctk.CTkFrame(content_area, fg_color="#f2f2f2")
        tasks_container.pack(padx=60, pady=10, ipadx=30, ipady=30, fill="both", expand=True)

        task_entry = ctk.CTkEntry(tasks_container, placeholder_text="Enter a new task...", width=400)
        task_entry.pack(pady=(10, 10))

        def refresh_tasks():
            for widget in tasks_list_frame.winfo_children():
                widget.destroy()

            for task in all_tasks:
                task_frame = ctk.CTkFrame(tasks_list_frame)
                task_frame.pack(fill="x", pady=5, padx=10)

                label_text = task['text'] + (" - Done" if task['done'] else "")
                task_label = ctk.CTkLabel(task_frame, text=label_text, anchor="w")
                task_label.pack(side="left", padx=10)

                def mark_done(t=task):
                    t['done'] = True
                    refresh_tasks()

                def delete_task(t=task):
                    all_tasks.remove(t)
                    refresh_tasks()

                ctk.CTkButton(task_frame, text="Done", width=50, fg_color="green", command=mark_done).pack(side="right", padx=5)
                ctk.CTkButton(task_frame, text="Delete", width=60, fg_color="red", command=delete_task).pack(side="right")

        def add_task():
            task_text = task_entry.get()
            if not task_text:
                return
            all_tasks.append({"text": task_text, "done": False})
            task_entry.delete(0, "end")
            refresh_tasks()

        ctk.CTkButton(tasks_container, text="Add Task", command=add_task).pack(pady=(5, 10))

        tasks_list_frame = ctk.CTkFrame(tasks_container)
        tasks_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        refresh_tasks()

#----------------------------------------------------------------
    def show_messages_page():
        for widget in content_area.winfo_children():
            widget.destroy()

        left_frame = ctk.CTkFrame(content_area, width=200, fg_color="#d3d3d3")
        left_frame.pack(side="left", fill="y", padx=(20, 10), pady=20)

        ctk.CTkLabel(left_frame, text="Colleagues:", font=ctk.CTkFont(weight="bold", size=14)).pack(anchor="nw", padx=10, pady=10)

        chat_area = ctk.CTkFrame(content_area)
        chat_area.pack(side="left", fill="both", expand=True, pady=(20, 10), padx=(0, 20))

        current_user = ctk.StringVar(value="Ali")

        messages_frame_dict = {}

        def open_chat(user):
            for widget in chat_area.winfo_children():
                widget.destroy()

            ctk.CTkLabel(chat_area, text=f"Chat with {user}", font=ctk.CTkFont(weight="bold", size=16)).pack(
                anchor="nw", padx=10, pady=(10, 5))

            messages_frame = ctk.CTkFrame(chat_area, fg_color="white")
            messages_frame.pack(fill="both", expand=True, padx=10)

            if user not in chat_data:
                chat_data[user] = []

            for msg in chat_data[user]:
                ctk.CTkLabel(messages_frame, text=msg, anchor="w", justify="left").pack(anchor="w", padx=10, pady=2)

            bottom_frame = ctk.CTkFrame(chat_area, height=50)
            bottom_frame.pack(fill="x", pady=10)

            message_entry = ctk.CTkEntry(bottom_frame, placeholder_text="Type your message here...")
            message_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

            def send_message():
                msg = message_entry.get()
                if msg.strip():
                    full_msg = f"You: {msg}"
                    chat_data[user].append(full_msg)

                    ctk.CTkLabel(messages_frame, text=full_msg, anchor="w", justify="left").pack(anchor="w", padx=10,
                                                                                                 pady=2)
                    message_entry.delete(0, "end")

            ctk.CTkButton(bottom_frame, text="Send", width=70, fg_color="green", command=send_message).pack(
                side="right", padx=10, pady=10)

        users = ["Ali", "Sara", "Lama", "Omar"]
        for user in users:
            ctk.CTkButton(left_frame, text=user, width=150, fg_color="white", text_color="black", anchor="w",
                          command=lambda u=user: open_chat(u)).pack(pady=5, padx=10)

        open_chat(current_user.get())

#----------------------------------------------------------------
    def show_files_page():
        for widget in content_area.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(content_area, fg_color="#d3d3d3")
        header.pack(fill="x")

        ctk.CTkLabel(header, text="Uploaded Files", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        files_container = ctk.CTkFrame(content_area, fg_color="#d3d3d3")
        files_container.pack(fill="both", expand=True)

        def refresh_file_list():
            for widget in files_container.winfo_children():
                widget.destroy()

            for file_path in file_list:
                row = ctk.CTkFrame(files_container)
                row.pack(fill="x", padx=10, pady=5)

                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path) // 1024
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M')

                info_label = ctk.CTkLabel(row, text=f"{file_name}  |  {file_size} KB  |  {file_time}", anchor="w")
                info_label.pack(side="left", padx=10)

                ctk.CTkButton(row, text="Open", width=60, command=lambda f=file_path: webbrowser.open(f)).pack(side="right", padx=5)
                ctk.CTkButton(row, text="Delete", width=60, fg_color="red", command=lambda f=file_path: delete_file(f)).pack(side="right")

        def upload_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                file_list.append(file_path)
                refresh_file_list()

        def delete_file(path):
            if path in file_list:
                file_list.remove(path)
                refresh_file_list()

        upload_btn = ctk.CTkButton(header, text="Upload File", width=120, command=upload_file)
        upload_btn.pack()

        refresh_file_list()

# ----------------------------------------------------------------
    home_image = ctk.CTkImage(light_image=Image.open("icons/home.png"), size=(40, 40))
    tasks_image = ctk.CTkImage(light_image=Image.open("icons/tasks.png"), size=(40, 40))
    messages_image = ctk.CTkImage(light_image=Image.open("icons/messages.png"), size=(40, 40))
    files_image = ctk.CTkImage(light_image=Image.open("icons/files.png"), size=(40, 40))
    logout_image = ctk.CTkImage(light_image=Image.open("icons/logout.png"), size=(40, 40))

    ctk.CTkButton(sidebar_frame, text="Home", image=home_image, compound="top", width=100, height=100, command=show_home_page).pack(pady=10)
    ctk.CTkButton(sidebar_frame, text="Tasks", image=tasks_image, compound="top", width=100, height=100, command=show_tasks_page).pack(pady=10)
    ctk.CTkButton(sidebar_frame, text="Messages", image=messages_image, compound="top", width=100, height=100, command=show_messages_page).pack(pady=10)
    ctk.CTkButton(sidebar_frame, text="Files", image=files_image, compound="top", width=100, height=100, command=show_files_page).pack(pady=10)

    ctk.CTkButton(sidebar_frame, text="Logout", image=logout_image, compound="top", width=100, height=100,
                 font=ctk.CTkFont(size=15, weight="bold"), fg_color="red", hover_color="#990000",
                 command=dashboard.destroy).pack(pady=100)

    show_home_page()
    dashboard.mainloop()

#----------------------------------------------------------------
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
    else:
        open_dashboard()

login_window = ctk.CTk()
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
login_window.geometry(f"{screen_width}x{screen_height}+0+0")
login_window.title("WorkNet Login")

content_frame = ctk.CTkFrame(login_window, fg_color="transparent")
content_frame.place(relx=0.5, rely=0.4, anchor="center")

logo_image = ctk.CTkImage(light_image=Image.open("icons/logo.png"), size=(150, 150))
ctk.CTkLabel(content_frame, image=logo_image, text="").pack(pady=(10, 5))

ctk.CTkLabel(content_frame, text="Welcome to WorkNet!", font=ctk.CTkFont(size=35, weight="bold")).pack(pady=(10, 20))
username_entry = ctk.CTkEntry(content_frame, placeholder_text="Username", width=250, height=40, font=ctk.CTkFont(size=16))
username_entry.pack(pady=10)
password_entry = ctk.CTkEntry(content_frame, placeholder_text="Password", show="●", width=250, height=40, font=ctk.CTkFont(size=16))
password_entry.pack(pady=10)
ctk.CTkButton(content_frame, text="Login", width=200, height=40, font=ctk.CTkFont(size=16, weight="bold"), command=validate_login).pack(pady=20)

login_window.mainloop()
