import re

file_path = "C:\\Users\\Kerem\\Desktop\\cr.txt"

class Barcode:
    def __init__(self, coordinate, type, value):
        self.coordinate = coordinate
        self.type = type
        self.value = value

    def set_coordinate(self, coordinate):
        self.coordinate = coordinate

    def set_type(self, type):
        self.type = type

    def set_value(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"Barcode(coordinate={self.coordinate}, type={self.type}, value={self.value})"

Barcodes = []

def find_mid(x1,y1,x3,y3):
    x=(x1+x3)/2
    y=(y1+y3)/2
    return (x,y)

def extract_coordinates(line):
    # Tüm (x,y) koordinatlarını bul
    coords = re.findall(r'\((\d+),(\d+)\)', line)
    x1, y1 = coords[0]
    x3, y3 = coords[2]
    mid = find_mid(int(x1), int(y1), int(x3), int(y3))
    return mid

def extract_barcode_type(line):
    # Barkod türünü yakalamak için örnek desen
    match = re.search(r'(EAN13|CODE 128|QR|UPCA|DATA_MATRIX|PDF417)', line.upper())
    if match:
        return match.group(1)
    return None

def extract_barcode_value(line):
    value_match = re.search(r'_p_([^\s]+)', line)
    barcode_value = value_match.group(1) if value_match else None
    return barcode_value

def is_inside_box(box_coords, barcode_mid_coords):
    x,y = barcode_mid_coords
    x1, y1, x2, y2 = box_coords
    if (x1 < x < x2) and (y1 < y < y2):
        return True
    return False

def parse_barcode_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            coords = extract_coordinates(line.strip())
            barcode_type = extract_barcode_type(line.strip())
            barcode_value = extract_barcode_value(line.strip())
            barcode = Barcode(coordinate=coords, type=barcode_type, value=barcode_value)
            Barcodes.append(barcode)
    # return Barcodes
