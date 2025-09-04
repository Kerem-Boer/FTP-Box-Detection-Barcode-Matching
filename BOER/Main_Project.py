import os
import Box_Detection
import FTP_Dinleyici
from datetime import datetime
import time
import cv2
import Dynamsoft


License = "t0084YQEAACs35KttOFqpGWG3cbrIK1d0Oe+ogzSpCQkXvztm/slNKz1REs1OJ1XTfKmON0NAmzWbsHKBgkhsMXr+9vbrzhVwxvdO470z5WJZyQ7sCkm0"
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
    FTP_Dinleyici.FTP_Login(FTP_Address, FTP_Username, FTP_Password)

    # Loop start
    while True:
        new_files = FTP_Dinleyici.check_files(FTP_Dinleyici.ftp)
        if new_files:
            for filename in new_files:
                while not FTP_Dinleyici.size_check(filename):
                    time.sleep(0.1)
                    # FTP_Dinleyici.print_size(filename)
                FTP_Dinleyici.download_file(Local_Path , filename)
            for filename in new_files:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # Check if file is an image
                    frame = Open_Image(Local_Path + filename)  # Open the image
                    Box_Detection.Detect_Boxes(frame)  # Detect boxes in the image
                    Box_Detection.Crop_Image(frame, Box_Detection.Boxes)
                    Dynamsoft.activate_license(License)
                    for idx, _ in enumerate(Box_Detection.Boxes):
                        items = Dynamsoft.get_items(f"Cropped_Image_{idx}.jpg")
                        if items:
                            Dynamsoft.Write_Info(items)
                            Box_Detection.Complex_Draw_Box(frame, items, Box_Detection.Boxes[idx])
                            Box_Detection.Add_Child_Barcode(items, Box_Detection.Boxes[idx])
                    

                    new_filename = Update_Filename(filename)
                    os.rename("output.jpg", Local_Path + new_filename)
                    FTP_Dinleyici.upload_file(Local_Path, new_filename)  # Upload the processed image to FTP
                    for box in Box_Detection.Boxes:
                        print(box)

                    Box_Detection.Export_Data(Local_Path + new_filename)
                    new_filename = os.path.splitext(new_filename)[0] + ".txt"
                    FTP_Dinleyici.upload_file(Local_Path, new_filename)

        time.sleep(0.5)
        # print("Waiting for new files...")

if __name__ == "__main__":
    main()