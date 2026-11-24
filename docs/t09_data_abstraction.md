# P03 · T09 · Trừu tượng hóa dữ liệu

| Dataset | Loại dataset | Đơn vị quan sát | Key |
|---|---|---|---|
| BACI HS02 gốc | Bảng đa chiều | Luồng HS6, nước đi, nước đến, năm | `t`, `i`, `j`, `k` |
| partner_year.csv | Bảng đa chiều | Đối tác × năm × chiều | `year`, `trade_flow`, `partner_code` |
| product_year.csv | Bảng đa chiều | Chương × năm × chiều | `year`, `trade_flow`, `hs2` |
| product_year_enriched.csv | Bảng đa chiều | Chương × năm × chiều | `year`, `trade_flow`, `hs2` |
| partner_product_year.csv | Bảng đa chiều | Đối tác × chương × năm × chiều | `year`, `trade_flow`, `partner_code`, `hs2` |
| partner_product_year_enriched.csv | Bảng đa chiều | Đối tác × chương × năm × chiều | `year`, `trade_flow`, `partner_code`, `hs2` |
| partner_section_year.csv | Bảng đa chiều | Đối tác × phần HS × năm × chiều | `year`, `trade_flow`, `partner_code`, `section_code` |
| section_year.csv | Bảng đa chiều | Phần HS × năm × chiều | `year`, `trade_flow`, `section_code` |
| trade_year.csv | Bảng đa chiều | Nước × năm | `country_iso3`, `year` |
| wdi_vietnam_clean.csv | Bảng đa chiều | Nước × năm | `country_iso3`, `year` |
| baci_wdi_vietnam_2005_2024.csv | Bảng đa chiều | Nước × năm | `country_iso3`, `year` |
| network_year.csv | Mạng có hướng, có trọng số, theo năm | Cạnh xuất khẩu → nhập khẩu × năm | `year`, `exporter_code`, `importer_code` |
| network_nodes.csv | Bảng nút của mạng | Một quốc gia hoặc thực thể BACI | `country_code` |
| hs_classification.csv | Cây phân cấp | Gốc → phần HS → chương HS | `hs2` |
| t01_survey_clean.csv | Bảng phẳng | Một mẫu khảo sát | `record_id` |
| t05_survey_final.csv | Bảng phẳng | Một mẫu khảo sát đã ghép | `record_id` |
| t05_survey_hs_summary.csv | Bảng đa chiều | Chương × điểm bán × xuất xứ × nhóm × mức giá | `hs2`, `store`, `origin_country`, `category_clean`, `price_tier` |
| t05_baci_hs_summary.csv | Bảng đa chiều | Chương × năm × chiều | `year`, `trade_flow`, `hs2` |
| t17_collector_by_record.csv | Bảng ánh xạ | Một mẫu khảo sát | `record_id` |
| cleaning_log.csv | Bảng nhật ký | Một ghi nhận chất lượng | Theo dòng ghi nhận |

Key biểu thị khóa tại cấp quan sát. Trong cây HS, section_code là mã nút cha, hs2 là mã nút con trong bảng chương. Ở bảng tổng hợp khảo sát, mức giá trống được giữ như một nhóm chưa xếp mức. Xem [data dictionary](data_dictionary.csv) để lọc theo cột, đơn vị và vai trò.

## BACI HS02 gốc

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `t` | Thời gian (tuần tự) | Key | Năm của giao dịch trong BACI gốc. |
| `i` | Định danh (không thứ tự) | Key | Mã nước xuất khẩu BACI. |
| `j` | Định danh (không thứ tự) | Key | Mã nước nhập khẩu BACI. |
| `k` | Định danh (không thứ tự) | Key | Mã sản phẩm HS2002 ở cấp 6 ký tự. Giữ số 0 đầu. |
| `v` | Định lượng (tuần tự) | Value | Kim ngạch BACI gốc. Nhân 1.000 để đổi sang USD. |
| `q` | Định lượng (tuần tự) | Value | Khối lượng BACI gốc khi nguồn có báo cáo. |

