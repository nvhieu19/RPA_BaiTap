import pandas as pd
import numpy as np

# 1. Tạo bảng dữ liệu Sinh Viên (có null)
data = {
    "MaSV": ["SV01","SV02","SV03","SV04","SV05","SV06","SV07","SV08","SV09","SV10"],
    "HoTen": ["An","Bình","Chi","Dũng","Em","Phúc","Giang","Hà","Khánh","Long"],
    "Lop": ["CNTT1","CNTT1","CNTT2","CNTT2","CNTT1","CNTT3","CNTT3","CNTT2","CNTT1","CNTT3"],
    "DiemPython": [8, 7, None, 9, 6, 5, None, 7, 8, 6],
    "DiemWeb": [7, None, 6, 8, 5, 6, 7, None, 9, 8],
    "DiemDatabase": [8, 7, 5, None, 6, 7, 8, 6, None, 7]
}

df = pd.DataFrame(data)

# 2. Đọc file + kiểm tra null
df = pd.read_csv("sinhvien.csv")

print("👉 Dữ liệu null:")
print(df.isnull().sum())

# 3. Điền null = 0
df.fillna(0, inplace=True)

# 4. Tạo cột Điểm TB
df["DiemTB"] = (df["DiemPython"] + df["DiemWeb"] + df["DiemDatabase"]) / 3

# 5. Xếp loại
def xep_loai(diem):
    if diem >= 8:
        return "Giỏi"
    elif diem >= 6.5:
        return "Khá"
    elif diem >= 5:
        return "Trung bình"
    else:
        return "Yếu"

df["XepLoai"] = df["DiemTB"].apply(xep_loai)

print("\n👉 Bảng sau xử lý:")
print(df)

# 6. Thống kê theo lớp
print("\n👉 Số lượng sinh viên mỗi lớp:")
print(df["Lop"].value_counts())

# 7. Điểm TB mỗi lớp
print("\n👉 Điểm TB trung bình mỗi lớp:")
print(df.groupby("Lop")["DiemTB"].mean())

# 8. Tạo bảng Thông Tin Lớp
lop_data = {
    "Lop": ["CNTT1","CNTT2","CNTT3"],
    "GiaoVien": ["Thầy A","Cô B","Thầy C"],
    "PhongHoc": ["P101","P102","P103"]
}

df_lop = pd.DataFrame(lop_data)

# 9. Ghép bảng
df_merged = pd.merge(df, df_lop, on="Lop")

print("\n👉 Bảng sau khi ghép:")
print(df_merged)