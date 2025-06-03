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




