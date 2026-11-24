# P03 · Data cards

## BACI · CEPII

| Mục | Mô tả |
|---|---|
| Nguồn | [CEPII BACI](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37) · [Trang CEPII thay thế và thông tin phát hành](https://www.international-economics.eu/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37) |
| Phiên bản và ngày tải | HS02 (HS2002), V202601. CEPII ghi cập nhật phiên bản ngày 30/01/2026. Ngày tải của nhóm: 23/10/2026 (23:59). |
| Giấy phép | [Licence Ouverte / Etalab 2.0](https://github.com/etalab/licence-ouverte/blob/master/LO.md). Ghi nguồn CEPII, BACI và phiên bản khi sử dụng. |
| Phạm vi | Bản HS02 của CEPII bao phủ 2002–2024. P03 dùng 2005–2024, lấy các luồng Việt Nam để tổng hợp theo năm, đối tác và chương HS. Mạng gồm các luồng có hướng giữa tập nút ASEAN-10 lịch sử và 30 đối tác thương mại lớn của Việt Nam, lấy hợp của hai tập. |
| Đơn vị quan sát | Bản gốc gồm năm × nước xuất khẩu × nước nhập khẩu × sản phẩm HS6. Khóa tương ứng là `t, i, j, k`. |
| Đơn vị đo | `v` gốc là nghìn USD hiện hành, nhân 1.000 để lưu `trade_usd` bằng USD danh nghĩa. `q` gốc là tấn khi có báo cáo. Các bảng tổng hợp P03 dùng kim ngạch. |
| Cách biên soạn | CEPII hài hòa hai phía khai báo thương mại từ UN Comtrade, điều chỉnh chênh lệch định giá CIF/FOB và cân nhắc độ tin cậy của bên báo cáo. P03 lọc năm, xác định chiều thương mại theo vai trò của Việt Nam và tổng hợp HS6 lên chương. |
| Vấn đề đã biết | Mã BACI `490` / `S19` biểu thị nhóm **Other Asia, nes**, được giữ trong đối chiếu tổng. Chỉ so sánh khảo sát HS2022 với BACI HS2002 ở chương hai ký tự và lưu ý thay đổi phạm vi chương giữa hai phiên bản. Kim ngạch USD danh nghĩa có thể thay đổi do giá và tỷ giá. |

## World Development Indicators · World Bank

| Mục | Mô tả |
|---|---|
| Nguồn | [World Development Indicators – DataBank](https://databank.worldbank.org/source/world-development-indicators) · [Metadata chỉ số](https://databank.worldbank.org/metadataglossary/world-development-indicators/series) |
| Phiên bản và ngày tải | WDI là bộ dữ liệu cập nhật định kỳ. Ngày xuất DataBank và phiên bản snapshot chính thức của tệp gốc chưa có trong hồ sơ kiểm tra. Snapshot dùng cho P03 được lưu ở `wdi_vietnam_clean.csv`. |
| Giấy phép | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) theo điều khoản dữ liệu World Bank, có ngoại lệ theo nguồn/chỉ số. Ghi nguồn World Bank, World Development Indicators và tham chiếu [điều khoản sử dụng dữ liệu](https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets). |
| Phạm vi và đơn vị quan sát | Việt Nam (`VNM`), 2005–2024, 20 dòng nước × năm. Dùng GDP, tăng trưởng GDP, FDI ròng vào, tỷ trọng thương mại hàng hóa/GDP và kim ngạch xuất khẩu hàng hóa. |
| Cách biên soạn và xử lý | World Bank tổng hợp chỉ số từ các cơ quan thống kê và nguồn quốc tế theo metadata từng chỉ số. P03 đọc bản xuất DataBank, chuyển năm từ cột sang dòng, đổi ký hiệu `..` thành giá trị thiếu, rồi ghép BACI theo nước và năm. |
| Đơn vị đo | GDP, FDI và xuất khẩu hàng hóa là USD hiện hành. Tăng trưởng GDP và thương mại hàng hóa/GDP là %. |
| Vấn đề đã biết | Chênh lệch xuất khẩu được tính bằng `100 × (BACI − WDI) / WDI`. Trong snapshot P03, chênh lệch dương **7,67–24,80%** trong 2005–2024 và **24,80% năm 2024**. Khoảng 15–25% nêu trong đề tóm lược nhiều năm. Khác biệt về biên soạn và phạm vi thống kê cần được xem xét khi diễn giải. P03 giữ hai chuỗi và ghi nhận chênh lệch. |

## Khảo sát điểm bán · Nhóm P03

| Mục | Mô tả |
|---|---|
| Nguồn | Dữ liệu sơ cấp của nhóm. [Bảng tổng khảo sát gốc (398 mẫu)](../P03%20Survey/data_raw/survey_398.csv) · [Bảng khảo sát đã làm sạch](../P03%20Survey/data_clean/survey_clean.csv) · [Bảng ghép T05](../P03%20Survey/data_clean/survey_final.csv). |
| Ngày và phiên bản | Đợt thu 12/11/2026 và 22/11/2026 theo trường ngày khảo sát. Phiên bản bàn giao T05/T06 gồm 398 mã mẫu. |
| Giấy phép | Chưa có giấy phép mở được công bố cho dữ liệu nhóm. |
| Phạm vi | AEON Bình Tân và GO! An Lạc, mỗi nơi 175 mẫu. AEON Tạ Quang Bửu 13 mẫu, GO! Tô Hiến Thành 35 mẫu. Mỗi dòng là một lần ghi nhận sản phẩm tại một điểm khảo sát. |
| Cách thu thập | Khảo sát trực tiếp tại điểm bán, ghi thông tin sản phẩm, nhãn xuất xứ, giá và quy cách quan sát. T01 chuẩn hóa dữ liệu. T02 gán chương HS2022. T04 phân nhóm hàng/mức giá. T05 ghép theo `record_id`. |
| Đơn vị đo | `price_vnd` là VND theo quy cách ghi nhận. `price_normalized` sử dụng đơn vị tại `price_comparison_unit`. Số mẫu là số lượt ghi nhận. |
| Vấn đề đã biết | Phạm vi giới hạn ở bốn điểm và hai đợt ghi nhận, nên tỷ lệ mẫu mô tả mẫu khảo sát. Giá và danh mục có thể thay đổi theo điểm/thời gian. Có 14 mẫu mang cờ cần xác minh từ T01. Có 306 mẫu đã xếp mức giá và 92 mẫu giữ trống mức giá kèm lý do T04. `collector` lưu mã C01–C05. |

Ngày rà soát tài liệu nguồn cho T09 là 24/11/2026. Xem [bảng trừu tượng hóa](t09_data_abstraction.md), [từ điển dữ liệu](data_dictionary.csv) và [nhật ký](cleaning_log.csv).
