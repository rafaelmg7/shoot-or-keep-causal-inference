"""Abstract Figure 1 (v6): raw gap vs adjusted ATT, and how the interval moves under other
uncertainty choices. Sources: confirmation/submission_results.json (point, bootstrap, analyses
visible_disk5), tier12_posthoc/tier1/dependence.csv, development phase result (Euro)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8984"
INK, INK2, GRID = "#1f1f1e", "#5f5e58", "#e4e3dd"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.5), dpi=200, width_ratios=(1, 1.9))
fig.set_facecolor("white")

# (a) raw association vs adjusted effect (World Cup, held out)
a.bar([0], [8.44], width=0.55, color=GREY)
a.bar([1], [3.08], width=0.55, color=ORANGE)
a.errorbar([1], [3.08], yerr=[[3.08 - 0.67], [5.48 - 3.08]], fmt="none", ecolor=INK, lw=1.2, capsize=4)
a.text(0, 8.44 + 0.3, "+8.4", ha="center", fontsize=9, color=INK)
a.text(1, 5.48 + 0.3, "+3.1", ha="center", fontsize=9, color=INK)
a.set_xticks([0, 1], ["Raw gap\n(no adjustment)", "Adjusted\neffect"], color=INK)
a.set_ylim(0, 10); a.set_ylabel("Percentage points")
a.set_title("a. World Cup: raw vs adjusted", loc="left", fontsize=10, color=INK)
a.grid(axis="y", color=GRID, lw=0.8); a.set_axisbelow(True)
for s in ("top", "right"): a.spines[s].set_visible(False)

# (b) intervals under alternative uncertainty choices and samples
rows = [("Primary: clustered by match", 3.08, 0.67, 5.48, ORANGE),
        ("Bootstrap, frozen design*", 3.08, 0.29, 5.61, ORANGE),
        ("Clustered by team", 3.08, 0.41, 5.74, ORANGE),
        ("Clustered by opponent", 3.08, -0.28, 6.43, ORANGE),
        ("Team and opponent", 3.08, -0.22, 6.37, ORANGE),
        ("Stricter 5 m visibility", 2.26, -0.47, 5.00, ORANGE),
        ("Euro (development)", 1.77, -0.22, 3.76, BLUE)]
for i, (lab, est, lo, hi, col) in enumerate(rows):
    y = i + (0.5 if i >= 5 else 0)
    b.plot([lo, hi], [y, y], color=col, lw=2, solid_capstyle="round", zorder=2)
    b.scatter([est], [y], s=36, color=col, edgecolor="white", linewidth=1.5, zorder=3)
    b.text(6.9, y, f"{lo:+.1f} to {hi:+.1f}", va="center", fontsize=8, color=INK2)
b.axhline(4.75, color=GRID, lw=0.8)
b.axvline(0, color=INK2, lw=1, zorder=1)
b.set_yticks([i + (0.5 if i >= 5 else 0) for i in range(len(rows))], [r[0] for r in rows], color=INK)
b.invert_yaxis(); b.set_xlim(-1.5, 8.6)
b.set_xlabel("Effect of shooting (pp, 95% interval)")
b.set_title("b. How the interval changes", loc="left", fontsize=10, color=INK)
b.grid(axis="x", color=GRID, lw=0.8); b.set_axisbelow(True)
for s in ("top", "right", "left"): b.spines[s].set_visible(False)

fig.text(0.01, 0.015, "Net scoring rate: first goal within 15 s (+1 scored, -1 conceded). "
         "*Refits nuisance models with design fixed; 489 of 500 draws failed a diagnostic.",
         fontsize=7, color=INK2)
fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig("fig5_estimate_and_uncertainty.png")
