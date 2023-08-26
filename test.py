import re
import unicodedata

import pandas as pd


def get_floor(row, ptr):
    address = row["address"]
    address = unicodedata.normalize("NFKC", address)
    for y in ptr:
        res = re.search(y, address)
        if res:
            if y == ptr[0]:
                if res.group(1):
                    row["rule"] = -1 * int(res.group(2))
                else:
                    row["rule"] = int(res.group(2))
                return row
            elif y == ptr[1]:
                if res.group(1):
                    row["rule"] = -1 * int(res.group(2))
                else:
                    row["rule"] = int(res.group(2))
                return row
            else:
                row["rule"] = -1 * int(res.group(1))
                return row
    return row

# r"(B)*(\d)+?F", r"B(\d)+?", r"(地下)*(\d)+?(階)"

def check_label(row):
    # label = row["label"]
    # rule = row["rule"]
    # print(label, rule, label == rule, row["label"] == row["rule"])
    # print(int(row["rule"]))
    row["res"] = (row["label"] == int(row["rule"]))
    return row

# name, address, target
def main():
    df = pd.read_csv("addresses.csv")
    df.drop(df.columns[[3]], axis=1)
    df = df.dropna(how="any", axis=1)

    df["rule"] = 0
    
    ptr = [r"(地下)*(\d)+?(階)", r"(B)*(\d)+?F", r"B(\d)+?"]
    compiled_ptr = []
    for x in ptr:
        compiled = re.compile(x)
        compiled_ptr.append(compiled)
    
    df = df.apply(get_floor, axis=1, ptr=compiled_ptr)
    print(df["rule"].value_counts())
    print(df.shape)
    
    df = df[df["rule"] != 0]
    print(df.shape)
    
    df["res"] = False
    df = df.apply(check_label, axis=1)
    # df.to_csv("address_rulebase.csv")
    print(df["res"].value_counts())
    
    
def main2():    
    df = pd.read_csv("address_rulebase.csv")
    # df = df.apply(check_label, axis=1)
    print(df.head())
    print(df["res"].value_counts())
    print(df["res"].value_counts()/df.shape[0])
    df = df[df["res"] == False]
    df.to_csv("address_incorrect.csv")


def re_test():
    lit = ["東京都千代田区丸の内１丁目９−１ 東京駅構内（改札内） グランスタ 地下１階 ＪＲ 東日本",
           "東京都千代田区丸の内１丁目９−１ 大丸東京店 Ｂ１Ｆ",
           "東京都千代田区丸の内１丁目９−１ ＪＲ東日本東京駅 Ｂ１",
           "東京都千代田区丸の内１丁目９−１ 東京駅 八重洲中央口改札 Ｂ１Ｆグランスタ八重洲内",
           "東京都千代田区丸の内２丁目４−１ 丸ビル ４階",
           "東京都渋谷区道玄坂１丁目１２−１ 渋谷東急フードショー２ しぶちか",
           "北海道札幌市中央区北５条西２丁目 ＪＲタワーエスタ ７階",
           
           ]
    normal_lit = []
    for x in lit:
        normal_lit.append(unicodedata.normalize("NFKC", x))
    ptr = [r"B*(\d)+?F", r"B(\d)+?", r"(地下)*(\d)+?(階)"]
    compiled_ptr = []
    for x in ptr:
        compiled_ptr.append(re.compile(x))
    
    for x in normal_lit:
        flag = False
        for y in ptr:
            res = re.search(y, x)
            if res:
                if y == r"(地下)*(\d)+?階":
                    print(res.group(2), x, y)
                else:
                    print(res.group(1), x, y)
                flag = True
            if flag:
                break
        

if __name__ == "__main__":
    main()