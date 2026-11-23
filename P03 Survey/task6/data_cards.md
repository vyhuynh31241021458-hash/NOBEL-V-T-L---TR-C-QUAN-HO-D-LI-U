# P03 · Nguồn và mô tả dữ liệu T06

## Quy trình tái lập

1. Dùng kết quả T01 làm bảng khảo sát gốc. T01 chuẩn hóa giá, xuất xứ và giờ, đồng thời giữ các trường gốc và cờ xác minh để đối chiếu.
2. Ghép mã HS2022 từ T02 và kết quả phân nhóm giá từ T04 bằng record_id. Giữ tất cả mẫu của T01. Chuẩn hóa Chapter thành chuỗi hai ký tự.
3. Chạy task5_merge.py để tạo ba CSV cuối. So sánh khảo sát và BACI ở cấp Chapter. Giữ kim ngạch trong bảng tổng hợp riêng.
4. Chạy 01_data.ipynb để kiểm tra khóa, dữ liệu thiếu, phạm vi năm, mã và tổng kim ngạch. Notebook xuất cleaning_log.csv và task6_quality.png vào data_clean/.

## Nguồn và cột chính

| Bảng | Đơn vị quan sát | Cột và đơn vị |
|---|---|---|
| survey_final.csv | Một mẫu khảo sát | record_id là mã mẫu, store là điểm khảo sát, origin_country là xuất xứ ghi nhận, price_vnd là giá VND, price_normalized là giá theo price_comparison_unit, price_tier là mức giá T04, hs2 là Chapter HS2022 |
| survey_hs_summary.csv | Một nhóm Chapter, siêu thị, xuất xứ, ngành hàng, mức giá | product_count là số mẫu trong nhóm |
| product_year.csv và baci_hs_summary.csv | Năm × Chapter × chiều thương mại | year là năm, hs2 là Chapter HS2002, trade_flow là Export/Import, trade_usd là USD |
| partner_year.csv | Năm × đối tác × chiều thương mại | partner_code là mã đối tác BACI, partner_iso3 là mã đối tác hoặc mã nhóm, partner_name là tên đối tác, trade_usd là USD |
| trade_year.csv | Một năm của Việt Nam | export_usd và import_usd là kim ngạch xuất và nhập khẩu bằng USD |
| cleaning_log.csv | Một ghi nhận chất lượng | record_id/mã đối tác, field, issue và action |

## Kết quả và hạn chế

- 398 mẫu khảo sát giữ đủ mã, 26 Chapter, 0 mẫu thiếu HS Chapter. Có 306 mẫu có mức giá và 92 mẫu thiếu kết quả T04. Có 14 mẫu mang cờ cần xác minh từ T01.
- BACI có 3.840 dòng sản phẩm và 6.776 dòng đối tác. Cả hai khớp trade_year.csv ở 40 cặp năm × chiều, chênh lệch tối đa 0 USD.
- 490/S19 là nhóm Other Asia, nes. Giữ nhóm này trong tổng kim ngạch.
- Khảo sát thu tại bốn điểm năm 2026. Dữ liệu BACI bao phủ 2005–2024. Số mẫu mô tả danh mục ghi nhận tại kệ. Kim ngạch mô tả giá trị thương mại.
- Việc đối chiếu HS2022 với HS2002 giả định cùng mã Chapter có thể so sánh ở cấp nhóm rộng. Phạm vi hàng hóa trong mỗi chương có thể khác giữa các phiên bản.
