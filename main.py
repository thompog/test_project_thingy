try:
    import os #i dont like most of the names in os functions
    from os.path import exists as exist
    from os.path import join as joinpaths
    from os.path import basename 
    from pathlib import Path
    from os import environ
    import sys
    import shutil
    import urllib.request

    program_name = sys.argv[0] # idk why i made this like it trough
    if program_name.startswith("C:\\"):
        program_name = basename(program_name)
    elif program_name.startswith("D:\\"):
        program_name = basename(program_name)
    elif program_name.startswith("E:\\"):
        program_name = basename(program_name)
    elif program_name.startswith("F:\\"):
        program_name = basename(program_name)
    elif program_name.startswith("T:\\"):
        program_name = basename(program_name)

    program_type = "" #it will change cause this file ends with .py (or if i conpile it) .exe
    if program_name.endswith(".py"):
        program_name = program_name.replace(".py", "")
        program_type = ".py"
    elif program_name.endswith(".exe"):
        program_name = program_name.replace(".exe", "")
        program_type = ".exe"

    def get_thingy(): #i still do not know why i did this but i like it it makes sense trust
        import getpass
        try:
            user = getpass.getuser()
        except OSError:
            try:
                user = Path.home().name
            except Exception:
                import ctypes
                buffer = ctypes.create_unicode_buffer(257)
                size = ctypes.c_ulong(ctypes.sizeof(buffer))
        
                if ctypes.windll.advapi32.GetUserNameW(buffer, ctypes.byref(size)):
                    user = buffer.value
                else:
                    print("Failed to retrieve username")
                    input("Press enter to exit")
                    sys.exit(1)

        return user

    try:
        user = environ.get('USERNAME')
        if user is None:
            user = get_thingy()
    except OSError:
        user = get_thingy()

    appdata = Path(f"C:\\Users\\{user}\\AppData")
    main_path = Path(f"{appdata}\\Local\\{program_name}")
    perts_path = Path(f"{main_path}\\PERTS")
    stuff_path = Path(f"{main_path}\\stuff")
    main_file_path = joinpaths(main_path, f"{program_name}{program_type}")
    script_file_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_file_path)

    perts_files = {"convert_path": joinpaths(perts_path, "convert_videos.py"), "get_point_screen_path": joinpaths(perts_path, "get_point_screen.py"), "installer": joinpaths(perts_path, "installer.helper.exe"), "installer_config": joinpaths(perts_path, "config.txt")}
    license_and_tos_and_readme = {"license_path": joinpaths(stuff_path, "LICENSE"), "TOS_path": joinpaths(stuff_path, "TOS.txt"), "readme_path": joinpaths(stuff_path, "README.md")}

    installer_config = f'''
    URLS;=
    https://raw.githubusercontent.com/thompog/test_project_thingy/refs/heads/main/PERTS/convert_videos.py
    https://raw.githubusercontent.com/thompog/test_project_thingy/refs/heads/main/PERTS/get_point_screen.py
    https://raw.githubusercontent.com/thompog/test_project_thingy/refs/heads/main/stuff/LICENSE
    https://raw.githubusercontent.com/thompog/test_project_thingy/refs/heads/main/stuff/TOS.txt
    https://raw.githubusercontent.com/thompog/test_project_thingy/refs/heads/main/stuff/README.md
    PATHS;=
    {perts_files["convert_path"]}
    {perts_files["get_point_screen_path"]}
    {license_and_tos_and_readme["license_path"]}
    {license_and_tos_and_readme["TOS_path"]}
    {license_and_tos_and_readme["readme_path"]}
    EOF;;
    '''

    tos_accepted_flag = joinpaths(main_path, "tos_accepted.flag")

    def show_first_time_agreement():
        # already agreed on a previous run, nothing to do
        if exist(tos_accepted_flag):
            return

        import tkinter as tk
        from tkinter import scrolledtext, messagebox

        def read_text(path, fallback):
            try:
                with open(path, "r", encoding="utf-8") as file:
                    return file.read()
            except Exception:
                return fallback

        pages = [
            ("License", read_text(license_and_tos_and_readme["license_path"], "LICENSE not found.")),
            ("Terms of Service", read_text(license_and_tos_and_readme["TOS_path"], "TOS not found.")),
            ("README", read_text(license_and_tos_and_readme["readme_path"], "README not found.")),
        ]

        root = tk.Tk()
        root.title(f"{program_name} - First Time Setup")
        root.geometry("700x500")

        state = {"index": 0}
        checkbox_var = tk.BooleanVar(value=False)

        title_label = tk.Label(root, text="", font=("Segoe UI", 14, "bold"))
        title_label.pack(pady=(10, 0))

        text_area = scrolledtext.ScrolledText(root, wrap="word")
        text_area.pack(fill="both", expand=True, padx=10, pady=10)

        checkbox_frame = tk.Frame(root)
        checkbox = tk.Checkbutton(
            checkbox_frame,
            text="I have read and agree to the Terms of Service",
            variable=checkbox_var,
            command=lambda: update_next_button(),
        )
        checkbox.pack(side="left")

        button_frame = tk.Frame(root)

        def update_next_button():
            is_last_page = state["index"] == len(pages) - 1
            if is_last_page:
                next_button.config(state="normal" if checkbox_var.get() else "disabled")
            else:
                next_button.config(state="normal")

        def load_page(index):
            state["index"] = index
            name, text = pages[index]
            title_label.config(text=name)
            text_area.config(state="normal")
            text_area.delete("1.0", "end")
            text_area.insert("1.0", text)
            text_area.config(state="disabled")

            is_last_page = index == len(pages) - 1
            checkbox_frame.pack_forget()
            if is_last_page:
                checkbox_frame.pack(pady=(0, 5))
            next_button.config(text="Finish" if is_last_page else "Next")
            update_next_button()

        def on_next():
            if state["index"] < len(pages) - 1:
                load_page(state["index"] + 1)
            else:
                with open(tos_accepted_flag, "w") as file:
                    file.write("accepted")
                root.destroy()

        def on_decline():
            if messagebox.askyesno("Decline", "You must accept the Terms of Service to use this program. Exit now?"):
                root.destroy()
                sys.exit(0)

        next_button = tk.Button(button_frame, text="Next", command=on_next, width=12)
        decline_button = tk.Button(button_frame, text="Decline", command=on_decline, width=12)
        decline_button.pack(side="right", padx=5)
        next_button.pack(side="right", padx=5)
        button_frame.pack(pady=(0, 10))

        root.protocol("WM_DELETE_WINDOW", on_decline)

        load_page(0)
        root.mainloop()

        # window was closed without accepting
        if not exist(tos_accepted_flag):
            sys.exit(0)

    if not exist(main_path):
        os.mkdir(main_path)

    if not exist(stuff_path):
        os.mkdir(stuff_path)

    if not exist(perts_path):
        os.mkdir(perts_path)

    if not exist(perts_files["installer"]):
        if not exist(perts_files["installer_config"]):
            with open(perts_files["installer_config"], "w") as file:
                file.write(installer_config)

        urllib.request.urlretrieve("https://github.com/thompog/installer-helper/releases/download/versions/installer.helper.exe", perts_files["installer"])

    if not exist(perts_files["convert_path"]):
        os.system(perts_files["installer"])
    elif not exist(perts_files["get_point_screen_path"]):
        os.system(perts_files["installer"])

    if script_file_path != main_file_path:
        try:
            shutil.copyfile(script_file_path, main_file_path)
            if exist(joinpaths(script_dir, "PERTS")):
                if not exist(perts_path):
                    os.mkdir(perts_path)
                perts_path_old = joinpaths(script_dir, "PERTS")
                convert = joinpaths(perts_path_old, "convert_videos.py")
                pointer = joinpaths(perts_path_old, "get_point_screen.py")

                if exist(convert):
                    shutil.move(convert, perts_files["convert_path"])
                if exist(pointer):
                    shutil.move(pointer, perts_files["get_point_screen_path"])

            if exist(joinpaths(script_dir, "stuff")):
                if not exist(stuff_path):
                    os.mkdir(stuff_path)
                stuff_path_old = joinpaths(script_dir, "stuff")
                readme = joinpaths(stuff_path_old, "README.md")
                tos = joinpaths(stuff_path_old, "TOS.txt")
                licens = joinpaths(stuff_path_old, "LISENSE")

                if exist(readme):
                    shutil.move(readme, license_and_tos_and_readme["readme_path"])
                if exist(tos):
                    shutil.move(tos, license_and_tos_and_readme["TOS_path"])
                if exist(licens):
                    shutil.move(licens, license_and_tos_and_readme["license_path"])

            batch_relocation_file = f'''
            @echo off
            title relocation and restarter of {program_name}
            timeout /t 3 >nul
            if not "{script_file_path}"=="{main_file_path}" (
                if exist "{main_file_path}" (
                    del /Q "{script_file_path}"
                    python "{main_file_path}"
                ) else (
                    copy "{script_file_path}" "{main_file_path}"
                    del /Q "{script_file_path}"
                    python "{main_file_path}"
                )
            ) else (
                echo cant relocate a file if its where it needs to be right?
                python "{main_file_path}"
            )
            exit /b 0
            '''
            path = joinpaths(perts_path, "relocation_and_restarter.bat")
            if not exist(path):
                with open(path, "w") as file:
                    file.write(batch_relocation_file)

            os.startfile(path)
            sys.exit(0)
        except Exception as E:
            raise Exception(E)

    if not exist(joinpaths(perts_path, "__init__.py")):
        with open(joinpaths(perts_path, "__init__.py"), "w") as file:
            file.write("")

    show_first_time_agreement()

    print(f"the new file is at: {main_path}")
    print()
    print()

    import PERTS.convert_videos as convert
    import PERTS.get_point_screen as gps

    convert.check_ffmpeg_available()

    if len(sys.argv) < 2:
        print(f"{program_name}{program_type} --convert")
        print(f'{program_name}{program_type} --get_point_screen --get -point -example_photo_path="C:\\path\\to\\photo.png"')
        print(f'{program_name}{program_type} --get_point_screen -click -example_photo_path="C:\\path\\to\\photo.png"')

    if '--get_point_screen --get' in sys.argv[1:]:
        args = ["--get", "-point"]
        for arg in sys.argv[1:]:
            if arg.startswith('-example_photo_path="'):
                args.append(arg)

        gps.main(args)
    elif '--get_point_screen -click' in sys.argv[1:]:
        args = ["-click"]
        for arg in sys.argv[1:]:
            if arg.startswith('-example_photo_path="'):
                args.append(arg)

        gps.main(args)
    elif '--convert' in sys.argv[1:]:
        convert.main()

    print("press enter to exit")
    input("")
    sys.exit(0)

except ModuleNotFoundError as E: #me got lazy me no want do work :(
    print("cannot get username from os and cannot import module getpass")
    print("please reinstall python with the Standard Library installed with it")
    input("Press enter to exit")
    pass

