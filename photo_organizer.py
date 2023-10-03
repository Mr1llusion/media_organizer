try:
    # Standard library imports
    import os
    import shutil
    from time import sleep
    from collections import defaultdict

    # Import Special libraries
    from termcolor import colored
    from natsort import natsorted
except ModuleNotFoundError:
    from subprocess import call

    modules = ["natsort", "termcolor"]
    call("pip install " + ' '.join(modules), shell=True)


def main():
    # The main program execution function.
    custom_photo_destination = ""
    custom_video_destination = ""
    scanned_current_location = False
    check_lost = "concealed"
    scan_location = os.path.dirname(os.path.abspath(__file__))
    photos_exists = os.path.join(scan_location, "photos")
    videos_exists = os.path.join(scan_location, "videos")
    skip_delete_folders = custom_video_destination + custom_photo_destination + photos_exists + videos_exists
    if os.path.exists(photos_exists) and os.path.exists(videos_exists):
        check_lost = "bold"
        custom_photo_destination = photos_exists
        custom_video_destination = videos_exists
        scanned_current_location = True

    while True:
        banner()
        print(colored("[+] Where do you want to scan?", "cyan", attrs=["bold"]))
        print(colored(" -  1) Current location", "green", attrs=["bold"]))
        print(colored(" -  2) Custom location", "green", attrs=["bold"]))

        start_choice = input(colored("\n[+] Enter number: ", 'red'))
        if start_choice == "1":
            break
        elif start_choice == "2":
            print("\n[?] Example: C:\\Users\\Name\\Pictures")
            try:
                scan_location = input(colored("[*] Enter the location to scan for media: ", "cyan"))
            except KeyboardInterrupt:
                os.system("cls")
                continue
            break
        else:
            print("[Invalid input]")
            sleep(1)
            os.system("cls")
            continue

    while True:
        os.system("cls")
        banner()
        print(colored(f"[+] Current location: [{scan_location}]\n", "cyan"))
        print(colored("[+] Options:\n", "yellow", attrs=["bold"]))
        print(colored(" -  1) Scan current location", "green", attrs=["bold"]))
        print(colored(" -  2) Check for duplicate in the Scan Location", "green", attrs=["bold"]))
        print(colored(" -  3) Check for lost media", "green", attrs=[check_lost]))
        print(colored("\n[!] 4) Delete media in current location", "red", attrs=[check_lost]))
        print(colored("\n0) Exit", "red"))

        choice = input(colored("\n[~] Enter your choice: ", "yellow", attrs=["bold"]))

        os.system("cls")
        if choice == "1":
            while True:
                os.system("cls")
                banner()
                print(colored(f"[+] Current location: [{scan_location}]\n", "cyan"))
                print(colored("\n[~] Photos:", "blue"))
                # Count the number of photos in the scan location
                num_photos = scan_for_media(scan_location, photo_extensions)
                print(colored(f"    [+] Number of Photos: {num_photos}", "red", attrs=["bold"]))

                # Count the number of unique photos in the scan location
                unique_photos = scan_for_unique_media(scan_location, photo_extensions)
                print(colored(f"    [#] Number of unique Photos: {len(unique_photos)}", "red"))

                print(colored("\n[~] Videos:", "blue"))
                # Count the number of videos in the scan location
                num_videos = scan_for_media(scan_location, video_extensions)
                print(colored(f"    [+] Number of Videos: {num_videos}", "red", attrs=["bold"]))

                # Count the number of unique videos in the scan location
                unique_videos = scan_for_unique_media(scan_location, video_extensions)
                print(colored(f"    [#] Number of unique Videos: {len(unique_videos)}\n\n", "red"))

                print(colored("[+] Where do you want to save?", "cyan", attrs=["bold"]))
                print(colored(" -  1) Current location", "green", attrs=["bold"]))
                print(colored(" -  2) Custom location", "green", attrs=["bold"]))
                try:
                    save_choice = input(colored("\n[+] Enter number: ", "green"))
                except KeyboardInterrupt:
                    break
                if save_choice == "1":
                    custom_photo_destination = os.path.join(scan_location, "photos")
                    custom_video_destination = os.path.join(scan_location, "videos")
                    scan_media_and_organize(scan_location, photo_extensions, custom_photo_destination)
                    scan_media_and_organize(scan_location, video_extensions, custom_video_destination)
                elif save_choice == "2":
                    # Ask the user for the destination folders
                    try:
                        print(colored("[!] Go Back? -> [Ctrl + C] or [Enter (Empty input)]", "red", attrs=["bold"]))
                        custom_photo_destination = input(colored("[+] Enter a path to save the Photos: ", "green"))
                        if custom_photo_destination == "":
                            continue
                        custom_video_destination = input(colored("[+] Enter a path to save the Video: ", "green"))
                        if custom_video_destination == "":
                            continue
                    except KeyboardInterrupt:
                        continue
                    # Scan for photos and videos and Organize
                    scan_media_and_organize(scan_location, photo_extensions, custom_photo_destination)
                    scan_media_and_organize(scan_location, video_extensions, custom_video_destination)

                else:
                    print("[Invalid Input]")
                    sleep(1)
                    continue
                scanned_current_location = True
                check_lost = "bold"
                print(colored("\n[+] Copy done", "red"))
                input(colored("\n[*] Press Enter to continue", "cyan"))
                break

        elif choice == "2":
            os.system("cls")
            banner()
            check_duplicate_media(scan_location)

        elif choice == "3":
            if scanned_current_location:
                os.system("cls")
                banner()
                check_lost_media(custom_photo_destination, custom_video_destination, scan_location)
                try:
                    input(colored("\n[*] Press Enter to continue", "cyan"))
                except KeyboardInterrupt:
                    continue
            else:
                os.system("cls")
                banner()
                print(colored("[!] Scan current location first, then run the check", "red", attrs=["bold"]))
                input(colored("\n[*] Press Enter to continue", "cyan"))

        elif choice == "4":
            if scanned_current_location:
                os.system("cls")
                banner()
                delete_media(scan_location, skip_delete_folders)
                try:
                    input(colored("\n[*] Press Enter to continue", "cyan"))
                except KeyboardInterrupt:
                    continue
            else:
                os.system("cls")
                banner()
                print(colored("[!] Scan current location first, then run the check", "red", attrs=["bold"]))
                input(colored("\n[*] Press Enter to continue", "cyan"))
        elif choice == "0":
            print("[$] Exiting the program.")
            sleep(2)
            exit()

        else:
            print("\n[!] Invalid choice. Please select a valid option.")
            sleep(1)


