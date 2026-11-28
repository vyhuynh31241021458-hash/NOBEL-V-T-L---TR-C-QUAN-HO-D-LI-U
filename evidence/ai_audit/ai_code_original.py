import matplotlib.pyplot as plt
import pandas as pd

# Đọc dữ liệu gốc từ file CSV
df = pd.read_csv('trade_year.csv')

# Lọc giai đoạn 2005-2024 và sắp xếp theo năm
df = df[(df['year'] >= 2005) & (df['year'] <= 2024)].sort_values('year')

# Quy đổi đơn vị từ USD sang tỷ USD
export_billion = df['export_usd'] / 1e9
import_billion = df['import_usd'] / 1e9

# Khởi tạo biểu đồ
plt.figure(figsize=(12, 6), dpi=150)

# Vẽ hai đường xuất khẩu và nhập khẩu trên cùng một trục Y
plt.plot(
    df['year'],
    export_billion,
    marker='o',
    linewidth=2.2,
    color='#1f77b4',
    label='Xuất khẩu (export_usd)',
)
plt.plot(
    df['year'],
    import_billion,
    marker='s',
    linewidth=2.2,
    color='#ff7f0e',
    label='Nhập khẩu (import_usd)',
)

# Thiết lập tiêu đề, nhãn trục và chú giải
plt.title(
    'Kim ngạch Xuất khẩu và Nhập khẩu của Việt Nam giai đoạn 2005–2024',
    fontsize=14,
    fontweight='bold',
    pad=15,
)
plt.xlabel('Năm', fontsize=12)
plt.ylabel('Kim ngạch (Tỷ USD)', fontsize=12)

# Hiển thị đầy đủ các năm trên trục X và lưới tọa độ
plt.xticks(df['year'], rotation=45)
plt.ylim(bottom=0)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11, loc='upper left')

plt.tight_layout()
plt.savefig('vietnam_trade_2005_2024.png', dpi=300)
plt.show()