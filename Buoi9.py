import requests
import json
import sys

# Đảm bảo terminal hiển thị được tiếng Việt
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# URL cơ sở của API JSONPlaceholder
BASE_URL = "https://jsonplaceholder.typicode.com"

def create_post():
    """1. Tạo một bài viết: POST /posts"""
    print("\n--- 1. Tạo một bài viết mới (POST) ---")
    new_data = {
        "title": "Học lập trình Python API",
        "body": "Đây là nội dung bài viết mới được tạo qua requests.",
        "userId": 1
    }
    # Gửi yêu cầu POST với dữ liệu dạng JSON
    response = requests.post(f"{BASE_URL}/posts", json=new_data)
    
    if response.status_code == 201: # 201 là Created
        print("Kết quả: Tạo thành công!")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    else:
        print(f"Lỗi: {response.status_code}")

def get_all_posts():
    """2. Lấy danh sách bài viết: GET /posts"""
    print("\n--- 2. Lấy danh sách bài viết (GET) ---")
    response = requests.get(f"{BASE_URL}/posts")
    
    if response.status_code == 200:
        posts = response.json()
        print(f"Kết quả: Lấy được {len(posts)} bài viết.")
        # Hiển thị thử 2 bài viết đầu tiên
        print(json.dumps(posts[:2], indent=4, ensure_ascii=False))
    else:
        print(f"Lỗi: {response.status_code}")

def get_post_detail(post_id):
    """3. Lấy chi tiết một bài viết: GET /posts/1"""
    print(f"\n--- 3. Lấy chi tiết bài viết ID {post_id} (GET) ---")
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    
    if response.status_code == 200:
        print("Kết quả:")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    else:
        print(f"Lỗi: {response.status_code} - Có thể ID không tồn tại")

def update_post(post_id):
    """4. Cập nhật một bài viết: PUT /posts/1"""
    print(f"\n--- 4. Cập nhật bài viết ID {post_id} (PUT) ---")
    update_data = {
        "id": post_id,
        "title": "Tiêu đề đã được sửa",
        "body": "Nội dung này đã được cập nhật thành công.",
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=update_data)
    
    if response.status_code == 200:
        print("Kết quả: Cập nhật thành công!")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    else:
        print(f"Lỗi: {response.status_code}")

def delete_post(post_id):
    """5. Xóa một bài viết: DELETE /posts/1"""
    print(f"\n--- 5. Xóa bài viết ID {post_id} (DELETE) ---")
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    
    if response.status_code == 200:
        print(f"Kết quả: Đã xóa bài viết {post_id} thành công!")
        # Lưu ý: JSONPlaceholder trả về object rỗng {} khi xóa thành công
        print(response.json())
    else:
        print(f"Lỗi: {response.status_code}")

if __name__ == "__main__":
    # Thực thi các chức năng theo yêu cầu
    create_post()       # 1. Tạo
    get_all_posts()     # 2. Lấy danh sách
    get_post_detail(1)  # 3. Lấy chi tiết ID 1
    update_post(1)      # 4. Cập nhật ID 1
    delete_post(1)      # 5. Xóa ID 1
