# Kiểm chứng tính toàn vẹn dữ liệu bằng Hash-linked Tamper-evident Ledger

Bài báo nghiên cứu khoa học (định dạng IEEE conference) về đánh giá bán
thực nghiệm cho cơ chế Hash-linked Tamper-evident Ledger trong Data
Pipeline nhiều giai đoạn.

## Cấu trúc thư mục

```
.
├── main.tex                 # File LaTeX gốc, gọi các phần trong sections/
├── references.bib           # Tài liệu tham khảo (BibTeX)
├── IEEEtran.cls              # Class IEEE conference (tải sẵn, không cần cài thêm)
├── IEEEtran.bst              # Style trích dẫn IEEE (tải sẵn)
├── sections/
│   ├── 01_gioi_thieu.tex
│   ├── 02_phuong_phap.tex
│   ├── 03_thiet_ke_moi_truong.tex
│   ├── 04_danh_gia.tex
│   ├── 05_moi_de_doa.tex
│   ├── 06_ket_luan.tex
│   └── 07_phu_luc.tex        # Phụ lục tái lập kết quả (Reproducibility Appendix)
└── images/
    ├── kien_truc_ledger.svg / .pdf / .png
    ├── quy_trinh_thuc_nghiem.svg / .pdf / .png
    ├── placeholders/          # Ảnh chụp màn hình CẦN THAY bằng ảnh thật
    │   ├── databricks_workspace.pdf/.png
    │   ├── verification_dashboard.pdf/.png
    │   └── lineage_join.pdf/.png
    └── charts/                # Biểu đồ thật dựng từ số liệu approximate hiện có
        ├── overhead_by_record_count.pdf/.png
        └── verification_latency_range.pdf/.png
```

## Biên dịch

Project dùng **XeLaTeX** (để hỗ trợ tiếng Việt qua `fontspec` với font
DejaVu Serif/Sans, không cần gói `vietnam`/babel).

```bash
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

## Ghi chú

- Hai hình gốc trong `images/` là sơ đồ kiến trúc hệ thống (`fig:architecture`)
  và quy trình thực nghiệm (`fig:procedure`), dùng bản `.pdf` khi biên dịch
  (`.svg` là bản gốc để chỉnh sửa, `.png` để xem nhanh).
- **`images/placeholders/`** chứa 3 ảnh placeholder (Databricks workspace,
  verification dashboard, lineage join) — cần chụp màn hình thật từ
  workspace Databricks và thay thế trước khi nộp bài chính thức. Xem
  hướng dẫn chụp trong `sections/03_thiet_ke_moi_truong.tex` và
  `sections/04_danh_gia.tex` (caption của từng `\includegraphics`).
- **`images/charts/`** chứa 2 biểu đồ thật (bar chart overhead, range chart
  verification latency) dựng từ số liệu approximate hiện có trong bài. Khi
  có số liệu raw export từ `experiment_metrics`, nên vẽ lại cho chính xác
  hơn (script tham khảo: `sql/dashboard_queries.sql` KPI 8/9 trong repo
  thực nghiệm).
- Repo mã nguồn thực nghiệm (Databricks notebooks, SQL, tests):
  <https://github.com/sonnntech/kma_hk2_chuyen_de_co_so_khoa_hoc>
- Các bảng dùng `table*` + `tabular` (không dùng `longtable`) vì IEEEtran
  ở chế độ hai cột (`conference`) không hỗ trợ `longtable` trực tiếp.
- Thông tin tác giả và email trong `main.tex` là placeholder, cần điền lại.
- File `references.bib` có 3 mục tham khảo (`databricksDelta`, `iso27001`,
  `nakamoto2008bitcoin`); phần `note`/`url` nên được kiểm tra/bổ sung ngày
  truy cập trước khi nộp bài chính thức.
- Phụ lục tái lập kết quả (`sections/07_phu_luc.tex`) công khai rõ các
  "Known Reproducibility Gaps" (CPU/RAM/Databricks Runtime chưa ghi nhận,
  overhead là approximate, n=3 runs/mức chưa đủ cho box-plot/CDF đầy đủ)
  theo đúng yêu cầu trung thực khoa học — không nên xóa các ghi chú này
  trừ khi đã thực sự bổ sung được số liệu chính xác.
