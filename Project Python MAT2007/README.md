# Stellar Property Discrimination: Dwarfs vs. Giants

A quantitative astronomical data analysis project developed in Python to evaluate whether **Absolute Magnitude ($Amag$)** or **Color Index ($B-V$)** serves as the stronger statistical discriminator between Dwarf and Giant stars.

---

## Scientific Question

> **Which observational parameter—Absolute Magnitude ($Amag$) or Color Index ($B-V$)—provides stronger quantitative separation between Dwarf and Giant stars?**

The analysis performs descriptive statistics, two-sample Welch's t-tests, and computes standardized separation metrics across both parameters using observational data from the Hipparcos catalog.

---

## Project Structure

```text
├── data/
│   └── stars.csv               # Hipparcos star catalog dataset
├── figures/
│   └── plot results/           # Generated statistical & distribution plots
│       ├── amag_histogram.png
│       ├── bv_histogram.png
│       ├── hr_diagram.png
│       └── separation_errorbars.png
├── report/
│   └── report.tex              # Final LaTeX report (max 2 pages)
├── src/
│   └── analysis.py             # Main statistical analysis and plotting script
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
