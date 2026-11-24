# P03 Survey — Hoàn thành Task 4

Task 4 phân loại 398 bản ghi khảo sát theo danh mục sản phẩm và xếp mức giá tương đối trong từng nhóm so sánh.

## File và cách chạy

| File | Nội dung |
|---|---|
| `data_clean/t04_survey_segment_all.csv` | Kết quả Task 4. Giữ các cột và thứ tự bản ghi từ Task 1, thêm 10 cột phân tích. |
| `data_clean/survey_segment_final.csv` | 306 dòng đã được xếp Thấp, Trung bình hoặc Cao. |
| `data_clean/survey_segment_unclassified.csv` | 92 dòng chưa xếp được mức giá, kèm lý do từng dòng. |
| `scripts/t04_category_price.py` | Code Python 3 dùng thư viện chuẩn. |
| `notes/t04_notes.md` | Quy tắc xử lý, kết quả và ví dụ tính giá. |

Chạy tại thư mục đã giải nén. Thay đường dẫn đầu vào bằng vị trí thực tế của file Task 1.

```bash
python scripts/t04_category_price.py data_clean/t01_survey_clean.csv data_clean/t04_survey_segment_all.csv
```

## Phân loại sản phẩm và chuẩn hóa giá

- Rà tên sản phẩm theo `record_id` và ghi lại ánh xạ trong code. Bộ này có 85 danh mục, bao gồm các nhóm nhỏ như bút bi, bút gel, tai nghe không dây và nước rửa chén. Khi thêm mã mới, cập nhật bảng ánh xạ. Nếu mã cũ được dùng lại cho sản phẩm khác, cần rà lại danh mục của mã đó.
- Tôm được tách riêng. Mực, bào ngư và sò điệp của bộ này thuộc Hải sản. Cá đông lạnh chưa chế biến có danh mục riêng với cá một nắng và cá chế biến.
- Quy giá về VNĐ/100 g hoặc VNĐ/100 ml với hàng có khối lượng hoặc dung tích. Công thức là giá quan sát × 100 ÷ tổng số g hoặc ml trong quy cách bán. Quy đổi kg và lít sang g và ml trước khi tính. Code cũng nhận dạng mô tả lít rõ ràng như `1 lit`.
- Với bút đóng gói, tất và viên giặt, chia theo số đơn vị đếm được. Với quần áo, đồ chơi và thiết bị, dùng giá trên một đơn vị bán theo quy cách ghi nhận. Một bộ đồ chơi được tính là một đơn vị bán.
- Đối chiếu `t01_notes.md` và `t01_issues_log.csv` với cột `verify_fields`. Giá hoặc quy cách cần xác minh được loại khỏi tập tính ngưỡng. Cờ xuất xứ được giữ trong các cột gốc và dòng vẫn có thể xếp giá nếu giá và quy cách hợp lệ. Hai dòng GO_017 và GO_071 có tổng khối lượng bán chưa rõ, nên để trống giá quy đổi.

## Tính mức giá

Tính chung ngưỡng cho bốn điểm khảo sát theo **danh mục × đơn vị so sánh**. Mỗi nhóm dùng giá quy đổi của tất cả bản ghi hợp lệ. Giá tính theo g và giá tính theo ml có ngưỡng riêng, kể cả cùng danh mục.

Sắp xếp các giá từ thấp đến cao. Với n mẫu, lấy phân vị tại 1/3 và 2/3 bằng nội suy tuyến tính ở vị trí `1 + (n - 1) × phân vị` khi đếm từ 1. Hai ngưỡng được gọi tắt là P33 và P67.

| Điều kiện | Kết quả |
|---|---|
| Giá ≤ P33 | Thấp |
| P33 < giá ≤ P67 | Trung bình |
| Giá > P67 | Cao |
| Dưới 3 mẫu hợp lệ, hai ngưỡng trùng, hoặc giá/quy cách chưa hợp lệ | Để trống và ghi lý do |

Nhóm có 3–4 mẫu hợp lệ được gắn cờ **Ít mẫu**. Giá trùng nhau có thể làm số sản phẩm ở ba mức chênh lệch.

### Ví dụ từ bộ mới

