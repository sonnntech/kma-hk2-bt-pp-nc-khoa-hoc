"""Regenerate Fig. 6 (overhead) and Fig. 7 (latency) with English labels to
guarantee correct font rendering across environments. Vietnamese context is
provided in the LaTeX figure caption; label-in-figure kept English keeps the
figures readable when the paper is rendered anywhere."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"

# --- Chart 1: Overhead ---
record_counts = ["1K", "5K", "10K", "50K"]
overhead_mid = [160, 157.5, 180, 220]
overhead_lo  = [160, 155, 180, 220]
overhead_hi  = [160, 160, 180, 220]
err_low = [m - l for m, l in zip(overhead_mid, overhead_lo)]
err_high = [h - m for h, m in zip(overhead_hi, overhead_mid)]

fig, ax = plt.subplots(figsize=(6, 3.6), dpi=200)
ax.bar(record_counts, overhead_mid, color="#0F6E56", alpha=0.85, width=0.55,
       yerr=[err_low, err_high], capsize=4, ecolor="#5F5E5A")
ax.set_ylabel("Approx. overhead (%)")
ax.set_xlabel("Record count")
ax.set_ylim(0, 260)
for i, v in enumerate(overhead_mid):
    ax.text(i, v + 8, f"~{v:.0f}%", ha="center", fontsize=10, color="#2C2C2A")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_title("Approximate overhead by record count\n(n=3 runs per size, values read from dashboard)",
             fontsize=9, color="#5F5E5A")
plt.tight_layout()
plt.savefig("images/charts/overhead_by_record_count.pdf")
plt.savefig("images/charts/overhead_by_record_count.png")
plt.close()

# --- Chart 2: Latency range ---
fig, ax = plt.subplots(figsize=(6, 2.6), dpi=200)
lo, med, hi = 24, 27, 31
ax.hlines(1, lo, hi, color="#534AB7", linewidth=4, alpha=0.35)
ax.plot([lo, hi], [1, 1], "o", color="#534AB7", markersize=8)
ax.plot(med, 1, "o", color="#26215C", markersize=10)
ax.plot(hi, 1, "o", color="#993C1D", markersize=10)
ax.annotate("min ~24s", (lo, 1), textcoords="offset points", xytext=(0, 14),
            ha="center", fontsize=9)
ax.annotate("~27s (typical)", (med, 1), textcoords="offset points", xytext=(0, -22),
            ha="center", fontsize=9)
ax.annotate("outlier ~31s", (hi, 1), textcoords="offset points", xytext=(0, 14),
            ha="center", fontsize=9, color="#993C1D")
ax.set_yticks([])
ax.set_xlabel("Verification latency (seconds)")
ax.set_xlim(20, 34)
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.set_title("Observed verification-latency range from dashboard\n(no raw per-run export yet - illustrative only, not a full box-plot)",
             fontsize=9, color="#5F5E5A")
plt.tight_layout()
plt.savefig("images/charts/verification_latency_range.pdf")
plt.savefig("images/charts/verification_latency_range.png")
plt.close()
print("charts regenerated with English labels")
