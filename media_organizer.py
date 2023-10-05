# Script Description:

# This Python script is a media organizer tool designed to help users manage and organize photo and video files.
# It offers the following features:

# - Scanning and categorizing media files (photos and videos) in a specified directory.
# - Listing files found and identifying duplicates.
# - Allowing users to save organized media to either the script's location or a custom location.
# - Providing an option to delete all media files from the scanned directory (except copied folders, which are skipped).
# - User-friendly interface.

# Supported file extensions:
# - Photos: .jpg, .jpeg, .png, .gif, .bmp
# - Videos: .mp4, .avi, .mov, .mkv

# Cross-platform compatibility: Works on both Windows and Linux.

# Designed for users seeking a quick and efficient way to
# organize and manage their media files while avoiding overwrites and duplicates.

try:
    # Standard library imports
    import os
    import hashlib
    import platform
    import shutil
    from time import sleep

    # Import Special libraries
    from termcolor import colored
except ModuleNotFoundError:
    from subprocess import call
    modules = ["termcolor"]
    call("pip install " + ' '.join(modules), shell=True)


def main(photo_extensions, video_extensions):
    """
    The main function for the media organizer program.

    Args:
        photo_extensions (list): List of photo file extensions.
        video_extensions (list): List of video file extensions.

    Returns:
        None
    """
    while True:
        chosen_scan_path = ask_scan_location()
        photos_scanned = 0
        videos_scanned = 0
        while True:
            clear_screen()
            main_menu(chosen_scan_path, photos_scanned, videos_scanned)
            try:
                menu_choice = input(f"{BOLD}{CYAN}└─{RED}#{RESET} ")
            except KeyboardInterrupt:
                break
            if menu_choice.isdigit():
                if menu_choice == "1":
                    print(f"{BOLD}\n{RED}  »»» ", end="")
                    print(colored(f"{BOLD}{GREEN}Scanning... ", attrs=["blink"]))
                    sleep(0.35)

                    # Scanning for photos
                    photo_list = start_scan(chosen_scan_path, photo_extensions)
                    print(f"{BOLD}\n{RED}  »»» ", end="")
                    print(colored(f"{BOLD}{GREEN}Listing... ", attrs=["blink"]))
                    sleep(0.35)

                    # Print the result for photos
                    print_list(photo_list, "Photos", chosen_scan_path, photo_extensions)
                    photos_scanned = len(photo_list)
                    continue

                elif menu_choice == "2":
                    print(f"{BOLD}\n{RED}  »»» ", end="")
                    print(colored(f"{BOLD}{GREEN}Scanning... ", attrs=["blink"]))
                    sleep(0.35)

                    # Scanning for videos
                    video_list = start_scan(chosen_scan_path, video_extensions)
                    print(f"{BOLD}\n{RED}  »»» ", end="")
                    print(colored(f"{BOLD}{GREEN}Listing... ", attrs=["blink"]))
                    sleep(0.35)

                    # Print the result for videos
                    print_list(video_list, "Videos", chosen_scan_path, video_extensions)
                    videos_scanned = len(video_list)
                    continue

                elif menu_choice == "0":
                    exit()

                else:
                    print("\nInvalid Input\n")
                    sleep(0.35)
                    continue

            elif menu_choice.lower() == "back":
                break

            else:
                print("\nInvalid Input\n")
                sleep(0.35)
                continue


def main_menu(scan_path, p_scanned, v_scanned):
    """
    Display the main menu with options for the user.

    Args:
        scan_path (str): The current scan location.
        p_scanned (int): The number of photos scanned.
        v_scanned (int): The number of videos scanned.

    Returns:
        None
    """
    p_status = WHITE
    v_status = WHITE

    # Set the status color based on the number of photos and videos scanned
    if p_scanned > 0:
        p_status = GREEN
    if v_scanned > 0:
        v_status = GREEN

    # Print the main menu options
    print(f"{BOLD}{CYAN}┌───────({BLUE}MEDIA ORGANIZER OPTIONS{CYAN})-[{WHITE}~{scan_path}{CYAN}]")
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}├ {WHITE}› ", end="")
    print(f"{BOLD}{YELLOW}Photos scanned: {p_status}{p_scanned}")
    print(f"{BOLD}{CYAN}├ {WHITE}› ", end="")
    print(f"{BOLD}{YELLOW}Videos scanned: {v_status}{v_scanned}")
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}├ {RED}» ", end="")
    print(f"{BOLD}{WHITE}1) {GREEN}Start Photo scan")
    print(f"{BOLD}{CYAN}├ {RED}» ", end="")
    print(f"{BOLD}{WHITE}2) {GREEN}Start Video scan")
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}├ {RED}» ", end="")
    print(f"{BOLD}{WHITE}0) {YELLOW}EXIT")
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}├ {WHITE}› ", end="")
    print(f"{CYAN}Type back/Ctrl+C to go Back")


