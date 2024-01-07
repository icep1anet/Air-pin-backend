import re
import unicodedata

import pandas as pd

# , r"B(\d)+?F?, r"(地下)?\s*?(\d)+?(F)?","
ptrs = [r"(b|地下)?\s*?(\d)+?(F)?"]
compiled_ptrs = [re.compile(ptr) for ptr in ptrs]
post_code_ptrs = [r"〒?[0-9]{3}-[0-9]{4}", r"〒?[0-9]{7}"]
compiled_post_code_ptrs = [re.compile(ptr) for ptr in post_code_ptrs]
prefectures = tuple(["北海道", "青森県", "岩手県", "宮城県", "秋田県",
            "山形県", "福島県", "茨城県", "栃木県", "群馬県",
            "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県",
            "富山県", "石川県", "福井県", "山梨県", "長野県", 
            "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", 
            "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", 
            "鳥取県", "島根県", "岡山県", "広島県", "山口県", 
            "徳島県", "香川県", "愛媛県", "高知県", "福岡県", 
            "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", 
            "鹿児島県", "沖縄県"])


def address_cleansing(address):
    address = unicodedata.normalize("NFKC", address)
    address = address.replace("階", "F")
    for post_code_ptr in compiled_post_code_ptrs:
        address = re.sub(post_code_ptr, "", address)
    address = address.lower()
    splited_address = address.split()
    for index in range(len(splited_address)):
        for prefecture in prefectures:
            if prefecture in splited_address[index]:
                if len(splited_address) > 1:
                    del splited_address[index]
                    address = " ".join(splited_address[:])
                    return address
    return address

def get_floor(address):
    level = 0
    for ptr in compiled_ptrs:
        # 繰り返しマッチ
        res = re.finditer(ptr, address)
        for match_object in res:
            print(match_object)
            if match_object:
                print(match_object.group(1), match_object.group(2))
                if match_object.group(1):
                    level = -1 * int(match_object.group(2))
                else:
                    if int(match_object.group(2)) == 1:
                        continue
                    elif int(match_object.group(2)) == abs(level):
                        continue
                    elif match_object.group(3):
                        level = int(match_object.group(2))
                    else:
                        continue
            print("level", level)
    if level == 0:
        # どれにも引っかからなかった場合地下街などのワードから地下1階を推測
        for tika in ["ちか", "地下"]:
            if tika in address:
                level = -1
            else:
                level = 1
    return level

def get_floor_level(address):
    address = address_cleansing(address)
    print(address)
    return get_floor(address)
