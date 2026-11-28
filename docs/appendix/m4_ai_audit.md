
# M4 – AI Audit: C01A

## 1. Mục tiêu kiểm toán

Đánh giá tính chính xác và hiệu quả trực quan của biểu đồ do AI hỗ trợ tạo ra, nhằm xác định những hạn chế trong quá trình xử lý dữ liệu, lựa chọn biểu đồ và truyền tải thông tin.

Các mục tiêu cụ thể:

- Kiểm tra tính chính xác của dữ liệu được sử dụng.
- Đánh giá cách lựa chọn màu sắc, trục, nhãn và chú giải.
- Phát hiện các vấn đề có thể gây hiểu nhầm hoặc làm giảm khả năng đọc biểu đồ.
- Đề xuất điều chỉnh và so sánh kết quả trước và sau kiểm toán.
- Xác định những nội dung cần có sự kiểm tra của con người thay vì phụ thuộc hoàn toàn vào AI.

## 2. Dataset
| Thuộc tính | Mô tả |
|---|---|
| Dataset | `data/clean/trade_year.csv` |
| Đối tượng | Việt Nam (VNM) |
| Thời gian | 2005–2024 |
| Biến thời gian | `year` |
| Xuất khẩu | `export_usd` |
| Nhập khẩu | `import_usd` |
| Cán cân thương mại | `trade_balance_usd` |
| Tổng kim ngạch | `total_trade_usd` |
| Đơn vị biểu đồ | Tỷ USD |

---

## 3. Audit criteria

Việc kiểm toán dựa trên các tiêu chí sau:

| Tiêu chí | Nội dung kiểm tra |
|---|---|
| Data accuracy | Dữ liệu có đúng quốc gia, thời gian và đơn vị không? |
| Chart selection | Biểu đồ đường có phù hợp để thể hiện xu hướng theo thời gian không? |
| Visual clarity | Màu sắc và kiểu đường có giúp phân biệt hai chuỗi không? |
| Axis & labels | Tiêu đề, nhãn trục và mốc thời gian có dễ đọc không? |
| Information integrity | Cách trình bày có gây hiểu nhầm về quy mô hoặc xu hướng không? |
| Accessibility | Biểu đồ có thể đọc được khi in đơn sắc hoặc với người khó phân biệt màu không? |

### Prompt AI

Đọc file trade_year.csv và tạo biểu đồ đường thể hiện kim ngạch xuất khẩu (export_usd) và nhập khẩu (import_usd) của Việt Nam giai đoạn 2005–2024. Dùng chung trục Y, đơn vị tỷ USD, có tiêu đề, chú giải và nhãn trục. Sử dụng Python Matplotlib, không tự tạo hoặc thay đổi dữ liệu.



## 5. Identified issues – Các vấn đề được xác định

Qua quá trình kiểm tra biểu đồ và mã nguồn ban đầu, xác định ba vấn đề thiết kế cần cải thiện.

| Mã | Vấn đề AI đề xuất | Hướng kiểm tra |
|---|---|---|
| I01 | Thiếu nhãn và thông điệp định lượng rõ ràng. | Kiểm tra action title, nhãn trục, đơn vị và nhãn dữ liệu. |
| I02 | Trục X có quá nhiều nhãn năm, gây rối mắt; lưới biểu đồ quá dày. | Kiểm tra mật độ tick, góc xoay nhãn và grid. |
| I03 | Màu sắc và kiểu đường chưa đủ phân biệt hai chuỗi dữ liệu. | Kiểm tra màu, linestyle và marker của hai đường. |


## 6. Correction – Điều chỉnh sau kiểm toán

| ID | Phương án điều chỉnh | Kết quả mong đợi |
|---|---|---|
| I01 | Bổ sung nhãn giá trị tại điểm cuối của mỗi đường | Người xem nhận biết nhanh giá trị xuất khẩu và nhập khẩu |
| I02 | Chỉ hiển thị các mốc năm 2005, 2010, 2015, 2020 và 2024 | Trục thời gian thông thoáng, dễ đọc hơn |
| I03 | Sử dụng màu sắc tương phản, kết hợp kiểu nét và marker khác nhau | Phân biệt hai chuỗi ngay cả khi in đơn sắc |

## 7. Giới hạn của AI

Qua quá trình kiểm toán, có thể nhận thấy một số giới hạn khi sử dụng AI trong trực quan hóa dữ liệu:

**1. AI không đảm bảo tính chính xác của dữ liệu đầu vào**

AI có thể tạo mã nguồn chạy thành công nhưng không đồng nghĩa với việc dữ liệu đã được kiểm tra đầy đủ về năm thiếu, bản ghi trùng, giá trị bất thường hoặc đơn vị đo lường.

**2. AI có xu hướng sử dụng các thiết lập mặc định**

Các lựa chọn về màu sắc, kiểu đường, mật độ nhãn và lưới có thể chưa phù hợp với mục tiêu truyền tải thông tin.

**3. AI chưa tự xác định được thông điệp quan trọng nhất**

AI có thể tạo biểu đồ đúng yêu cầu kỹ thuật nhưng chưa chắc đã làm nổi bật được thông tin mà người xem cần nhận biết nhanh.

**4. AI không thể thay thế việc đánh giá của con người**

Việc lựa chọn biểu đồ, kiểm tra tính trung thực và đánh giá khả năng diễn giải vẫn cần dựa trên kiến thức trực quan hóa dữ liệu và mục tiêu phân tích.

**5. Kết quả AI cần được kiểm chứng bằng bằng chứng độc lập**

Không nên chấp nhận nhận xét hoặc kết luận của AI nếu chưa đối chiếu với dữ liệu, mã nguồn và biểu đồ thực tế.

## 8. Kết luận

AI hỗ trợ rút ngắn thời gian viết mã và tạo biểu đồ ban đầu. Tuy nhiên, biểu đồ được tạo ra chưa mặc nhiên đáp ứng đầy đủ các yêu cầu về tính chính xác, khả năng đọc và hiệu quả truyền tải thông tin.

Thông qua quá trình kiểm toán, ba vấn đề chính được xác định liên quan đến nhãn giá trị, mật độ nhãn thời gian và khả năng phân biệt hai chuỗi dữ liệu.

Sau khi điều chỉnh, biểu đồ cần giữ nguyên dữ liệu và phạm vi phân tích, đồng thời cải thiện cách trình bày để người xem dễ dàng nhận biết và so sánh xu hướng xuất khẩu – nhập khẩu.

**Kết luận chung:** AI đóng vai trò là công cụ hỗ trợ tạo biểu đồ, trong khi con người chịu trách nhiệm kiểm chứng dữ liệu, đánh giá thiết kế và xác nhận tính trung thực của thông tin trước khi công bố.

---
