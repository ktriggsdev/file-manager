import os
import shutil

os.chdir('module/root_folder')


def convert_file_size(size_in_bytes):
    if size_in_bytes < 1024:
        value, prefix = size_in_bytes, "B"
    elif size_in_bytes < 1024 * 1024:
        value, prefix = (size_in_bytes / 1024), "KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        value, prefix = (size_in_bytes / (1024 * 1024)), "MB"
    else:
        value, prefix = (size_in_bytes / (1024 * 1024 * 1024)), "GB"

    return f"{int(value)}{prefix}"


def print_files(arg):
    dirs, files = [], []
    for filename in os.listdir(os.getcwd()):
        if os.path.isdir(filename):
            dirs.append((filename, None))
        else:
            st_size = os.stat(filename).st_size
            if arg == "-lh":
                files.append((filename, convert_file_size(st_size)))
            elif arg == "-l":
                files.append((filename, st_size))
            else:
                files.append((filename, None))

    dirs.extend(files)

    for file, value in dirs:
        print(file, value if value is not None else "")


def delete_files(arg):
    if arg is None:
        print("Specify the file or directory")
        return
    if arg.startswith("."):  # Check if arg is an extension
        extension = arg
        files_to_delete = []
        for filename in os.listdir(os.getcwd()):
            if filename.endswith(extension):
                files_to_delete.append(filename)

        if not files_to_delete:
            print(f"File extension {extension} not found in this directory.")
            return

        for file in files_to_delete:
            try:
                os.remove(file)
                print(f"{file} has been removed.")
            except OSError as e:
                print(f"Error {e.strerror}")
    else:
        # Existing logic for deleting a specific file or directory
        target = os.path.join(os.getcwd(), arg)
        if not os.path.exists(target):
            print("No such file or directory")
            return

        try:
            if os.path.isdir(target):
                os.rmdir(target)
            else:
                os.remove(target)
            print(f"{arg} has been removed.")
        except OSError as e:
            print(f"Error {e.strerror}")


def move_or_rename_files(src, dest):
    if src.startswith("."):  # Check if src is an extension
        extension = src
        files_to_move = []
        for filename in os.listdir(os.getcwd()):
            if filename.endswith(extension):
                files_to_move.append(filename)

        if not files_to_move:
            print(f"File extension {extension} not found in this directory.")
            return

        for file in files_to_move:
            src_path = os.path.join(os.getcwd(), file)
            dest_path = os.path.join(dest, file)
            if os.path.exists(dest_path):
                while True:
                    user_input = input(f"{file} already exists in this directory. Replace? (y/n): ").strip().lower()
                    if user_input == 'y':
                        try:
                            shutil.move(src_path, dest_path)
                            print(f"{file} has been moved to {dest}.")
                            break
                        except shutil.Error as e:
                            print(f"Error {e.strerror}")
                    elif user_input == 'n':
                        print("Skipping this file.")
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
            else:
                try:
                    shutil.move(src_path, dest_path)
                    print(f"{file} has been moved to {dest}.")
                except shutil.Error as e:
                    print(f"Error {e.strerror}")
    else:
        try:
            # Check if the destination is a directory
            if os.path.isdir(dest):
                dest = os.path.join(dest, os.path.basename(src))

            if os.path.exists(dest):
                print("The file or directory already exists")
            # Move or rename the file
            shutil.move(src, dest)
            print(f"{src} has been moved to {dest}.")
        except FileNotFoundError:
            print("No such file or directory")
        except shutil.Error as e:
            print(f"Error {e.strerror}")
        except IsADirectoryError:
            print("Specify the current name of the file or directory and the new location and/or name")


def create_directory(arg):
    if not arg:
        print("Specify the name of the directory to be made")
        return

    new_dir = os.path.join(os.getcwd(), arg)
    if os.path.exists(new_dir):
        print("The directory already exists")
        return

    try:
        os.mkdir(new_dir)
        print(f"Directory '{arg}' has been created.")
    except OSError as e:
        print(f"Error {e.strerror}")


def copy_files(src, dest):
    if src.startswith("."):  # Check if src is an extension
        extension = src
        files_to_copy = []
        for filename in os.listdir(os.getcwd()):
            if filename.endswith(extension):
                files_to_copy.append(filename)

        if not files_to_copy:
            print(f"File extension {extension} not found in this directory.")
            return

        for file in files_to_copy:
            src_path = os.path.join(os.getcwd(), file)
            dest_path = os.path.join(dest, file)
            if os.path.exists(dest_path):
                while True:
                    user_input = input(f"{file} already exists in this directory. Replace? (y/n): ").strip().lower()
                    if user_input == 'y':
                        try:
                            shutil.copy(src_path, dest_path)
                            print(f"{file} has been copied to {dest}.")
                            break
                        except shutil.Error as e:
                            print(f"Error {e.strerror}")
                    elif user_input == 'n':
                        print("Skipping this file.")
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
            else:
                try:
                    shutil.copy(src_path, dest_path)
                    print(f"{file} has been copied to {dest}.")
                except shutil.Error as e:
                    print(f"Error {e.strerror}")
    else:
        try:
            if os.path.isdir(dest):
                dest = os.path.join(dest, os.path.basename(src))
            shutil.copy(src, dest)
            print(f"{src} has been copied to {dest}.")
        except FileNotFoundError:
            print("No such file or directory")
        except shutil.SameFileError:
            print(f"{src} already exists in this directory.")
        except shutil.Error as e:
            print(f"Error {e.strerror}")
        except IsADirectoryError:
            print("Specify the current name of the file or directory and the new location and/or name")


print("Input the command")
while True:
    command = input().strip()

    if command == "pwd":
        print(os.getcwd())
    elif command.startswith("cd"):
        command = command.split(" ")
        if len(command) == 2:
            path = command[1]
            if path == "..":
                os.chdir(os.path.dirname(os.getcwd()))
                print(os.path.basename(os.getcwd()))
            else:
                try:
                    os.chdir(path)
                    print(os.path.basename(os.getcwd()))
                except FileNotFoundError:
                    print("Invalid command")
        else:
            print("Invalid command")
    elif command.startswith("ls"):
        command = command.split(" ")
        argument = command[1] if len(command) == 2 else None
        print_files(argument)

    elif command.startswith("rm"):
        command = command.split(" ")
        argument = " ".join(command[1:]) if len(command) > 1 else None
        delete_files(argument)

    elif command.startswith("cp"):
        args = command.split(" ")
        if len(args) < 3:
            if len(args) == 1:
                print("Specify the file")
            else:
                print("Specify the current name of the file or directory and the new location and/or name")
        else:
            src, dest = args[1], args[2]
            copy_files(src, dest)

    elif command.startswith("mv"):
        args = command.split(" ")
        if len(args) != 3:
            print("Specify the current name of the file or directory and the new location and/or name")
        else:
            src, dest = args[1], args[2]
            move_or_rename_files(src, dest)

    elif command.startswith("mkdir"):
        command = command.split(" ")
        argument = " ".join(command[1:]) if len(command) > 1 else None
        create_directory(argument)

    elif command == "quit":
        break
    else:
        print("Invalid command")