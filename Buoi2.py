# Một người gửi tiết kiệm với:
#  Số tiền ban đầu: 100,000,000 VND
#  Lãi suất: 5% / năm
#  Thời gian: 5 năm
# Tính:
# Tiền lãi sau 3 năm (lãi đơn)
# Tổng tiền nhận được
# Tiền lãi trung bình mỗi tháng
# Công thức lãi đơn: Lãi = Vốn × Lãi suất × Số năm

so_tien_goc = 100_000_000
lai_suat_nam = 0.05   
thoi_gian_gui = 5 

# 1. Tính tiền lãi sau 3 năm (lãi đơn)
# Công thức: Lãi = Vốn * Lãi suất * Số năm
thoi_gian_3_nam = 3
tien_lai_3_nam = so_tien_goc * lai_suat_nam * thoi_gian_3_nam

# 2. Tính tổng tiền nhận được sau 5 năm
# Tổng tiền = Gốc + (Gốc * Lãi suất * 5 năm)
tien_lai_5_nam = so_tien_goc * lai_suat_nam * thoi_gian_gui
tong_tien_nhan_duoc = so_tien_goc + tien_lai_5_nam

# 3. Tính tiền lãi trung bình mỗi tháng
# Tổng số tháng gửi là 5 năm * 12 tháng
tong_so_thang = thoi_gian_gui * 12
lai_trung_binh_thang = tien_lai_5_nam / tong_so_thang

print(f"1. Tiền lãi sau 3 năm: {tien_lai_3_nam:,.0f} VND")
print(f"2. Tổng tiền nhận được sau 5 năm: {tong_tien_nhan_duoc:,.0f} VND")
print(f"3. Tiền lãi trung bình mỗi tháng: {lai_trung_binh_thang:,.0f} VND")
    