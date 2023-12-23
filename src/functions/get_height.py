from google.cloud import storage
from google.cloud import storage
import xml.etree.ElementTree as ET
import os
from shapely.geometry import Point, Polygon

# (lat, long) difference pair by mesh
PRIMARY = (40/60, 1)
SECONDARY = (5/60, 7/60 + 30/3600)
THIRD = (30/3600, 45/3600)


def get_building_height(bldg_lat, bldg_long):
    dest = Point(bldg_lat, bldg_long)
    
    path = get_meshcode(bldg_lat, bldg_long)
    if not os.path.isfile(path):
        download_blob("air-pin-backend", f"bldg/{path}", path)
    if not os.path.isfile(path):
        return None
    tree = ET.parse(path)
    namespaces = {node[0]: node[1] for _, node in ET.iterparse(path, events=['start-ns'])}
    for key, value in namespaces.items(): 
        ET.register_namespace(key, value)
    root = tree.getroot()
    
    for building in root.findall('{http://www.opengis.net/citygml/2.0}cityObjectMember'):
        roof_edge = building[0].findall('{http://www.opengis.net/citygml/building/2.0}lod0RoofEdge')
        if roof_edge:
            for gml_posList in roof_edge[0][0][0][0][0][0]:
                    # 経度と緯度に分割して取得
                    posList = gml_posList.text.split()
                    if isIncludePoint(dest, posList):
                        ceiling_height = get_ceiling_height(building[0])
                        return ceiling_height
            continue
        foot_print = building[0].findall('{http://www.opengis.net/citygml/building/2.0}lod0FootPrint')
        if foot_print:
            for gml_posList in foot_print[0][0][0][0][0][0]:
                # 経度と緯度に分割して取得
                posList = gml_posList.text.split()
                if isIncludePoint(dest, posList):
                    ceiling_height = get_ceiling_height(building[0])
                    return ceiling_height
    return None

def isIncludePoint(point, posList):
    # 目的地が建物に含まれるか判定
    posList = [(float(posList[3*x]), float(posList[3*x+1])) for x in range(int(len(posList)/3))]
    poly = Polygon(posList)
    return poly.contains(point)

def get_ceiling_height(building:ET.Element):
    print("found")
    height = building.findall('{http://www.opengis.net/citygml/building/2.0}measuredHeight')
    if height:
        height = height[0].text
    else:
        height = None
    level = building.findall('{http://www.opengis.net/citygml/building/2.0}storeysAboveGround')
    if level:
        level = level[0].text
    else:
        level = None
    print(height)
    print(level)
    if height and level:
        ceiling_height = float(height)/float(level)
        print(ceiling_height)
    return ceiling_height

def get_meshcode(lat, long):
    # meshcodeを緯度経度から探索
    # 参考
    # https://www.gis-py.com/entry/py-latlon2mesh
    #1次メッシュ上2けた
    quotient_lat, remainder_lat = divmod(lat * 60, 40)
    first2digits = str(quotient_lat)[0:2]

    #1次メッシュ下2けた
    last2digits = str(long - 100)[0:2]
    remainder_lon = long - int(last2digits) - 100
    #1次メッシュ
    first_mesh = first2digits + last2digits

    #2次メッシュ上1けた
    first1digits, remainder_lat = divmod(remainder_lat, 5)
    #2次メッシュ下1けた
    last1digits, remainder_lon = divmod(remainder_lon * 60, 7.5)
    #2次メッシュ
    second_mesh = first_mesh + str(first1digits)[0:1] + str(last1digits)[0:1]

    #3次メッシュ上1けた
    first1digits, remainder_lat = divmod(remainder_lat * 60, 30)
    #3次メッシュ下1けた
    last1digits, remainder_lon = divmod(remainder_lon * 60, 45)
    #3次メッシュ
    third_mesh = second_mesh + str(first1digits)[0:1] + str(last1digits)[0:1]

    mesh_code = third_mesh
    print(mesh_code)
    # mesh_code = 50302290
    # mesh_code = 50303303
    return f"{mesh_code}_bldg_6697_op.gml"

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )