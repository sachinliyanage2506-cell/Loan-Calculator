#-----------------------
#Business Loan Decision Support System
#Created By Student (u3334431)
#-----------------------

#Description:
"""
The following code is a business loan decision support system that
will help business owners calculate whether a loan is affordable based on the
loan_amount, interest rate, loan term, monthly income and monthly expenses.
"""


#List of Inputs loan amount, rate, term, income and expenses

#Imports the necessary tools to build a desktop application with a Graphical
#User Interface (GUI) and a local database.

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3





#Calculation Section


def calculate_loan (P, rate, years, income, expenses):
    """
    M = Monthly repayment
    P = Loan amount
    r = Monthly interest rate
    n = Total number of monthly repayments
    Convert annual interest rate to monthly interest rate
    If interest is 0 use simple formula, otherwise use standard formula
    Total repayment amount = total
    Total Interest = interest = total - P
    Monthly cash surplus = surplus
    If surplus>=0, status = Affordable, otherwise status = Not Affordable
    return statement: once calculate_loan does all its calculations, it
    hands the results (M, total, interest, surplus and status) back to on_calculate, so it can be displayed in the GUI 
    """



    r = rate / 1200 #Convert annual interest rate to monthly interest rate
    n = int(years * 12) # n = loan term in years, Total number of monthly payments

    #If interest is 0 use simple formula, otherwise use standard formula
    if rate == 0:
        M = P / n 
    
    else: 
        M = (P * r * ((1 + r) ** n)) / (((1+r) ** n) - 1)
        
    total = M * n               #Total repayment amount
    interest = total - P        #Total interest paid

    #Monthly cash surplus after paying the loan
    surplus = income - expenses - M

    #Determine affordability based on surplus
    if surplus >= 0:
        status = "Affordable"
    else:
        status = "Not Affordable"

    return M, total, interest, surplus, status

#Button Handlers

def on_calculate():
    """
    The following inputs,
    P = Loan amount
    rate = Monthly interest rate
    years = Loan term in years
    income = Monthly income
    expenses = Monthly expenses
    Validating inputs, (try/except catches non-numeric entries).
    For example, numbers such as 2000, 100 or 3 will be accepted, as for letters such as a, b, c, an error message will be displayed
    informing the user that these values are invalid, and must be re-entered correctly.
    Once all inputted values are valid, the calculation will run (M, total, interest, surplus, status = calculate_loan(
    P, rate, years, income, expenses)
    Monthly surplus status is displayed in the GUI with green (for affordable) or red (for unaffordable)
    Results are displayed in the GUI

    """
    
    # Validate inputs (try/except catches non-numeric entries)
    try:
        P = float(entry_loan.get())
        rate = float(entry_rate.get())
        years = float(entry_term.get())
        income = float(entry_income.get())
        expenses = float(entry_expenses.get())
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "These values are invalid, please try again. \n"
            "All fields must contain numbers."
    )
        return

    # Validate realistic values

    if P <= 0:
        messagebox.showerror("Invalid Input",
            "These values are invalid, please try again. \n"
            "Loan amount must be greater than 0.")
        return
    if rate < 0:
        messagebox.showerror("Invalid Input",
            "These values are invalid, please try again. \n"
            "Interest rate cannot be negative.")
        return

    if years <= 0:
        messagebox.showerror("Invalid Input",
            "These values are invalid, please try again. \n"
            "Loan term cannot be negative.")
        return
    
    if income < 0:
        messagebox.showerror("Invalid Input",
            "These values are invalid, please try again.\n"
            "Monthly income cannot be negative.")
        
        return
    if expenses < 0:
        messagebox.showerror("Invalid Input",
            "These values are invalid, please try again.\n"
            "Monthly Expenses cannot be negative.")

        return

    # Run Calculation

    try:
        M, total, interest, surplus, status = calculate_loan(
            P, rate, years, income, expenses
        )

    # If numbers are too large for the system to calculate then this error message will appear
    except OverflowError:
        messagebox.showerror("Calculation Error",
            "The values entered are too large to calculate.\n"
            "Please enter more realistic values.")
        return

    # Affordability check (Is monthly surplus >= 0?)

    if surplus >= 0:
        lbl_status_val.config(text = "Affordable", fg ="#2e7d32")
    else:
        lbl_status_val.config(text = "Not Affordable", fg ="#c62828")

    # Display all results in GUI

    lbl_monthly_val.config(text=f"${M:,.2f}")
    lbl_total_val.config(text=f"${total:,.2f}")
    lbl_interest_val.config(text=f"${interest:,.2f}")
    lbl_surplus_val.config(text=f"${surplus:,.2f}")

