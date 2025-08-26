import smbclient
import os
import time

# Global variables
# server_address = "192.168.0.4"
share_path = r"\\192.168.0.4\Fax_teknik\Test"
# username = "boerltd\\stajyer"
# password = "Boer2637#"
# previous_files = set()

def SMB_Login(server_address, username, password):
    smbclient.register_session(server=server_address, username=username, password=password)
    global previous_files
    previous_files = set(smbclient.listdir(share_path))
    print(f"Connected to SMB share: {share_path}")

def download_file(local_path, filename):
    remote_file_path = os.path.join(share_path, filename)
    with smbclient.open_file(remote_file_path, mode="rb") as remote_file:
        with open(os.path.join(local_path, filename), "wb") as local_file:
            local_file.write(remote_file.read())
    print(f"Downloaded: {filename}")

def upload_file(local_path, filename):
    remote_file_path = os.path.join(share_path + "\\Islenmis", filename)
    with open(os.path.join(local_path, filename), "rb") as local_file:
        with smbclient.open_file(remote_file_path, mode="wb") as remote_file:
            remote_file.write(local_file.read())
    print(f"Uploaded: {filename}")

def print_size(filename):
    remote_file_path = os.path.join(share_path, filename)
    size = smbclient.stat(remote_file_path).st_size
    print(f"Size of {filename}: {size} bytes")

# def size_check(filename):
#     remote_file_path = os.path.join(share_path, filename)
#     size = smbclient.stat(remote_file_path).st_size
#     if size is None or size <= 0:
#         return False
#     else:
#         return True

def check_files():
    global previous_files
    current_files = set(smbclient.listdir(share_path))
    new_files = current_files - previous_files
    previous_files = current_files
    return new_files

def is_file_safe_to_process(filename):
    remote_file_path = os.path.join(share_path, filename)
    try:
        # size1 = smbclient.stat(remote_file_path).st_size
        # time.sleep(0.5)
        # size2 = smbclient.stat(remote_file_path).st_size
        # if size1 != size2 or size1 == 0:
            # return False
        with smbclient.open_file(remote_file_path, mode="rb") as f:
            return True
    except Exception:
        return False


# def main():
#     SMB_Login(server_address, username, password)
#     # Example usage
#     download_file("C:\\Users\\Kerem\\Desktop\\VSC\\Python\\BOER\\DEPO", "Test1212.txt")
#     upload_file("C:\\Users\\Kerem\\Desktop\\VSC\\Python\\BOER\\DEPO", "Test3.txt")
    # print_size("file_name.txt")
    # if size_check("file_name.txt"):
    #     print("File is not empty.")
    # else:
    #     print("File is empty.")
    # new_files = check_files()
    # if new_files:
    #     print("New files detected:")
    #     for file in new_files:
    #         print(f" - {file}")
    # else:
    #     print("No new files detected.")