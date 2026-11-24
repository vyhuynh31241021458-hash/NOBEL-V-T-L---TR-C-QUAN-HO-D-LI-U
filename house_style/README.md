# House style P03

Bộ quy chuẩn Matplotlib dùng chung cho báo cáo BACI và khảo sát. Phần A quy định cách trình bày, phần B minh họa cách áp dụng, phần C lưu kết quả kiểm tra.

## A. Quy tắc dùng chung

| Thành phần | Quy chuẩn và cách sử dụng |
| --- | --- |
| Đối tác | Top 5 theo tổng xuất khẩu + nhập khẩu BACI 2005–2024 từ `partner_year.csv`. Thứ tự cố định CHN → USA → KOR → JPN → THA → Khác. Dùng mã ISO3 để tra màu và giữ thứ tự tương đối khi lọc. Biểu đồ xếp hạng có thể đổi thứ tự theo giá trị và giữ màu theo ISO3. |
| Khác và dữ liệu thiếu | `Other` hiển thị là Khác, xám `#BDBDBD` và đứng cuối. Gộp đối tác hợp lệ ngoài Top 5, bỏ dòng tổng hợp như World. Dữ liệu thiếu dùng `#EEEEEE` kèm nhãn N/A hoặc khoảng trống. Giá trị 0 có nhãn số riêng. |
| Chiều thương mại | Xuất khẩu `#22577A`, nét liền, marker tròn. Nhập khẩu `#B86E24`, nét đứt, marker vuông. Khi cần mã hóa cả đối tác lẫn chiều thương mại, dùng màu cho đối tác và nét hoặc họa tiết cho chiều thương mại. |
| HS Section | Nhãn rút gọn theo HS2002 của BACI, thứ tự I–XXI. Giữ màu theo mã khi lọc. Ưu tiên tối đa 7 Section + Khác khi phân biệt bằng màu. Với cả 21 nhóm, ưu tiên nhãn trực tiếp, màu đơn hoặc thang tuần tự nếu màu mã hóa giá trị. Nhãn bảng khảo sát HS2022 cần đối chiếu riêng theo nguồn. |
| Thang tuần tự | `Blues` với `Normalize`, nhạt → đậm cho độ lớn. Ưu tiên gốc 0 với dữ liệu không âm. Dùng chung giới hạn khi so sánh các hình cùng chỉ tiêu, đơn vị và phạm vi. |
| Thang phân kỳ | `RdBu` với `TwoSlopeNorm`, âm đỏ, 0 trung tính, dương xanh, giới hạn đối xứng. Vạch 0 và dấu trên nhãn làm rõ chiều chênh lệch trong bản xám. |
| Font | Modern Editorial. Bricolage Grotesque cho tiêu đề chính, nhãn trục, vạch chia, chú giải, nhãn số, KPI và nguồn. Platypi cho phụ đề và chú thích diễn giải. DejaVu Sans là font dự phòng. Tiêu đề 18 pt đậm, phụ đề 12 pt, nhãn trục 11 pt, vạch chia, chú giải và nhãn trực tiếp 10 pt, nguồn 9 pt. |
| Bố cục | Nền trắng, lưới định lượng `#E5E5E5` phía sau dữ liệu, ẩn viền trên/phải. Chú giải không viền, đặt phía trên hoặc bên phải khi cần. Hình mặc định 10 × 6 inch, bản slide ngang 12 × 6.75 inch. Xuất PNG 300 DPI theo mặc định. |
| Điểm nhấn | Giữ màu riêng của nhóm được chọn nếu đã có bảng màu nhận diện. Màu nhấn dự phòng `#0072B2`, nhóm bối cảnh `#BDBDBD`. Thêm nhãn đậm, marker hoặc đường 3 pt để giữ điểm nhấn khi mất màu. |
| Thể hiện số | Dấu phẩy phân cách hàng nghìn, dấu chấm thập phân, dấu trừ `−`. Kim ngạch mặc định 1 chữ số thập phân theo tỷ USD, có thể chuyển sang triệu USD. Cán cân và tăng trưởng ghi dấu + cho số dương. Chênh lệch tỷ lệ dùng pp. |