## partner_year.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `trade_flow` | Phân loại danh nghĩa (không thứ tự) | Key | Chiều thương mại nhìn từ Việt Nam. Export hoặc Import. |
| `partner_code` | Định danh (không thứ tự) | Key | Mã đối tác BACI dùng làm khóa. 490 là nhóm Other Asia, nes. |
| `partner_iso3` | Định danh (không thứ tự) | Value | Mã hiển thị ISO3 hoặc mã nhóm BACI như S19. |
| `partner_name` | Văn bản (không thứ tự) | Value | Tên đối tác theo danh mục BACI. |
| `trade_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch của nhóm theo khóa bảng. |

## product_year.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `trade_flow` | Phân loại danh nghĩa (không thứ tự) | Key | Chiều thương mại nhìn từ Việt Nam. Export hoặc Import. |
| `hs2` | Định danh (không thứ tự) | Key | Mã chương HS gồm hai ký tự. Survey dùng HS2022, BACI dùng HS2002. |
| `trade_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch của nhóm theo khóa bảng. |

## product_year_enriched.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `trade_flow` | Phân loại danh nghĩa (không thứ tự) | Key | Chiều thương mại nhìn từ Việt Nam. Export hoặc Import. |
| `hs2` | Định danh (không thứ tự) | Key | Mã chương HS gồm hai ký tự. Survey dùng HS2022, BACI dùng HS2002. |
| `trade_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch của nhóm theo khóa bảng. |
| `chapter_name` | Văn bản (không thứ tự) | Value | Tên chương HS2002. |
| `section_code` | Định danh (không thứ tự) | Value | Mã phần HS2002 bằng số La Mã, giữ dạng chuỗi. |
| `section_name` | Văn bản (không thứ tự) | Value | Tên phần HS2002. |

## partner_product_year.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `trade_flow` | Phân loại danh nghĩa (không thứ tự) | Key | Chiều thương mại nhìn từ Việt Nam. Export hoặc Import. |
| `partner_code` | Định danh (không thứ tự) | Key | Mã đối tác BACI dùng làm khóa. 490 là nhóm Other Asia, nes. |
| `hs2` | Định danh (không thứ tự) | Key | Mã chương HS gồm hai ký tự. Survey dùng HS2022, BACI dùng HS2002. |
| `trade_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch của nhóm theo khóa bảng. |

## partner_product_year_enriched.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `trade_flow` | Phân loại danh nghĩa (không thứ tự) | Key | Chiều thương mại nhìn từ Việt Nam. Export hoặc Import. |
| `partner_code` | Định danh (không thứ tự) | Key | Mã đối tác BACI dùng làm khóa. 490 là nhóm Other Asia, nes. |
| `hs2` | Định danh (không thứ tự) | Key | Mã chương HS gồm hai ký tự. Survey dùng HS2022, BACI dùng HS2002. |
| `trade_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch của nhóm theo khóa bảng. |
| `chapter_name` | Văn bản (không thứ tự) | Value | Tên chương HS2002. |
| `section_code` | Định danh (không thứ tự) | Value | Mã phần HS2002 bằng số La Mã, giữ dạng chuỗi. |
| `section_name` | Văn bản (không thứ tự) | Value | Tên phần HS2002. |

## partner_section_year.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `trade_flow` | Phân loại danh nghĩa (không thứ tự) | Key | Chiều thương mại nhìn từ Việt Nam. Export hoặc Import. |
| `partner_code` | Định danh (không thứ tự) | Key | Mã đối tác BACI dùng làm khóa. 490 là nhóm Other Asia, nes. |
| `section_code` | Định danh (không thứ tự) | Key | Mã phần HS2002 bằng số La Mã, giữ dạng chuỗi. |
| `section_name` | Văn bản (không thứ tự) | Value | Tên phần HS2002. |
| `trade_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch của nhóm theo khóa bảng. |

