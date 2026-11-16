"""
SACCO Loan Portfolio Report
---------------------------
Generates the quarterly summary table, charts, and findings.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_report():
    # Load the processed data
    df = pd.read_csv("data/processed_sacco_data.csv")
    
    # Convert Quarter to categorical so it plots in order (Q1, Q2, Q3, Q4)
    df["Quarter"] = pd.Categorical(df["Quarter"], categories=["Q1", "Q2", "Q3", "Q4"], ordered=True)

    # --- 1. QUARTERLY REPAYMENT TABLE ---
    # Group by Quarter and calculate the mean of the boolean column
    quarterly_summary = df.groupby("Quarter")["Fully_Repaid_90d"].mean() * 100
    quarterly_summary = quarterly_summary.round(1).reset_index()
    quarterly_summary.columns = ["Quarter", "Repayment_Rate_90d (%)"]

    print("=" * 50)
    print(" 📊 QUARTERLY REPAYMENT RATE (WITHIN 90 DAYS) 📊 ")
    print("=" * 50)
    print(quarterly_summary.to_string(index=False))
    print("=" * 50)

    # Save table to CSV for the client
    quarterly_summary.to_csv("data/quarterly_summary.csv", index=False)

    # --- 2. CHARTS ---
    sns.set_theme(style="whitegrid")

    # Chart 1: Quarterly Repayment Rate (Bar Chart)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=quarterly_summary, x="Quarter", y="Repayment_Rate_90d (%)", color="#4facfe")
    plt.title("Percentage of Loans Fully Repaid within 90 Days", fontsize=14, fontweight="bold")
    plt.ylabel("Repayment Rate (%)")
    plt.ylim(0, 100)
    plt.savefig("charts/chart1_quarterly_rate.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Chart 2: Distribution of Days to Repay (Histogram)
    # We filter out the defaults (NaNs) to see the distribution of actual payers
    payers = df.dropna(subset=["Days_to_Repay"])
    plt.figure(figsize=(8, 5))
    sns.histplot(payers["Days_to_Repay"], bins=20, color="#ff6b6b", kde=True)
    plt.axvline(90, color="black", linestyle="--", label="90-Day Target")
    plt.title("Distribution of Days to Repay", fontsize=14, fontweight="bold")
    plt.xlabel("Days to Repay")
    plt.ylabel("Number of Loans")
    plt.legend()
    plt.savefig("charts/chart2_days_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Chart 3: Loan Amount vs. Days to Repay (Scatter Plot)
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=payers, x="Loan_Amount", y="Days_to_Repay", alpha=0.6, color="darkblue")
    plt.title("Loan Amount vs. Days to Repay", fontsize=14, fontweight="bold")
    plt.xlabel("Loan Amount (KES)")
    plt.ylabel("Days to Repay")
    plt.savefig("charts/chart3_amount_vs_days.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("✅ Charts saved successfully (chart1, chart2, chart3).")

if __name__ == "__main__":
    generate_report()