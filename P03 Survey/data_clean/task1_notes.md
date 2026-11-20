# Task 1 – Ghi chú lỗi phát hiện và cách xử lý

**Dữ liệu:** 350 sản phẩm (175 AEON Bình Tân + 175 GO! An Lạc), khảo sát ngày 12/11/2026.
**Số dòng trước xử lý: 350 – sau xử lý: 350** (không có dòng trùng hoàn toàn, không xóa dòng nào).
Mã sản phẩm có sẵn (AEON_001…, GO_001…) đầy đủ và không trùng nên được giữ nguyên làm `record_id`.
Các cột gốc được giữ lại để đối chiếu (`price_raw`, `origin_raw`, `spec_raw`, `date_raw`, `time_raw`, `brand_raw`, `source_row`).

## 1. Đã sửa tự động bằng code
| Lỗi | Số dòng | Cách xử lý |
|---|---|---|
| Giá viết cách bằng dấu cách ("319 000") | 70 | Đổi thành số nguyên VNĐ |
| Xuất xứ viết không thống nhất (VN, TQ, TL, Hàn, Singapor, China, Cambodia, hoa/thường, sai chính tả…) | 73 | Gom về một tên chuẩn (Việt Nam, Trung Quốc…) |
| Nhãn ghi gộp "xuất xứ thương hiệu X, sản xuất tại Y" | 5 | Tách: `origin_country` = nơi sản xuất (Y), `brand_origin` = X |
| Giờ viết dạng "9h10", "9h6", "10n15" | 61 | Đổi thành HH:MM |
| Thương hiệu viết hoa/thường khác nhau (Giorno Mimosa, Purité de Provence, Thiên Long) | 7 | Thống nhất theo dạng xuất hiện nhiều nhất |
| Ngày "12/11/2026" | 350 | Đổi thành 2026-11-12 |

Quy ước: `origin_country` là **nơi sản xuất (Made in)**, không phải nước của thương hiệu.

## 2. Đã xác minh với ảnh nhãn và sửa tay (2 dòng)
Người kiểm tra: [Ngọc], ngày [20/11/2026]. Các giá trị gốc vẫn còn ghi lại ở đây để đối chiếu.
| record_id | Giá trị gốc | Sau khi kiểm tra | Lý do |
|---|---|---|---|
| GO_175 | Giá "233 00" (sai định dạng, không rõ 23.300 hay 233.000) | **233.000 VNĐ** | Đối chiếu ảnh nhãn giá |
| GO_060 | Thương hiệu để trống | **WM** | Đối chiếu ảnh nhãn |

## 3. Đã kiểm tra, giữ nguyên (9 dòng vẫn mang cờ "Cần xác minh" trong file)
Code đánh dấu các dòng này theo quy tắc nên cờ vẫn hiện, nhưng nhóm đã kiểm tra và quyết định như sau:
| record_id | Vấn đề | Quyết định |
|---|---|---|
| GO_147 | Nhãn ghi "Xuất xứ VN cấp phép TL" | Ghi **Việt Nam** theo chữ "Xuất xứ VN"; Thái Lan chỉ là bên cấp phép thương hiệu, không phải nơi sản xuất |
| AEON_026, 112, 113, 114, 116, 118, 119, 123 | Giá cao hơn 10 lần giá giữa của cả bảng (89.000đ) | Đã đối chiếu ảnh giá, **không đổi giá**. Giá đúng vì là đồ điện tử / mỹ phẩm cao cấp |

## 4. Ghi chú khác
- 8 sản phẩm thiếu "Thông tin chi tiết" (dây nịt, nón, dép, tất, dây sạc) là GO_040, 041, 044, 046, 047, 056, 057, 070 và 2 sản phẩm thiếu giờ khảo sát: không bắt buộc, để trống.
- Cột "Thông tin chi tiết" gồm nhiều loại: 213 dòng có dung tích/khối lượng (đã tách `spec_value`, `spec_unit`), 41 dòng là size, 88 dòng là mô tả khác (chất liệu, kích thước…). Dòng ghi hai đơn vị (vd "3,8 kg; 3,84 L") chỉ tách đơn vị đầu tiên; chuỗi gốc vẫn còn ở `spec_text`.
- Bảng chưa có cột ngành hàng nên chưa kiểm tra giá bất thường theo từng ngành (sẽ làm ở Task 4).
- Lưu ý khi tải CSV từ Google Sheet: Sheet có thể tự đổi giá "7.000" thành số 7. Luôn kiểm tra cột giá trước khi chạy code.
