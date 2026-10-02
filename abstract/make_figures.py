"""Abstract figures. Numbers are copied from the run of record (results/run_of_record/) and the
post-hoc outputs (results/posthoc_tier12/). fig4_robustness.png is the abstract figure; fig1 and
fig2 are supplementary and exploratory (distance subgroups did not meet balance criteria).
Euro distance-subgroup CIs in fig1 are a read-only recomputation from the saved development
att_contributions (Hajek within stratum, match-cluster t(101), fixed nuisances)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE = "#2a78d6", "#eb6834"          # validated categorical slots 1-2
INK, INK2, GRID, SURF = "#1f1f1e", "#5f5e58", "#e4e3dd", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "figure.facecolor": SURF, "axes.facecolor": SURF})

# ---- Figure 1: effect of shooting vs keeping the ball by pre-registered distance subgroup
# (percentage points of net scoring rate within 15 s), 95% match-cluster CI
rows = ["All analysed shots", "Shots within 18 m", "Shots beyond 18 m"]
euro = [(1.77, -0.22, 3.76, 2195), (2.92, 0.11, 5.72, 1323), (0.04, -1.45, 1.52, 872)]
wc   = [(3.08, 0.67, 5.48, 1228), (5.94, 2.16, 9.72, 743), (-1.31, -3.13, 0.51, 485)]
fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=200)
fig.set_facecolor("white"); ax.set_facecolor("white")   # white for print/PDF
for i, _ in enumerate(rows):
    for off, data, col, lab in [(-0.14, euro, BLUE, "Euro 2020+2024 (development)"),
                                (0.14, wc, ORANGE, "World Cup 2022 (held out)")]:
        est, lo, hi, n = data[i]
        y = i + off
        ax.errorbar([est], [y], xerr=[[est - lo], [hi - est]], fmt="o", ms=6, color=col, mec="white",
                    mew=1.2, ecolor=col, elinewidth=2, capsize=4, capthick=1.5, zorder=3,
                    label=lab if i == 0 else None)
        ax.text(hi + 0.25, y, f"{est:+.1f}  ({lo:+.1f} to {hi:+.1f})", va="center", fontsize=8, color=INK2)
ax.axvline(0, color=INK2, lw=1, zorder=1)
ax.set_yticks(range(len(rows)), rows, color=INK)
ax.invert_yaxis()
ax.set_xlim(-4.5, 14.5); ax.set_xticks(range(-4, 15, 2))
ax.set_xlabel("Effect of shooting (percentage points, 95% CI)")
ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc="lower right", fontsize=8.5)
fig.suptitle("Adjusted effect of shooting vs keeping the ball, overall and by shot distance", x=0.01, ha="left",
             fontsize=11, color=INK)
fig.text(0.01, 0.015, "Net scoring rate = first goal within 15 s (+1 scored, -1 conceded). Bars: 95% CI, clustered by match. "
         "Distance groups are prespecified.", fontsize=7.5, color=INK2, va="bottom")
fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig("fig1_effect_by_distance.png"); plt.close(fig)

# ---- Figure 2 (descriptive): observed 15-s scoring rate of shots vs model-estimated rate had they continued
bins = ["<11", "11-14", "14-18", "18-22", "22-26", "26-40"]
data = {"Euro 2020+2024 (development)": ([15.74, 12.93, 8.50, 5.49, 4.13, 0.00], [12.53, 8.75, 7.07, 5.46, 4.21, 2.75]),
        "World Cup 2022 (held out)":    ([20.06, 15.23, 10.13, 4.17, 2.45, 2.83], [11.90, 8.27, 6.64, 5.65, 3.66, 2.91])}
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2), dpi=200, sharey=True)
for ax, (title, (shot, cont)) in zip(axes, data.items()):
    x = range(len(bins))
    ax.plot(x, shot, color=ORANGE, lw=2, marker="o", ms=5, mec=SURF, mew=1.5, label="Shot taken (observed)")
    ax.plot(x, cont, color=BLUE, lw=2, marker="o", ms=5, mec=SURF, mew=1.5, label="If continued (outcome model)")
    ax.set_xticks(list(x), bins); ax.set_xlabel("Shot distance (m)")
    ax.set_title(title, fontsize=9.5, color=INK, loc="left")
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
axes[0].set_ylabel("Goal within 15 s (%)")
axes[0].legend(frameon=False, fontsize=8)
fig.suptitle("Where the gap opens: inside ~18 m", x=0.02, ha="left", fontsize=11, color=INK)
fig.tight_layout(); fig.savefig("fig2_rates_by_distance.png"); plt.close(fig)

# ---- Figure 4: robustness of the held-out World Cup estimate (v3 abstract figure)
# Sources: confirmation/submission_results.json (point, analyses.records[].score_interval, bootstrap),
# tier12_posthoc/tier1/dependence.csv, tier12_posthoc/report/tier2_estimates.md (post hoc arms).
# Row: (label, est, lo, hi, cohort, balance_ok). None marks a group header.
rob = [
    ("Primary (World Cup, held out)", None),
    ("Clustered by match", 3.08, 0.67, 5.48, "wc", True),
    ("Other ways to measure uncertainty", None),
    ("Bootstrap refitting all models", 3.08, 0.29, 5.61, "wc", True),
    ("Clustered by team", 3.08, 0.41, 5.74, "wc", True),
    ("Clustered by opponent", 3.08, -0.28, 6.43, "wc", True),
    ("Clustered by team and opponent", 3.08, -0.22, 6.37, "wc", True),
    ("Other model choices", None),
    ("GAM outcome model", 2.84, 0.31, 5.37, "wc", True),
    ("Boosted-tree outcome model", 3.00, 0.46, 5.55, "wc", True),
    ("5-second window", 3.91, 1.59, 6.23, "wc", True),
    ("10-second window", 3.18, 0.81, 5.56, "wc", True),
    ("30-second window", 3.18, 0.66, 5.69, "wc", True),
    ("Other decision samples", None),
    ("Carries excluded", 3.58, 0.38, 6.79, "wc", False),
    ("5 m visible area (1,175 shots)", 2.26, -0.47, 5.00, "wc", True),
    ("Extra covariates (post hoc)", None),
    ("+ build-up context", 2.97, 0.76, 5.19, "wc", False),
    ("Goalkeeper-visible subset (1,006 shots)", 3.52, 0.37, 6.67, "wc", True),
    ("  + build-up context and goalkeeper", 3.57, 0.38, 6.77, "wc", False),
    ("Development data", None),
    ("Euro 2020 + 2024", 1.77, -0.22, 3.76, "euro", True),
]
fig, ax = plt.subplots(figsize=(7.2, 6.4), dpi=200)
labels, weights = [], []
for i, row in enumerate(rob):
    labels.append(row[0]); weights.append("bold" if len(row) == 2 else "normal")
    if len(row) == 2:
        continue
    _, est, lo, hi, cohort, ok = row
    col = ORANGE if cohort == "wc" else BLUE
    ax.plot([lo, hi], [i, i], color=col, lw=2, solid_capstyle="round", zorder=2)
    ax.scatter([est], [i], s=42, zorder=3, linewidth=1.8,
               color=col if ok else SURF, edgecolor=col if not ok else SURF)
    ax.text(7.25, i, f"{est:.1f}  ({lo:.1f} to {hi:.1f})", va="center", fontsize=8, color=INK2)
ax.axvline(0, color=INK2, lw=1, zorder=1)
ax.axvline(3.08, color=GRID, lw=1, ls=(0, (3, 3)), zorder=1)
ax.set_yticks(range(len(rob)), labels)
for t, w in zip(ax.get_yticklabels(), weights):
    t.set_fontweight(w); t.set_color(INK if w == "bold" else INK2); t.set_fontsize(8.5)
ax.tick_params(axis="y", length=0)
ax.set_ylim(len(rob) - 0.4, -0.6)
ax.set_xlim(-1.5, 7.2)
ax.set_xlabel("Shooting minus keeping the ball (percentage points, 95% CI)")
ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
fig.suptitle("The estimate is stable; how certain it is depends on the clustering", x=0.01, ha="left",
             fontsize=11, color=INK)
fig.text(0.01, 0.012, "Outcome: net scoring rate within 15 s (first goal, +1 for, -1 against), other windows where stated.\n"
         "Intervals clustered by match unless stated. Hollow points: weighting failed balance checks.\n"
         "Hidden-confounding sensitivity: the estimated lower bound reaches zero at Γ ≈ 1.35.",
         fontsize=7.5, color=INK2, va="bottom")
fig.tight_layout(rect=(0, 0.065, 1, 1)); fig.savefig("fig4_robustness.png"); plt.close(fig)
