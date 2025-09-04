import dynamsoft_barcode_reader_bundle as dbr
import cv2

# License = "t0084YQEAACs35KttOFqpGWG3cbrIK1d0Oe+ogzSpCQkXvztm/slNKz1REs1OJ1XTfKmON0NAmzWbsHKBgkhsMXr+9vbrzhVwxvdO470z5WJZyQ7sCkm0"
# image_path = r"C:\Users\Kerem\Desktop\VSC\Python\BOER\Cropped_Image_0.jpg"
output_path = r"C:\Users\Kerem\Desktop\VSC\Python\BOER\Cropped_Image21.jpg"

def activate_license(License):
    dbr.LicenseManager.init_license(license=License)
    print("License activated.")

def Draw_Box(image_path,items,output_path):
    image = cv2.imread(image_path)
    for item in items:
        quad = item.get_location()
        cv2.rectangle(image, (quad.points[0].x, quad.points[0].y), (quad.points[2].x, quad.points[2].y), (255, 0, 0), 2)
    cv2.imwrite(output_path, image)
    print("Drawed Boxes")

def Find_Mid(item):
    quad = item.get_location()
    mid_x = (quad.points[0].x + quad.points[2].x) // 2
    mid_y = (quad.points[0].y + quad.points[2].y) // 2
    return (mid_x, mid_y)

def Write_Info(items):
    print("\nBunlar aynı kutu üzerinde bulunan barkodlar:")
    for item in items:
        mid_point = Find_Mid(item)
        print(f"Format: {item.get_format_string()}; "
                f"Text: {item.get_text()}; "
                f"Mid: {mid_point}")

def get_items(image_path):
    items = dbr.CaptureVisionRouter().capture_multi_pages(image_path, dbr.EnumPresetTemplate.PT_READ_BARCODES).get_results()[0].get_decoded_barcodes_result().get_items()
    return items

def Export_Write_Info(items , output_file):
    output_file = output_file.replace(".jpg", ".txt")
    with open(output_file, 'w') as f:
        f.write("\nBunlar ayni kutu üzerinde bulunan barkodlar:")
        for item in items:
            mid_point = Find_Mid(item)
            f.write(f"Format: {item.get_format_string()}; "
                f"Text: {item.get_text()}; "
                f"Mid: {mid_point}\n")
    # print(f"Boxes' data has been written to: {output_file}")