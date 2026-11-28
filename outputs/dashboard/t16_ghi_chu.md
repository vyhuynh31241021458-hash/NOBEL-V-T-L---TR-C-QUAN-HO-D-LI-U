# T16 – Dựng lại bằng Excel: ghi chú cho T17

**Công cụ:** Microsoft Excel 
**Dữ liệu:** 7 CSV từ T15 nhập vào các sheet cùng tên; chữ xanh = dữ liệu nhập, xanh lá = liên kết sheet, đen = công thức.

## Đã dựng
- C01A xu hướng XK/NK (đường liền chấm tròn / nét đứt chấm vuông, #22577A / #B86E24)
- C04A, C04B thay đổi tỷ trọng đối tác (2005 viền trắng, 2024 tô đặc)
- C02A cơ cấu xuất khẩu theo phần HS (cột chồng 100%, màu theo mã HS của House Style, sheet `c02a_wide` lấy tỷ trọng bằng SUMIFS)
- C05A HHI (có nhãn đầu/cuối đường) + dòng giải thích; 4 thẻ KPI 2024 (công thức liên kết sheet `kpi_2024`)

## Đối chiếu (sheet `doi_chieu`)
- 15/15 chỉ tiêu (gồm C02A XVI và Khác 2005/2024; tổng mỗi năm = 100%) khớp Python và `02_core_charts`; lệch Excel − Python = 0.
- Thay đổi tỷ trọng tính lại bằng công thức `2024 − 2005` từng đối tác, khớp cột `doi_pp` của Python. Không cộng tỷ trọng.
- Tỷ USD tính lại từ `trade_year_raw`: lệch tối đa 0; cán cân = XK − NK đúng cả 20 năm.

## Thuận lợi
- Nhập CSV nhanh; công thức INDEX/MATCH cho đối chiếu và KPI tự cập nhật khi đổi dữ liệu.
- Biểu đồ cột/đường dựng sẵn, dễ sửa tay.

## Khó khăn
- Không có biểu đồ dumbbell: thay bằng cột ngang 2005 vs 2024; mất đường nối và nhãn thay đổi (pp) nằm trong bảng, không nằm trên biểu đồ.
- Không dùng được font Bricolage/Platypi và họa tiết HS của House Style; dùng Arial.
- Nhãn đầu/cuối đường phải gắn từng điểm một (C01A, C05A); nhãn phần HS dưới 8.5% chỉ ẩn được bằng định dạng có điều kiện, bản chụp LibreOffice vẫn hiện các nhãn nhỏ.
- Cột chồng không có họa tiết nét chéo như House Style; phân biệt bằng màu và thứ tự.
- Nhãn trục năm hiển thị dày hơn bản Python (xem trên Excel thật có thể khác bản chụp).
- Bản chụp được xuất qua LibreOffice, chưa xem trên Excel thật.