def clear_screen():
    """Clears the terminal screen (works on both Windows and Linux)."""
    if platform.system() == "Windows":
        os.system("cls")  # Clear screen for Windows
    else:
        os.system("clear")  # Clear screen for Linux and macOS


def ask_scan_location():
    """
    Asking user for the scan location
    returns The picked path location
    """
    while True:
        clear_screen()
        print(f"{BOLD}{CYAN}┌───────({BLUE}Where do you want to scan?{CYAN})-[{WHITE}~\\root{CYAN}]")
        print(f"{BOLD}{CYAN}│")
        print(f"{BOLD}{CYAN}├ {RED}» ", end="")
        print(f"{BOLD}{WHITE}1) {GREEN}Current script location")
        print(f"{BOLD}{CYAN}├ {RED}» ", end="")
        print(f"{BOLD}{WHITE}2) {GREEN}Custom location")
        print(f"{BOLD}{CYAN}│")
        try:
            scan_location_choice = input(f"{BOLD}{CYAN}└─{RED}#{RESET} ")
        except KeyboardInterrupt:
            exit()

        if scan_location_choice.isdigit():
            if scan_location_choice == "1":
                directory = os.getcwd()  # Get current working directory
                return directory

            elif scan_location_choice == "2":
                clear_screen()
                try:
                    print(f"{BOLD}{CYAN}┌───────({BLUE}Specify the path you want to scan{CYAN}"
                          f")-[{WHITE}~\\root\\path{CYAN}]")
                    print(f"{BOLD}{CYAN}│")
                    print(f"{BOLD}{CYAN}├ {RED}» ", end="")
                    print(f"{GREEN}Example: {YELLOW}C:\\Users\\name\\pictures")
                    print(f"{BOLD}{CYAN}│")
                    print(f"{BOLD}{CYAN}├ {RED}» ", end="")
                    print(f"{CYAN}Enter/Ctrl+C to go Back")
                    custom_path = input(f"{BOLD}{CYAN}└─{RED}#{RESET} ")  # user choose scan location
                except KeyboardInterrupt:
                    continue
                return custom_path
            else:
                print("\nInvalid Input\n")
                sleep(0.35)
                continue
        else:
            print("\nInvalid Input\n")
            sleep(0.35)
            continue


def start_scan(directory, extension):
    """
    Start scanning files in all directories in the set scan location.
    Getting file hash to avoid duplicates.
    returns unique_path_list
    """
    try:
        buffer_size = 1024  # Read file in chunks to get hash
        # unique hash list
        hash_list = set()

        unique_path_list = []

        # for loop to scan all files in the directory
        for root_directory, _, files in os.walk(directory):
            try:
                for file in files:
                    if any(file.lower().endswith(ext) for ext in extension):

                        # Get full path of the current file
                        full_path = os.path.join(root_directory, file)

                        # Read hash file
                        try:
                            with open(full_path, 'rb') as f:
                                try:
                                    md5 = hashlib.md5()
                                    while True:
                                        data = f.read(buffer_size)
                                        if not data:
                                            break
                                        md5.update(data)
                                except KeyboardInterrupt:
                                    return
                        except Exception as e:
                            print(f"{BOLD}\n\n{CYAN}  »»» ", end="")
                            print(f"{BOLD}{RED}ERROR Reading hash file for: {file}")
                            print(f"{RED}{e}\n\n")

                        # check if hash exist
                        current_hash = md5.hexdigest()
                        if current_hash in hash_list:
                            continue

                        # if not add hash to the list
                        else:
                            hash_list.add(md5.hexdigest())
                            # Get path of the unique file
                            unique_path = os.path.join(root_directory, file)
                            unique_path_list.append(unique_path)
            except KeyboardInterrupt:
                return
        return unique_path_list

    except KeyboardInterrupt:
        return


