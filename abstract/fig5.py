"""Abstract Figure 1 (v7): World Cup raw gap vs adjusted effect of shooting.
Sources: confirmation/submission_results.json (point: observed 10.75%, continuation 7.67%,
ATT 3.08, match-cluster interval 0.67-5.48); raw gap 8.44 from the estimator comparison."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ORANGE, GREY, INK, INK2, GRID = "#eb6834", "#8a8984", "#1f1f1e", "#5f5e58", "#e4e3dd"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig, a = plt.subplots(figsize=(4.6, 3.4), dpi=200)
fig.set_facecolor("white"); a.set_facecolor("white")
a.bar([0], [8.44], width=0.55, color=GREY)
a.bar([1], [3.08], width=0.55, color=ORANGE)
a.errorbar([1], [3.08], yerr=[[3.08 - 0.67], [5.48 - 3.08]], fmt="none", ecolor=INK, lw=1.2, capsize=5)
a.text(0, 8.44 + 0.3, "+8.4", ha="center", fontsize=9.5, color=INK)
a.text(1.33, 3.08, "+3.1\n(0.7 to 5.5)", va="center", fontsize=8.5, color=INK)
a.set_xticks([0, 1], ["Raw gap\n(no adjustment)", "Adjusted effect\n(95% CI)"], color=INK)
a.set_xlim(-0.5, 1.75); a.set_ylim(0, 10)
a.set_ylabel("Net scoring rate, shot minus keep (pp)")
a.set_title("World Cup 2022 (held out)", loc="left", fontsize=10.5, color=INK)
a.grid(axis="y", color=GRID, lw=0.8); a.set_axisbelow(True)
for s in ("top", "right"): a.spines[s].set_visible(False)
fig.text(0.01, 0.01, "Adjusted: 10.7% after shots vs 7.7% estimated had the same players kept the ball.",
         fontsize=6.8, color=INK2)
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig("fig5_estimate_and_uncertainty.png")
