
import re
import unicodedata
import pandas as pd

ptrs = [r"(地下)*(\d)+?(F)", r"(B)*(\d)+?F", r"B(\d)+?"]
compiled_ptr = [re.compile(ptr) for ptr in ptrs]
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
def test():
    lit = [ "東京都千代田区丸の内１丁目９−１ 東京駅構内（改札内） グランスタ 地下１階 ＪＲ 東日本",
            "東京都千代田区丸の内１丁目９−１ 大丸東京店 Ｂ１Ｆ",
            "東京都千代田区丸の内１丁目９−１ ＪＲ東日本東京駅 Ｂ１",
            "東京都千代田区丸の内１丁目９−１ 東京駅 八重洲中央口改札 Ｂ１Ｆグランスタ八重洲内",
            "東京都千代田区丸の内２丁目４−１ 丸ビル ４階",
            "東京都渋谷区道玄坂１丁目１２−１ 渋谷東急フードショー２ しぶちか",
            "北海道札幌市中央区北５条西２丁目 ＪＲタワーエスタ ７階",
            ]
    normal_lit = []
    for x in lit:
        normal_lit.append(address_cleansing(x))
    print(normal_lit)
    
    df = pd.read_csv("addresses.csv")
    df["rule"] = 1
    df = df[:100]
    df.apply(set_floor, axis=1)
    eval = evaluate(df, "label", "rule")
    print(eval)
    print(df)
    df.to_csv("address_test.csv")
    return
    


def address_cleansing(address):
    address = unicodedata.normalize("NFKC", address)
    address = address.replace("階", "F")
    splited_address = address.split()
    for prefecture in prefectures:
        if prefecture in splited_address[0]:
            if len(splited_address) > 1:
                address = "".join(splited_address[1:])
                return address
    return address


    # for x in normal_lit:
    #     flag = False
    #     for y in compiled_ptr:
    #         res = re.search(y, x)
    #         if res:
    #             if y == r"(地下)*(\d)+?階":
    #                 print(res.group(2), x, y)
    #             else:
    #                 print(res.group(1), x, y)
    #             flag = True
    #         if flag:
    #             break
    
def get_floor(address):
    level = 1
    for y in compiled_ptr:
        res = re.search(y, address)
        print(res)
        if res:
            if y == compiled_ptr[0]:
                if res.group(1):
                    level = -1 * int(res.group(2))
                else:
                    level = int(res.group(2))
                return level
            elif y == compiled_ptr[1]:
                if res.group(1):
                    level = -1 * int(res.group(2))
                else:
                    level = int(res.group(2))
                return level
            else:
                level = -1 * int(res.group(1))
                return level
    return level

def set_floor(row):
    row["rule"] = get_floor(row["address"])
    return row

def check_label(row, true_label, pred_label):
    # if predict_label == true_label
    # return true else false
    row["result"] = (int(row[true_label]) == int(row[pred_label]))
    return row

def evaluate(df: pd.DataFrame, true_label_name, pred_label_name):
    df["result"] = False
    df = df.apply(check_label, args=(true_label_name, pred_label_name), axis=1)
    eval = df["result"].value_counts() / df.shape[0]
    return eval
    
if __name__ == "__main__":
    test()

