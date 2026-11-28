# T23 / C09 — Bàn giao heatmap tăng trưởng đối tác

- Người thực hiện: Vân; người CHECK theo phân công: Ngọc (chờ rà soát).
- Nhánh làm việc: `t23-van-20261128`, dựa trên main `c9d2e17`.
- Notebook: `notebooks/multivariate/C09_heatmap.ipynb`.
- Hình xuất: `outputs/multivariate/C09_heatmap.png` và `.svg`.
- Bảng kiểm toán: `outputs/multivariate/C09_growth_audit.csv` (400 dòng, gồm 20 dòng năm gốc); bảng thứ hạng: `C09_partner_ranking.csv`.

## Phạm vi và quyết định

Top 20 theo tổng xuất khẩu + nhập khẩu quan sát trong 2005–2024; xếp giảm dần theo cùng tiêu chí. Hình có 20 hàng × 19 năm (2006–2024). Tăng trưởng tính với năm liền trước, chỉ khi đủ cả Export và Import ở hai năm và năm trước > 0. Không nội suy, không điền 0. Không thay đổi nguồn dữ liệu sạch.

Thang màu House Style RdBu có tâm 0, cố định ±100%. Đỏ giảm, xanh tăng; dấu và nhãn số giúp đọc hướng mà không chỉ dựa màu. Nhãn làm tròn số nguyên; bảng kiểm toán giữ giá trị đầy đủ và cờ color_clipped. Chỉ màu bị bão hòa ở ba ô vượt +100%, không cắt giá trị hay nhãn số. Ô thiếu dùng màu MISSING_COLOR và dấu —.

Một ô thiếu trong hình: ARE năm 2024. Ba ô vượt +100%: HKG 2024 (+107.7334%), SGP 2024 (+111.2050%), ARE 2017 (+197.5820%). Năm 2009 có 17/20 đối tác giảm; 2020 có 13/20, 2023 có 12/20.

## Cách chạy

Cài thư viện theo requirements.txt, mở notebook từ trong repository, chọn Python kernel và Restart and Run All. Không cần dữ liệu BACI raw; notebook đọc partner_year.csv đã sạch. Các tham số năm, số đối tác, chiều và ngưỡng màu ở ô chạy. Nếu đổi tham số cần cập nhật phần nhận xét mặc định ở cuối.

## Kiểm tra đã thực hiện

- Thực thi tuần tự cả ba ô code trong một tiến trình Python/IPython mới, không lỗi.
- Đối chiếu độc lập 380 ô với các dòng gốc năm t và t−1; bảng đầu vào không bị sửa.
- Kiểm tra dữ liệu giả định: năm khuyết không nối qua năm, thiếu một chiều không tính tổng thiếu thành tổng đủ, năm gốc bằng 0 cho kết quả thiếu, giảm thật về 0 cho −100%.
- Khóa trùng, số âm và vô hạn bị từ chối; kiểm tra cả tùy chọn Export và Import.
- Ảnh PNG nhúng notebook trùng byte với PNG xuất; kiểm tra PNG/SVG và bố cục bằng mắt.

## Bước tiếp theo

Ngọc đọc và CHECK độc lập. Sau khi duyệt, người tổng hợp ghép C08, C09, C10 vào 04_multivariate.ipynb. Task này chưa sửa notebook tổng, House Style hay bảng dữ liệu sạch và chưa cập nhật DONE trong Sheet.
