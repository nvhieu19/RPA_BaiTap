# =============================================================
# BÀI TẬP RPA: TỰ ĐỘNG KIỂM TRA PHẠT NGUỘI & GỬI EMAIL
# Buổi 9 - Python + Selenium + SMTP Email
# =============================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import time
import sys
import os

# Fix encoding cho Windows console
sys.stdout.reconfigure(encoding='utf-8')

# ======================== CẤU HÌNH ========================

# Đường dẫn file Excel chứa danh sách biển số
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_BIEN_SO = os.path.join(BASE_DIR, "danh_sach_bien_so.xlsx")

# URL website tra cứu phạt nguội
URL = "https://www.phatnguoixe.com/"

# Cấu hình Email SMTP (Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_LOGIN = "trickerhiuml@gmail.com"
EMAIL_PASSWORD = "xxx-xxx-xxx-xxx"
SENDER_EMAIL = "trickerhiuml@gmail.com"
RECEIVER_EMAIL = "trickerhiuml@gmail.com"


# ======================== HÀM GỬI EMAIL ========================

def gui_email(bien_so, chi_tiet_vi_pham):
    """
    Gửi email cảnh báo phạt nguội qua Gmail SMTP.
    
    Args:
        bien_so: Biển số xe vi phạm
        chi_tiet_vi_pham: Danh sách các vi phạm (list of dict)
    """
    # Tạo nội dung email
    noi_dung = f"Biển số: {bien_so}\n"
    noi_dung += f"Trạng thái: Có vi phạm\n\n"
    noi_dung += "Chi tiết:\n"
    noi_dung += "=" * 50 + "\n"

    for i, vp in enumerate(chi_tiet_vi_pham, 1):
        noi_dung += f"\nVi phạm {i}:\n"
        noi_dung += f"  - Thời gian: {vp.get('thoi_gian', 'N/A')}\n"
        noi_dung += f"  - Địa điểm: {vp.get('dia_diem', 'N/A')}\n"
        noi_dung += f"  - Lỗi: {vp.get('loi', 'N/A')}\n"
        noi_dung += f"  - Trạng thái xử lý: {vp.get('trang_thai', 'N/A')}\n"
        noi_dung += "-" * 50 + "\n"

    # Tạo message email
    message = MIMEText(noi_dung, "plain", "utf-8")
    message["Subject"] = f"Cảnh báo phạt nguội - Biển số {bien_so}"
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL

    # Gửi email qua SMTP
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        print(f"  ✅ Đã gửi email cảnh báo cho biển số {bien_so}")
    except Exception as e:
        print(f"  ❌ Lỗi gửi email: {e}")


# ======================== HÀM ĐỌC FILE EXCEL ========================

def doc_danh_sach_bien_so(file_path):
    """
    Đọc danh sách biển số xe từ file Excel.
    
    Args:
        file_path: Đường dẫn file .xlsx
    Returns:
        Danh sách biển số (list)
    """
    df = pd.read_excel(file_path)
    # Lấy cột đầu tiên chứa biển số
    danh_sach = df.iloc[:, 0].astype(str).tolist()
    print(f"📋 Đã đọc {len(danh_sach)} biển số từ file {file_path}")
    for bs in danh_sach:
        print(f"   - {bs}")
    return danh_sach


# ======================== HÀM KIỂM TRA PHẠT NGUỘI ========================

