# import os
# import datetime
#
# # Step 1: Give the path of your file
# file_path = "file1.jpeg"  # change to your file name
#
# # Step 2: Get file information
# file_info = os.stat(file_path)
#
# # Step 3: Convert timestamps into readable format
# created = datetime.datetime.fromtimestamp(file_info.st_ctime)
# modified = datetime.datetime.fromtimestamp(file_info.st_mtime)
#
# # Step 4: Print results
# print("📄 File:", file_path)
# print("📅 Created:", created)
# print("🕒 Modified:", modified)
#
# # Step 5: Check if file was modified after creation
# if modified > created:
#     print("⚠️ The file was modified AFTER creation!")
#     print("⌛ Time Difference:", modified - created)
# else:
#     print("✅ File has not been modified after creation.")

# check_timestamps.py
import os
import datetime

def check_timestamps(file_path):
    file_info = os.stat(file_path)
    created = datetime.datetime.fromtimestamp(file_info.st_ctime)
    modified = datetime.datetime.fromtimestamp(file_info.st_mtime)

    print("📄 File:", file_path)
    print("📅 Created:", created)
    print("🕒 Modified:", modified)

    if modified > created:
        print("⚠️ The file was modified AFTER creation!")
        print("⌛ Time Difference:", modified - created)
    else:
        print("✅ File has not been modified after creation.")

    return created, modified

