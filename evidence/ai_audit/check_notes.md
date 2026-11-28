# M4 – AI Audit Check Notes

## 1. Mục đích

Tài liệu ghi nhận quá trình sử dụng AI để kiểm toán chất lượng biểu đồ trong M4 – Trả lời bằng biểu đồ cốt lõi.

Quy trình gồm:
- Sử dụng AI để nhận diện các vấn đề trong biểu đồ.
- Kiểm tra độc lập từng nhận xét bằng dữ liệu và mã nguồn.
- Đánh giá nhận xét nào chính xác, chưa chính xác hoặc cần điều chỉnh.
- Chỉnh sửa biểu đồ dựa trên bằng chứng.
- Lưu lại kết quả trước và sau kiểm toán để đảm bảo tính minh bạch và khả năng tái lập.

**Nguyên tắc:** AI đóng vai trò công cụ hỗ trợ kiểm toán, không phải nguồn xác nhận tính chính xác cuối cùng.

---

## 2. Phạm vi kiểm toán

### Biểu đồ được lựa chọn
- Tên: Xu hướng xuất khẩu và nhập khẩu của Việt Nam.
- Dạng biểu đồ: Line chart.
- Quốc gia: Việt Nam (VNM).
- Giai đoạn: 2005–2024.
- Đơn vị: Tỷ USD.
- Dữ liệu nguồn: `data/clean/trade_year.csv`.

### Câu hỏi phân tích

Xu hướng xuất khẩu và nhập khẩu của Việt Nam thay đổi như thế nào trong giai đoạn 2005–2024?

### Thông điệp chính

So sánh quy mô và tốc độ tăng trưởng của xuất khẩu và nhập khẩu Việt Nam trong 20 năm.

---

## 3. Các vấn đề AI nhận diện

| Mã | Vấn đề AI đề xuất | Hướng kiểm tra |
|---|---|---|
| I01 | Thiếu nhãn và thông điệp định lượng rõ ràng. | Kiểm tra action title, nhãn trục, đơn vị và nhãn dữ liệu. |
| I02 | Trục X có quá nhiều nhãn năm, gây rối mắt; lưới biểu đồ quá dày. | Kiểm tra mật độ tick, góc xoay nhãn và grid. |
| I03 | Màu sắc và kiểu đường chưa đủ phân biệt hai chuỗi dữ liệu. | Kiểm tra màu, linestyle và marker của hai đường. |

Lưu ý: Các nhận xét trên là danh sách vấn đề cần xác minh. Chỉ kết luận một vấn đề là đúng sau khi đối chiếu với biểu đồ và code ban đầu.

---

## 4. Kiểm tra và xử lý từng vấn đề

### I01 – Nhãn và thông điệp định lượng

**Vấn đề cần kiểm tra:**

Biểu đồ cần giúp người xem nhận biết ngay nội dung phân tích và thông điệp chính, thay vì chỉ hiển thị hai đường dữ liệu.

**Điều chỉnh:**
- Bổ sung action title.
- Thể hiện đơn vị kim ngạch trên trục Y.
- Bổ sung nhãn giá trị tại các mốc năm quan trọng.
- Hiển thị mức tăng trưởng của xuất khẩu và nhập khẩu.

**Tiêu đề sau chỉnh sửa:**

Xu hướng xuất khẩu và nhập khẩu của Việt Nam

Giai đoạn: 2005–2024

Xuất khẩu tăng X lần; nhập khẩu tăng Y lần.

Hai hệ số X và Y được tính trực tiếp từ dữ liệu đầu kỳ và cuối kỳ, không nhập thủ công.

### I02 – Mật độ nhãn trục và lưới

**Vấn đề cần kiểm tra:**

Việc hiển thị liên tục 20 nhãn năm trên trục X có thể làm giảm khả năng đọc và gây chồng lấn.

**Điều chỉnh:**
- Chỉ giữ các mốc 2005, 2010, 2015, 2020 và 2024.
- Không xoay nhãn năm.
- Chỉ giữ grid ngang.
- Giảm độ đậm của đường lưới.
- Loại bỏ viền trên và viền phải.

### I03 – Phân biệt hai chuỗi dữ liệu

**Vấn đề cần kiểm tra:**

Hai chuỗi dữ liệu cần được phân biệt rõ ràng, kể cả khi người xem không nhận biết được màu sắc.

**Điều chỉnh:**

| Thành phần | Xuất khẩu | Nhập khẩu |
|---|---|---|
| Màu sắc | `#17365D` | `#B07A48` |
| Kiểu đường | Liền (`-`) | Đứt (`--`) |
| Marker | Hình tròn (`o`) | Hình vuông (`s`) |

Việc kết hợp màu sắc, kiểu đường và marker giúp tăng khả năng phân biệt hai chuỗi.

---

## 5. Kiểm toán dữ liệu 
### Điều kiện kiểm tra

1. Lọc đúng quốc gia VNM.
2. Dữ liệu bao phủ đủ giai đoạn 2005–2024.
3. Có đúng 20 quan sát.
4. Không có năm trùng lặp.
5. Không thiếu năm.
6. Giá trị xuất khẩu và nhập khẩu không bị thiếu.
7. Không có giá trị âm hoặc vô hạn.

---
## 6. Kết quả thiết kế sau chỉnh sửa

Biểu đồ sau kiểm toán cần đáp ứng:

- Chỉ hiển thị biểu đồ, không có bảng giá trị bên dưới.
- Có action title màu đen.
- Dòng giai đoạn nằm ngay dưới title.
- Dòng thông điệp tăng trưởng nằm dưới dòng giai đoạn.
- Hai đường dữ liệu sử dụng màu và kiểu nét khác nhau.
- Có marker để tăng khả năng phân biệt.
- Trục X chỉ hiển thị năm đại diện.
- Trục Y có đơn vị tỷ USD và bắt đầu từ 0.
- Grid ngang nhẹ.
- Bỏ viền trên và viền phải.
- Có nhãn giá trị tại các mốc năm quan trọng.

## 7. Danh mục bằng chứng kiểm toán

Các bằng chứng cần được lưu trong:

`evidence/ai_audit/`

| File | Nội dung |
|---|---|
| `prompt.txt` | Prompt gửi AI. |
| `ai_response_original.txt` | Phản hồi AI nguyên bản. |
| `ai_code_original.py` | Code biểu đồ trước chỉnh sửa. |
| `ai_chart_original.png` | Hình ảnh biểu đồ trước chỉnh sửa. |
| `issues.csv` | Danh sách vấn đề AI nhận diện. |
| `audit_comparison.csv` | Đối chiếu nhận xét AI với kết quả xác minh. |
| `corrected_chart.png` | Biểu đồ sau chỉnh sửa. |
| `check_notes.md` | Nhật ký kiểm toán và các quyết định chỉnh sửa. |

Các file phải được tạo từ quá trình thực hiện thực tế. Không sử dụng dữ liệu hoặc kết quả giả định làm bằng chứng kiểm toán.

---
**Kết luận:** AI Audit M4 không chỉ nhằm cải thiện hình thức biểu đồ mà còn đánh giá tính chính xác dữ liệu, khả năng truyền tải thông tin và tính hợp lý của các quyết định trực quan hóa. Mọi thay đổi đều cần có căn cứ và có thể giải trình.