## section_year.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `trade_flow` | Phân loại danh nghĩa (không thứ tự) | Key | Chiều thương mại nhìn từ Việt Nam. Export hoặc Import. |
| `section_code` | Định danh (không thứ tự) | Key | Mã phần HS2002 bằng số La Mã, giữ dạng chuỗi. |
| `section_name` | Văn bản (không thứ tự) | Value | Tên phần HS2002. |
| `trade_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch của nhóm theo khóa bảng. |

## trade_year.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `export_usd` | Định lượng (tuần tự) | Value | Tổng xuất khẩu hàng hóa của Việt Nam từ BACI. |
| `import_usd` | Định lượng (tuần tự) | Value | Tổng nhập khẩu hàng hóa của Việt Nam từ BACI. |
| `trade_balance_usd` | Định lượng (phân kỳ quanh 0) | Value | Cán cân bằng xuất khẩu trừ nhập khẩu. |
| `total_trade_usd` | Định lượng (tuần tự) | Value | Tổng export_usd và import_usd. |
| `country_iso3` | Định danh (không thứ tự) | Key | Mã ISO3 quốc gia. VNM trong bảng Việt Nam. |

## wdi_vietnam_clean.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `country_iso3` | Định danh (không thứ tự) | Key | Mã ISO3 quốc gia. VNM trong bảng Việt Nam. |
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `fdi_inflows_usd` | Định lượng (tuần tự) | Value | FDI ròng vào theo WDI BX.KLT.DINV.CD.WD. Có thể âm. |
| `gdp_growth_pct` | Định lượng (phân kỳ quanh 0) | Value | Tăng trưởng GDP hằng năm theo giá cố định, WDI NY.GDP.MKTP.KD.ZG. |
| `gdp_usd` | Định lượng (tuần tự) | Value | GDP theo WDI NY.GDP.MKTP.CD. |
| `merchandise_trade_gdp_pct` | Định lượng (tuần tự) | Value | Thương mại hàng hóa/GDP theo WDI TG.VAL.TOTL.GD.ZS. |
| `wdi_merchandise_exports_usd` | Định lượng (tuần tự) | Value | Xuất khẩu hàng hóa theo WDI TX.VAL.MRCH.CD.WT. |

## baci_wdi_vietnam_2005_2024.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `export_usd` | Định lượng (tuần tự) | Value | Tổng xuất khẩu hàng hóa của Việt Nam từ BACI. |
| `import_usd` | Định lượng (tuần tự) | Value | Tổng nhập khẩu hàng hóa của Việt Nam từ BACI. |
| `trade_balance_usd` | Định lượng (phân kỳ quanh 0) | Value | Cán cân bằng xuất khẩu trừ nhập khẩu. |
| `total_trade_usd` | Định lượng (tuần tự) | Value | Tổng export_usd và import_usd. |
| `country_iso3` | Định danh (không thứ tự) | Key | Mã ISO3 quốc gia. VNM trong bảng Việt Nam. |
| `fdi_inflows_usd` | Định lượng (tuần tự) | Value | FDI ròng vào theo WDI BX.KLT.DINV.CD.WD. Có thể âm. |
| `gdp_growth_pct` | Định lượng (phân kỳ quanh 0) | Value | Tăng trưởng GDP hằng năm theo giá cố định, WDI NY.GDP.MKTP.KD.ZG. |
| `gdp_usd` | Định lượng (tuần tự) | Value | GDP theo WDI NY.GDP.MKTP.CD. |
| `merchandise_trade_gdp_pct` | Định lượng (tuần tự) | Value | Thương mại hàng hóa/GDP theo WDI TG.VAL.TOTL.GD.ZS. |
| `wdi_merchandise_exports_usd` | Định lượng (tuần tự) | Value | Xuất khẩu hàng hóa theo WDI TX.VAL.MRCH.CD.WT. |
| `baci_exports_to_gdp_pct` | Định lượng (tuần tự) | Value | 100 × xuất khẩu BACI / GDP WDI. |
| `baci_total_trade_to_gdp_pct` | Định lượng (tuần tự) | Value | 100 × tổng thương mại BACI / GDP WDI. |
| `baci_vs_wdi_exports_pct_diff` | Định lượng (phân kỳ quanh 0) | Value | 100 × (xuất khẩu BACI − xuất khẩu WDI) / xuất khẩu WDI. |

## network_year.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `exporter_code` | Định danh (không thứ tự) | Key | Mã nút đi. Tham chiếu network_nodes.country_code. |
| `importer_code` | Định danh (không thứ tự) | Key | Mã nút đến. Tham chiếu network_nodes.country_code. |
| `trade_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch của nhóm theo khóa bảng. |