def print_list(files, folder_name, scan_path, extensions):
    """
    Print a list of files, count duplicates, and provide user options.

    :param extensions: file extension
    :param files: List of file paths
    :param folder_name: Type of files
    :param scan_path: Display scan-path
    """
    if not files:
        return
    clear_screen()
    line_number = 0  # Counter for displaying line numbers
    file_counts = {}  # Dictionary to count unique files and duplicates
    total_unique = 0  # Total count of unique files found
    sum_duplicates = 0  # Total count of duplicate files

    # Print the header
    print(f"{BOLD}{CYAN}┌───────({BLUE}LIST OF {folder_name.upper()} FOUND{CYAN})-[{WHITE}~{scan_path}{CYAN}]")
    print(f"{BOLD}{CYAN}│")

    # Scan and count files
    for file in files:
        # Split the file path
        split_path = file.split("\\")

        # Check if the file name already exists in the list
        if split_path[-1] in file_counts:
            file_counts[split_path[-1]] += 1
            continue

        # If it's a unique file, update counters
        file_counts[split_path[-1]] = 1
        total_unique += 1

    # Print the list of files
    for file, count in file_counts.items():
        line_number += 1
        if count > 1:
            # If the file name appeared more than once, then print in red
            print(f"{BOLD}{CYAN}├[{RED}{line_number}{CYAN}] {MAGENTA}› ", end="")
            print(f"{BOLD}{RED}{file}")
        else:
            print(f"{BOLD}{CYAN}├[{WHITE}{line_number}{CYAN}] {MAGENTA}› ", end="")
            print(f"{BOLD}{WHITE}{file}")

    # Print duplicate counts
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}├────[", end="")
    print(f"{BOLD}{YELLOW}List of {RED}name{YELLOW} Duplicates{CYAN}]")
    print(f"{BOLD}{CYAN}│")

    for file, count in file_counts.items():
        if count <= 1:
            continue
        # Display the number of duplicates for each file
        print(f"{BOLD}{CYAN}│   count›[{WHITE}{count}{CYAN}]{RED} > ", end="")
        print(f"{file}{CYAN}")

    # Calculate and display totals
    for count in file_counts.values():
        if count <= 1:
            continue
        sum_duplicates += count

    # status and options
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}├ {WHITE}› ", end="")
    print(f"{BOLD}{YELLOW}Total unique {folder_name}: {GREEN}{total_unique}")
    print(f"{BOLD}{CYAN}├ {WHITE}› ", end="")
    print(f"{BOLD}{YELLOW}Total name Duplicates(List above): {RED}{sum_duplicates} {WHITE}"
          f"(Different {folder_name} with the same name)")
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}├ {RED}» ", end="")
    print(f"{BOLD}{WHITE}1) {GREEN}Copy all {folder_name} {WHITE}(Rename duplicates to avoid overwriting)")
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}├ {WHITE}› ", end="")
    print(f"{CYAN}Enter/Ctrl+C to go Back")
    while True:
        try:
            copy_choice = input(f"{BOLD}{CYAN}└─{RED}#{RESET} ")
        except KeyboardInterrupt:
            return
        if copy_choice.isdigit():
            if copy_choice == "1":
                save_media(folder_name, scan_path, files, extensions)
                return
            elif copy_choice == "":
                return
            else:
                continue
        elif copy_choice == "":
            return


