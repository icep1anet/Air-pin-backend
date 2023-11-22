import os
import googlemaps
from dotenv import load_dotenv


class GoogleMapsAPI:
    # 公式refference
    # https://googlemaps.github.io/google-maps-services-python/docs/index.html
    def __init__(self):
        self.client = self.create_client()

    def get_API_KEY(self):
        load_dotenv()
        key = os.environ.get("GMP_API_KEY")
        return key

    def create_client(self):
        key = self.get_API_KEY()
        client = googlemaps.Client(key=key)
        return client

    def elevation(self, lat, long):
        # Elevation API は、地方平均海抜（LMSL）を基準とした高度（メートル単位）です。
        # 高度は、次のように正または負の値で返されます。
        # 正の値は、表面位置や高地湖の底部など、LMSL を超える位置を示します。
        # 負の値は、地表または海底の場所など、LMSL より下にある場所を示します。
        # [解像度] は、データポイントと標高の間の距離がメートル単位で表示されます。
        elevation = self.client.elevation((lat, long))
        # elevation = [{'elevation': 20.24903106689453,
        # 'location': {'lat': 33.59758, 'lng': 130.22412},
        # 'resolution': 9.543951988220215}]
        return elevation

    def geocode(self, address=None, place_id=None):
        # 住所またはplace_idを元に住所のgeoデータを取得
        # {'address_components': # [{'long_name': 'センター1号館', 'short_name': 'センター1号館', 'types': ['premise']}, {'long_name': '744', 'short_name': '744', 'types': ['premise']}, {'long_name': 'Motooka', 'short_name': 'Motooka', 'types': ['political', 'sublocality', 'sublocality_level_2']}, {'long_name': 'Nishi Ward', 'short_name': 'Nishi Ward', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': 'Fukuoka', 'short_name': 'Fukuoka', 'types': ['locality', 'political']}, {'long_name': 'Fukuoka', 'short_name': 'Fukuoka', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Japan', 'short_name': 'JP', 'types': ['country', 'political']}, {'long_name': '819-0385', 'short_name': '819-0385', 'types': ['postal_code']}],
        # 'formatted_address': 'Japan, 〒819-0385 Fukuoka, Nishi Ward, Motooka, ７４４ センター1号館',
        # 'geometry': {'bounds': {'northeast': {'lat': 33.597627, 'lng': 130.2242474}, 'southwest': {'lat': 33.5975196, 'lng': 130.2239923}}, 'location': {'lat': 33.5975765, 'lng': 130.2241188}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 33.5989604802915, 'lng': 130.2253366802915}, 'southwest': {'lat': 33.5962625197085, 'lng': 130.2226387197085}}}, 
        # 'place_id': 'ChIJuY9nBFnpQTUR-WFM0LawzQM',
        # 'types': ['premise']}
        if place_id is not None:
            return self.client.geocode(place_id=place_id)
        return self.client._geocode(address)

    def distance(self, origin, dest):
        distance = self.client.distance_matrix(origin, dest)
        return distance

if __name__ == "__main__":
    GM = GoogleMapsAPI()
    places = GM.geocode(place_id="ChIJuY9nBFnpQTUR-WFM0LawzQM")
    # for place in places[0]["address_components"]:
    #     print(place)
    # print(places[0]["formatted_address"])
    print(places[0]["geometry"]["bounds"])
    print(places[0]["geometry"]["location"])
    lat = places[0]["geometry"]["location"]["lat"]
    long = places[0]["geometry"]["location"]["lng"]
    elevation, resolution = GM.elevation(lat, long)
    print(elevation[0]["elevation"])

