
#1: Nhập vào họ tên, tuổi, điểm trung bình và in ra màn hình
print("\n1: Thông tin sinh viên")
ho_ten = input("Nhập họ tên: ")
tuoi = int(input("Nhập tuổi: "))
diem_tb = float(input("Nhập điểm trung bình: "))

print("\nKết quả")
print(f"Họ tên: {ho_ten}")
print(f"Tuổi: {tuoi}")
print(f"Điểm trung bình: {diem_tb}")
#2: Tính diện tích và chu vi hình chữ nhậ
print("\n2: Diện tích và chu vi hình chữ nhật ===")
dai = float(input("Nhập chiều dài hình chữ nhật: "))
rong = float(input("Nhập chiều rộng hình chữ nhật: "))

dien_tich = dai * rong
chu_vi = 2 * (dai + rong)

print("\nKết quả")
print(f"Chiều dài: {dai}")
print(f"Chiều rộng: {rong}")
print(f"Diện tích: {dien_tich}")
print(f"Chu vi: {chu_vi}")

#3: Chuyển đổi nhiệt độ từ C sang F
print("\n3: Chuyển đổi nhiệt độ")
celsius = float(input("Nhập nhiệt độ Celsius: "))
fahrenheit = (celsius * 9/5) + 32

print("\nKết quả chuyển đổi")
print(f"Celsius: {celsius}°C")
print(f"Fahrenheit: {fahrenheit}°F")



#4: Kiểm tra số chẵn hay lẻ

print("\n4: Kiểm tra số chẵn hay lẻ")
so_nguyen = int(input("Nhập một số nguyên: "))

if so_nguyen % 2 == 0:
    print(f"\n{so_nguyen} là số CHẴN")
else:
    print(f"\n{so_nguyen} là số LẺ")

#5: Tính tổng, hiệu, thương của hai số thực
print("\n=== BÀI 5: Tính tổng, hiệu, thương ===")
so_1 = float(input("Nhập số thực thứ nhất: "))
so_2 = float(input("Nhập số thực thứ hai: "))

tong = so_1 + so_2
hieu = so_1 - so_2
thuong = so_1 / so_2 if so_2 != 0 else "Không thể chia cho 0"

print("\nKết quả")
print(f"Số thứ nhất: {so_1}")
print(f"Số thứ hai: {so_2}")
print(f"Tổng: {tong}")
print(f"Hiệu: {hieu}")
print(f"Thương: {thuong}")
