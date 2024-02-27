# GponAndBrasTool_Be

Ở dự án này, chúng tôi sử dụng fastapi để xây dựng một webserver có thể nhận các thay đổi thông số cấu hình thiết bị mạng từ client.

Sau đó tiến hành kết nối đến các thiết bị để thực hiện thay đổi các thông số đó.

Dự án sử dụng python 3.7.x

# Cài đặt và cấu hình

    - Tạo môi trường ảo bằng cách sử dụng lệnh: python -m venv venv
    - Di chuyển vào venv, đối với linux sử dụng source ./venv/bin/Activate. Đối với Windows ./venv/Scripts/Activate
    - Cài đặt các thư viện

# Khởi động dự án

    Sử dụng lệnh uvicorn index:app --reload dự án sẽ được khởi động.
