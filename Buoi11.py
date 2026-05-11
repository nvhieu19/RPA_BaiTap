# =============================================================
# BÀI TẬP RPA: BOT MUA HÀNG TỰ ĐỘNG
# Buổi 11 - Python + Selenium + SMTP Email
# Website: https://www.automationexercise.com
# =============================================================

import time
import sys
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Fix encoding cho Windows console
sys.stdout.reconfigure(encoding='utf-8')

# ======================== CẤU HÌNH ========================

BASE_URL       = "https://www.automationexercise.com"
LOGIN_EMAIL    = "xxxxx"       # Email đăng ký tài khoản
LOGIN_PASSWORD = "xxxxx"

SMTP_SERVER    = "smtp.gmail.com"
SMTP_PORT      = 587
EMAIL_LOGIN    = "xxxxx"
EMAIL_PASSWORD = "xxxxx"     # App password từ pass app.txt
SENDER_EMAIL   = "xxxxx"
RECEIVER_EMAIL = "xxxxx"

SEARCH_KEYWORD = "shirt"

# Thông tin thanh toán giả
FAKE_CARD = {
    "name":  "Nguyen Van Hieu",
    "number": "4111111111111111",
    "cvc":    "123",
    "month":  "12",
    "year":   "2027",
}

# ======================== KHỞI TẠO DRIVER ========================

def tao_driver():
    """Khởi tạo trình duyệt Edge ở chế độ tối đa."""
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.implicitly_wait(5)
    return driver


def wait_click(driver, by, selector, timeout=15):
    """Chờ element clickable rồi click."""
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.3)
    el.click()
    return el


