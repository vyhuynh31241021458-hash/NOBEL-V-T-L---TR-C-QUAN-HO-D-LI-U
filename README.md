# P03 – Made in…?

## Cấu trúc

| Thư mục | Nội dung |
| --- | --- |
| `notebooks/` | `01_data.ipynb` và thư mục `house_style/` chứa code, fonts, evidence, tests và README của style. |
| `data/data_cards.md`, `data/cleaning_log.csv`, `data/data_dictionary.csv` | Thẻ dữ liệu, nhật ký làm sạch và từ điển dữ liệu. |
| `data/clean/` | 11 bảng CSV dùng vẽ biểu đồ; bản sao nguyên nội dung từ các đầu ra bên dưới. |
| `data/baci/` | Toàn bộ `P03 Baci/` cũ được chuyển nguyên khối; giữ nguyên script và cấu trúc bên trong. |
| `data/survey/scripts/` | Code T01, T04, T05; chỉ cập nhật vị trí đọc/ghi và tên tệp. |
| `data/survey/data_raw/` | Khảo sát gốc 398 bản ghi và bản phân loại HS hiện có, giữ nguyên dữ liệu. |
| `data/survey/data_clean/` | Đầu ra T01/T04/T05 và bảng mã người thu T17. |
| `docs/` | Bảng trừu tượng hóa, hướng dẫn chạy và phụ lục. |
| `outputs/` | Biểu đồ chất lượng T06. Bằng chứng T10 nằm trong `notebooks/house_style/evidence/`; T12 trong `docs/appendix/`. |
| `evidence/` | Bằng chứng, ghi chú phỏng vấn đã ẩn danh; xem README bên trong. |
| `data/survey/notes/` | Ghi chú T01/T04, issues log và phần nhật ký T09 dùng để tái tạo cleaning log. |

## Cài đặt

Mở thư mục gốc repository trong VS Code. Python 3.11 trở lên; cài dependencies từ repository:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Chọn kernel `.venv` cho notebook. Các lệnh dưới chạy từ thư mục gốc repository.

## Chạy từ các bảng đã xử lý

1. Chạy `python data/survey/scripts/t05_merge.py` để tạo lại ba bảng T05.
2. Mở `notebooks/01_data.ipynb`, chọn Restart and Run All. Notebook chạy T05, kiểm tra và xuất 11 bảng vào `data/clean/`; nhật ký tại `data/cleaning_log.csv`, ảnh tại `outputs/t06_quality.png`.
3. Code biểu đồ đọc CSV từ `data/clean/`. Khi đầu ra nguồn thay đổi, chạy lại notebook để cập nhật các bản sao; không chỉnh trực tiếp CSV trong `data/clean/`.
4. Kiểm tra màu: từ gốc repository chạy `python -m notebooks.house_style.evidence.generate`. Từ gốc chạy `python -m docs.appendix.t12_honest_vs_misleading` để tạo lại T12. Kiểm thử style: từ gốc repository chạy `python -m unittest discover -s notebooks/house_style/tests`.

## Tái tạo khảo sát T01 → T04 → T05

```powershell
python -c "import runpy; m=runpy.run_path('data/survey/scripts/t01_clean.py'); m['clean_survey'](%27data/survey/data_raw/survey_398.csv%27%2C%20%27data/survey/data_clean%27%2C%20%27data/survey/notes%27)"
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

## Phạm vi giữ nguyên và tệp còn thiếu

Đây là thay đổi cấu trúc và đường dẫn, không thay quy tắc làm sạch, phân giá, phân loại hoặc tổng hợp. Giữ giả định so sánh Chapter HS2022–HS2002 trong T05 hiện có; việc di chuyển không xác nhận giả định này là đã được kiểm chứng.

Snapshot nguồn có 398 bản ghi, không phải 350. Các tệp mã hóa riêng của Vy/Yến, bảng agreement, question tree T07, team agreement/interview insights T08, team log, AI log và makeover T11 chưa có trong snapshot này; nhóm bổ sung bản thật đúng tên/vị trí dự kiến. Không tạo nội dung hoặc bằng chứng giả. `evidence/interviews/` hiện chỉ là chỗ lưu.

`01_data.ipynb` hiện kiểm tra từ các đầu ra đã xử lý T01/T02/T04/BACI; các bước tái tạo raw được hướng dẫn riêng phía trên. Không mô tả notebook hiện tại là đã chạy toàn bộ raw BACI.

Xem [data card](data/data_cards.md), [từ điển dữ liệu](data/data_dictionary.csv), [hướng dẫn T05/T06](docs/t05_t06_run_guide.md) và [bản đồ đường dẫn cũ → mới](docs/restructure_paths.csv).

## Các mẫu cần nhóm bổ sung

`t02_hs_agreement.csv` chỉ có tiêu đề cột; cần điền từ hai kết quả mã hóa độc lập thật, không suy ra mức đồng thuận từ bảng HS cuối. `docs/ai_log.csv` và `evidence/team_log.md` là mẫu trống để nhóm nhập lịch sử thật. `data/cleaning_log.csv` đã chứa phần T09; giữ bản nguồn T09 tại `data/survey/notes/t09_cleaning_log_additions.csv` để notebook chạy lại không mất nhật ký.
