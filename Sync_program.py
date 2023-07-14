import os
import filecmp
import shutil
import time
import logging

def folder_sync(source_folder, replica_folder):
    # Compare both folder's contents
    check_content = filecmp.dircmp(source_folder, replica_folder)

    # Iterate over the files that exist in the source and not the replica
    for file in check_content.left_only:
        # Create a path for each file in the source and the destination
        source_file = os.path.join(source_folder, file)
        replica_file = os.path.join(replica_folder, file)
        # Check if source_file is a directory
        if os.path.isdir(source_file):
            shutil.copytree(source_file, replica_file, symlinks=True)
            logging.info(f"Directory ({replica_file}) added to {replica_folder}")
        else:
            shutil.copy2(source_file, replica_file)
            logging.info(f"Copied ({replica_file}) to {replica_folder}")

    # Files that exist in the replica and not the source
    for file in check_content.right_only:
        some_file = os.path.join(replica_folder, file)
        if os.path.isdir(some_file):
            shutil.rmtree(some_file)
            logging.info(f"Deleted {some_file} from {replica_folder}")
        else:
            os.remove(some_file)
            logging.info(f"Deleted {some_file} from {replica_folder}")


    # Check subdirectories
    # Recursive action to check every item in the subdirectories
    for subdir in check_content.common_dirs:
        sub_source = os.path.join(source_folder, subdir)
        sub_replica = os.path.join(replica_folder, subdir)
        folder_sync(sub_source, sub_replica)

def sync_interval():
    source_folder = input("Please enter the main folder directory: ")
    replica_folder = input("Please enter the replica folder directory: ")
    log_directory = input("Please enter the log directory path: ")

    #log directory must be different than replica directory
    if log_directory == replica_folder:
        log_directory = input("Please enter a path that is outside the replica folder: ")

    interval = float(input("Please enter the desired sync interval in minutes: "))


    # Logging
    log_file = os.path.join(log_directory, "sync_log.txt")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    folder_sync(source_folder, replica_folder)  # Initial synchronization

    #sync interval
    while True:
        time.sleep(interval * 60)
        folder_sync(source_folder, replica_folder)


sync_interval()



