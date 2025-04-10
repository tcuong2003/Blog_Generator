============================
README - Hướng dẫn chạy dự án
============================

Tên dự án: Ứng dụng AI chuyển đổi link video thành bài viết blog

Mô tả:
--------
Dự án này là một hệ thống web được xây dựng bằng Django, sử dụng AI để trích xuất nội dung từ link video và chuyển thành bài viết blog tự động. 
Hệ thống hỗ trợ người dùng đăng ký, đăng nhập, nhập link video, tạo blog, chỉnh sửa và lưu trữ bài viết.

Yêu cầu môi trường:
---------------------
- Python 3.9+
- Django 4.2+
- PostgreSQL
- Git (nếu clone từ GitHub)

Cài đặt và chạy: (mở terminal trong dự án và cd đến dự án)
------------------

1. Tạo virtual environment (venv) và chạy máy ảo đó:
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

2. Cài đặt các thư viện: chạy lệnh "pip install -r requirements.txt" để cài các thư viện cần thiết của án được gói trong requirements.txt


3. Tạo cơ sở dữ liệu PostgreSQL:
- Tạo database mới với tên là "blog", password là "20031101" hoặc bạn có thể chỉnh sửa bên trong dự án để phù hợp 
(BLOG_AI > settings.py(dòng 94 - 103))

4. Thực hiện các lệnh sau:
- python manage.py makemigrations 
- python manage.py migrate

5. Chạy server:
- python manage.py runserver

6. Truy cập website:
- Trình duyệt: http://127.0.0.1:8000/

7. Tạo tài khoản 
- user nếu bạn chưa có (tạo tài khoản trên giao diện signup)
- admin thì bạn hãy chạy lệnh python manage.py createsuperuser rồi nhập các thông tin được yêu cầu



Cấu trúc chính:
-------------------
- `blog_generator/`: xử lý chuyển video thành blog bằng AI
- `user/`: quản lý đăng ký, đăng nhập
- `blog/`: quản lý bài viết đã được tạo
- `media/`: nơi lưu trữ cái file audio

Tác giả: TRẦN CƯỜNG
Năm thực hiện: 2025





