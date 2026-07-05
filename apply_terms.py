# -*- coding: utf-8 -*-
"""Apply the user's requirement list (sections 2, 3, 6-14, 17) as raw text replacements.
Order matters: longer/more specific patterns first to avoid cascading rewrites.
Regex is used for word-boundary-like cases; plain str.replace for exact phrases.
"""
import re, glob, os

TARGETS = sorted(glob.glob('sections/*.tex'))

# (needle, replacement, description)
REPLACEMENTS = [
    # === Section 3: outright wrong/awkward phrasings ===
    ("ledger nội dung", "nội dung ledger"),
    ("pipeline giai đoạn", "giai đoạn pipeline"),
    ("security chi phí phát sinh", "overhead bảo mật"),
    ("Security chi phí phát sinh", "Overhead bảo mật"),
    ("giai đoạn name", "tên giai đoạn"),
    ("transformation siêu dữ liệu", "metadata của transformation"),
    ("data tampering", "sửa đổi dữ liệu không hợp lệ"),
    ("ledger tampering", "sửa đổi ledger không hợp lệ"),
    ("outcome non-VALID", "kết quả khác VALID"),
    ("coverage phổ quát", "mức bao phủ phổ quát"),
    ("lineage flow mẫu", "luồng lineage mẫu"),
    ("source report", "báo cáo nguồn"),
    ("caveats", "các giới hạn cần lưu ý"),
    ("distributed consensus", "đồng thuận phân tán"),
    ("replicated nút", "các nút sao chép"),
    ("Databricks không gian làm việc", "workspace Databricks"),
    ("dữ liệu giao dịch synthetic", "dữ liệu giao dịch tổng hợp"),
    ("dữ liệu synthetic", "dữ liệu tổng hợp"),
    ("external neo tin cậy", "điểm neo tin cậy bên ngoài"),
    ("neo tin cậy", "điểm neo tin cậy bên ngoài"),
    ("controlled không gian làm việc setting", "môi trường workspace được kiểm soát"),
    ("privileged người có quyền truy cập nội bộ modification",
     "sửa đổi bởi người dùng nội bộ có đặc quyền"),
    ("Runtime chi phí phát sinh", "Overhead thời gian chạy"),
    ("runtime chi phí phát sinh", "overhead thời gian chạy"),
    # === Section 2: general Vietnamization list ===
    ("verification engine", "bộ kiểm chứng"),
    ("Verification engine", "Bộ kiểm chứng"),
    ("verification outcome", "kết quả kiểm chứng"),
    ("Verification outcome", "Kết quả kiểm chứng"),
    ("tamper scenario", "kịch bản tamper"),
    ("Tamper scenario", "Kịch bản tamper"),
    ("clean scenario", "kịch bản sạch"),
    ("Clean scenario", "Kịch bản sạch"),
    ("bounded scope", "phạm vi giới hạn"),
    ("bounded set", "tập kịch bản giới hạn"),
    ("detection rate", "tỷ lệ phát hiện"),
    ("Detection rate", "Tỷ lệ phát hiện"),
    ("false positive", "dương tính giả"),
    ("false negative", "âm tính giả"),
    ("cloud runtime variance", "dao động thời gian chạy trên môi trường cloud"),
    ("construct validity", "tính hợp lệ khái niệm"),
    ("overclaiming", "tuyên bố quá mức"),
    ("privileged writes", "thao tác ghi bởi tài khoản đặc quyền"),
    ("modification trái phép", "sửa đổi trái phép"),
    ("affected giai đoạn", "giai đoạn bị ảnh hưởng"),
    ("raw benchmark dataset", "dữ liệu benchmark thô"),
    ("repeated runs", "các lần chạy lặp lại"),
    ("operational complexity", "độ phức tạp vận hành"),
    # Sections 8-13: results/discussion/threats/conclusion adjustments
    ("first broken block", "block sai lệch đầu tiên"),
    ("first-broken-block", "block sai lệch đầu tiên"),
    ("verification latency", "độ trễ kiểm chứng"),
    ("Verification latency", "Độ trễ kiểm chứng"),
    ("runs gần nhất", "các lần chạy gần nhất"),
    ("hành vi tamper", "hành vi sửa đổi"),
    ("cache state, scheduling và resource allocation",
     "trạng thái cache, cơ chế lập lịch và phân bổ tài nguyên"),
    ("procedure", "quy trình"),
    # RESET_BASELINE token uses procedure as part of description; safe to substitute
    ("Construct được đánh giá là", "Khái niệm được đánh giá trong nghiên cứu là"),
    ("hashes và previous-hash links", "các giá trị hash và liên kết \\texttt{previous\\_hash}"),
    ("metric detection rate", "chỉ số tỷ lệ phát hiện"),
    ("record-count levels", "các mức số lượng bản ghi"),
    ("30 repeated runs", "30 lần chạy lặp lại"),
    # Conclusion-specific finer edits
    ("phạm vi bounded scope", "phạm vi giới hạn của nghiên cứu"),
    ("lineage context", "ngữ cảnh lineage"),
    ("cloud compute variability", "dao động của môi trường cloud"),
    ("decentralized consensus, nhiều independent nút", "đồng thuận phân tán, nhiều nút độc lập"),
    ("smart contracts", "smart contract"),
    ("security boundary", "ranh giới bảo mật"),
    ("controlled không gian làm việc", "workspace thực nghiệm được kiểm soát"),
    ("externalize ledger", "đưa ledger"),
    ("tăng số lần số lần lặp lại", "tăng số lần lặp lại"),  # duplication fix
    # Ledger fields renaming
    ("schema hash", "schema\\_hash"),
    ("batch hash", "batch\\_hash"),
    ("block hash", "block\\_hash"),
    ("previous block hash", "previous\\_hash"),
    ("previous hash", "previous\\_hash"),
    ("previous-hash link", "liên kết \\texttt{previous\\_hash}"),
    # Section 9 Traceability adjustments
    ("Kết quả traceability", "Kết quả truy vết"),
    ("mismatch", "sai khớp"),
    ("lineage events", "các sự kiện lineage"),
    ("pipeline run identifier", "định danh lần chạy pipeline"),
    # approximate wording
    ("approximate", "xấp xỉ"),
    ("là xấp xỉ vì được lấy từ bảng điều khiển observation thay vì dữ liệu benchmark thô được xuất dữ liệu đầy đủ",
     "mang tính xấp xỉ vì được đọc từ dashboard quan sát thay vì xuất trực tiếp từ dữ liệu benchmark thô"),
]

# regex-based, applied AFTER simple substitutions
REGEX_REPLACEMENTS = [
    # \_ artifacts: schema hash -> schema\_hash may already have been escaped;
    # ensure double-escape doesn't occur
    (r"schema\\_\\_hash", r"schema\\_hash"),
    (r"batch\\_\\_hash", r"batch\\_hash"),
    (r"block\\_\\_hash", r"block\\_hash"),
    (r"previous\\_\\_hash", r"previous\\_hash"),
]

def process(text):
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    for pat, rep in REGEX_REPLACEMENTS:
        text = re.sub(pat, rep, text)
    return text

for path in TARGETS:
    with open(path, encoding='utf-8') as f:
        original = f.read()
    updated = process(original)
    if updated != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"UPDATED  {path}")
    else:
        print(f"no-op    {path}")
print("Batch pass done.")
