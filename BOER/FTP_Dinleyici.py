import ftplib

def FTP_Login(FTP_Address, FTP_Username, FTP_Password):
    global ftp
    ftp = ftplib.FTP(FTP_Address)
    ftp.login(FTP_Username, FTP_Password)
    ftp.set_pasv(True)
    global previous_files
    previous_files = set(ftp.nlst())
    print(f"Connected to FTP server: {FTP_Address}")

def download_file(Local_Path, filename):
    ftp.cwd('/')
    with open(Local_Path + filename, 'wb') as local_file:
       ftp.retrbinary(f'RETR {filename}', local_file.write)
    print(f"Downloaded: {filename}")

def upload_file(Local_Path, filename):
    ftp.cwd('/Islenmis')
    with open(Local_Path + filename, 'rb') as local_file:
        ftp.storbinary(f'STOR {filename}', local_file)
    print(f"Uploaded: {filename}")
    ftp.cwd('/')

def print_size(Path):
    print(f"Size of {Path}: {ftp.size(Path)} bytes")

def size_check(Path):
    size = ftp.size(Path)
    if size is None or size <= 0:
        return False
    else:
        return True

def check_files(ftp):
    global previous_files
    current_files = set(ftp.nlst())
    new_files = current_files - previous_files
    previous_files = current_files
    return new_files