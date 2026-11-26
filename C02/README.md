# C02 · Thương mại Việt Nam theo phần và chương HS

| Biểu đồ | Nội dung | Tệp |
| --- | --- | --- |
| C02A | Cơ cấu xuất khẩu tại 5 mốc, 6 nhóm | [PNG](C02A.png) · [SVG](C02A.svg) |
| C02B | Cơ cấu nhập khẩu tại 5 mốc, Top 5 nhập khẩu + Khác | [PNG](C02B.png) · [SVG](C02B.svg) |
| C02C | Kim ngạch xuất khẩu theo năm, Top 5 xuất khẩu + Khác | [PNG](C02C.png) · [SVG](C02C.svg) |
| C02D | Kim ngạch nhập khẩu theo năm, Top 5 nhập khẩu + Khác, cùng thang dọc với C02C | [PNG](C02D.png) · [SVG](C02D.svg) |
| C02E | HS84 và HS85, mỗi ô có hai chiều, cùng thang dọc | [PNG](C02E.png) · [SVG](C02E.svg) |

## Chạy và tích hợp

Từ gốc repository, sau khi cài các thư viện trong `requirements.txt`:

```powershell
python -m C02.ve_c02
python -m C02.ve_c02 C02B
```

Thay `C02B` bằng tên hình cần xuất. PNG theo DPI của House Style. SVG chuyển chữ thành đường vector để giữ font và dấu tiếng Việt.

```python
from C02.du_lieu import load_data
from C02.bieu_do import plot_c02a, plot_c02b, plot_c02c, plot_c02d, plot_c02e

data = load_data()
figure = plot_c02a(data)
```

[du_lieu.py](du_lieu.py) đọc, kiểm tra và xử lý dữ liệu. [bieu_do.py](bieu_do.py) chứa năm hàm trả về đối tượng Matplotlib `Figure`. Dashboard có thể tải dữ liệu một lần, rồi truyền cùng đối tượng dữ liệu cho các hàm cần dùng. [ve_c02.py](ve_c02.py) là điểm chạy xuất file.

## Dữ liệu và đối chiếu

Nguồn là hai bảng [section_year.csv](../data/clean/section_year.csv) và [product_year.csv](../data/clean/product_year.csv), theo [data card BACI](../data/data_cards.md). Hai bảng dùng đơn vị USD danh nghĩa. Kiểm tra kiểu, giá trị thiếu, khóa trùng, mã HS hai ký tự và chiều `Export`/`Import` trước khi gộp. Các phép cộng và so tổng dùng giá trị USD gốc. Nhãn tỷ trọng và kim ngạch hiển thị một chữ số thập phân.

1. Lọc xuất khẩu ở các năm **2005, 2010, 2015, 2020, 2024**. Cộng USD theo phần HS và sắp giảm dần. Top 5 theo thứ tự là **XVI, XI, XII, XX, II**. Dùng thứ tự này cho A và C. C02B và C02D xếp hạng riêng theo tổng nhập khẩu qua cùng 5 mốc, được **XVI, XV, XI, VI, VII**. Mỗi hình đặt **Khác** cuối danh sách và gộp các phần ngoài Top 5 của hình đó.
2. Đối chiếu A/B bằng cách chia kim ngạch từng nhóm cho tổng của **cùng năm, cùng chiều**. Thí dụ năm 2024, XVI chiếm **54.9%** xuất khẩu và **46.1%** nhập khẩu. Nhóm Khác chiếm **19.4%** xuất khẩu và **25.3%** nhập khẩu. Hai nhóm Khác được tính riêng theo danh sách Top 5 của mỗi chiều. Tổng tỷ trọng theo số chưa làm tròn bằng 100%.
3. C/D lấy đủ năm 2005–2024 và chia kim ngạch USD cho 1 tỷ. Nhóm Khác của C02D đạt **95.2 tỷ USD** năm 2024. C02B và C02D dùng cùng nhóm Khác của nhập khẩu. Dệt may (XI) có tỷ trọng xuất khẩu giảm từ **16.3% xuống 9.9%**, trong khi kim ngạch tăng từ **6.1 lên 49.8 tỷ USD**.
4. E lấy chương `84` và `85` trong bảng sản phẩm. Năm 2024, chênh lệch XK − NK của hai chương lần lượt khoảng **+45.8** và **+58.0 tỷ USD**. Chênh lệch được tính trên số gốc trước khi làm tròn.

## House Style và khả năng tiếp cận

Các hình vẽ trong `apply_style()` của [House Style chung](../notebooks/house_style/house_style.py). Module biểu đồ dùng `HS_COLORS`, `HS_LABELS`, `HS_ORDER` và `OTHER` cho phần HS, `COUNTRY_COLORS` cho nhãn Việt Nam và nhóm `TRADE_FLOW_*` cho C02E. Font, nền, trục, chú giải, cỡ chữ và màu chữ kế thừa từ theme. `DIRECT_LABEL`, `SUBTITLE`, `SOURCE`, `format_year`, `format_number` và `format_percent` xử lý các vai trò tương ứng. Các biến đều dùng mã hóa phân loại hoặc kim ngạch tuyệt đối, nên không cần áp thang tuần tự hay phân kỳ vào các hình này.

House Style có màu theo phần HS và quy ước marker/họa tiết cho đối tác hoặc chiều thương mại. A/B bổ sung họa tiết và C/D bổ sung marker ở lớp mã hóa của biểu đồ để nhận diện nhóm khi mất màu. Nếu các nhóm khác cần cùng quy ước dấu hiệu theo HS, có thể bổ sung ánh xạ tập trung theo mã HS vào House Style ở một lần cập nhật riêng.

## Kết quả kiểm tra

- Kiểm tra **840 dòng phần HS** và **3,840 dòng chương HS**. **40/40** tổng năm–chiều khớp giữa hai bảng và được bảo toàn sau khi gộp Khác. **10/10** cột A/B cộng thành 100% trước khi làm tròn.
- Kiểm tra màu theo mã HS trên A–D, kể cả khi các tập Top 5 khác nhau và màu theo chiều trên E. C/D có **120 điểm mỗi hình**. E có **80 điểm**, với thang dọc giống nhau giữa hai ô. Mỗi giá trị đường được đối chiếu với USD gốc chia cho 1 tỷ.
- Đo khung tiêu đề, phụ đề, chú giải, nhãn trục và bảng số. Các phần đầu hình tách nhau và chữ trong các bảng nằm trong ô. Dựng đủ PNG/SVG và chạy riêng C02E thành công. **14/14** kiểm thử House Style đạt.
- Xem bản xám và mô phỏng protanomaly, deuteranomaly, tritanomaly bằng hàm House Style. Họa tiết, marker hoặc kiểu nét vẫn phân biệt được các nhóm. Một số đường có kim ngạch nhỏ ở C/D nằm gần nhau trên thang chung, nên bảng dưới hình hỗ trợ đọc chính xác.