Thành viên dùng `format_percent(0.256)` cho tỷ lệ đầu vào 0–1 và `format_percentage_points(-2.5)` cho chênh lệch đã tính theo điểm phần trăm. `format_usd` nhận USD gốc. `format_vnd` nhận VND, có thể truyền `per="kg"` hoặc `per="L"` nếu dữ liệu đã được quy đổi theo đơn vị đó. Dùng `price_comparison_unit` để kiểm tra giá khảo sát đã quy đổi trước khi đặt nhãn. Giữ nguyên dữ liệu gốc trong CSV.

Tham chiếu bài giảng gồm Lecture 2 slide 15–17, 20 và Lecture 3 slide 32–49, 56–57. Các ánh xạ HEX, phạm vi BACI và thứ tự đối tác là lựa chọn cho P03.

### Sử dụng font Modern Editorial

Bricolage Grotesque tạo hệ chữ thống nhất cho phần tiêu đề và số liệu. Platypi tạo phân biệt bằng chữ serif ở phần phụ đề và lời diễn giải. Kích thước, màu chữ và nền trắng theo cùng hệ phân cấp của House Style.

`apply_style()` đăng ký các font đi kèm bằng `matplotlib.font_manager.fontManager.addfont()` trước khi áp dụng cấu hình, nên có thể vẽ ngay cả trên máy chưa cài hai font. Bricolage Grotesque dùng ba bản tĩnh Regular 400, Medium 500 và Bold 700 được tạo từ font biến thiên gốc, với độ rộng 100 và cỡ quang học 14. Platypi dùng bản upright gốc. Các tệp font và giấy phép SIL Open Font License 1.1 nằm trong `fonts/`. [Nguồn Bricolage Grotesque](https://github.com/google/fonts/tree/main/ofl/bricolagegrotesque) · [Nguồn Platypi](https://github.com/google/fonts/tree/main/ofl/platypi)

Trong khối `with apply_style()`, chữ mặc định dùng Bricolage Grotesque. Khi thêm phụ đề, lời diễn giải, KPI hoặc nguồn, truyền bộ thuộc tính theo vai trò.

```python
from house_style.typography import ANNOTATION, KPI, SOURCE, SUBTITLE

# Đặt các lệnh trong khối with apply_style() của biểu đồ.
fig.text(0.1, 0.91, "Kim ngạch xuất khẩu · Tỷ USD", **SUBTITLE)
ax.annotate("Điểm cần diễn giải", xy=(0, 1), **ANNOTATION)
ax.text(0.8, 0.9, "125.6", transform=ax.transAxes, **KPI)
fig.text(0.1, 0.02, "Nguồn: Dữ liệu minh họa", **SOURCE)
```

## B. Mẫu áp dụng

Ảnh minh họa dùng dữ liệu giả định. Bốn mẫu gồm đối tác với họa tiết riêng, HS theo hai cách mã hóa màu, cán cân với vạch 0 và làm nổi bật một đối tác với nhãn đậm. Khi vẽ hình báo cáo, chọn dạng và chỉ tiêu theo câu hỏi phân tích rồi áp dụng cùng quy ước màu, font và đơn vị.

```python
import matplotlib.pyplot as plt
from house_style import PARTNER_COLORS, apply_style
from house_style.theme import declutter

with apply_style():
    fig, ax = plt.subplots()
    ax.bar(["Trung Quốc", "Hoa Kỳ"], [94.0, 140.5],
           color=[PARTNER_COLORS["CHN"], PARTNER_COLORS["USA"]])
    ax.set_ylabel("Kim ngạch (tỷ USD)")
    declutter(ax)
```

## C. Kiểm thử và ảnh bằng chứng

Chạy từ gốc repo bằng Python 3.12.

```powershell
python -m pip install matplotlib==3.10.8 numpy==2.3.5 colorspacious==1.1.2
python -m unittest discover -s house_style/tests -v
python -m house_style.evidence.generate
```

| Chế độ | Bảng màu | Biểu đồ |
| --- | --- | --- |
| Màu gốc | [PNG](evidence/original/palette_original.png) | [PNG](evidence/original/charts_original.png) |
| Protanopia | [PNG](evidence/protanopia/palette_protanopia.png) | [PNG](evidence/protanopia/charts_protanopia.png) |
| Deuteranopia | [PNG](evidence/deuteranopia/palette_deuteranopia.png) | [PNG](evidence/deuteranopia/charts_deuteranopia.png) |
| Tritanopia | [PNG](evidence/tritanopia/palette_tritanopia.png) | [PNG](evidence/tritanopia/charts_tritanopia.png) |
| Thang xám | [PNG](evidence/greyscale/palette_greyscale.png) | [PNG](evidence/greyscale/charts_greyscale.png) |

Mô phỏng dùng mô hình Machado của Colorspacious với mức 100. Ảnh bảng màu ghi mã HEX gốc để đối chiếu. Ảnh biểu đồ giữ nguyên dữ liệu, vị trí và nhãn giữa các chế độ.

### Kết quả

| Tiêu chí | Kết quả | Cách kiểm tra hoặc điều chỉnh |
| --- | --- | --- |
| Màu đối tác | Đạt | Test tra màu theo ISO3 sau khi lọc. |
| Thứ tự đối tác | Đạt | Test giữ thứ tự tương đối, kể cả khi đầu vào đảo thứ tự. |
| Màu HS | Đạt | Test giữ ánh xạ HEX và thứ tự khi lọc. |
| Khác | Đạt | Test màu xám và thứ tự cuối. Ảnh có nhãn Khác riêng. |
| Dữ liệu thiếu | Đạt | Test mã thiếu và mã tổng hợp. Mẫu HS ghi N/A, mẫu cán cân hiện số 0 riêng. |
| Tuần tự | Đạt | Test kiểm tra độ sáng giảm dần khi giá trị tăng. |
| Tâm phân kỳ | Đạt | Test kiểm tra màu trung tính tại 0, kể cả khi mọi giá trị bằng 0. |
| Giới hạn đối xứng | Đạt | Test ánh xạ hai cực và tâm bằng giới hạn dữ liệu bất đối xứng. |
| Dấu âm/dương | Đạt trên mẫu | Bản xám có dấu và vạch 0. |
| Mô phỏng mù màu | Đạt trên mẫu có nhãn | Một số cặp màu gần nhau, chẳng hạn Hoa Kỳ và Thái Lan ở mô phỏng deutan. Tên và họa tiết giữ được nhận diện. |
| Thang xám | Đạt trên mẫu có nhãn | Đọc nhóm bằng tên và họa tiết, đọc giá trị bằng nhãn và chiều dài thanh. |
| Điểm nhấn | Đạt trên mẫu | Tên và giá trị của nhóm nhấn dùng chữ đậm qua cả năm chế độ. |
| Font | Đạt | Kiểm tra Matplotlib chọn đúng tệp font đi kèm, phủ đủ chữ tiếng Việt hoa/thường và các ký hiệu số liệu như `%`, `−`, `+`, `×`, `₫`. Render thử trục, chú giải, phụ đề, chú thích và dòng nguồn. |
| Tương phản chữ | Đạt trên nền trắng | Test kiểm tra màu chữ mặc định, nhãn trục và vạch chia theo ngưỡng 4.5:1. |
| Định dạng số | Đạt | Test kiểm tra đơn vị, dấu, phần trăm, pp, năm và N/A. |
| Xuất ảnh | Kiểm tra trực quan | Ảnh PNG 300 DPI. Nới khoảng trống phía âm để tách nhãn giá trị khỏi tên đối tác. |

Bảng 21 màu HS dùng để giữ ánh xạ nhất quán. Các mẫu kiểm tra khả năng đọc bằng nhãn trực tiếp và sáu section minh họa.
