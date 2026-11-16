"""
SACCO Data Generator
--------------------
Creates two related tables: loans and repayments.
"""
import pandas as pd
import numpy as np
from datetime import timedelta

def generate_data():
    np.random.seed(42)
    
    # 1. Create 100 Loans over 12 months (2025)
    loan_ids = [f"LN-{i:04d}" for i in range(1, 101)]
    start_date = pd.Timestamp("2025-01-01")
    
    # Random issue dates over 2025
    issue_dates = [start_date + timedelta(days=int(x)) for x in np.random.randint(0, 365, 100)]
    # Random amounts (mostly 10k-100k)
    amounts = np.random.randint(10000, 100000, 100)
    
    loans_df = pd.DataFrame({
        "Loan_ID": loan_ids,
        "Issue_Date": issue_dates,
        "Loan_Amount": amounts
    })

    # 2. Create Repayments
    repayments = []
    for i, row in loans_df.iterrows():
        loan_id = row["Loan_ID"]
        issue_date = row["Issue_Date"]
        amount = row["Loan_Amount"]
        
        # Simulate: 60% fully repay within 90 days, 20% take longer, 20% default (unpaid)
        scenario = np.random.choice(["fast", "slow", "default"], p=[0.6, 0.2, 0.2])
        
        if scenario == "fast":
            repay_days = np.random.randint(30, 90)
            repay_date = issue_date + timedelta(days=repay_days)
            repayments.append({"Loan_ID": loan_id, "Payment_Date": repay_date, "Amount_Paid": amount})
        elif scenario == "slow":
            repay_days = np.random.randint(91, 200)
            repay_date = issue_date + timedelta(days=repay_days)
            repayments.append({"Loan_ID": loan_id, "Payment_Date": repay_date, "Amount_Paid": amount})
        else:
            # Partial payment for defaults
            repayments.append({"Loan_ID": loan_id, "Payment_Date": issue_date + timedelta(days=30), "Amount_Paid": amount * 0.5})
            
    repayments_df = pd.DataFrame(repayments)

    # Save to CSV
    loans_df.to_csv("loans.csv", index=False)
    repayments_df.to_csv("repayments.csv", index=False)
    print("✅ Generated loans.csv and repayments.csv")

if __name__ == "__main__":
    generate_data()