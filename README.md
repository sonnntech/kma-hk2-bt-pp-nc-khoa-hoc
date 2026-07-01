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
│   └── 06_ket_luan.tex
└── images/
    ├── kien_truc_ledger.svg / .pdf / .png
    └── quy_trinh_thuc_nghiem.svg / .pdf / .png
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

- Hai hình trong `images/` là sơ đồ kiến trúc hệ thống (`fig:architecture`)
  và quy trình thực nghiệm (`fig:procedure`), dùng bản `.pdf` khi biên dịch
  (`.svg` là bản gốc để chỉnh sửa, `.png` để xem nhanh).
- Các bảng dùng `table*` + `tabular` (không dùng `longtable`) vì IEEEtran
  ở chế độ hai cột (`conference`) không hỗ trợ `longtable` trực tiếp.
- Thông tin tác giả và email trong `main.tex` là placeholder, cần điền lại.
- File `references.bib` có 3 mục tham khảo (`databricksDelta`, `iso27001`,
  `nakamoto2008bitcoin`); phần `note`/`url` nên được kiểm tra/bổ sung ngày
  truy cập trước khi nộp bài chính thức.
