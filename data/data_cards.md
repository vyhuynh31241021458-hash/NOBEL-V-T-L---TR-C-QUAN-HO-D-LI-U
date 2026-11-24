# P03 · Data cards

## BACI · CEPII

| Mục | Mô tả |
|---|---|
| Nguồn | [CEPII BACI](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37). Tài liệu phương pháp là Gaulier & Zignago (2010), *BACI: International Trade Database at the Product-Level*, CEPII Working Paper 2010-23. |
| Phiên bản và ngày tải | HS02 (HS2002), phiên bản **V202601**. CEPII cập nhật phiên bản ngày **30/01/2026**. Nhóm tải dữ liệu ngày **23/10/2026** lúc **23:59**. |
| Giấy phép | [Licence Ouverte / Etalab 2.0](https://github.com/etalab/licence-ouverte/blob/master/LO.md). Khi sử dụng, ghi nguồn CEPII, tên bộ dữ liệu BACI và phiên bản `V202601`. |
| Phạm vi | Bản HS02 của CEPII bao phủ **2002–2024**. P03 sử dụng giai đoạn **2005–2024** để tổng hợp luồng thương mại của Việt Nam theo năm, đối tác và chương HS. Tập nút của mạng là hợp của ASEAN-10 theo phạm vi nghiên cứu và 30 đối tác đứng đầu theo tổng kim ngạch xuất khẩu và nhập khẩu với Việt Nam, cộng dồn trong giai đoạn 2005–2024. |
| Đơn vị quan sát | Mỗi dòng trong dữ liệu gốc biểu thị một luồng thương mại theo tổ hợp **năm × nước xuất khẩu × nước nhập khẩu × sản phẩm HS6**. Khóa tương ứng gồm `t`, `i`, `j` và `k`. |
| Đơn vị đo | Biến `v` trong dữ liệu gốc có đơn vị nghìn USD hiện hành. P03 nhân `v` với 1.000 để lưu `trade_usd` theo USD danh nghĩa. Biến `q` có đơn vị tấn khi có số liệu. Các bảng tổng hợp P03 sử dụng kim ngạch. |
| Cách biên soạn và xử lý | CEPII đối chiếu khai báo của bên xuất khẩu và bên nhập khẩu từ UN Comtrade, điều chỉnh khác biệt định giá CIF/FOB và xét độ tin cậy của bên báo cáo. P03 lọc theo năm, xác định chiều thương mại theo vai trò xuất hoặc nhập của Việt Nam và tổng hợp mã HS6 lên cấp chương. |
| Vấn đề đã biết | Mã BACI `490` / `S19` biểu thị nhóm **Other Asia, nes**. P03 giữ nhóm này khi đối chiếu tổng kim ngạch. Khảo sát dùng HS2022, còn BACI dùng HS2002. P03 chỉ đối chiếu ở cấp chương hai ký tự vì phạm vi chương có thể thay đổi giữa các phiên bản. Kim ngạch tính theo USD danh nghĩa chịu ảnh hưởng của giá và tỷ giá. |

## World Development Indicators · World Bank

| Mục | Mô tả |
|---|---|
| Nguồn | [World Development Indicators – World Bank DataBank](https://databank.worldbank.org/source/world-development-indicators) · [Siêu dữ liệu chỉ số WDI](https://databank.worldbank.org/metadataglossary/world-development-indicators/series) |
| Ngày truy cập và tải | Nhóm truy cập và tải dữ liệu ngày **27/10/2026**, khoảng **11:36:53 (UTC+7)**. Bản dữ liệu đã làm sạch dùng trong P03 được lưu tại `wdi_vietnam_clean.csv`. |
| Giấy phép | Dữ liệu World Bank áp dụng [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) theo điều khoản sử dụng dữ liệu, trừ trường hợp có điều kiện riêng theo nguồn hoặc chỉ số. Khi sử dụng, ghi nguồn World Bank, *World Development Indicators*. [Điều khoản sử dụng dữ liệu World Bank](https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets) |
| Phạm vi và đơn vị quan sát | Việt Nam (`VNM`), **2005–2024**, gồm **20 quan sát quốc gia–năm**. Các chỉ số sử dụng gồm GDP, tăng trưởng GDP, FDI ròng vào, tỷ lệ thương mại hàng hóa trên GDP và kim ngạch xuất khẩu hàng hóa. |
| Cách biên soạn và xử lý | World Bank tổng hợp các chỉ số từ cơ quan thống kê và nguồn quốc tế theo siêu dữ liệu của từng chỉ số. P03 chuyển các cột năm của tệp xuất DataBank thành dòng, chuyển ký hiệu `..` thành giá trị thiếu và ghép với BACI theo quốc gia và năm. |
| Đơn vị đo | GDP, FDI ròng vào và kim ngạch xuất khẩu hàng hóa được ghi bằng USD hiện hành. Tăng trưởng GDP và tỷ lệ thương mại hàng hóa trên GDP được ghi bằng phần trăm. |
| Vấn đề đã biết | Chênh lệch kim ngạch xuất khẩu hàng hóa được tính bằng `100 × (BACI − WDI) / WDI`. Trong dữ liệu P03, BACI cao hơn WDI trong cả 20 năm. Chênh lệch thấp nhất là **7,67% năm 2011**, cao nhất là **24,80% năm 2024**. Có **13/20 năm** nằm trong khoảng 15–25%. Khác biệt về phương pháp biên soạn và phạm vi thống kê là những khả năng cần kiểm chứng. |

## Khảo sát điểm bán · Nhóm P03

| Mục | Mô tả |
|---|---|
| Nguồn | Dữ liệu sơ cấp do nhóm P03 thu thập. [Bảng tổng khảo sát gốc (398 mẫu)](survey/data_raw/survey_398.csv) · [Bảng khảo sát đã làm sạch](survey/data_clean/t01_survey_clean.csv) · [Bảng ghép T05](survey/data_clean/t05_survey_final.csv) |
| Ngày và phiên bản | Hai đợt khảo sát diễn ra ngày **12/11/2026** và **22/11/2026** theo trường ngày khảo sát. Bản bàn giao T05/T06 gồm **398 mã mẫu**. |
| Giấy phép | Dữ liệu do nhóm thu thập. Nhóm chưa công bố giấy phép mở. |
| Phạm vi và đơn vị quan sát | AEON Bình Tân và GO! An Lạc có **175 mẫu mỗi nơi**. AEON Tạ Quang Bửu có **13 mẫu**, GO! Tô Hiến Thành có **35 mẫu**. Mỗi dòng là một lượt ghi nhận sản phẩm tại một điểm bán, định danh bằng `record_id`. |
| Cách thu thập và xử lý | Nhóm khảo sát trực tiếp tại điểm bán và ghi thông tin sản phẩm, xuất xứ trên nhãn, giá và quy cách. T01 chuẩn hóa dữ liệu. T02 gán chương HS2022. T04 phân nhóm hàng và xếp mức giá khi đủ căn cứ. T05 ghép các bảng theo `record_id`. |
| Đơn vị đo | `price_vnd` là giá bằng VND theo quy cách ghi nhận. `price_normalized` là giá được quy đổi theo đơn vị ghi trong `price_comparison_unit`. Số mẫu được tính theo lượt ghi nhận. |
| Vấn đề đã biết | Các tỷ lệ phản ánh **398 lượt ghi nhận tại bốn điểm bán trong hai đợt khảo sát**. Giá và danh mục sản phẩm có thể thay đổi theo điểm bán và thời điểm. Có **14 mẫu** mang cờ cần xác minh từ T01. T04 xếp mức giá cho **306 mẫu** và ghi lý do để trống mức giá cho **92 mẫu**. Trường `collector` sử dụng mã `C01`–`C05`. |

Ngày rà soát tài liệu nguồn cho T09 là **24/11/2026**. Xem thêm [bảng trừu tượng hóa](../docs/t09_data_abstraction.md), [từ điển dữ liệu](data_dictionary.csv) và [nhật ký làm sạch](cleaning_log.csv).