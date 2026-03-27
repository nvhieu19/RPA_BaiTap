import math

def bai1():
    a = float(input("Nhập a: "))
    b = float(input("Nhập b: "))
    c = float(input("Nhập c: "))
    delta = b**2 - 4*a*c
    if delta > 0:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        print("Phương trình có hai nghiệm phân biệt:", x1, x2)
    elif delta == 0:
        x = -b / (2*a)
        print("Phương trình có nghiệm kép:", x)
    else:
        print("Phương trình vô nghiệm trong tập số thực")

def bai2():
    for i in range(2, 10):
        print(f"Bảng cửu chương {i}:")
        for j in range(1, 11):
            print(f"{i} x {j} = {i*j}")
        print("_________________________________")

def bai3():
    print("Tổng các số chẵn từ 1 đến 100 là:", sum(range(2, 101, 2)))

def bai4():
    num = int(input("Nhập số nguyên: "))
    if num < 2:
        print(num, "không phải số nguyên tố")
        return
    for i in range(2, int(math.sqrt(num))+1):
        if num % i == 0:
            print(num, "không phải số nguyên tố")
            return
    print(num, "là số nguyên tố")

def bai5():
    n_triangle = int(input("Nhập chiều cao tam giác: "))
    print("Tam giác cân:")
    for i in range(1, n_triangle+1):
        print(' '*(n_triangle-i)+'*'*(2*i-1))

def bai6():
    a = int(input("Nhập số a: "))
    b = int(input("Nhập số b: "))
    if a == 0 or b == 0:
        print("Không thể tính BCNN khi có số 0")
        return
    def ucln(x,y):
        while y!=0:
            x,y = y, x%y
        return x
    def bcnn(x,y):
        return x*y//ucln(x,y)
    print("UCLN:", ucln(a,b))
    print("BCNN:", bcnn(a,b))

def bai7():
    num_digit = abs(int(input("Nhập số nguyên: ")))
    count = 1 if num_digit==0 else 0
    while num_digit>0:
        num_digit//=10
        count+=1
    print("Số chữ số là:", count)

while True:
    print("1. Viết chương trình giải phương trình bậc 2")
    print("2. Viết chương trình in ra bảng cửu chương từ 2 đến 9")
    print("3. Tính tổng các số chẵn từ 1 đến 100")
    print("4. Viết chương trình kiểm tra số nguyên tố")
    print("5. In ra hình tam giác so với chiều cao n")
    print("6. Viết chương trình tìm ƯCLN và BCNN của hai số")
    print("7. Viết chương trình đếm số lượng chữ số của một số nguyên")
    print("0. Thoát chương trình")
    print("_________________________________________________________________")
    choice = int(input())
    if choice==0:
        break
    elif choice==1: bai1()
    elif choice==2: bai2()
    elif choice==3: bai3()
    elif choice==4: bai4()
    elif choice==5: bai5()
    elif choice==6: bai6()
    elif choice==7: bai7()
    else:
        print("Chọn sai, nhập lại")