from ..functions.get_level import address_cleansing, get_floor


def test():
    lit = [ "東京都千代田区丸の内１丁目９−１ 東京駅構内（改札内） グランスタ 地下１階 ＪＲ 東日本",
            "東京都千代田区丸の内１丁目９−１ 大丸東京店 Ｂ１Ｆ",
            "東京都千代田区丸の内１丁目９−１ ＪＲ東日本東京駅 Ｂ１",
            "東京都千代田区丸の内１丁目９−１ 東京駅 八重洲中央口改札 Ｂ１Ｆグランスタ八重洲内",
            "東京都千代田区丸の内２丁目４−１ 丸ビル ４階",
            "東京都渋谷区道玄坂１丁目１２−１ 渋谷東急フードショー２ しぶちか",
            "北海道札幌市中央区北５条西２丁目 ＪＲタワーエスタ ７階",
            "福岡県福岡市西区北原１丁目２−１ 3F",
            "日本、〒812-0012 福岡県福岡市博多区博多駅中央街１−１ アミュプラザ博多内 JR博多シティ 8F",
            ]
    normal_lit = []
    for x in lit:
        normal_lit.append(address_cleansing(x))
    print(normal_lit)
    for x in normal_lit:
        print("住所", x)
        print("階層", get_floor(x))
    return
    
if __name__ == "__main__":
    test()