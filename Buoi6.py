class Account:
    def __init__(self, id, name, balance):
        self.id = id
        self.name = name
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def set_balance(self, value):
        self.__balance = value

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print("Nạp tiền thành công")
        else:
            print("Số tiền không hợp lệ")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Không đủ tiền để rút")
        else:
            self.__balance -= amount
            print("Rút tiền thành công")

    def display(self):
        print("ID:", self.id)
        print("Name:", self.name)
        print("Balance:", self.__balance)


# =========================

class SavingAccount(Account):
    def __init__(self, id, name, balance, interest_rate):
        super().__init__(id, name, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        return self.get_balance() * self.interest_rate

    def display(self):
        super().display()
        print("Interest rate:", self.interest_rate)
        print("Interest:", self.calculate_interest())


# =========================

class CheckingAccount(Account):
    def __init__(self, id, name, balance, overdraft):
        super().__init__(id, name, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if amount > self.get_balance() + self.overdraft:
            print("Vượt quá hạn mức rút tiền")
        else:
            new_balance = self.get_balance() - amount
            self.set_balance(new_balance)
            print("Rút tiền thành công")

    def display(self):
        super().display()
        print("Overdraft:", self.overdraft)


# =========================
# QUẢN LÝ DANH SÁCH

accounts = []

def find_account(id):
    for acc in accounts:
        if acc.id == id:
            return acc
    return None


# =========================
# MENU

while True:
    print("\n===== MENU =====")
    print("1. Tạo tài khoản")
    print("2. Nạp tiền")
    print("3. Rút tiền")
    print("4. Hiển thị tất cả")
    print("0. Thoát")

    choice = input("Chọn: ")

    if choice == "1":
        id = input("Nhập ID: ")
        name = input("Nhập tên: ")
        balance = float(input("Nhập số dư: "))

        print("1. Tài khoản tiết kiệm")
        print("2. Tài khoản thanh toán")
        type_acc = input("Chọn loại: ")

        if type_acc == "1":
            rate = float(input("Nhập lãi suất: "))
            acc = SavingAccount(id, name, balance, rate)
        else:
            overdraft = float(input("Nhập hạn mức: "))
            acc = CheckingAccount(id, name, balance, overdraft)

        accounts.append(acc)
        print("Tạo tài khoản thành công")

    elif choice == "2":
        id = input("Nhập ID: ")
        acc = find_account(id)

        if acc:
            amount = float(input("Nhập số tiền: "))
            acc.deposit(amount)
        else:
            print("Không tìm thấy")

    elif choice == "3":
        id = input("Nhập ID: ")
        acc = find_account(id)

        if acc:
            amount = float(input("Nhập số tiền: "))
            acc.withdraw(amount)
        else:
            print("Không tìm thấy")

    elif choice == "4":
        for acc in accounts:
            print("---------------")
            acc.display()

    elif choice == "0":
        break

    else:
        print("Lựa chọn không hợp lệ")