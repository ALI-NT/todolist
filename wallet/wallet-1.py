import json
import os
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal

class PersonalWallet:
    """Main wallet application class"""
    
    def __init__(self, data_file="wallet_data.json"):
        self.data_file = data_file
        self.transactions = []
        self.balance = Decimal("0.00")
        self.categories = {
            "income": ["Salary", "Freelance", "Investment", "Bonus", "Other"],
            "expense": ["Food", "Transport", "Entertainment", "Utilities", "Shopping", "Other"]
        }
        self.load_data()
    
    def load_data(self):
        """Load wallet data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.transactions = data.get('transactions', [])
                    self.balance = Decimal(str(data.get('balance', '0.00')))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")
        else:
            self.balance = Decimal("0.00")
            self.transactions = []
    
    def save_data(self):
        """Save wallet data to JSON file"""
        try:
            data = {
                'transactions': self.transactions,
                'balance': str(self.balance),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def add_transaction(self, amount, trans_type, category, description=""):
        """Add a new transaction"""
        try:
            amount = Decimal(str(amount))
            
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            
            if trans_type == "income":
                self.balance += amount
            elif trans_type == "expense":
                if amount > self.balance:
                    raise ValueError("Insufficient balance for this expense")
                self.balance -= amount
            else:
                raise ValueError("Invalid transaction type")
            
            transaction = {
                'id': len(self.transactions) + 1,
                'amount': f"+${amount:.2f}" if trans_type == "income" else f"-${amount:.2f}",
                'type': trans_type.capitalize(),
                'category': category,
                'description': description if description else "No description",
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.transactions.append(transaction)
            self.save_data()
            return True, "Transaction added successfully"
        
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_balance(self):
        """Get current balance"""
        return f"${self.balance:.2f}"
    
    def get_transactions(self):
        """Get all transactions"""
        return sorted(self.transactions, key=lambda x: x['id'], reverse=True)
    
    def delete_transaction(self, trans_id):
        """Delete a transaction by ID"""
        try:
            trans = next((t for t in self.transactions if t['id'] == trans_id), None)
            if not trans:
                return False, "Transaction not found"
            
            # Reverse the transaction
            amount = Decimal(trans['amount'].replace('$', '').replace('+', '').replace('-', ''))
            if trans['type'] == "Income":
                self.balance -= amount
            else:
                self.balance += amount
            
            self.transactions = [t for t in self.transactions if t['id'] != trans_id]
            self.save_data()
            return True, "Transaction deleted successfully"
        except Exception as e:
            return False, str(e)


class WalletGUI:
    """GUI for the Personal Wallet application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Wallet - Basic Version")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.wallet = PersonalWallet()
        self.setup_ui()
        self.refresh_display()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Balance display with dark background
        balance_frame = tk.Frame(main_frame, bg='#3a4f5c', relief=tk.FLAT, borderwidth=0)
        balance_frame.pack(fill=tk.X, pady=(0, 20))
        
        balance_text = tk.Label(balance_frame, text=f"Current Balance: $0.00", 
                               font=("Arial", 24, "bold"), 
                               foreground="#4caf50", 
                               bg='#3a4f5c')
        balance_text.pack(pady=30)
        
        self.balance_display = balance_text
        
        # Add Transaction Section
        trans_frame = tk.LabelFrame(main_frame, text="Add Transaction", 
                                   font=("Arial", 12, "bold"),
                                   bg='white', fg='black',
                                   relief=tk.GROOVE, borderwidth=2, padx=15, pady=15)
        trans_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Amount
        tk.Label(trans_frame, text="Amount:", font=("Arial", 10), bg='white').grid(row=0, column=0, sticky=tk.W, padx=5, pady=8)
        self.amount_entry = tk.Entry(trans_frame, width=18, font=("Arial", 10))
        self.amount_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=8)
        
        # Type
        tk.Label(trans_frame, text="Type:", font=("Arial", 10), bg='white').grid(row=0, column=2, sticky=tk.W, padx=(30, 5), pady=8)
        self.type_var = tk.StringVar(value="income")
        type_combo = ttk.Combobox(trans_frame, textvariable=self.type_var, 
                                  values=["income", "expense"], state="readonly", width=15, font=("Arial", 10))
        type_combo.grid(row=0, column=3, sticky=tk.W, padx=5, pady=8)
        type_combo.bind("<<ComboboxSelected>>", self.on_type_change)
        
        # Category
        tk.Label(trans_frame, text="Category:", font=("Arial", 10), bg='white').grid(row=1, column=0, sticky=tk.W, padx=5, pady=8)
        self.category_var = tk.StringVar(value="Salary")
        self.category_combo = ttk.Combobox(trans_frame, textvariable=self.category_var, 
                                           values=self.wallet.categories["income"], 
                                           state="readonly", width=15, font=("Arial", 10))
        self.category_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=8)
        
        # Description
        tk.Label(trans_frame, text="Description:", font=("Arial", 10), bg='white').grid(row=1, column=2, sticky=tk.W, padx=(30, 5), pady=8)
        self.description_entry = tk.Entry(trans_frame, width=30, font=("Arial", 10))
        self.description_entry.grid(row=1, column=3, sticky=tk.EW, padx=5, pady=8)
        
        # Buttons with custom styling
        button_frame = tk.Frame(trans_frame, bg='white')
        button_frame.grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=(15, 5))
        
        add_income_btn = tk.Button(button_frame, text="✚ Add Income", command=self.add_income,
                                   bg='#4caf50', fg='white', font=("Arial", 10, "bold"),
                                   relief=tk.RAISED, borderwidth=2, padx=20, pady=8,
                                   cursor='hand2', activebackground='#45a049')
        add_income_btn.pack(side=tk.LEFT, padx=5)
        
        add_expense_btn = tk.Button(button_frame, text="➖ Add Expense", command=self.add_expense,
                                    bg='#f44336', fg='white', font=("Arial", 10, "bold"),
                                    relief=tk.RAISED, borderwidth=2, padx=20, pady=8,
                                    cursor='hand2', activebackground='#da190b')
        add_expense_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="🗑 Clear Form", command=self.clear_form,
                             bg='#9e9e9e', fg='white', font=("Arial", 10, "bold"),
                             relief=tk.RAISED, borderwidth=2, padx=20, pady=8,
                             cursor='hand2', activebackground='#757575')
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Transaction History Section
        hist_frame = tk.LabelFrame(main_frame, text="Transaction History", 
                                  font=("Arial", 12, "bold"),
                                  bg='white', fg='black',
                                  relief=tk.GROOVE, borderwidth=2, padx=15, pady=15)
        hist_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview
        columns = ("#", "Amount", "Type", "Category", "Description", "Date")
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                       background="white",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="white",
                       font=("Arial", 10))
        style.configure("Treeview.Heading", 
                       font=("Arial", 10, "bold"),
                       background="#e0e0e0",
                       foreground="black")
        style.map('Treeview', background=[('selected', '#0078d7')])
        
        self.tree = ttk.Treeview(hist_frame, columns=columns, height=12, show="headings")
        
        # Define headings and columns
        self.tree.column("#", width=40, anchor=tk.CENTER)
        self.tree.column("Amount", width=100, anchor=tk.CENTER)
        self.tree.column("Type", width=90, anchor=tk.CENTER)
        self.tree.column("Category", width=120, anchor=tk.CENTER)
        self.tree.column("Description", width=200, anchor=tk.W)
        self.tree.column("Date", width=160, anchor=tk.CENTER)
        
        self.tree.heading("#", text="#")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Date", text="Date")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(hist_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right-click menu for deleting transactions
        self.tree.bind("<Button-3>", self.on_right_click)
    
    def on_type_change(self, event=None):
        """Update category dropdown when type changes"""
        trans_type = self.type_var.get()
        categories = self.wallet.categories.get(trans_type, [])
        self.category_combo['values'] = categories
        self.category_var.set(categories[0] if categories else "")
    
    def add_income(self):
        """Add income transaction"""
        self.add_transaction("income")
    
    def add_expense(self):
        """Add expense transaction"""
        self.add_transaction("expense")
    
    def add_transaction(self, trans_type):
        """Add a transaction"""
        try:
            amount = self.amount_entry.get().strip()
            category = self.category_var.get()
            description = self.description_entry.get().strip()
            
            if not amount:
                messagebox.showwarning("Validation Error", "Please enter an amount")
                return
            
            success, message = self.wallet.add_transaction(amount, trans_type, category, description)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.refresh_display()
            else:
                messagebox.showerror("Error", message)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add transaction: {str(e)}")
    
    def clear_form(self):
        """Clear the form fields and reset all wallet data"""
        try:
            # Ask for confirmation before clearing all data
            if messagebox.askyesno("Confirm Clear", "This will clear the form AND delete all transactions. Continue?"):
                # Clear all transactions and reset balance
                self.wallet.transactions = []
                self.wallet.balance = Decimal("0.00")
                self.wallet.save_data()
                
                # Clear form fields
                self.amount_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)
                
                # Reset type to income
                self.type_var.set("income")
                
                # Update category dropdown based on type
                self.on_type_change()
                
                # Reset category to default
                self.category_var.set("Salary")
                
                # Refresh the display
                self.refresh_display()
                
                # Set focus back to amount entry
                self.amount_entry.focus_set()
                
                messagebox.showinfo("Success", "All data cleared successfully!")
        except Exception as e:
            print(f"Error clearing form: {str(e)}")
            messagebox.showerror("Error", f"Failed to clear form: {str(e)}")
    
    def refresh_display(self):
        """Refresh the display with current data"""
        # Update balance
        self.balance_display.config(text=f"Current Balance: {self.wallet.get_balance()}")
        
        # Clear and update transaction tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for trans in self.wallet.get_transactions():
            self.tree.insert("", "end", values=(
                trans['id'],
                trans['amount'],
                trans['type'],
                trans['category'],
                trans['description'],
                trans['date']
            ))
    
    def on_right_click(self, event):
        """Handle right-click on transaction"""
        item = self.tree.selection()
        if not item:
            return
        
        # Create context menu
        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label="Delete", command=lambda: self.delete_transaction(item[0]))
        menu.post(event.x_global, event.y_global)
    
    def delete_transaction(self, item_id):
        """Delete selected transaction"""
        try:
            values = self.tree.item(item_id)['values']
            trans_id = values[0]
            
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this transaction?"):
                success, message = self.wallet.delete_transaction(trans_id)
                if success:
                    messagebox.showinfo("Success", message)
                    self.refresh_display()
                else:
                    messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete transaction: {str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = WalletGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()