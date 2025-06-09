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

def revenue_per_month(filePath):
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
    statistical = [{k:v} for k, v in month_value.items()]
    return statistical

def expense_per_month(filePath_trans, filePath_base):
    with open(filePath_trans, "r", encoding= "utf-8") as f:
        data_cal = json.load(f)
    with open(filePath_base, "r", encoding="utf-8") as f:
        data_base= json.load(f)

    # Lấy giá tiền điện nước base
    base = data_base[0]
    base_price_electric = int(base["electric_base_price"])
    base_price_water = int(base["water_base_price"])

    # Lấy tháng và lấy số điện nước
    usage_value = {}
    for i in data_cal:
        month = i["time"].split("/")[0]
        usage_electric = int(i["number_electric"])
        usage_water = int(i["number_water"])
        cost = usage_electric * base_price_electric + usage_water * base_price_water

        if month in usage_value:
            usage_value[month] += cost
        else:
            usage_value[month] = cost
    result_usage_value = [{k:v} for k, v in usage_value.items()]
    return result_usage_value


