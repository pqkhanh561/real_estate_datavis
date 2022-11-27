import csv, sqlite3
from enum import Enum
import random

DatabaseConnection = sqlite3.connect("../db.sqlite3")
ConnectionCursor = DatabaseConnection.cursor()

"""
    Import utility to database with follow order

"""
UTILITY = [
    "ID",
    "utility_Gần chợ, siêu thị",
    "utility_Gần trường học",
    "utility_Di chuyển thuận tiện ra trung tâm",
    "utility_Thiết kế thông thoáng",
    "utility_Khu vực an ninh, yên tĩnh",
    "utility_Gần mặt tiền đường",
    "utility_Gần bệnh viện",
    "utility_Gần công viên, trung tâm",
    "utility_Sân để xe rộng rãi",
    "utility_Hẻm thông",
    "utility_Cần bán gấp",
    "utility_Nở hậu",
    "utility_2 Mặt hẻm",
    "utility_2 Mặt đường chính"
]

DB_UTILITY = [
    'id', 'near_market', 'near_school', 'near_center',
    'good_design', 'security', 'near_front_road', 'near_hospital',
    'near_park', 'parking', 'through_road', 'fast_trade', 'open_house', 'two_small_roads', 'two_roads'
]


def handle_utility(key, value):
    return UTILITY.index(key), value.lower() == "true"


PROPERTY = [
    "ID",
    "property_Phòng ngủ",
    "property_Phòng tắm",
    "property_Diện tích sử dụng",
    "property_Hướng",
    "property_Hiện trạng nhà",
    "property_Giấy tờ",
    "property_Chiều dài",
    "property_Chiều rộng",
    "property_Độ rộng hẻm",
    "property_Kết cấu nhà",
    "property_Năm xây dựng",
    "property_Độ rộng mặt tiền đường"
]
DB_PROPERTY = ['id', 'num_bedroom', 'num_bathroom', 'area',
               'direction', 'status', 'license', 'width', 'height',
               'road_width', 'structure', 'year', 'front_width']


def handle_property(key, value):
    if value == '':
        value = None
    try:
        return PROPERTY.index(key), int(value)
    except (ValueError, TypeError):
        if key in ['property_Diện tích sử dụng', 'property_Chiều dài', 'property_Chiều rộng', 'property_Độ rộng hẻm', "property_Độ rộng mặt tiền đường"] and value !=None:
            value = int(value.split(' ')[0])
            return PROPERTY.index(key), value
        return PROPERTY.index(key), value


DB_HOUSE = ['code', 'name', 'address', 'total_price', 'unit_price', 'property_id', 'utility_id']


def handle_general(key, value):
    if key == "item_code":
        return 0, int(value)
    if key == "item_name":
        return 1, value
    if key == "total_price":
        if value.split(' ')[1].lower() == "tỷ":
            return DB_HOUSE.index(key), float(value.split(' ')[0].replace(',', '.'))*1000
        else:
            return DB_HOUSE.index(key), float(value.split(' ')[0].replace(',', '.'))
    return DB_HOUSE.index(key), value


if __name__ == '__main__':

    ConnectionCursor.execute("DELETE FROM search_utility")
    ConnectionCursor.execute("DELETE FROM search_property")
    ConnectionCursor.execute("DELETE FROM search_house")
    DatabaseConnection.commit()

    ConnectionCursor.execute("SELECT * FROM search_utility")
    num_utility_fields = len(ConnectionCursor.description)
    ConnectionCursor.execute("SELECT * FROM search_property")
    num_property_fields = len(ConnectionCursor.description)
    field_names = [i[0] for i in ConnectionCursor.description]
    ConnectionCursor.execute("SELECT * FROM search_house")
    num_house_fields = len(ConnectionCursor.description)

    with open('../../data/post_propzy.csv', 'r') as fin:
        lines = csv.DictReader(fin)
        for random_id, data in enumerate(lines):
            item_utility = [None] * num_utility_fields
            item_property = [None] * num_property_fields
            item_house = [None] * num_house_fields
            item_utility[0] = random_id
            item_house[-1] = random_id
            item_house[-2] = random_id
            item_property[0] = random_id
            for keys, value in data.items():
                if "utility" in keys and keys != "utility_Na":
                    p, v = handle_utility(keys, value)
                    item_utility[p] = v
                elif "property" in keys:
                    try:
                        p, v = handle_property(keys, value)
                        item_property[p] = v
                    except ValueError:
                        pass
                else:
                    try:
                        p, v = handle_general(keys, value)
                        item_house[p] = v
                    except ValueError:
                        pass
            # House insert database
            db_house_str = f"{DB_HOUSE}".replace("[", '').replace("]", '').replace("'", '')
            value_house_str = f"{item_house}".replace("[", '').replace("]", '').replace("''", "NULL")
            try:
                ConnectionCursor.execute(
                    f"INSERT INTO search_house({db_house_str}) VALUES ({value_house_str})")
            except sqlite3.IntegrityError as e:
                print(e)
                continue
            # Property insert database
            db_property_str = f"{DB_PROPERTY}".replace("[", '').replace("]", '').replace("'", '')
            value_property_str = f"{item_property}".replace("[", '').replace("]", '').replace("None", "NULL")
            ConnectionCursor.execute(f"INSERT INTO search_property({db_property_str}) VALUES ({value_property_str})")
            # Utility insert database
            db_utility_str = f"{DB_UTILITY}".replace("[", '').replace("]", '').replace("'", '')
            value_utility_str = f"{item_utility}".replace("[", '').replace("]", '').replace("True", "TRUE").replace(
                "False", "FALSE")
            ConnectionCursor.execute(f"INSERT INTO search_utility({db_utility_str}) VALUES ({value_utility_str})")
    DatabaseConnection.commit()
    DatabaseConnection.close()