def on_save():
    """
    Activates when user clicks Save.
    If no inputs are written in, an error message box will appear, informing the user to "calculate before saving"
    Writes current results to loan_report.txt.
    If the results are saved, the message box informs the user that the results have been saved successfully to the loan report
    However, if the results could not be saved, an error message will appear, 'could not save file:'
    Returns to GUI once user clicks close, (waits for next button click).

    """

    if lbl_monthly_val.cget("text") == "-":
        messagebox.showwarning("No Results",
            "Please calculate first before saving.")
        return

    try:
        with open("loan_report.txt","a") as f:
            f.write("=" * 40 + "\n")
            f.write("==== Business Loan Report ====\n\n")
            f.write("=" * 40 + "\n\n")

            f.write("Inputs --\n")
            f.write("=" * 40 + "\n")
            f.write(f"Loan Amount:           ${float(entry_loan.get()):,.2f}\n")
            f.write(f"Annual Interest Rate:   {entry_rate.get()}%\n")
            f.write(f"Loan Term:              {entry_term.get()} years\n")
            f.write(f"Monthly Income:         ${float(entry_income.get()):,.2f}\n")
            f.write(f"Monthly Expenses:       ${float(entry_expenses.get()):,.2f}\n\n")
            f.write("=" * 40 + "\n\n")
            f.write("--Results--\n")
            f.write("=" * 40 + "\n")
            f.write(f"Monthly Repayment:     {lbl_monthly_val.cget('text')}\n")
            f.write(f"Total Repayment:       {lbl_total_val.cget('text')}\n")
            f.write(f"Total Interest Paid:   {lbl_interest_val.cget('text')}\n")
            f.write(f"Monthly Surplus:       {lbl_surplus_val.cget('text')}\n")
            f.write(f"Affordability:         {lbl_status_val.cget('text')}\n")
            f.write("=" * 40 + "\n")

        messagebox.showinfo("Saved", "Results saved to loan_report.txt")

    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")

def on_load():
    """
    Activates when user clicks Load.
    Reads previosuly saved results from loan_report.txt
    and displays the contents in a popup window.
    If the file cannot be found or user clicks load before saving, error message should appear.
    """
    try:
        with open("loan_report.txt", "r") as f:
            content = f.read()

        popup = tk.Toplevel(root)
        popup.title("Loaded Loan Report")
        popup.configure(bg="#0a0a0a")
        popup.resizable(True, True)

        tk.Label(popup, text="Saved Loan Report",
                 font=("Arial", 11, "bold"),
                 bg="#0a0a0a", fg="#00FF00", pady=8).pack()

        tk.Frame(popup, bg="#00FF00", height=2).pack(fill="x", padx=15)

        text_box = tk.Text(popup, font=("Courier", 9),
                           bg="#1a1a1a", fg="#00FF00",
                           width=50, height=20,
                           padx=10, pady=10)
        text_box.insert("1.0", content)
        text_box.config(state="disabled")
        text_box.pack(padx=15, pady=10)

        tk.Button(popup, text="Close", command=popup.destroy,
                  bg="#c62828", fg="white",
                  font=("Arial", 9, "bold"),
                  width=10).pack(pady=8)

    except FileNotFoundError:
        messagebox.showerror("File Not Found",
                             "No saved file found. Please click save first.")
            
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file:\n{e}")