Fanta `AEON_001`, giá 7.000 ₫ cho 320 ml, được quy đổi thành **2.187,50 ₫/100 ml**. Nhóm Nước có ga theo 100 ml có 8 mẫu hợp lệ. P33 nằm ở vị trí khoảng 3,33 và P67 ở vị trí khoảng 5,67 trong dãy giá đã sắp xếp. Nội suy cho ra hai ngưỡng **2.096,69** và **2.441,86 ₫/100 ml**. Giá Fanta nằm giữa hai ngưỡng nên được xếp **Trung bình**.

## Các cột Task 4

| Cột | Ý nghĩa |
|---|---|
| `category_clean` | Danh mục đã chuẩn hóa. |
| `price_comparison_unit`, `price_normalized` | Đơn vị so sánh và giá đã quy đổi. |
| `group_valid_n` | Số mẫu có giá quy đổi hợp lệ trong nhóm. |
| `p33`, `p67` | Giá tại hai ngưỡng phân vị của nhóm. |
| `price_tier` | Thấp, Trung bình, Cao hoặc để trống. |
| `sample_flag` | Cờ Ít mẫu cho nhóm có 3–4 mẫu hợp lệ. |
| `task4_note` | Quy tắc xếp giá hoặc lý do chưa xếp của dòng. |
| `price_display_group` | Nhóm hiển thị gồm Thấp, Trung bình, Cao, Dưới 3 mẫu hợp lệ và Chưa xếp – lý do khác. |

## Kết quả

**306/398 bản ghi được xếp giá (76,9%)**, còn 92 bản ghi chưa xếp. Có 60 dòng mang cờ Ít mẫu.

| Điểm khảo sát | Thấp | Trung bình | Cao | Chưa xếp | Tổng |
|---|---:|---:|---:|---:|---:|
| AEON Bình Tân | 42 | 47 | 47 | 39 | 175 |
| AEON Tạ Quang Bửu | 5 | 1 | 6 | 1 | 13 |
| GO! An Lạc | 58 | 38 | 32 | 47 | 175 |
| GO! Tô Hiến Thành | 14 | 7 | 9 | 5 | 35 |
| **Tổng** | **119** | **93** | **94** | **92** | **398** |

### Vì sao 92 bản ghi chưa được xếp giá?

| Lý do | Số dòng | Ảnh hưởng đến việc xếp giá |
|---|---:|---|
| Nhóm dưới 3 mẫu hợp lệ | 73 | Có danh mục và giá đã quy đổi, nhưng mỗi nhóm cùng danh mục và đơn vị chỉ có 1–2 mẫu hợp lệ. Task 4 đặt điều kiện tối thiểu 3 mẫu để áp dụng quy tắc P33/P67. |
| P33 bằng P67 | 6 | Nhóm có đủ mẫu, nhưng hai ngưỡng giá trùng nhau. Khoảng giá dành cho mức Trung bình bị rỗng theo điều kiện P33 < giá ≤ P67. |
| Giá thiếu hoặc cần xác minh theo Task 1 | 9 | Giá đang chờ đối chiếu được loại khỏi tập tính ngưỡng và dòng tương ứng chưa được gán mức giá. |
| Tổng khối lượng trong quy cách bán chưa rõ | 2 | GO_017 và GO_071 có quy cách chưa đủ rõ để biết tổng khối lượng ứng với giá ghi nhận, nên chưa tính được giá trên 100 g. |
| Thiếu khối lượng hoặc dung tích hợp lệ | 1 | Chưa có số đo cần thiết để quy đổi giá về đơn vị chung. |
| Quy cách cần xác minh theo Task 1 | 1 | Quy cách của GO_203 đang chờ kiểm tra, nên giá của dòng này chưa được đưa vào tập tính ngưỡng. |
| **Tổng** | **92** | **79 dòng vướng điều kiện của nhóm, 13 dòng vướng giá hoặc quy cách.** |

File `t04_survey_segment_all.csv` giữ đủ **398 dòng** theo thứ tự gốc. File `survey_segment_final.csv` gồm **306 dòng đã xếp mức giá**. File `survey_segment_unclassified.csv` gồm **92 dòng chưa xếp mức giá**, bao gồm 73 dòng thuộc nhóm dưới 3 mẫu, 6 dòng có hai ngưỡng trùng nhau và 13 dòng vướng giá hoặc quy cách. Cột `task4_note` ghi lý do theo từng dòng. Code tạo cả ba CSV trong cùng thư mục khi chạy lệnh ở đầu tài liệu.
