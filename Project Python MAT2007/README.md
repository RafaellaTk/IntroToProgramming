# Stelar Property Discrimination

A quantitative astronomical data analysis project developed in Python to evaluate whether Absolute Magnitude (`Amag`) or Color Index (`B-V`) serves as the strongest statistical discriminator between Dwarf and Giant stars.

## Project Structure

```text
├── data/
│   └── stars.csv            # Hipparcos star catalog dataset
├── figures/
│   └── results_plot.png     # Generated Color-Magnitude & distribution plots
├── report/
│   └── report.tex           # Final LaTeX report (max 2 pages)
├── src/
│   └── analysis.py          # Main Python analysis script
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Scientific Question

Which observational parameter (Absolute Magnitude Amag or Color Index B-V) provides a stronger quantitative discrimination between Dwarf and Giant stars?

Dependencies

The project requires Python 3.9+ and the following libraries:

-pandas

-matplotlib

-scipy

Install dependencies by running the following command in the terminal:
pip install -r requirements.txt (for windows)

