# P03 · Hướng dẫn chạy T05 và T06

## Phạm vi

T05 ghép khảo sát với kết quả phân loại HS2022 và phân nhóm giá bằng `record_id`, sau đó tổng hợp số mẫu và kim ngạch ở hai bảng riêng. T06 chạy lại T05 và kiểm tra kết quả. Các CSV đầu vào là bản đã xử lý từ T01, T02, T04 và BACI. Có thể chạy hai tác vụ này ngay từ bản clone chứa các tệp được liệt kê bên dưới.

## Chạy trên Windows PowerShell

Mở Terminal tại thư mục gốc của repo. Các lệnh dưới dùng Python 3.12.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-t05-t06.txt
.\.venv\Scripts\python.exe -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=120 notebooks/01_data.ipynb
```

Có thể chạy trong VS Code bằng cách mở `notebooks/01_data.ipynb`, chọn kernel từ `.venv` và chọn **Restart & Run All**. Notebook gọi T05 tự động. Nếu cần chạy riêng T05:

```powershell
.\.venv\Scripts\python.exe "P03 Survey/scripts/task5_merge.py"
```

Trên macOS hoặc Linux, dùng `python3.12 -m venv .venv` để tạo môi trường và `.venv/bin/python` để chạy hai lệnh còn lại.

## CSV đầu vào cần có trên Git

| Nguồn | Đường dẫn |
|---|---|
| T01 | `P03 Survey/data_clean/survey_clean.csv` |
| T02 | `P03 Survey/data_clean/HS2022_FINAL.csv` |
| T04 | `P03 category price/data_clean/survey_segment_All.csv` |
| BACI | `P03 Baci/data_clean/product_year.csv`, `partner_year.csv` và `trade_year.csv` trong cùng thư mục |
| Mã người thu | `docs/collector_by_record.csv` |

## Đầu ra

- T05 ghi `survey_final.csv`, `survey_hs_summary.csv` và `baci_hs_summary.csv` vào `P03 Survey/data_clean/`.
- T06 ghi `cleaning_log.csv` và `task6_quality.png` vào `docs/`. Xem `data_cards.md` để tra trường dữ liệu và giới hạn so sánh.

Bản bàn giao có 398 mã mẫu duy nhất, 398 mẫu có nhóm hàng, mã HS2 và mã người thu. Có 306 mẫu được xếp mức giá và 92 mẫu chưa được xếp kèm lý do. Các bảng BACI đối chiếu khớp 40 cặp năm và chiều thương mại với sai số cho phép 0,01 USD.
