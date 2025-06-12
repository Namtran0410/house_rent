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
def change_string_to_float(string):
    string = string.replace(",", "")
    return float(string)
    
def change_to_string(string):
    # Tách thành 2 phần của chuỗi trước dấu . 
    convert_string = string.split(".")[0]
    convert_string = convert_string.replace(",", "")
    return convert_string

def revenue_per_month(filePath, filter_year):
    with open(filePath, "r", encoding = "utf-8") as f:
        data = json.load(f)
    month_value = {}
    for i in data:
        month = i["time"].split("/")[0]
        year = i["time"].split("/")[2]
        value = i["total_fee"]
        if year != filter_year:
            continue
        if month in month_value:
            month_value[month] += int(value)
        else:
            month_value[month] = int(value)
    statistical = [{k:v} for k, v in month_value.items()]
    return statistical

def consume_per_month(filePath, filter_year): 
    with open(filePath, "r", encoding= "utf-8") as f:
        data = json.load(f)

    # Lấy giá điện nước và tiền dịch vụ 
    with open('data/setting.json', "r", encoding= "utf-8") as f:
        business_data = json.load(f)
    price_electrics = int(business_data[0]['electric_business_price'])
    price_waters = int(business_data[0]['water_business_price'])

    month_value = {}
    for i in data: 
        month = i['time'].split("/")[0]
        year = i['time'].split("/")[-1]
        consume_electric = int(i['number_electric'])
        consume_water = int(i['number_water'])
        if year != filter_year:
            continue
        if month in month_value:
            month_value[month] +=consume_electric*price_electrics + consume_water*price_waters
        else: 
            month_value[month] = consume_electric*price_electrics + consume_water*price_waters
    statistical = [{k:v} for k, v in month_value.items()]
    return statistical

def expense_per_month(filePath_trans, filePath_base, year):
    with open(filePath_trans, "r", encoding="utf-8") as f:
        data_cal = json.load(f)
    with open(filePath_base, "r", encoding="utf-8") as f:
        data_base = json.load(f)

    base = data_base[0]
    base_price_electric = int(base["electric_base_price"])
    base_price_water = int(base["water_base_price"])

    usage_value = {}
    for i in data_cal:
        month = i["time"].split("/")[0]
        item_year = i["time"].split("/")[-1]
        if item_year != year:
            continue  # Bỏ qua nếu không đúng năm

        usage_electric = int(i["number_electric"])
        usage_water = int(i["number_water"])
        cost = usage_electric * base_price_electric + usage_water * base_price_water

        if month in usage_value:
            usage_value[month] += cost
        else:
            usage_value[month] = cost

    return [{k: v} for k, v in usage_value.items()]