def delete_media(delete_path, skip_delete_folders):
    all_extensions = photo_extensions + video_extensions
    if not os.path.exists(delete_path):
        print("\n[!] Current location not found.")
        return

    print(f"{BOLD}{RED}┌────────────([!] WARNING - YOU ARE ABOUT TO DELETE ALL MEDIA FROM CURRENT LOCATION [!])-[~]"
          f"{RESET}")
    print(f"{BOLD}{CYAN}│")
    # Allow the user to input "Delete all" to confirm the action
    print(f"{BOLD}{CYAN}├ ", end="")
    print(f"{BOLD}{RED}Delete from location: {delete_path}{RESET}")
    print(f"{BOLD}{CYAN}│")
    print(f"{BOLD}{CYAN}├ Type \"Delete all\" to delete all media{RESET}")
    print(f"{BOLD}{CYAN}├ Enter/Ctrl+C to go Back{RESET}")
    try:
        delete_media_input = input(f"{BOLD}{RED}└─# {RESET}")
    except KeyboardInterrupt:
        print(colored("\n[+] Operation Canceled", "green"))
        return
    if delete_media_input.lower() == "delete all":
        for root, dirs, files in os.walk(delete_path):
            dirs[:] = [d for d in dirs if d not in skip_delete_folders]

            for file in files:
                if any(file.lower().endswith(ext) for ext in all_extensions):
                    current_file = os.path.join(root, file)
                    try:
                        os.remove(current_file)
                        print(f"Deleted: {current_file}")
                    except Exception as e:
                        print(f"Error deleting {current_file}: {str(e)}")
    else:
        print(colored("[+] Operation Canceled", "green"))
        return