def save_media(folder_name, scan_path, files, extensions):
    """
    Save media to specified location

    :param extensions: file extension
    :param folder_name: Type of files
    :param scan_path: script main scan location
    :param files: List of file paths
    :return:
    """
    clear_screen()
    print(f"{BOLD}{RED}┌────({CYAN}Where do you want to save {folder_name}?{RED})-[{GREEN}~{scan_path}{RED}]")
    print(f"{BOLD}{RED}│")
    print(f"{BOLD}{RED}├ {CYAN}» ", end="")
    print(f"{BOLD}{RED}1) {GREEN}Current script location")
    print(f"{BOLD}{RED}├ {CYAN}» ", end="")
    print(f"{BOLD}{RED}2) {GREEN}Custom location")
    print(f"{BOLD}{RED}│")
    print(f"{BOLD}{RED}├ {WHITE}› ", end="")
    print(f"{CYAN}Enter/Ctrl+C to go Back")
    while True:
        hold_output = False
        try:
            save_choice = input(f"{BOLD}{RED}└─{CYAN}#{RESET} ")
            if save_choice == "1":
                print(f"{BOLD}\n{RED}  »»» ", end="")
                print(colored(f"{BOLD}{GREEN}Copying... ", attrs=["blink"]))
                media_folder = os.path.join(scan_path, folder_name)
                # Try to create new folder to save media
                try:
                    os.makedirs(media_folder)
                except FileExistsError:
                    pass

                # Create a set to keep track of used file names
                used_names = set()

                for file in files:
                    split_path = file.split("\\")
                    base_name = os.path.basename(file)
                    name_parts = os.path.splitext(base_name)
                    new_name = base_name

                    # Check if the file name is already used, if so, add a number to make it unique
                    count = 1
                    while new_name in used_names:
                        new_name = f"{name_parts[0]}_{count}{name_parts[1]}"
                        count += 1

                    used_names.add(new_name)
                    destination_path = os.path.join(media_folder, new_name)
                    try:
                        shutil.copy2(file, destination_path)
                    except shutil.SameFileError:
                        hold_output = True
                        print(f"{BOLD}{CYAN}  »─» ", end="")
                        root_path = split_path.copy()  # Create a copy to avoid modifying split_path
                        root_path.pop()  # Remove the last element from root_path
                        root_path_string = "\\".join(root_path)  # Join the elements into one string
                        print(f"{BOLD}{RED}{split_path[-1]} {CYAN}already exist in: "
                              f"{YELLOW}{root_path_string}\\{RED}{split_path[-1]}")
                        continue
                if hold_output:
                    try:
                        print(f"\n{BOLD}{CYAN}╟ {RED}» ", end="")
                        input(f"{CYAN}Enter to continue")
                    except KeyboardInterrupt:
                        pass
                sleep(1.35)
                # delete function
                delete(scan_path, extensions, folder_name)
                return
            elif save_choice == "2":
                clear_screen()
                try:
                    print(f"{BOLD}{RED}┌────({CYAN}Specify the path you want to save {WHITE}{folder_name}?"
                          f"{RED})-[{GREEN}~{scan_path}{RED}]")
                    print(f"{BOLD}{RED}│")
                    print(f"{BOLD}{RED}├ {RED}» ", end="")
                    print(f"{GREEN}Example: {YELLOW}C:\\Users\\name\\{folder_name}")
                    print(f"{BOLD}{RED}│")
                    print(f"{BOLD}{RED}├ {CYAN}» ", end="")
                    print(f"{CYAN}Enter/Ctrl+C to go Back")
                    custom_path = input(f"{BOLD}{RED}└─{CYAN}#{RESET} ")  # User specifies a custom location
                    custom_media_folder = custom_path
                    print(f"{BOLD}\n{RED}  »»» ", end="")
                    print(colored(f"{BOLD}{GREEN}Copying... ", attrs=["blink"]))
                    # Try to create a new folder at the custom location
                    try:
                        os.makedirs(custom_media_folder)
                    except FileExistsError:
                        pass

                    # Create a set to keep track of used file names
                    used_names = set()

                    for file in files:
                        split_path = file.split("\\")
                        base_name = os.path.basename(file)
                        name_parts = os.path.splitext(base_name)
                        new_name = base_name

                        # Check if the file name is already used, if so, add a number to make it unique
                        count = 1
                        while new_name in used_names:
                            new_name = f"{name_parts[0]}_{count}{name_parts[1]}"
                            count += 1

                        used_names.add(new_name)
                        destination_path = os.path.join(custom_media_folder, new_name)
                        try:
                            shutil.copy2(file, destination_path)
                        except shutil.SameFileError:
                            hold_output = True
                            print(f"{BOLD}\n{CYAN}  »─» ", end="")
                            print(f"{BOLD}{RED}{split_path[-1]} {CYAN}already exists in: "
                                  f"{YELLOW}{custom_media_folder}\\{RED}{split_path[-1]}")
                            continue

                    if hold_output:
                        try:
                            print(f"\n{BOLD}{CYAN}╟ {RED}» ", end="")
                            input(f"{CYAN}Enter to continue")
                        except KeyboardInterrupt:
                            pass
                    # delete function
                    custom_delete(scan_path, extensions, custom_path, folder_name)
                    sleep(1.35)
                    return
                except KeyboardInterrupt:
                    continue
            elif save_choice == "":
                return
            else:
                continue

        except KeyboardInterrupt:
            return