def wait_visible(driver, by, selector, timeout=15):
    """Chờ element hiện ra."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )


def dong_quang_cao(driver):
    """Đóng popup quảng cáo nếu có."""
    try:
        close_btn = driver.find_element(
            By.CSS_SELECTOR, "button.fc-button.fc-cta-consent, .modal-close, #dismiss-button"
        )
        close_btn.click()
        time.sleep(0.5)
    except Exception:
        pass


# ======================== BƯỚC 1: LOGIN ========================

def buoc_login(driver):
    """
    Đăng nhập vào tài khoản.
    Nếu login thất bại sẽ raise Exception.
    """
    print("\n🔐 [BƯỚC 1] Đăng nhập tài khoản...")
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)

    wait = WebDriverWait(driver, 15)

    # Điền email
    email_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-qa='login-email']"))
    )
    email_input.clear()
    email_input.send_keys(LOGIN_EMAIL)

    # Điền password
    pw_input = driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']")
    pw_input.clear()
    pw_input.send_keys(LOGIN_PASSWORD)

    # Click nút Login
    wait_click(driver, By.CSS_SELECTOR, "button[data-qa='login-button']")
    time.sleep(2)

    # Kiểm tra đăng nhập thành công
    if "login" in driver.current_url.lower():
        raise Exception("❌ Đăng nhập thất bại! Kiểm tra lại email/password.")

    print(f"  ✅ Đăng nhập thành công! URL: {driver.current_url}")


# ======================== BƯỚC 2-4: TÌM KIẾM SẢN PHẨM ========================

def buoc_tim_kiem(driver):
    """
    Truy cập trang Products và tìm kiếm từ khóa.
    Trả về danh sách sản phẩm (list of dict: name, price, element).
    """
    print(f"\n🔍 [BƯỚC 2-4] Tìm kiếm sản phẩm '{SEARCH_KEYWORD}'...")

    # Vào trang Products
    driver.get(f"{BASE_URL}/products")
    time.sleep(2)
    dong_quang_cao(driver)

    # Nhập từ khóa tìm kiếm
    search_box = wait_visible(driver, By.ID, "search_product")
    search_box.clear()
    search_box.send_keys(SEARCH_KEYWORD)

    # Click nút Search
    wait_click(driver, By.ID, "submit_search")
    time.sleep(2)

    print(f"  ✔ Đã tìm kiếm với từ khóa: '{SEARCH_KEYWORD}'")

    # Lấy danh sách sản phẩm trên trang đầu
    san_pham_list = lay_danh_sach_san_pham(driver)
    print(f"  📦 Tìm thấy {len(san_pham_list)} sản phẩm trên trang đầu")
    for sp in san_pham_list:
        print(f"     - {sp['name']} | Giá: Rs. {sp['price']}")

    return san_pham_list


def lay_danh_sach_san_pham(driver):
    """Lấy danh sách sản phẩm cùng giá từ trang hiện tại."""
    products = driver.find_elements(By.CSS_SELECTOR, ".productinfo.text-center")
    result = []
    for p in products:
        try:
            price_text = p.find_element(By.TAG_NAME, "h2").text.strip()   # "Rs. 500"
            name = p.find_element(By.TAG_NAME, "p").text.strip()
            price_num = int(re.sub(r"[^\d]", "", price_text))
            result.append({
                "name": name,
                "price": price_num,
                "element": p,
            })
        except Exception:
            continue
    return result


# ======================== BƯỚC 5-6: CHỌN & THÊM VÀO GIỎ ========================

def buoc_chon_va_them_gio(driver, san_pham_list):
    """
    Chọn sản phẩm rẻ nhất rồi thêm vào giỏ hàng.
    Trả về dict thông tin sản phẩm đã chọn.
    """
    print("\n🛒 [BƯỚC 5-6] Chọn sản phẩm rẻ nhất và thêm vào giỏ...")

    if not san_pham_list:
        raise Exception("❌ Không có sản phẩm nào để chọn!")

    # Sắp xếp theo giá tăng dần
    sorted_list = sorted(san_pham_list, key=lambda x: x["price"])
    chosen = sorted_list[0]
    print(f"  ✔ Chọn sản phẩm rẻ nhất: {chosen['name']} | Giá: Rs. {chosen['price']}")

    # Hover vào product card để hiện nút "Add to cart"
    card = chosen["element"]
    actions = ActionChains(driver)
    actions.move_to_element(card).perform()
    time.sleep(1)

    # Click nút "Add to cart" trong overlay
    try:
        add_btn = card.find_element(By.CSS_SELECTOR, ".add-to-cart")
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
        time.sleep(0.3)
        add_btn.click()
    except Exception:
        # Fallback: tìm nút add-to-cart gần với card
        add_btn = card.find_element(By.XPATH, ".//a[contains(@class,'add-to-cart')]")
        add_btn.click()

    time.sleep(1.5)
    print(f"  ✅ Đã thêm '{chosen['name']}' vào giỏ hàng!")

    # Đóng modal "Added!" nếu có - click "Continue Shopping"
    try:
        continue_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close-modal, .modal button"))
        )
        continue_btn.click()
        time.sleep(0.5)
    except Exception:
        pass

    return chosen


# ======================== BƯỚC 7: KIỂM TRA GIỎ HÀNG ========================

def buoc_kiem_tra_gio(driver, ten_san_pham):
    """
    Vào trang Cart và verify sản phẩm + số lượng = 1.
    """
    print("\n🛍️  [BƯỚC 7] Kiểm tra giỏ hàng...")
    driver.get(f"{BASE_URL}/view_cart")
    time.sleep(2)

    # Lấy tất cả row trong bảng giỏ hàng
    cart_rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    print(f"  📋 Số sản phẩm trong giỏ: {len(cart_rows)}")

    for row in cart_rows:
        try:
            name = row.find_element(By.CSS_SELECTOR, ".cart_description h4").text.strip()
            qty  = row.find_element(By.CSS_SELECTOR, ".cart_quantity button").text.strip()
            price= row.find_element(By.CSS_SELECTOR, ".cart_price p").text.strip()
            print(f"  🛒 {name} | Số lượng: {qty} | Giá: {price}")

            if qty == "1":
                print(f"  ✅ Verify OK - Số lượng = 1")
            else:
                print(f"  ⚠ Số lượng = {qty} (không phải 1)")
        except Exception:
            continue


# ======================== BƯỚC 8-9: CHECKOUT ========================

def buoc_checkout(driver):
    """Proceed to Checkout và điền comment."""
    print("\n📝 [BƯỚC 8-9] Proceed to Checkout...")

    # Click Proceed To Checkout
    wait_click(driver, By.CSS_SELECTOR, ".btn.btn-default.check_out")
    time.sleep(2)

    # Nếu hiện modal đăng nhập -> đã login rồi nên không cần xử lý
    # Kiểm tra xem có modal không
    try:
        modal_login = driver.find_element(By.CSS_SELECTOR, "#checkoutModal .modal-body a")
        modal_login.click()   # Click "Register / Login"
        time.sleep(1)
        buoc_login(driver)    # Login lại nếu cần
        driver.get(f"{BASE_URL}/view_cart")
        time.sleep(1)
        wait_click(driver, By.CSS_SELECTOR, ".btn.btn-default.check_out")
        time.sleep(2)
    except Exception:
        pass

    # Điền comment
    try:
        comment_box = driver.find_element(By.NAME, "message")
        comment_box.clear()
        comment_box.send_keys("Bot RPA - Đặt hàng tự động. Vui lòng giao hàng sớm!")
        print("  ✔ Đã điền comment đơn hàng")
    except Exception:
        print("  ⚠ Không tìm thấy ô comment, bỏ qua")

    # Click Place Order
    wait_click(driver, By.CSS_SELECTOR, "a.btn.btn-default.check_out")
    time.sleep(2)
    print("  ✅ Đã chuyển sang trang thanh toán")


# ======================== BƯỚC 10-11: THANH TOÁN ========================

def buoc_thanh_toan(driver):
    """Điền thông tin credit card giả và xác nhận thanh toán."""
    print("\n💳 [BƯỚC 10-11] Điền thông tin thanh toán...")

    wait = WebDriverWait(driver, 15)

    # Tên trên thẻ
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[data-qa='name-on-card']")
    )).send_keys(FAKE_CARD["name"])

    # Số thẻ
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='card-number']")\
          .send_keys(FAKE_CARD["number"])

    # CVC
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='cvc']")\
          .send_keys(FAKE_CARD["cvc"])

    # Tháng hết hạn
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='expiry-month']")\
          .send_keys(FAKE_CARD["month"])

    # Năm hết hạn
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='expiry-year']")\
          .send_keys(FAKE_CARD["year"])

    print(f"  ✔ Đã điền thông tin thẻ: **** **** **** {FAKE_CARD['number'][-4:]}")

    # Click Pay and Confirm Order
    wait_click(driver, By.CSS_SELECTOR, "button[data-qa='pay-button']")
    time.sleep(3)
    print("  ✅ Đã click xác nhận thanh toán!")


# ======================== BƯỚC 12: XÁC NHẬN ĐƠN HÀNG ========================

def buoc_xac_nhan(driver):
    """
    Kiểm tra thông báo đặt hàng thành công.
    Trả về (thanh_cong: bool, thong_bao: str).
    """
    print("\n✅ [BƯỚC 12] Xác nhận đặt hàng...")
    time.sleep(2)

    page_text = driver.find_element(By.TAG_NAME, "body").text

    # Các cụm từ xác nhận thành công
    success_keywords = [
        "Order Placed!", "Congratulations!", "Your order has been",
        "ORDER PLACED", "order has been confirmed"
    ]

    thanh_cong = any(kw.lower() in page_text.lower() for kw in success_keywords)

    if thanh_cong:
        print("  🎉 ĐẶT HÀNG THÀNH CÔNG!")
        # Lấy thông báo từ trang
        try:
            msg = driver.find_element(By.CSS_SELECTOR, "#success-message, .order-placed p, section p").text
        except Exception:
            msg = "Đặt hàng thành công!"
        return True, msg
    else:
        print("  ❌ Không tìm thấy thông báo thành công")
        print(f"  URL hiện tại: {driver.current_url}")
        return False, "Không xác định được trạng thái đơn hàng."


# ======================== BƯỚC 13: GỬI EMAIL ========================

def buoc_gui_email(san_pham, thanh_cong, thong_bao):
    """Gửi email xác nhận kết quả đặt hàng."""
    print("\n📧 [BƯỚC 13] Gửi email thông báo...")

    trang_thai = "✅ THÀNH CÔNG" if thanh_cong else "❌ THẤT BẠI"
    icon = "🎉" if thanh_cong else "⚠️"

    # Nội dung email HTML
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
        <div style="background: {'#28a745' if thanh_cong else '#dc3545'}; color: white;
                    padding: 20px; border-radius: 8px 8px 0 0; text-align: center;">
            <h1>{icon} BOT MUA HÀNG RPA</h1>
            <h2>Kết quả: {trang_thai}</h2>
        </div>
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 0 0 8px 8px;">
            <h3>📦 Thông tin đơn hàng:</h3>
            <table style="width:100%; border-collapse: collapse;">
                <tr style="background:#f8f9fa;">
                    <td style="padding:8px; border:1px solid #ddd;"><b>Sản phẩm</b></td>
                    <td style="padding:8px; border:1px solid #ddd;">{san_pham.get('name', 'N/A')}</td>
                </tr>
                <tr>
                    <td style="padding:8px; border:1px solid #ddd;"><b>Giá</b></td>
                    <td style="padding:8px; border:1px solid #ddd;">Rs. {san_pham.get('price', 'N/A')}</td>
                </tr>
                <tr style="background:#f8f9fa;">
                    <td style="padding:8px; border:1px solid #ddd;"><b>Từ khóa tìm kiếm</b></td>
                    <td style="padding:8px; border:1px solid #ddd;">{SEARCH_KEYWORD}</td>
                </tr>
                <tr>
                    <td style="padding:8px; border:1px solid #ddd;"><b>Website</b></td>
                    <td style="padding:8px; border:1px solid #ddd;">{BASE_URL}</td>
                </tr>
                <tr style="background:#f8f9fa;">
                    <td style="padding:8px; border:1px solid #ddd;"><b>Trạng thái</b></td>
                    <td style="padding:8px; border:1px solid #ddd;"><b>{trang_thai}</b></td>
                </tr>
            </table>
            <br>
            <p><b>Thông báo từ hệ thống:</b><br>{thong_bao}</p>
            <hr>
            <p style="color:#888; font-size:12px;">
                Email này được gửi tự động bởi RPA Bot - Buổi 11<br>
                Thời gian: {time.strftime('%d/%m/%Y %H:%M:%S')}
            </p>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{icon} [RPA Bot] Kết quả mua hàng - {trang_thai}"
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECEIVER_EMAIL
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print(f"  ✅ Email đã gửi đến: {RECEIVER_EMAIL}")
    except Exception as e:
        print(f"  ❌ Lỗi gửi email: {e}")


# ======================== HÀM CHÍNH ========================

def main():
    print("=" * 60)
    print("  🤖 RPA BOT - TỰ ĐỘNG MUA HÀNG")
    print(f"  🌐 Website: {BASE_URL}")
    print(f"  🔍 Từ khóa: '{SEARCH_KEYWORD}'")
    print("=" * 60)

    driver = tao_driver()
    san_pham_da_chon = {}
    thanh_cong = False
    thong_bao  = "Bot chưa hoàn thành quy trình."

    try:
        # ── BƯỚC 1: LOGIN ──────────────────────────────────────────
        buoc_login(driver)

        # ── BƯỚC 2-4: TÌM KIẾM ────────────────────────────────────
        san_pham_list = buoc_tim_kiem(driver)

        # ── BƯỚC 5-6: CHỌN & THÊM GIỎ ────────────────────────────
        san_pham_da_chon = buoc_chon_va_them_gio(driver, san_pham_list)

        # ── BƯỚC 7: KIỂM TRA GIỎ HÀNG ────────────────────────────
        buoc_kiem_tra_gio(driver, san_pham_da_chon["name"])

        # ── BƯỚC 8-9: CHECKOUT ────────────────────────────────────
        buoc_checkout(driver)

        # ── BƯỚC 10-11: THANH TOÁN ───────────────────────────────
        buoc_thanh_toan(driver)

        # ── BƯỚC 12: XÁC NHẬN ───────────────────────────────────
        thanh_cong, thong_bao = buoc_xac_nhan(driver)

    except Exception as e:
        thong_bao = f"Lỗi trong quá trình chạy bot: {e}"
        print(f"\n❌ LỖI: {e}")

    finally:
        # ── BƯỚC 13: GỬI EMAIL ───────────────────────────────────
        buoc_gui_email(san_pham_da_chon, thanh_cong, thong_bao)

        # Tổng kết
        print("\n" + "=" * 60)
        if thanh_cong:
            print("  🎉 BOT CHẠY THÀNH CÔNG - ĐÃ ĐẶT HÀNG!")
        else:
            print("  ⚠️  BOT KẾT THÚC - Kiểm tra lại kết quả")
        print("=" * 60)

        time.sleep(4)
        driver.quit()
        print("🔒 Đã đóng trình duyệt.")


# ======================== CHẠY CHƯƠNG TRÌNH ========================

if __name__ == "__main__":
    main()