# Function to create a cool banner
def banner():
    print(colored(r"""
       ___  __             __   __   __              __  ___ 
 |\/| |__  |  \ |  /\     /  \ |__) / _`  /\  |\ | |  / |__  
 |  | |___ |__/ | /~~\    \__/ |  \ \__> /~~\ | \| | /_ |___ 

""", "green", attrs=["bold"]))


def scan_media_and_organize(scan_location, extensions, destination_folder):
    print("\n")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, _, files in os.walk(scan_location):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)
                try:
                    shutil.copy2(source_path, destination_path)
                except:
                    pass


def scan_for_unique_media(directory, extensions):
    unique_media = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                unique_media.add(file.lower())

    return unique_media


def scan_for_media(directory, extensions):
    media_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                media_count += 1

    return media_count


def find_duplicate_media(scan_location, extensions):
    duplicate_media = defaultdict(list)

    for root, _, files in os.walk(scan_location):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                duplicate_media[file.lower()].append(file_path)

    duplicate_media = {key: value for key, value in duplicate_media.items() if len(value) > 1}
    return duplicate_media


def copy_duplicates(duplicate_media, duplicate_folder):
    for filename, paths in duplicate_media.items():
        if len(paths) > 1:
            base_name, ext = os.path.splitext(filename)
            copy_number = 1

            for path in paths:
                new_filename = f"{base_name}_{copy_number}{ext}"
                copy_path = os.path.join(duplicate_folder, new_filename)

                try:
                    shutil.copy2(path, copy_path)
                    copy_number += 1
                except Exception as e:
                    print(f"\nError copying {path} to {copy_path}: {str(e)}\n")


def check_lost_media(dir_photo, dir_video, main_scan):
    unique_photos = scan_for_unique_media(main_scan, photo_extensions)
    unique_videos = scan_for_unique_media(main_scan, video_extensions)

    photos_in_organized = scan_for_unique_media(dir_photo, photo_extensions)
    videos_in_organized = scan_for_unique_media(dir_video, video_extensions)

    missing_photos = list(unique_photos - photos_in_organized)
    missing_videos = list(unique_videos - videos_in_organized)

    # Sort the missing photos and videos
    missing_photos = natsorted(missing_photos)
    missing_videos = natsorted(missing_videos)
    if not missing_photos:
        p_status = "green"
    else:
        p_status = "red"

    if not missing_videos:
        v_status = "green"
    else:
        v_status = "red"
    print(colored(f"\n[*] Location of Current folder: [{main_scan}]", "cyan"))
    print(colored(f"[*] Location of Organized folder: [{dir_photo}]\n", "cyan", attrs=["bold"]))
    print(colored(f"    Number of unique photos at current folder: {len(unique_photos)}", p_status))
    print(
        colored(f"    Number of photos in the organized folder: {len(photos_in_organized)}", p_status, attrs=["bold"]))
    print("\nTransfer: ", end='')
    if not missing_photos:
        print(colored("✔ Successful ✔\n\n", "green"))
    else:

        print(colored(f"Missing {len(missing_photos)} photos:\n", "red"))
        for missing_photo in missing_photos:
            print(colored(f"    [!]  - {missing_photo}", "red", attrs=["bold"]))

    print(colored(f"\n[*] Location of Current folder: [{main_scan}]", "cyan"))
    print(colored(f"[*] Location of Organized folder: [{dir_video}]\n", "cyan", attrs=["bold"]))
    print(colored(f"    Number of unique videos at current folder: {len(unique_videos)}", v_status))
    print(colored(f"    Number of videos in organized folder: {len(videos_in_organized)}", v_status, attrs=["bold"]))
    print("\nTransfer: ", end='')
    if not missing_videos:
        print(colored("✔ Successful ✔\n\n", "green"))
    else:
        print(colored(f"Missing {len(missing_videos)} videos:\n", "red"))
        for missing_video in missing_videos:
            print(colored(f"    [!]  - {missing_video}", "red", attrs=["bold"]))