def delete(scan_path, extensions, folder_name):
    """
    Delete media files from the scan_path (except those from copied folders).

    Args:
        scan_path (str): The directory to scan for media files.
        extensions (list): List of allowed file extensions.
        folder_name (str): Type of files (e.g., 'Photos' or 'Videos').

    Returns:
        None
    """
    clear_screen()
    print(f"{BOLD}{RED}┌────({CYAN}DELETE SECTION{RED})-[{GREEN}~{scan_path}{RED}]")
    print(f"{BOLD}{RED}│")
    print(f"{BOLD}{RED}├ {CYAN}» ", end="")
    print(f"{BOLD}{CYAN}{GREEN}Type [ {RED}Delete All {GREEN}] to {RED}delete all {folder_name} {YELLOW}From:")
    print(f"{BOLD}{RED}├ {CYAN}»»»»  ", end="")
    print(f"{BOLD}{RED}{scan_path}")
    print(f"{BOLD}{RED}│")
    print(f"{BOLD}{RED}│")
    print(f"{BOLD}{RED}├ {CYAN}» ", end="")
    print(f"{BOLD}{CYAN}{GREEN}Type [ {CYAN}0{GREEN} /{CYAN} Exit{GREEN} ] to go back")
    print(f"{BOLD}{RED}├ {WHITE}› ", end="")
    print(f"{CYAN}Ctrl+C to go Back")
    try:
        while True:
            delete_choice = input(f"{BOLD}{RED}└─{CYAN}#{RED} ")
            if delete_choice == "Delete All":
                skip = os.path.join(scan_path, folder_name)
                for root_directory, _, files in os.walk(scan_path):
                    # Check if the root_directory starts with the skip path
                    if root_directory.startswith(skip):
                        continue
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in extensions):
                            remove = os.path.join(root_directory, file)
                            os.remove(remove)
                return
            elif delete_choice.lower() == "exit":
                return
            else:
                print(f"{BOLD}{RED}{CYAN}» ", end="")
                print(f"{BOLD}{CYAN}Invalid input")
                continue
    except KeyboardInterrupt:
        return


def custom_delete(scan_path, extensions, custom_path, file_scan_name):
    """
    Delete media files from the scan_path (except those from the custom_path directory).

    Args:
        scan_path (str): The directory to scan for media files.
        extensions (list): List of allowed file extensions.
        custom_path (str): Custom location to skip deleting media files from.
        file_scan_name (str): Type of files (e.g., 'Photos' or 'Videos').

    Returns:
        None
    """
    clear_screen()
    print(f"{BOLD}{RED}┌────({CYAN}DELETE SECTION{RED})-[{GREEN}~{scan_path}{RED}]")
    print(f"{BOLD}{RED}│")
    print(f"{BOLD}{RED}├ {CYAN}» ", end="")
    print(f"{BOLD}{CYAN}{GREEN}Type [ {RED}Delete All {GREEN}] to {RED}delete all {file_scan_name} {YELLOW}From:")
    print(f"{BOLD}{RED}├ {CYAN}»»»»  ", end="")
    print(f"{BOLD}{RED}{scan_path}")
    print(f"{BOLD}{RED}│")
    print(f"{BOLD}{RED}│")
    print(f"{BOLD}{RED}├ {CYAN}» ", end="")
    print(f"{BOLD}{CYAN}{GREEN}Type [ {CYAN}0{GREEN} /{CYAN} Exit{GREEN} ] to go back")
    print(f"{BOLD}{RED}├ {WHITE}› ", end="")
    print(f"{CYAN}Ctrl+C to go Back")
    try:
        while True:
            delete_choice = input(f"{BOLD}{RED}└─{CYAN}#{RED} ")
            if delete_choice == "Delete All":
                for root_directory, _, files in os.walk(scan_path):
                    # Check if the root_directory starts with the skip path
                    if root_directory.startswith(custom_path):
                        continue
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in extensions):
                            remove = os.path.join(root_directory, file)
                            os.remove(remove)
                return
            elif delete_choice.lower() == "exit":
                return
            else:
                print(f"{BOLD}{RED}{CYAN}» ", end="")
                print(f"{BOLD}{CYAN}Invalid input")
                continue
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    photos_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    videos_extensions = [".mp4", ".avi", ".mov", ".mkv"]
    # ANSI escape codes for text formatting and colors
    RESET = "\033[0m"  # Reset all formatting and color
    BOLD = "\033[1m"  # Bold text
    UNDERLINE = "\033[4m"  # Underlined text
    BLACK = "\033[30m"  # Black text
    RED = "\033[31m"  # Red text
    GREEN = "\033[32m"  # Green text
    YELLOW = "\033[33m"  # Yellow text
    BLUE = "\033[34m"  # Blue text
    MAGENTA = "\033[35m"  # Magenta text
    CYAN = "\033[36m"  # Cyan text
    WHITE = "\033[37m"  # White text
    main(photos_extensions, videos_extensions)
