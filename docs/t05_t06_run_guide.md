# Hướng dẫn chạy T05/T06

## Chạy từ các bảng đã xử lý

1. Chạy `python data/survey/scripts/t05_merge.py` để tạo lại ba bảng T05.
2. Mở `notebooks/01_data.ipynb`, chọn Restart and Run All. Notebook chạy T05, kiểm tra và xuất 11 bảng vào `data/clean/`; nhật ký tại `docs/cleaning_log.csv`, ảnh tại `outputs/t06_quality.png`.
3. Code biểu đồ đọc CSV từ `data/clean/`. Khi đầu ra nguồn thay đổi, chạy lại notebook để cập nhật các bản sao; không chỉnh trực tiếp CSV trong `data/clean/`.
4. Kiểm tra màu: từ `notebooks/` chạy `python -m p03_style.evidence.generate`. Từ gốc chạy `python -m docs.appendix.t12_honest_vs_misleading` để tạo T12.

## Tái tạo khảo sát T01 → T04 → T05

```powershell
python -c "import runpy; m=runpy.run_path('data/survey/scripts/t01_clean.py'); m['clean_survey']('data/survey/data_raw/survey_398.csv', 'data/survey/data_clean', 'data/survey/notes')"
python data/survey/scripts/t04_category_price.py data/survey/data_clean/t01_survey_clean.csv data/survey/data_clean/t04_survey_segment_all.csv
python data/survey/scripts/t05_merge.py
```

Sau đó chạy `01_data.ipynb`. T02 là kết quả mã hóa thủ công: script đọc `data/survey/data_raw/hs/t02_hs2022_final.csv`. Không tự tạo lại kết quả hai người mã hóa hoặc tỷ lệ đồng thuận từ bản cuối.

## Tái tạo BACI

Đặt dữ liệu nguồn đúng phiên bản HS02 V202601, bảng mã quốc gia/sản phẩm, WDI và `hs2002_wco_source.html` trong `data/baci/data_raw/`. Thư mục này được bỏ qua bởi Git; chuyển thư mục raw cục bộ cũ sang đây nếu đã có.

```powershell
python data/baci/scripts/filter_baci_vietnam.py
python data/baci/scripts/prepare_baci.py
python data/baci/scripts/merge_baci_wdi.py
node data/baci/scripts/complete_hs_network.mjs
node data/baci/scripts/validate_hs_network.mjs
python data/baci/scripts/audit_baci_data.py
python data/baci/scripts/verify_baci_2024.py
```

Hai lệnh `node` cần Node.js; lệnh lọc và dựng mạng quét bộ raw lớn. `analyze_export_gap.ps1` dùng các phản hồi Comtrade đã lưu và có thể chạy riêng bằng PowerShell. Sau khi cập nhật BACI, chạy lại T05 và `01_data.ipynb` để đồng bộ bảng biểu đồ.


