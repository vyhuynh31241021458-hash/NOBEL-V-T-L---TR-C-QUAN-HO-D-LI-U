# Task 1 — Làm sạch dữ liệu khảo sát siêu thị

- Nguồn dữ liệu: survey_398 (1).csv
- Số mẫu sau khi làm sạch: 398
- Số mã sản phẩm duy nhất: 398
- Số mẫu cần xác minh: 14
- Số mẫu thiếu giờ: 0

## Số mẫu theo điểm khảo sát

- AEON Bình Tân: 175
- AEON Tạ Quang Bửu: 13
- GO! An Lạc: 175
- GO! Tô Hiến Thành: 35

## Quy tắc xử lý

- Dùng record_id làm khóa đối chiếu.
- Chuẩn hóa giá về số VND, ngày về YYYY-MM-DD và giờ về HH:MM.
- Chuẩn hóa tên quốc gia và giữ dữ liệu gốc để đối chiếu.
- Chuẩn hóa giờ ghi trong CSV về HH:MM. Ô giờ thiếu được giữ trống.
- Xem t01_issues_log.csv để đối chiếu từng mã.