def kiem_tra_phat_nguoi(driver, bien_so):
    """
    Kiểm tra phạt nguội cho 1 biển số xe trên website.
    
    Args:
        driver: Selenium WebDriver
        bien_so: Biển số xe cần tra cứu
    Returns:
        (co_vi_pham: bool, chi_tiet: list of dict)
    """
    wait = WebDriverWait(driver, 15)
    
    # Bước 1: Truy cập website
    driver.get(URL)
    time.sleep(2)

    # Bước 2: Chọn loại phương tiện - Ô tô (radio button đầu tiên)
    try:
        # Click vào radio button "Ô tô"
        oto_radio = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label.radio-inline"))
        )
        oto_radio.click()
        print(f"  ✔ Đã chọn loại phương tiện: Ô tô")
    except Exception as e:
        print(f"  ⚠ Không tìm thấy radio button Ô tô, thử cách khác...")
        try:
            radio_buttons = driver.find_elements(By.CSS_SELECTOR, "label.radio-inline")
            if radio_buttons:
                radio_buttons[0].click()
                print(f"  ✔ Đã chọn Ô tô (cách 2)")
        except:
            print(f"  ⚠ Bỏ qua chọn loại phương tiện")

    time.sleep(1)

    # Bước 3: Nhập biển số xe
    try:
        input_bien_so = wait.until(
            EC.presence_of_element_located((By.ID, "bienso96"))
        )
        input_bien_so.clear()
        # Đảm bảo xóa sạch ô input
        input_bien_so.send_keys(Keys.CONTROL, "a")
        input_bien_so.send_keys(Keys.BACKSPACE)
        input_bien_so.send_keys(bien_so)
        print(f"  ✔ Đã nhập biển số: {bien_so}")
    except Exception as e:
        print(f"  ❌ Không tìm thấy ô nhập biển số: {e}")
        return False, []

    time.sleep(1)

    # Bước 4: Click nút "KIỂM TRA PHẠT NGUỘI"
    try:
        btn_kiem_tra = wait.until(
            EC.element_to_be_clickable((By.ID, "submit99"))
        )
        btn_kiem_tra.click()
        print(f"  ✔ Đã click nút Kiểm tra phạt nguội")
    except Exception as e:
        print(f"  ❌ Không tìm thấy nút kiểm tra: {e}")
        return False, []

    # Chờ kết quả tải
    time.sleep(8)

    # Bước 5: Lấy kết quả
    try:
        page_source = driver.page_source

        # Kiểm tra nếu "Không tìm thấy vi phạm"
        if "Không tìm thấy vi phạm" in page_source or "Chúc mừng" in page_source:
            return False, []

        # Kiểm tra nếu có vi phạm - tìm bảng kết quả
        chi_tiet_vi_pham = []

        # Thử tìm bảng vi phạm (table)
        try:
            tables = driver.find_elements(By.TAG_NAME, "table")
            for table in tables:
                rows = table.find_elements(By.TAG_NAME, "tr")
                for row in rows[1:]:  # Bỏ qua header
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 3:
                        vi_pham = {
                            "thoi_gian": cols[0].text.strip() if len(cols) > 0 else "N/A",
                            "dia_diem": cols[1].text.strip() if len(cols) > 1 else "N/A",
                            "loi": cols[2].text.strip() if len(cols) > 2 else "N/A",
                            "trang_thai": cols[3].text.strip() if len(cols) > 3 else "N/A",
                        }
                        chi_tiet_vi_pham.append(vi_pham)
        except:
            pass

        # Thử tìm kết quả dạng div/list
        if not chi_tiet_vi_pham:
            try:
                result_elements = driver.find_elements(By.CSS_SELECTOR, ".violation-item, .result-item, .phat-nguoi-item")
                for elem in result_elements:
                    vi_pham = {
                        "thoi_gian": "Xem chi tiết trên website",
                        "dia_diem": "Xem chi tiết trên website",
                        "loi": elem.text.strip(),
                        "trang_thai": "Chưa xử lý",
                    }
                    chi_tiet_vi_pham.append(vi_pham)
            except:
                pass

        # Kiểm tra số lượng vi phạm từ text "Vi phạm: X"
        if not chi_tiet_vi_pham:
            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text
                if "Vi phạm:" in body_text:
                    # Tìm số vi phạm
                    import re
                    match = re.search(r"Vi phạm:\s*(\d+)", body_text)
                    if match and int(match.group(1)) > 0:
                        vi_pham = {
                            "thoi_gian": "Xem chi tiết trên website",
                            "dia_diem": "Xem chi tiết trên website",
                            "loi": f"Có {match.group(1)} vi phạm - Xem chi tiết tại {URL}",
                            "trang_thai": "Chưa xử lý",
                        }
                        chi_tiet_vi_pham.append(vi_pham)
            except:
                pass

        if chi_tiet_vi_pham:
            return True, chi_tiet_vi_pham
        else:
            return False, []

    except Exception as e:
        print(f"  ❌ Lỗi khi lấy kết quả: {e}")
        return False, []


# ======================== HÀM CHÍNH ========================

def main():
    print("=" * 60)
    print("  🚗 RPA BOT - KIỂM TRA PHẠT NGUỘI & GỬI EMAIL")
    print("=" * 60)
    print()

    # Bước 1: Đọc danh sách biển số từ file Excel
    try:
        danh_sach_bien_so = doc_danh_sach_bien_so(FILE_BIEN_SO)
    except Exception as e:
        print(f"❌ Lỗi đọc file Excel: {e}")
        return

    # Bước 2: Khởi tạo trình duyệt Edge
    print("\n🌐 Đang mở trình duyệt Edge...")
    driver = webdriver.Edge()
    driver.maximize_window()

    try:
        # Bước 3: Lặp qua từng biển số
        for i, bien_so in enumerate(danh_sach_bien_so, 1):
            print(f"\n{'─' * 50}")
            print(f"📌 [{i}/{len(danh_sach_bien_so)}] Đang kiểm tra biển số: {bien_so}")
            print(f"{'─' * 50}")

            # Kiểm tra phạt nguội
            co_vi_pham, chi_tiet = kiem_tra_phat_nguoi(driver, bien_so)

            # Bước 6: Xử lý logic
            if co_vi_pham:
                print(f"  🚨 Biển số {bien_so}: CÓ VI PHẠM!")
                print(f"  📧 Đang gửi email cảnh báo...")
                gui_email(bien_so, chi_tiet)
            else:
                print(f"  ✅ Biển số {bien_so}: Không có vi phạm")

            # Chờ giữa các lần tra cứu
            if i < len(danh_sach_bien_so):
                print(f"\n  ⏳ Chờ 3 giây trước khi tra cứu biển số tiếp theo...")
                time.sleep(3)

    except Exception as e:
        print(f"\n❌ Lỗi trong quá trình xử lý: {e}")

    finally:
        # Đóng trình duyệt
        print(f"\n{'=' * 60}")
        print("🏁 Hoàn tất kiểm tra tất cả biển số!")
        print(f"{'=' * 60}")
        time.sleep(3)
        driver.quit()
        print("🔒 Đã đóng trình duyệt.")


# ======================== CHẠY CHƯƠNG TRÌNH ========================

if __name__ == "__main__":
    main()
