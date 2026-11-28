# T17 – So sánh hai công cụ: Python và Excel

**Khách hàng giả định:** VietTrade Insight Unit – đơn vị xúc tiến thương mại; nhóm đảm nhận vai trò chuyên viên phân tích cấp cao.

**Phạm vi:** dashboard thương mại hàng hóa Việt Nam 2005–2024 (T15 bằng Python/matplotlib, T16 bằng Excel).

## 1. Điều gì dễ hơn
- **Python:** tính toán và kiểm soát. Lọc đối tác hợp lệ, tính HHI từ toàn bộ đối tác, vẽ dumbbell, áp House Style (font, họa tiết), và chạy lại toàn bộ bằng Run All kèm `assert` đối chiếu.
- **Excel:** nhập CSV và chỉnh tay nhanh. Biểu đồ cột/đường dựng sẵn, công thức nhìn thấy ngay, người không biết lập trình mở là dùng được.

## 2. Điều gì không làm được
- **Python:** không có người dùng cuối sửa trực tiếp; không có link chia sẻ sẵn; kết quả là ảnh/PDF tĩnh, không lọc tương tác.
- **Excel:** không có dumbbell (thay bằng cột ngang, mất đường nối và nhãn pp trên hình); không dùng được font và họa tiết House Style. Bản T16 **không tính lại HHI**: HHI nhập từ CSV, vì Excel chỉ nhận bảng đã xử lý (6 đối tác hàng đầu), không có đủ đối tác để tính bình phương tỷ trọng. Việc lọc đối tác hợp lệ và tính tỷ trọng vẫn nằm ở Python.

## 3. Bàn giao cho VietTrade Insight Unit
Nhóm là bên phân tích, còn đơn vị xúc tiến thương mại là bên dùng và cập nhật hằng kỳ, nên tiêu chí chọn là người nhận tự vận hành được mà không cần nhóm. Nhu cầu lấy từ Cây câu hỏi P03 và tổng hợp phỏng vấn:
- **Có cần lọc: có.** Explorer cho chọn chương HS, khoảng năm, chiều xuất/nhập; HHI tính lại từ toàn bộ đối tác trong phạm vi lọc. Python hiện chỉ cho ảnh tĩnh; Excel lọc được bằng PivotTable/slicer nhưng bản T16 mới nhận 6 đối tác đã xử lý, chưa đủ dữ liệu cho Explorer.
- **Có cần chia sẻ link: có**, vì người xem gồm bộ, ngành, doanh nghiệp xuất khẩu và công chúng. Excel đưa lên OneDrive/Google Drive để lấy link; Python không có.
- **Ai cập nhật dữ liệu:** Nhân viên đơn vị không lập trình → Excel; nếu có người biết Python → giữ Python.

**Đề xuất:** bàn giao **Excel** làm công cụ khách tự xem và cập nhật, kèm CSV và notebook Python làm nguồn tính chuẩn (lọc đối tác hợp lệ, HHI). Để Excel đáp ứng Explorer, cần nạp dữ liệu đối tác theo chương HS đầy đủ và dựng PivotTable/slicer; việc này chưa làm trong T16.

## Bảng đối chiếu (cùng dữ liệu, cùng cách tính)
| Chỉ tiêu | Python (T15) | Excel (T16) | Lệch |
|---|---|---|---|
| Xuất khẩu 2024 (tỷ USD) | 505.2 | 505.2 | 0 |
| Cán cân 2024 (tỷ USD) | +128.4 | +128.4 | 0 |
| Tỷ trọng phần XVI trong xuất khẩu 2005 → 2024 (%) | 9.4 → 54.9 | 9.4 → 54.9 | 0 |
| Tỷ trọng Trung Quốc trong nhập khẩu 2024 (%) | 43.8 | 43.8 | 0 |
| HHI nhập khẩu 2024 (điểm) | 2,298 | 2,298 | 0 |

*Nguồn đối chiếu: sheet `doi_chieu` trong `t16_dashboard_excel.xlsx` (15/15 chỉ tiêu khớp `02_core_charts`).*
