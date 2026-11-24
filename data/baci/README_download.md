# Tải dữ liệu gốc (không đưa file lớn lên Git)

**BACI:** CEPII BACI HS02/HS2002, phiên bản V202601; website: https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37. Dữ liệu dự án dùng 2005–2024. Kiểm tra lại phiên bản khi tải; không trộn các phiên bản HS.

**World Bank WDI:** https://databank.worldbank.org/source/world-development-indicators. Bảng đã dùng có Việt Nam, các năm 2005–2024 và các chỉ số GDP (USD hiện hành), tăng trưởng GDP, FDI ròng vào, merchandise trade (% GDP), merchandise exports (USD). Xem danh mục tên cột ở `../data_clean/wdi_vietnam_clean.csv` và mô tả ở `../data_cards.md` (từ thư mục baci, thực tế là `../data_cards.md`).

Đặt các file BACI HS02 gốc, file mã quốc gia/sản phẩm, file WDI export và tài liệu HS2002 phục vụ script trong `data/baci/data_raw/` đúng tên mà script đang yêu cầu. Thư mục `data_raw` bị `.gitignore` loại trừ vì dữ liệu nguồn lớn. Giữ nguyên mã nguồn trong `data/baci/scripts/`; chạy lại theo thứ tự trong README gốc của repository. Nếu thiếu file gốc, phải tải đúng nguồn, không suy đoán các dòng dữ liệu.