## network_nodes.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `country_code` | Định danh (không thứ tự) | Key | Mã nút theo danh mục nước BACI. |
| `country_iso3` | Định danh (không thứ tự) | Value | Mã ISO3 quốc gia. VNM trong bảng Việt Nam. |
| `country_name` | Văn bản (không thứ tự) | Value | Tên quốc gia hoặc thực thể trong danh mục BACI. |
| `is_asean_2005_2024` | Boolean (không thứ tự) | Value | Cờ thuộc tập ASEAN-10 lịch sử mà P03 sử dụng. |
| `top30_rank` | Thứ bậc (tuần tự) | Value | Hạng đối tác theo tổng kim ngạch với Việt Nam 2005–2024. Trống ngoài top 30. |
| `vietnam_total_trade_2005_2024_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch hai chiều của nút với Việt Nam trong giai đoạn phân tích. |

## hs_classification.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `hs2` | Định danh (không thứ tự) | Key | Mã chương HS gồm hai ký tự. Survey dùng HS2022, BACI dùng HS2002. |
| `chapter_name` | Văn bản (không thứ tự) | Value | Tên chương HS2002. |
| `section_code` | Định danh (không thứ tự) | Value | Mã phần HS2002 bằng số La Mã, giữ dạng chuỗi. |
| `section_name` | Văn bản (không thứ tự) | Value | Tên phần HS2002. |
| `hs_revision` | Phân loại danh nghĩa (không thứ tự) | Value | Phiên bản danh mục của cây HS. HS2002 trong tệp phân loại. |
| `source_url` | Văn bản (không thứ tự) | Value | URL nguồn của danh mục HS. |

## t01_survey_clean.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `record_id` | Định danh (không thứ tự) | Key | Mã duy nhất của mẫu khảo sát, dùng để ghép các bảng khảo sát. |
| `stt_goc` | Định danh (không thứ tự) | Value | Số thứ tự theo bảng nhập, dùng để truy vết. |
| `store` | Phân loại danh nghĩa (không thứ tự) | Value | Điểm bán khảo sát. |
| `survey_date` | Thời gian (tuần tự) | Value | Ngày khảo sát chuẩn hóa YYYY-MM-DD. |
| `survey_time` | Thời gian (chu kỳ trong ngày) | Value | Giờ khảo sát chuẩn hóa HH:MM nếu có. |
| `product_name` | Văn bản (không thứ tự) | Value | Tên sản phẩm quan sát. |
| `brand` | Phân loại danh nghĩa (không thứ tự) | Value | Thương hiệu sau chuẩn hóa. Ô trống khi thiếu. |
| `spec_text` | Văn bản (không thứ tự) | Value | Mô tả quy cách dùng sau khi đọc tệp. |
| `spec_std` | Văn bản (không thứ tự) | Value | Biểu diễn quy cách đã chuẩn hóa. |
| `spec_value` | Định lượng (tuần tự) | Value | Giá trị số của quy cách đã chuẩn hóa. |
| `spec_unit` | Phân loại danh nghĩa (không thứ tự) | Value | Đơn vị quy cách chuẩn hóa của spec_value. |
| `spec_type` | Phân loại danh nghĩa (không thứ tự) | Value | Loại quy cách dùng để diễn giải số lượng hoặc đơn vị. |
| `price_vnd` | Định lượng (tuần tự) | Value | Giá quan sát theo quy cách ghi nhận. |
| `origin_country` | Phân loại danh nghĩa (không thứ tự) | Value | Nơi sản xuất hoặc xuất xứ theo thông tin ghi nhận, đã chuẩn hóa. |
| `brand_origin` | Phân loại danh nghĩa (không thứ tự) | Value | Nước gắn với thương hiệu khi có bằng chứng trong dữ liệu. |
| `made_in_vietnam` | Boolean (không thứ tự) | Value | Cờ xuất xứ Việt Nam từ kết quả chuẩn hóa. |
| `origin_note` | Văn bản (không thứ tự) | Value | Ghi chú về xuất xứ, nếu có. |
| `verify_status` | Phân loại danh nghĩa (không thứ tự) | Value | Trạng thái xác minh đã ghi ở T01. |
| `verify_fields` | Văn bản (không thứ tự) | Value | Danh sách trường cần xác minh từ T01. |
| `brand_raw` | Văn bản (không thứ tự) | Value | Giá trị thương hiệu trước chuẩn hóa. |
| `price_raw` | Văn bản (không thứ tự) | Value | Giá hoặc nội dung giá trước khi phân tích thành VND. |
| `spec_raw` | Văn bản (không thứ tự) | Value | Quy cách trước chuẩn hóa. |
| `origin_raw` | Văn bản (không thứ tự) | Value | Ghi nhận xuất xứ trước chuẩn hóa. |
| `date_raw` | Văn bản (không thứ tự) | Value | Chuỗi ngày trước chuẩn hóa. |
| `time_raw` | Văn bản (không thứ tự) | Value | Chuỗi giờ trước chuẩn hóa. |
| `source_row` | Định danh (không thứ tự) | Value | Số dòng trong nguồn nhập. Dùng để truy vết. |

## t05_survey_final.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `record_id` | Định danh (không thứ tự) | Key | Mã duy nhất của mẫu khảo sát, dùng để ghép các bảng khảo sát. |
| `stt_goc` | Định danh (không thứ tự) | Value | Số thứ tự theo bảng nhập, dùng để truy vết. |
| `store` | Phân loại danh nghĩa (không thứ tự) | Value | Điểm bán khảo sát. |
| `survey_date` | Thời gian (tuần tự) | Value | Ngày khảo sát chuẩn hóa YYYY-MM-DD. |
| `survey_time` | Thời gian (chu kỳ trong ngày) | Value | Giờ khảo sát chuẩn hóa HH:MM nếu có. |
| `product_name` | Văn bản (không thứ tự) | Value | Tên sản phẩm quan sát. |
| `brand` | Phân loại danh nghĩa (không thứ tự) | Value | Thương hiệu sau chuẩn hóa. Ô trống khi thiếu. |
| `spec_text` | Văn bản (không thứ tự) | Value | Mô tả quy cách dùng sau khi đọc tệp. |
| `spec_std` | Văn bản (không thứ tự) | Value | Biểu diễn quy cách đã chuẩn hóa. |
| `spec_value` | Định lượng (tuần tự) | Value | Giá trị số của quy cách đã chuẩn hóa. |
| `spec_unit` | Phân loại danh nghĩa (không thứ tự) | Value | Đơn vị quy cách chuẩn hóa của spec_value. |
| `spec_type` | Phân loại danh nghĩa (không thứ tự) | Value | Loại quy cách dùng để diễn giải số lượng hoặc đơn vị. |
| `price_vnd` | Định lượng (tuần tự) | Value | Giá quan sát theo quy cách ghi nhận. |
| `origin_country` | Phân loại danh nghĩa (không thứ tự) | Value | Nơi sản xuất hoặc xuất xứ theo thông tin ghi nhận, đã chuẩn hóa. |
| `brand_origin` | Phân loại danh nghĩa (không thứ tự) | Value | Nước gắn với thương hiệu khi có bằng chứng trong dữ liệu. |
| `made_in_vietnam` | Boolean (không thứ tự) | Value | Cờ xuất xứ Việt Nam từ kết quả chuẩn hóa. |
| `origin_note` | Văn bản (không thứ tự) | Value | Ghi chú về xuất xứ, nếu có. |
| `verify_status` | Phân loại danh nghĩa (không thứ tự) | Value | Trạng thái xác minh đã ghi ở T01. |
| `verify_fields` | Văn bản (không thứ tự) | Value | Danh sách trường cần xác minh từ T01. |
| `brand_raw` | Văn bản (không thứ tự) | Value | Giá trị thương hiệu trước chuẩn hóa. |
| `price_raw` | Văn bản (không thứ tự) | Value | Giá hoặc nội dung giá trước khi phân tích thành VND. |
| `spec_raw` | Văn bản (không thứ tự) | Value | Quy cách trước chuẩn hóa. |
| `origin_raw` | Văn bản (không thứ tự) | Value | Ghi nhận xuất xứ trước chuẩn hóa. |
| `date_raw` | Văn bản (không thứ tự) | Value | Chuỗi ngày trước chuẩn hóa. |
| `time_raw` | Văn bản (không thứ tự) | Value | Chuỗi giờ trước chuẩn hóa. |
| `source_row` | Định danh (không thứ tự) | Value | Số dòng trong nguồn nhập. Dùng để truy vết. |
| `category_clean` | Phân loại danh nghĩa (không thứ tự) | Value | Nhóm hàng chuẩn hóa từ T04. |
| `price_tier` | Thứ bậc (tuần tự) | Value | Thấp < Trung bình < Cao. Ô trống là chưa xếp mức. |
| `price_normalized` | Định lượng (tuần tự) | Value | Giá quy về đơn vị tại price_comparison_unit. |
| `task4_note` | Văn bản (không thứ tự) | Value | Ghi chú phân nhóm hoặc lý do để trống mức giá. |
| `price_comparison_unit` | Phân loại danh nghĩa (không thứ tự) | Value | Đơn vị so sánh của price_normalized. |
| `hs2022_section` | Định danh (không thứ tự) | Value | Mã phần HS2022 bằng số La Mã. |
| `hs2` | Định danh (không thứ tự) | Value | Mã chương HS gồm hai ký tự. Survey dùng HS2022, BACI dùng HS2002. |
| `collector` | Định danh (không thứ tự) | Value | Mã người thu C01–C05. |

## t05_survey_hs_summary.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `hs2` | Định danh (không thứ tự) | Key | Mã chương HS gồm hai ký tự. Survey dùng HS2022, BACI dùng HS2002. |
| `store` | Phân loại danh nghĩa (không thứ tự) | Key | Điểm bán khảo sát. |
| `origin_country` | Phân loại danh nghĩa (không thứ tự) | Key | Nơi sản xuất hoặc xuất xứ theo thông tin ghi nhận, đã chuẩn hóa. |
| `category_clean` | Phân loại danh nghĩa (không thứ tự) | Key | Nhóm hàng chuẩn hóa từ T04. |
| `price_tier` | Thứ bậc (tuần tự) | Key | Thấp < Trung bình < Cao. Ô trống là chưa xếp mức. |
| `product_count` | Định lượng (tuần tự) | Value | Số lượt ghi nhận sản phẩm trong nhóm. |

## t05_baci_hs_summary.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `year` | Thời gian (tuần tự) | Key | Năm quan sát, từ 2005 đến 2024 trong các bảng BACI/WDI P03. |
| `hs2` | Định danh (không thứ tự) | Key | Mã chương HS gồm hai ký tự. Survey dùng HS2022, BACI dùng HS2002. |
| `trade_flow` | Phân loại danh nghĩa (không thứ tự) | Key | Chiều thương mại nhìn từ Việt Nam. Export hoặc Import. |
| `trade_usd` | Định lượng (tuần tự) | Value | Tổng kim ngạch của nhóm theo khóa bảng. |

## t17_collector_by_record.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `record_id` | Định danh (không thứ tự) | Key | Mã duy nhất của mẫu khảo sát, dùng để ghép các bảng khảo sát. |
| `collector` | Định danh (không thứ tự) | Value | Mã người thu C01–C05. |

## cleaning_log.csv

| Column | Type (direction) | Role | Note |
|---|---|---|---|
| `record_id` | Định danh (không thứ tự) | Value | Mã mẫu, mã đối tác hoặc mã ghi nhận cấp tập dữ liệu. Có thể lặp hoặc để trống. |
| `field` | Phân loại danh nghĩa (không thứ tự) | Value | Trường liên quan đến ghi nhận chất lượng. |
| `issue` | Phân loại danh nghĩa (không thứ tự) | Value | Loại sự cố hoặc lưu ý chất lượng. |
| `action` | Văn bản (không thứ tự) | Value | Cách xử lý hoặc giới hạn cần ghi nhận. |
