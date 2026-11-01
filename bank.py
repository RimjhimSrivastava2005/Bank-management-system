import os
import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Bank:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management")

        # Get screen width and height
        scrn_width = self.root.winfo_screenwidth()
        scrn_height = self.root.winfo_screenheight()

        # Set the window size to be the full screen
        self.root.geometry(f"{scrn_width}x{scrn_height}+0+0")

        # Label for the main heading
        main_label = tk.Label(self.root, text="Bank Account Management System", font=("Arial", 40, "bold"), bg="light green", bd=5, relief="groove")
        main_label.pack(side="top", fill="x")

        # Main frame for buttons
        mainFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="ridge")
        mainFrame.place(x=400, y=90, width=450, height=550)


        # Buttons for different actions
        openAcBtn = tk.Button(mainFrame, command=self.openAc, width=20, text="Open Account", bg="light blue", bd=3, relief="raised", font=("Arial", 20, "bold"))
        openAcBtn.grid(row=0, column=0, padx=40, pady=70)

        depBtn = tk.Button(mainFrame, command=self.deposit, width=20, text="Deposit", bg="light blue", bd=3, relief="raised", font=("Arial", 20, "bold"))
        depBtn.grid(row=1, column=0, padx=40, pady=70)

        wdBtn = tk.Button(mainFrame, width=20, command=self.wd,text="Withdraw", bg="light blue", bd=3, relief="raised", font=("Arial", 20, "bold"))
        wdBtn.grid(row=2, column=0, padx=40, pady=70)

    def openAc(self):
        # Create a new frame to open account
        self.openAcFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="ridge")
        self.openAcFrame.place(x=400, y=90, width=450, height=550)

        # Username label and input field
        uNameLabel = tk.Label(self.openAcFrame, text="User Name:", bg="light gray", font=("Arial", 15, "bold"))
        uNameLabel.grid(row=0, column=0, padx=20, pady=30)
        self.uNameIn = tk.Entry(self.openAcFrame, width=15, font=("Arial", 15))
        self.uNameIn.grid(row=0, column=1, padx=5, pady=30)

        uPWLabel = tk.Label(self.openAcFrame, text="Enter Password:", bg="light gray", font=("Arial", 15, "bold"))
        uPWLabel.grid(row=1, column=0, padx=20, pady=30)
        self.uPWIn = tk.Entry(self.openAcFrame, width=15, font=("Arial", 15))
        self.uPWIn.grid(row=1, column=1, padx=5, pady=30)

        confirmLabel = tk.Label(self.openAcFrame, text="Confirm Password:", bg="light gray", font=("Arial", 15, "bold"))
        confirmLabel.grid(row=2, column=0, padx=5, pady=30)
        self.confirmIn = tk.Entry(self.openAcFrame, width=15, font=("Arial", 15, "bold"))
        self.confirmIn.grid(row=2, column=1, padx=5, pady=30)

        # OK button
        okBtn = tk.Button(self.openAcFrame, command=self.insert, text="Ok", width=10, bg="light blue", bd=3, relief="raised", font=("Arial", 15, "bold"))
        okBtn.grid(row=3, column=0, padx=40, pady=120)

        # Close button
        closeBtn = tk.Button(self.openAcFrame, command=self.close_openAc, text="Close", width=10, bg="light blue", bd=3, relief="raised", font=("Arial", 15, "bold"))
        closeBtn.grid(row=3, column=1, padx=40, pady=120)

    def close_openAc(self):
        self.openAcFrame.destroy()

    def insert(self):
        uName = self.uNameIn.get()
        uPW = self.uPWIn.get()
        confirm = self.confirmIn.get()

        if uPW == confirm:
            con = mysql.connector.connect(host="localhost", user="root", passwd=os.getenv("DB_PASSWORD"), database="bankdb")
            cur = con.cursor()
            cur.execute("Insert into account(userName, userPW) values(%s, %s)", (uName, uPW))
            con.commit()
            con.close()
            tk.messagebox.showinfo("Success", "Account Opened Successfully!")
            self.clear()
        else:
            tk.messagebox.showerror("Error", "Both passwords should be the same!")
            self.clear()

    def clear(self):
        self.uNameIn.delete(0, tk.END)
        self.uPWIn.delete(0, tk.END)
        self.confirmIn.delete(0, tk.END)

    def deposit(self):
        # Create a new frame for deposit
        self.depFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="ridge")
        self.depFrame.place(x=400, y=90, width=450, height=550)

        # Username label and input field for deposit
        NameLabel = tk.Label(self.depFrame, text="User Name:", bg="light gray", font=("Arial", 15, "bold"))
        NameLabel.grid(row=0, column=0, padx=20, pady=30)
        self.depUNameIn = tk.Entry(self.depFrame, width=15, font=("Arial", 15))
        self.depUNameIn.grid(row=0, column=1, padx=5, pady=30)

        # Amount label and input field for deposit
        amountLabel = tk.Label(self.depFrame, text="Enter Amount:", bg="light gray", font=("Arial", 15, "bold"))
        amountLabel.grid(row=1, column=0, padx=20, pady=30)
        self.amountIn = tk.Entry(self.depFrame, width=15, font=("Arial", 15))
        self.amountIn.grid(row=1, column=1, padx=5, pady=30)

        # OK button for deposit
        OKBtn = tk.Button(self.depFrame, command=self.deposit_fun, text="Deposit", width=10, bg="light blue", bd=3, relief="raised", font=("Arial", 15, "bold"))
        OKBtn.grid(row=2, column=0, padx=40, pady=120)

        # Close button for deposit
        closeBtn = tk.Button(self.depFrame, command=self.close_dep, text="Close", width=10, bg="light blue", bd=3, relief="raised", font=("Arial", 15, "bold"))
        closeBtn.grid(row=2, column=1, padx=40, pady=120)

    def deposit_fun(self):
        uName = self.depUNameIn.get()
        amount = int(self.amountIn.get())

        con = mysql.connector.connect(host="localhost", user="root",passwd=os.getenv("DB_PASSWORD"), database="bankdb")
        cur = con.cursor()
        cur.execute("select balance from account where userName=%s", (uName,))
        data = cur.fetchone()
        if data:
            balance = data[0]
            if data[0] is None:
                balance=0
            update = balance + amount
            cur.execute("update account set balance=%s where userName=%s", (update, uName))
            con.commit()
            con.close()
            tk.messagebox.showinfo("Success", "Operation Was Successfull!")
        else:
            tk.messagebox.showerror("Error", "Invalid Customer Name!")

    def close_dep(self):
        self.depFrame.destroy()

    def wd(self):
        self.wdFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="ridge")
        self.wdFrame.place(x=400, y=90, width=450, height=550)

        cNameLabel = tk.Label(self.wdFrame, text="User Name:", bg="light gray", font=("Arial", 15, "bold"))
        cNameLabel.grid(row=0, column=0, padx=20, pady=30)
        self.cNameIn = tk.Entry(self.wdFrame, width=15, font=("Arial", 15))
        self.cNameIn.grid(row=0, column=1, padx=5, pady=30)

        cPWLabel = tk.Label(self.wdFrame, text="Enter Password:", bg="light gray", font=("Arial", 15, "bold"))
        cPWLabel.grid(row=1, column=0, padx=20, pady=30)
        self.cPWIn = tk.Entry(self.wdFrame, width=15, font=("Arial", 15))
        self.cPWIn.grid(row=1, column=1, padx=5, pady=30)

        wdLabel = tk.Label(self.wdFrame, text="Enter Amount:", bg="light gray", font=("Arial", 15, "bold"))
        wdLabel.grid(row=2, column=0, padx=5, pady=30)
        self.wdIn = tk.Entry(self.wdFrame, width=15, font=("Arial", 15, "bold"))
        self.wdIn.grid(row=2, column=1, padx=5, pady=30)

        # OK button for withdrawal
        okBtn = tk.Button(self.wdFrame, command=self.wd_fun, text="Withdraw", width=10, bg="light blue", bd=3, relief="raised", font=("Arial", 15, "bold"))
        okBtn.grid(row=3, column=0, padx=40, pady=120)

        # Close button for withdrawal
        closeBtn = tk.Button(self.wdFrame, command=self.close_wd, text="Close", width=10, bg="light blue", bd=3, relief="raised", font=("Arial", 15, "bold"))
        closeBtn.grid(row=3, column=1, padx=40, pady=120)

    def wd_fun(self):
        name = self.cNameIn.get()
        pw = self.cPWIn.get()
        amount = float(self.wdIn.get())

        con = mysql.connector.connect(host="localhost", user="root", passwd="rimjhimsrivastava@123", database="bankdb")
        cur = con.cursor()
        cur.execute("SELECT userPW, balance FROM account WHERE userName=%s", (name,))
        data = cur.fetchone()

        if data:
            if data[0] == pw:
                if data[1] >= amount:
                    update = data[1] - amount
                    cur.execute("UPDATE account SET balance=%s WHERE userName=%s", (update, name))
                    con.commit()
                    con.close()
                    tk.messagebox.showinfo("Success", "Withdrawal Successful!")
                else:
                    tk.messagebox.showerror("Error", "Insufficient Balance!")
            else:
                tk.messagebox.showerror("Error", "Invalid Password!")
        else:
            tk.messagebox.showerror("Error", "Invalid User Name!")

    def close_wd(self):
        self.wdFrame.destroy()

# Create the Tkinter root window
root = tk.Tk()

# Create an instance of the Bank class
obj = Bank(root)

# Start the Tkinter event loop
root.mainloop()