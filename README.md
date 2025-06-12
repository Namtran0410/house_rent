# Tab 1: Overview 
- Title : Dashboard
- Biểu đồ thể hiện số người, số phòng, tình trạng phòng trống 
- Doanh thu qua các tháng
- Lợi nhuận qua từng tháng
- Biểu đồ thể hiện tiền điện, nước qua từng tháng
- Các tab khác

# Tab 2: Danh sách phòng, số người 
- Toplevel 1
- Title: Thống kê phòng và người 
- Nút thêm sửa xoá
- Treeview table thể hiện phòng, người (phòng 101 - tên người ở... )
- Đang học/ đi làm/ NA

# Tab 3: Giao dịch
- Toplevel 2
- Title: Giao dịch qua hàng tháng
- Nút thêm sửa xoá - popup toplevel hiện lên để lấy thông tin 
- Treeview table thể hiện thời gian, số phòng, số người, số điện, số nước, tiền dịch vụ, tổng thu, trạng thái(đã thanh toán/ chưa thanh toán, quá hạn)

# Tab 4: Doanh thu 
- topLevel 3
- Title: Doanh thu hàng tháng 
- Treeview thể hiện doanh thu theo thời gian, số phòng, số người, chi phí, lợi nhuận
|Tháng|-----|Chi phí ban đầu|-----|Chi phí thêm|-----|Doanh thu|-----|Lợi nhuận|-----|Tăng giảm|

- Tháng: Lấy tháng gần nhất có data
- Chi phí ban đầu = Tổng số điện * giá điện + Tổng số nước* giá nước + chi phí dịch vụ ban đầu
- Chi phí thêm = Sửa chữa, thay, mua mới, nếu có
- Doanh thu = số tiền thu được qua giao dịch - theo tháng và đã thanh toán
- Lợi nhuận = Doanh thu - chi phí 
- Tăng giảm so với tháng trước
- Tính toán doanh thu bonus thêm điện tổng, nước tổng, và phí dịch vụ, ngoài ra còn phụ phí 
    + Lấy điện tổng trừ đi điện đã dùng 
    + Lấy nước tổng, trừ đi nước đã dùng
    + Lấy tiền dịch vụ đã chi 
    => Tính tổng tiền chi + tiền phòng 
    + Doanh thu = điện * giá + nước* giá + tiền phòng + tiền dịch vụ 
    => Lợi nhuận = doanh thu - tổng tiền chi 

    Nếu lợi nhuận > giá phòng => doanh thu tăng 
    Nếu lợi nhuận < giá phòng => doanh thu giảm 
     
# Tab 5: Cài đặt
- topLevel 4
- Title: Cài đặt 
- Các entry để nhập thông số: 
    - Giá đầu tư ban đầu
    - Giá điện gốc 
    - Giá điện kinh doanh
    - Giá nước gốc
    - Giá nước kinh doanh
    - Giá dịch vụ kinh doanh -> Phải tính theo người
    - Nút lưu thông tin - lưu file dưới dạng json

# Tab 6: Thông tin
- topLevel 5
- Title: Doanh thu hàng tháng 
- Các label thể hiện thông tin liên lạc, hướng dẫn sử dụng