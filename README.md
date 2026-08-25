# Loan-Calculator

Introduction: A desktop GUI application built with Python and Tkinter that assist business owners determine whether a loan is affordable. Simply input the loan amount, interest rate, term, income and expenses, and the software calculates the monthly repayment, total interest and cash surplus. Then stores the results in a report and a local database for future reference.

Features:
- Loan Affordability Calculation - computes monthly repayments, total repayment, total interest paid, and monthly cash surplus using established formulas
- Input Validation - Rejects unrealistic values, such as negative income, zero loan term, etc) with clear error messages
- Save to Text Report - appends a formatted summary of each calculation to loan.report.txt
- Load Previous Report - view the saved text report
- SQLite Database Logging - stores every calculation in loan_record.db across two related tables (loans and results)
- Aggregate Insights - view total records, average monthly repayment, total amount borrowed, and count of affordable loans, calculated straight from the database with COUNT, AVG, and SUM
- HTML Report Export - generates a styled loan_report.html, summary of your inputs and results
- Clear & Reset, instantly clears all inputs and outputs when pressing the clear button

Possible Future Improvements
- Add support for comparing multiple loan scenarios side by side
- Export database records directly to CSV/Excel

Author
- Sachin Liyanage

License 
- This project is available for educational and personal use