def check_duplicate_media(scan_location):
    duplicate_photos = find_duplicate_media(scan_location, photo_extensions)
    duplicate_videos = find_duplicate_media(scan_location, video_extensions)
    dup_photos = []
    dup_videos = []
    print(colored(f"\n[*] Duplicates in [{scan_location}]", "cyan"))
    if not duplicate_photos and not duplicate_videos:
        print(colored("No duplicate media found.", "green"))
    else:
        if duplicate_photos:
            print(colored(f"Number of duplicate photos: {len(duplicate_photos)}", "red", attrs=["bold"]))
            for filename, paths in duplicate_photos.items():
                print(colored(f"\n  [!] {filename}", "red"))
                for path in paths:
                    dup_photos.append(path)
                    print(f"    - {path}")
        if duplicate_videos:
            print(colored(f"Number of duplicate videos: {len(duplicate_videos)}", "red", attrs=["bold"]))
            for filename, paths in duplicate_videos.items():
                print(colored(f"\n  [!] {filename}", "red"))
                for path in paths:
                    dup_videos.append(path)
                    print(f"    - {path}")
    try:
        print(colored("\n[+] Choose an option:", "cyan", attrs=["bold"]))
        print(colored("    1) Copy duplicate paths to a text file", "red"))
        print(colored("    2) Copy duplicates to a duplicate folder\n", "red"))
        print(colored("    [!] Go Back? -> [Ctrl + C] or [Enter (Empty input)]: ", "yellow", attrs=["bold"]))
        copy_duplicates_option = input(colored("    [~] Enter your choice: ", "blue", attrs=["bold"]))
    except KeyboardInterrupt:
        return

    if copy_duplicates_option == "1":
        try:
            print("[?] Example: C:\\Users\\Name\\Desktop\\Paths.txt")
            duplicate_paths_file = input(
                colored("[+] Enter the path to create text file: ", "red", attrs=["bold"]))
        except KeyboardInterrupt:
            return

        duplicate_photos = natsorted(dup_photos)
        duplicate_videos = natsorted(dup_videos)

        with open(duplicate_paths_file, 'w') as file:
            file.write("\nDuplicate Photos:\n")
            for path in duplicate_photos:
                file.write(path + "\n")
            file.write("\nDuplicate Videos:\n")
            for path in duplicate_videos:
                file.write(path + "\n")

        print(f"\n[•] Duplicate paths written to '{duplicate_paths_file}'.")

    elif copy_duplicates_option == "2":
        try:
            duplicate_folder = input(
                colored("\n[+] Enter the path to create the duplicate folder: ", "red", attrs=["bold"]))
        except KeyboardInterrupt:
            return
        if not os.path.exists(duplicate_folder):
            os.makedirs(duplicate_folder)
        duplicate_photos = find_duplicate_media(scan_location, photo_extensions)
        duplicate_videos = find_duplicate_media(scan_location, video_extensions)
        copy_duplicates(duplicate_photos, duplicate_folder)
        copy_duplicates(duplicate_videos, duplicate_folder)
        print(f"\n[•] Duplicates copied to '{duplicate_folder}'.")


if __name__ == "__main__":
    # ANSI escape codes for text formatting and colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    # Define photo and video extensions separately
    photo_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    video_extensions = [".mp4", ".avi", ".mov", ".mkv"]

    main()
