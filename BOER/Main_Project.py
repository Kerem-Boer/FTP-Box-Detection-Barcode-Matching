import os
import Box_Detection
import FTP_Dinleyici
import Coordinates
from datetime import datetime
import time
import cv2
import Dosya_Dinleyici

Local_Path = "C:\\Users\\Kerem\\Desktop\\VSC\\Python\\BOER\\Depo\\" # Local path to download Images
Model_Path = "C:\\Users\\Kerem\\Desktop\\VSC\\my_model\\my_model.pt" #YOLO model path
confidence_threshold = 0.8 # Confidence threshold for object detection

server_address = "192.168.0.4"
username = "boerltd\\stajyer"
password = "Boer2637#"

FTP_Address = "192.168.0.12"
FTP_Username = "stajyer"
FTP_Password = "Boer2637#"

Box_Detection.initialize_model(Model_Path)
Box_Detection.set_confidence_threshold(confidence_threshold)

def Update_Filename(filename):
    base_name, ext = os.path.splitext(filename)
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    new_filename = f"{base_name}_islendi_{date_str}{ext}"
    return new_filename

def Open_Image(image_path):
    if not os.path.exists(image_path):
        print(f"Can not find image: {image_path}")
        return None
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return None
    print(f"Image opened: {image_path}")
    return image

def Save_Image(frame, output_path):
    cv2.imwrite(output_path, frame)
    print(f"Image saved: {output_path}")

def main():
    # FTP_Dinleyici.FTP_Login(FTP_Address, FTP_Username, FTP_Password)
    Dosya_Dinleyici.SMB_Login(server_address, username, password)

    # Loop start
    while True:
        # print("Loop start")
        # new_files = FTP_Dinleyici.check_files(FTP_Dinleyici.ftp)
        new_files = Dosya_Dinleyici.check_files()
        # print("File Check")
        if new_files:
            # print("new file")
            for filename in new_files:
                # print("first for loop")
                # while not FTP_Dinleyici.size_check(filename):
                while not Dosya_Dinleyici.is_file_safe_to_process(filename):
                    # print("size check loop")
                    time.sleep(0.1)
                    # FTP_Dinleyici.print_size(filename)
                    # Dosya_Dinleyici.print_size(filename)
                # Dosya_Dinleyici.print_size(filename)
                # print("out of size check loop")
                # FTP_Dinleyici.download_file(Local_Path , filename)
                #print("b4 download")
                Dosya_Dinleyici.download_file(Local_Path , filename)
                # print("after download")
            for filename in new_files:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # Check if file is an image
                    frame = Open_Image(Local_Path + filename)  # Open the image
                    Box_Detection.Detect_Boxes(frame)  # Detect boxes in the image
                    # Draw boxes on the image & upload to FTP
                    processed_frame = Box_Detection.Draw_Boxes(frame, Box_Detection.Boxes)  # Draw boxes on the image
                    new_filename = Update_Filename(filename)
                    Save_Image(processed_frame, Local_Path + new_filename)  # Save the processed image
                    # FTP_Dinleyici.upload_file(Local_Path, new_filename)  # Upload the processed image to FTP
                    Dosya_Dinleyici.upload_file(Local_Path, new_filename)  # Upload the processed image to SMB
                    # Export box coordinates as .txt file & upload to FTP
                    new_filename = os.path.splitext(new_filename)[0] + ".txt"
                    Box_Detection.Export_Box_Coordinates(Box_Detection.Boxes, Local_Path + new_filename)  # Export box coordinates
                    # FTP_Dinleyici.upload_file(Local_Path, new_filename)  # Upload the box coordinates to FTP
                    Dosya_Dinleyici.upload_file(Local_Path, new_filename)  # Upload the box coordinates to SMB

                elif filename.lower().endswith((".txt", ".csv")):
                    print(f"File is a text or CSV file: {filename}")
                    # Coordinates.parse_barcode_file(Local_Path + filename)
                    # for b in Coordinates.Barcodes:
                    #     for i in Box_Detection.Boxes:
                    #         if Coordinates.is_inside_box(i.coordinates , b.coordinate):
                    #             i.add_child(b)
                    #             print(f"Barcode {b} is inside box {i}")
            # for i in Box_Detection.Boxes:
            #     print(f"Barcode {i.childs} is inside box {i}")

        time.sleep(0.5)
        # print("Waiting for new files...")

if __name__ == "__main__":
    main()