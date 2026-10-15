import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# Load the CSV table into a DataFrame
data = pd.read_csv("data/stars.csv")

# Clean missing entries in key columns
data = data.dropna(subset=["Amag", "B-V", "TargetClass"])

# Split into Giants (TargetClass == 0) and Dwarfs (TargetClass == 1)
giants = data[data["TargetClass"] == 0]
dwarfs = data[data["TargetClass"] == 1]


def run_statistical_analysis(parameter_name):
    # Separate the values for both star groups
    g_values = giants[parameter_name]
    d_values = dwarfs[parameter_name]

    # Descriptive statistics: mean, standard deviation, and sample size
    mean_g = np.mean(g_values)
    std_g = np.std(g_values)
    n_g = len(g_values)

    mean_d = np.mean(d_values)
    std_d = np.std(d_values)
    n_d = len(d_values)

    # Welch's two-sample t-test (handles unequal variances between groups)
    t_stat, p_value = stats.ttest_ind(g_values, d_values, equal_var=False)

    # Standardized Difference: difference in means divided by the average standard deviation
    # This places both parameters on the same unitless scale to compare them directly
    mean_diff = abs(mean_g - mean_d)
    avg_spread = (std_g + std_d) / 2
    standardized_separation = mean_diff / avg_spread

    return {
        "name": parameter_name,
        "mean_g": mean_g,
        "std_g": std_g,
        "mean_d": mean_d,
        "std_d": std_d,
        "t_stat": t_stat,
        "p_value": p_value,
        "separation": standardized_separation
    }

# Compute statistics for Absolute Magnitude and Color Index
amag_stats = run_statistical_analysis("Amag")
bv_stats = run_statistical_analysis("B-V")


print(" STATISTICAL COMPARISON ")
for res in [amag_stats, bv_stats]:
    print(f"Parameter: {res['name']}")
    print(f"  Giants Mean +/- SD: {res['mean_g']:.3f} +/- {res['std_g']:.3f}")
    print(f"  Dwarfs Mean +/- SD: {res['mean_d']:.3f} +/- {res['std_d']:.3f}")
    print(f"  t-statistic:        {res['t_stat']:.3f}")
    print(f"  p-value:            {res['p_value']:.4e}")
    print(f"  Separation Score:   {res['separation']:.3f} standard deviations")
    print("-" * 56)

# Determine the winner quantitatively
if amag_stats["separation"] > bv_stats["separation"]:
    ratio = amag_stats["separation"] / bv_stats["separation"]
    winner = "Absolute Magnitude (Amag)"
else:
    ratio = bv_stats["separation"] / amag_stats["separation"]
    winner = "Color Index (B-V)"

print(f"Conclusion: {winner} is the stronger statistical discriminator.")
print(f"Its standardized separation is {ratio:.2f}x greater between classes.")


import os

# Create the folder if it doesn't already exist
output_dir = "figures/plot results"
os.makedirs(output_dir, exist_ok=True)

# ----------------- Plot 1: Histogram of Absolute Magnitude -----------------
plt.figure(figsize=(8, 5))
plt.hist(giants["Amag"], bins=30, alpha=0.6, label="Giants (Class 0)", color="crimson")
plt.hist(dwarfs["Amag"], bins=30, alpha=0.6, label="Dwarfs (Class 1)", color="royalblue")
plt.title(f"Amag Separation Score: {amag_stats['separation']:.2f} SD")
plt.xlabel("Absolute Magnitude (Amag)")
plt.ylabel("Star Count")
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/amag_histogram.png", dpi=300)
plt.close()

# ----------------- Plot 2: Histogram of Color Index ------------------------
plt.figure(figsize=(8, 5))
plt.hist(giants["B-V"], bins=30, alpha=0.6, label="Giants (Class 0)", color="crimson")
plt.hist(dwarfs["B-V"], bins=30, alpha=0.6, label="Dwarfs (Class 1)", color="royalblue")
plt.title(f"B-V Separation Score: {bv_stats['separation']:.2f} SD")
plt.xlabel("Color Index (B-V)")
plt.ylabel("Star Count")
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/bv_histogram.png", dpi=300)
plt.close()

# ----------------- Plot 3: Observational HR Diagram ------------------------
plt.figure(figsize=(8, 5))
plt.scatter(giants["B-V"], giants["Amag"], color="crimson", alpha=0.3, s=12, label="Giants")
plt.scatter(dwarfs["B-V"], dwarfs["Amag"], color="royalblue", alpha=0.3, s=12, label="Dwarfs")
plt.title("Hertzsprung-Russell (HR) Diagram")
plt.xlabel("Color Index (B-V)")
plt.ylabel("Absolute Magnitude (Amag)")
plt.gca().invert_yaxis()
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/hr_diagram.png", dpi=300)
plt.close()

# ----------------- Plot 4: Error Bar / Separation Plot --------------------
fig, ax = plt.subplots(figsize=(8, 5))
ax2 = ax.twinx()

# Plot Amag (left axis)
ax.errorbar(
    0.8, amag_stats["mean_g"], yerr=amag_stats["std_g"], 
    fmt='o', color='crimson', ecolor='crimson', capsize=5, markersize=8, label="Giants (Amag)"
)
ax.errorbar(
    1.2, amag_stats["mean_d"], yerr=amag_stats["std_d"], 
    fmt='s', color='royalblue', ecolor='royalblue', capsize=5, markersize=8, label="Dwarfs (Amag)"
)
ax.set_ylabel("Absolute Magnitude (Amag)", color='crimson')
ax.invert_yaxis()

# Plot B-V (right axis)
ax2.errorbar(
    1.8, bv_stats["mean_g"], yerr=bv_stats["std_g"], 
    fmt='o', color='darkred', ecolor='darkred', capsize=5, markersize=8, label="Giants (B-V)"
)
ax2.errorbar(
    2.2, bv_stats["mean_d"], yerr=bv_stats["std_d"], 
    fmt='s', color='darkblue', ecolor='darkblue', capsize=5, markersize=8, label="Dwarfs (B-V)"
)
ax2.set_ylabel("Color Index (B-V)", color='darkblue')

ax.set_xticks([1.0, 2.0])
ax.set_xticklabels([
    f"Amag\n({amag_stats['separation']:.2f} SD)", 
    f"B-V\n({bv_stats['separation']:.2f} SD)"
])
ax.set_title("Mean ± 1 SD Comparison")
ax.set_xlim(0.4, 2.6)
plt.tight_layout()
plt.savefig(f"{output_dir}/separation_errorbars.png", dpi=300)
plt.close()