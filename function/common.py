import os
import json
# Chuyển đổi từ chuỗi -> chuỗi có dấu phẩy ngăn cách hàng nghìn
def change_number_to_thousand(number):
    number = float(number)
    num_ = "{:,}".format(number)
    return num_

# chuyển đổi từ chuỗi có dấu phẩy -> sang số float
def change_to_float(number):
    string = change_number_to_thousand(number)
    number_str = string.replace(",", "")
    return float(number_str)

def change_to_string(string):
    # Tách thành 2 phần của chuỗi trước dấu . 
    convert_string = string.split(".")[0]
    convert_string = convert_string.replace(",", "")
    return convert_string

def value_month(filePath):
    with open(filePath, "r", encoding = "utf-8") as f:
        data = json.load(f)
    month_value = {}
    for i in data:
        month = i["time"].split("/")[0]
        value = i["total_fee"]
        if month in month_value:
            month_value[month] += int(value)
        else:
            month_value[month] = int(value)
    return [month_value]
        



result = value_month("data/transaction.json")
print(result)

