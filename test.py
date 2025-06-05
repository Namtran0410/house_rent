
# Viết code tính tổng các số chẵn trong danh sách này.
numbers = [1, 4, 6, 7, 8, 3, 10]
sum = 0
for i in numbers:
    sum+=i

# Tìm số lớn thứ hai trong danh sách.
numbers = [10, 20, 4, 45, 99]
first = numbers[0]
indexs = 0
for index, i in enumerate(numbers):
    if i > first:
        first = i
        indexs= index

numbers.pop(indexs)
second = numbers[0]
for i in numbers:
    if i > second:
        second = i

# Tạo dict lưu số lần xuất hiện của từng ký tự trong text.
text = "hello world"
text = text.replace(" ", "")
result = []
dict_result = {}
for i in text:
    result.append(i)

for i in result:
    if i not in dict_result:
        dict_result[i] =1
    else:
        dict_result[i] += 1


# Tìm tên người có điểm cao nhất.
scores = {'Alice': 90, 'Bob': 85, 'Charlie': 95}
s_max = scores['Alice']
h = ""
for name, s in scores.items():
    if s > s_max:
        s_max = s
        h = name

print(h, s_max)


    





