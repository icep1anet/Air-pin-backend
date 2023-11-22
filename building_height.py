import xml.etree.ElementTree as ET

# (lat, long) difference pair by mesh
PRIMARY = (40/60, 1)
SECONDARY = (5/60, 7/60 + 30/3600)
THIRD = (30/3600, 45/3600)
base_path = "40130_fukuoka-shi_2022_citygml_1_op/udx/bldg/"

test_data = {
    "destName": "ABC-MARTイオンモール福岡伊都店",
    "destAddress": "日本、〒819-0379 福岡県福岡市西区北原１丁目２−１ 3F",
    "destLat": 33.5774038,
    "destLong": 130.2582227
}

def get_building_height(bldg_lat, bldg_long):
    path = search_mesh(bldg_lat, bldg_long)
    tree = ET.parse(base_path + path)
    root = tree.getroot()
    count = 0
    for child in root:
        count += 1
        if count >= 10:
            break
        print(child.tag, child.attrib)
    return
    
def search_mesh(lat, long):
    
    return "50302290_bldg_6697_op.gml"


if __name__ == "__main__":
    get_building_height(33, 135)