def on_database():
    """
    Activates when user clicks Database.
    Creates two tables:
    loans: stores the user's inputs values (loan amount, rate, term, income, expenses)
    result: stores the calculated output values (monthly repayment, total repayment, total interest, surplus, affordability status)
    Inserts current inputs into loans table.
    Inserts current results into result table.
    Performs a multi-table JOIN query between loans and result tables.
    Performs aggregate queries (COUNT, AVG, SUM) on the joined tables.
    Display all records and aggregate summaries in a popup window.
    Returns to GUI (waits for next button click).
    To view saved records, open 'loan_record.db' in DB Browser for SQLite and select the 'Browse Data' tab.
    """

    try:
        # Connect and create table
        conn = sqlite3.connect("loan_record.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                loan_amount REAL,
                annual_rate REAL,
                loan_term   REAL,
                income      REAL,
                expenses    REAL
                
                
                
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS result (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                monthly_rep REAL,
                total_rep   REAL,
                total_int   REAL,
                surplus     REAL,
                status      TEXT        
                
            )
        """)

        
        # Insert current record
        if lbl_monthly_val.cget("text") != "-":
            cursor.execute("""
            INSERT INTO loans (loan_amount, annual_rate, loan_term, income, expenses
                               )

            VALUES (?, ?, ?, ?, ?)
        """, (
            float(entry_loan.get()),
            float(entry_rate.get()),
            float(entry_term.get()),
            float(entry_income.get()),
            float(entry_expenses.get())
        ))
            

            cursor.execute("""
            INSERT INTO result (
                               monthly_rep, total_rep,
                               total_int, surplus, status)

            VALUES (?, ?, ?, ?, ?)
        """, (
            float(lbl_monthly_val.cget("text").replace("$", "").replace(",", "")),
            float(lbl_total_val.cget("text").replace("$", "").replace(",", "")),
            float(lbl_interest_val.cget("text").replace("$", "").replace(",", "")),
            float(lbl_surplus_val.cget("text").replace("$", "").replace(",", "")),
            lbl_status_val.cget("text")
            
        ))

        
        conn.commit()

        if lbl_monthly_val.cget("text") != "-":
            messagebox.showinfo("Record Saved",
                                "Your loan record has been saved to the database.\n"
                                "Loading all saved records...")

        cursor.execute("SELECT * FROM loans")
        all_loans = cursor.fetchall()

        cursor.execute("SELECT * FROM result")
        all_results = cursor.fetchall()

        
        
         # Multi-table JOIN query
        # Joins loans and result tables to retrieve latest combined record
        cursor.execute("""
            SELECT
                loans.id,
                loans.loan_amount,
                result.monthly_rep,
                result.status
            FROM loans
            JOIN result ON loans.id=result.id
            ORDER BY loans.id DESC
            LIMIT 1
        """)
        join_result = cursor.fetchone()


        # Aggregate query
        # Uses COUNT, AVG, SUM aggregates on the loans table
        cursor.execute("""
            SELECT
                COUNT(*) AS total_records,
                AVG(result.monthly_rep) AS avg_monthly_rep,
                SUM(loan_amount) AS total_borrowed,
                SUM(CASE WHEN result.status = 'Affordable' THEN 1 ELSE 0 END)
                    AS affordable_count
            FROM loans
            JOIN result ON loans.id=result.id
        """)
        agg = cursor.fetchone()
 
        # Insert aggregate result text for display
        if agg and agg[0] > 0:
            stats_text = (f"Total Records: {agg[0]}  |  "
                          f"Avg Monthly Repayment: ${agg[1]:,.2f}  | "
                          f"Total Amount Borrowed: ${agg[2]:,.2f}  | "
                          f"Affordable Count: {agg[3]}")

        else:
            stats_text = "No aggregate data available."




        
        # Retrieve all records
        cursor.execute("SELECT loans.*,result.monthly_rep, result.total_rep, result.total_int, result.surplus, result.status FROM loans JOIN result ON loans.id=result.id")
        rows = cursor.fetchall()
        conn.close()

        # Display records in popup window
        popup = tk.Toplevel(root)
        popup.title("Loan Database Records")
        popup.resizable(True, True)

        tk.Label(popup, text="All Saved Loan Records",
                 font=("Arial", 8, "bold"), pady=8).pack()

        #Scrollable treeview table
        frame = tk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=10, pady=6)

        scroll_y = tk.Scrollbar(frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = tk.Scrollbar(popup, orient="horizontal")
        scroll_x.pack(fill="x", padx=10)

        cols = ("ID", "Loan $", "Rate %", "Term (yr)",
                "Income $", "Expenses $", "Monthly $",
                "Total $", "Interest $", "Surplus $", "Status")

        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            yscrollcommand=scroll_y.set,
                            xscrollcommand=scroll_x.set,
                            height=12)

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)

        #Column headings and widths
        widths = [35, 85, 65, 75, 85, 90, 85, 85, 85, 80, 105]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center", minwidth=w)


        #Insert each record as a row
        for row in rows:
            formatted = (
                row[0],
                f"${row[1]:,.2f}",
                f"{row[2]}%",
                f"{row[3]}",
                f"${row[4]:,.2f}",
                f"${row[5]:,.2f}",
                f"${row[6]:,.2f}",
                f"${row[7]:,.2f}",
                f"${row[8]:,.2f}",
                f"${row[9]:,.2f}",
                row[10]

            )
            tree.insert("", "end", values=formatted)

        tree.pack(fill="both", expand=True)

        summary_frame = tk.LabelFrame(popup, text=" Database Summary (Aggregates) ",
                                      font=('Arial', 9, "bold"), padx=10, pady=10)
        summary_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(summary_frame, text=stats_text, font=('Arial', 9),
                 fg="#006400").pack()
        

        #Show message if no records exist yet
        if not rows:
            tk.Label(popup, text="No records saved yet.",
                     font=("Arial", 10), pady=6).pack()

        tk.Button(popup, text="Close", command=popup.destroy,
                  bg="#c62828", fg="white",
                  font=("Arial", 9, "bold"),
                  width=10, pady=4).pack(pady=8)

    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")

def on_html():
    """
    Activates when user clicks HTML Report.
    Display error message when user clicks HTML without calculating anything
    
    Generates a formatted loan_report.html file
    Returns to GUI (waits for next button click).
    """

    if lbl_monthly_val.cget("text") == "-":
        messagebox.showwarning ("No Results",
                "Please calculate first before generating HTML.")
        return

    try:
        status = lbl_status_val.cget("text")
        colour = "#2e7d32" if status == "Affordable" else "#c62828"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Loan Report</title>
    <style>
        body     {{ font-family: Arial, sans-serif; max-width: 650px;
                    margin: 40px auto; color: #222;}}
        h1       {{ color: #2c4c3b; border-bottom: 3px solid #2c4c3b; padding-bottom: 8px; }}
        h2       {{ color: white; background: #2c4c3b; padding: 8px 14px;
                    border-radius: 6px; margin-top: 24px; }}
        table    {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td   {{ padding: 10px 14px; border: 1px solid #ddd; text-align: left; }}
        th       {{ background: #2c4c3b; color: white; }}
        tr:nth-child(even) {{ background: #f5f5f5 }}
        .status  {{ font-weight: bold; color: {colour}; }}
    </style>

</head>
<body>
    <h1>Business Loan Report</h1>
    <h2>Inputs</h2>
    <table>
    
        <tr><th>Field</th><th>Value</th></tr>
        <tr><td>Loan Amount</td><td>${float(entry_loan.get()):,.2f}</td></tr>
        <tr><td>Annual Interest Rate</td><td>{entry_rate.get()}%</td></tr>
        <tr><td>Loan Term</td><td>{entry_term.get()} years</td></tr>
        <tr><td>Monthly Income</td><td>${float(entry_income.get()):,.2f}</td></tr>
        <tr><td>Monthly Expenses</td><td>${float(entry_expenses.get()):,.2f}</td></tr>
    </table>

    <h2>Results</h2>
    <table>
        <tr><th>Field</th><th>Value</th></tr>
        <tr><td>Monthly Repayment</td><td>{lbl_monthly_val.cget('text')}</td></tr>
        <tr><td>Total Repayment</td><td>{lbl_total_val.cget('text')}</td></tr>
        <tr><td>Total Interest Paid</td><td>{lbl_interest_val.cget('text')}</td></tr>
        <tr><td>Monthly Surplus</td><td>{lbl_surplus_val.cget('text')}</td></tr>
        <tr><td>Affordability</td><td class="status">{status}</td></tr>
    </table>

</body>
</html>"""

        with open("loan_report.html", "w") as f:
            f.write(html)

        messagebox.showinfo("HTML Report",
            "loan_report.html has been generated successfully. Find in, C:\\Users\\sachi\\OneDrive\\Desktop\\The Final IIT Database Assignment")

    except Exception as e:
        messagebox.showerror("Error", f"Could not generate HTML:\n{e}")

def on_clear():
    """
    Activates when user clicks Clear.
    Resets all input fields and result labels,
    then returns focus to the first input field (back to input step).
    """
    entry_loan.delete(0, tk.END)
    entry_rate.delete(0, tk.END)
    entry_term.delete(0, tk.END)
    entry_income.delete(0, tk.END)
    entry_expenses.delete(0, tk.END)

    lbl_monthly_val.config(text="-")
    lbl_total_val.config(text="-")
    lbl_interest_val.config(text="-")
    lbl_surplus_val.config(text="-")
    lbl_status_val.config(text="-", fg="#333333")


    #Return focus to first input field (back to input step in flowchart)

    entry_loan.focus()

def on_exit():
    """
Activated when user clicks Exit.
Closes the program and ends execution
    """

    root.destroy()

# GUI Layout

"""
Displays the visual elements seen in the GUI
GUI depicts appropriate title
User can only move the window but they cannot horizontally or vertically resize it
Input/Results section incorporating headings and labels
"""

root = tk.Tk()
root.title("Business Loan Decision Support System")
root.resizable(False, False)
root.configure(bg="#0a0a0a")

PADX = 12
PADY = 6

#Title
tk.Label(root,
         text="Business Loan Decision Support System",
         font=("Helvetica", 14, "bold"),
         bg="#0a0a0a",
         fg="#00FF00").grid(row=0, column=0, columnspan=2, padx=PADX, pady=(15,5))

#Input Section Heading
tk.Label(root, text="--- Inputs ---",
        font= ("Arial", 10, "bold"),
        bg="#0a0a0a",
        fg="#00FF00").grid(row=1, column=0, columnspan=2, pady=(4, 2))

#A list storing the label text and which row to put it in
input_fields = [
    ("Loan Amount ($):",                2),
    ("Annual Interest Rate (%):",       3),
    ("Loan Term (years):",              4),
    ("Monthly Income ($):",             5),
    ("Monthly Expenses ($):",           6),
]

for text, row in input_fields:
    tk.Label(root, text=text, anchor="w",
             bg="#0a0a0a",
             fg="white").grid(row=row, column=0, sticky="w", padx=PADX, pady=PADY)

#Input entry boxes that allow the user to type in values
    
entry_loan      = tk.Entry(root, width=30, bg="#1a1a1a", fg="#00FF00",
                           insertbackground="#00FF00", relief="flat",
                           highlightthickness=1, highlightcolor="#00FF00",
                           highlightbackground="#333333")
entry_rate      = tk.Entry(root, width=30, bg="#1a1a1a", fg="#00FF00",
                           insertbackground="#00FF00", relief="flat",
                           highlightthickness=1, highlightcolor="#00FF00",
                           highlightbackground="#333333")
entry_term      = tk.Entry(root, width=30, bg="#1a1a1a", fg="#00FF00",
                           insertbackground="#00FF00", relief="flat",
                           highlightthickness=1, highlightcolor="#00FF00",
                           highlightbackground="#333333")
entry_income    = tk.Entry(root, width=30, bg="#1a1a1a", fg="#00FF00",
                           insertbackground="#00FF00", relief="flat",
                           highlightthickness=1, highlightcolor="#00FF00",
                           highlightbackground="#333333")
entry_expenses  = tk.Entry(root, width=30, bg="#1a1a1a", fg="#00FF00",
                           insertbackground="#00FF00", relief="flat",
                           highlightthickness=1, highlightcolor="#00FF00",
                           highlightbackground="#333333")
#enumerate displays both the position number (i) and the item (entry) at the same time.
for i, entry in enumerate(
        [entry_loan, entry_rate, entry_term, entry_income, entry_expenses]):
    entry.grid(row=i + 2, column=1, padx=PADX, pady=PADY, sticky="ew")

# Results Section Heading
tk.Label(root, text="--Results--",
         font=("Arial", 10, "bold"),
         bg="#0a0a0a",
         fg="#00FF00").grid(row=7, column=0, columnspan=2, pady=(15,5))

result_fields = [
    ("Monthly Repayment:",          8),
    ("Total Repayment:",            9),
    ("Total Interest Paid:",        10),
    ("Monthly Surplus:",            11),
    ("Affordability Status:",       12),
]

for text, row in result_fields:
    tk.Label(root, text=text, anchor="w",
    bg="#0a0a0a",
    fg="white").grid(row=row, column=0, sticky="w", padx=PADX, pady=PADY)

#Output boxes that display output values
lbl_monthly_val = tk.Label(root, text="-", anchor="w", width=20,
                           relief="flat", bg="#1a1a1a", fg="#00FF00",
                           highlightthickness=1, highlightbackground="#333333")
lbl_total_val   = tk.Label(root, text="-", anchor="w", width=20,
                           relief="flat", bg="#1a1a1a", fg="#00FF00",
                           highlightthickness=1, highlightbackground="#333333")
lbl_interest_val = tk.Label(root, text="-", anchor="w", width=20,
                           relief="flat", bg="#1a1a1a", fg="#00FF00",
                           highlightthickness=1, highlightbackground="#333333")
lbl_surplus_val = tk.Label(root, text="-", anchor="w", width=20,
                           relief="flat", bg="#1a1a1a", fg="#00FF00",
                           highlightthickness=1, highlightbackground="#333333")
lbl_status_val  = tk.Label(root, text="-", anchor="w", width=20,
                           relief="flat", bg="#1a1a1a", fg="#00FF00",
                           highlightthickness=1, highlightbackground="#333333",
                           font=("Helvetica", 9, "bold"))

#enumerate displays both the position number (i) and the item (lbl) at the same time.
for i, lbl in enumerate ([lbl_monthly_val, lbl_total_val,
                            lbl_interest_val, lbl_surplus_val, lbl_status_val]):
    lbl.grid(row=i + 8, column=1, padx=PADX, pady=PADY, sticky="ew")

#Buttons
btn_frame = tk.Frame(root, bg="#0a0a0a")
btn_frame.grid(row=13, column=0, columnspan=2, pady=14)

buttons = [
    ("Calculate", on_calculate, "#00FF00", "#0a0a0a"),
    ("Save", on_save, "#00FF00", "#0a0a0a"),
    ("Load", on_load, "#00FF00", "#0a0a0a"),
    ("Database", on_database, "#00FF00", "#0a0a0a"),
    ("HTML", on_html, "#00FF00", "#0a0a0a"),
    ("Clear", on_clear, "#00FF00", "#0a0a0a"),
    ("Exit", on_exit, "#FF0000", "white"),
]

for i, (text, cmd, bg, fg) in enumerate(buttons):
    tk.Button(btn_frame, text=text, command=cmd,
              bg=bg, fg=fg, width=9,
              activebackground="#005500",
              activeforeground="#00FF00",
              relief="flat",
              font=("Arial", 9, "bold")).grid(
              row=0, column=i, padx=4)

#Start the program
root.mainloop()

    
    

                           

            
            

        



