import pandas as pd

def process_sacco_data():
    # 1. Load the data
    loans = pd.read_csv("data/loans.csv")
    repayments = pd.read_csv("data/repayments.csv")

    # 2. Transform dates (Convert strings to datetime objects)
    loans["Issue_Date"] = pd.to_datetime(loans["Issue_Date"])
    repayments["Payment_Date"] = pd.to_datetime(repayments["Payment_Date"])

    # 3. Group repayments so we only have ONE row per loan
    # We want the total paid, and the date of their LAST payment
    repayments_grouped = repayments.groupby("Loan_ID").agg(
        Total_Paid=("Amount_Paid", "sum"),
        Last_Payment_Date=("Payment_Date", "max")
    ).reset_index()

    # 4. Merge the tables
    merged = pd.merge(loans, repayments_grouped, on="Loan_ID", how="left")

    # 5. Calculate Days to Repay
    # We only calculate this if they made a payment (hence the .dt.days from a timedelta)
    merged["Days_to_Repay"] = (merged["Last_Payment_Date"] - merged["Issue_Date"]).dt.days

    # 6. Flag if fully repaid within 90 days
    # Condition: Total_Paid >= Loan_Amount AND Days_to_Repay <= 90
    # (Handle NaNs by filling them with False)
    merged["Fully_Repaid_90d"] = (
        (merged["Total_Paid"] >= merged["Loan_Amount"]) & 
        (merged["Days_to_Repay"] <= 90)
    ).fillna(False)

    # 7. Extract Quarter from Issue_Date
    merged["Quarter"] = "Q" + merged["Issue_Date"].dt.quarter.astype(str)
    
    # Sort by quarter for readability
    merged = merged.sort_values("Quarter")

    return merged

if __name__ == "__main__":
    df = process_sacco_data()
    print("--- Transformed Data (First 10 rows) ---")
    print(df[["Loan_ID", "Issue_Date", "Loan_Amount", "Total_Paid", "Days_to_Repay", "Fully_Repaid_90d", "Quarter"]].head(10))
    
    # Save the processed data for the next step
    df.to_csv("data/processed_sacco_data.csv", index=False)
    print("\n✅ Processed data saved to 'processed_sacco_data.csv'")