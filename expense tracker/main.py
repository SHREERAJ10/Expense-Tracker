import json #To store expenses data
import pandas as pd #Used to get summary and present expenses in tabular format
import os #Used to verify if json file is empty or not

class Expense:
    def __init__(self,item,amount,description):
        self.item = item
        self.amount = f"${amount}"
        self.description = description
        
    def to_dict(self):
        return {
            "Item":self.item,
            "Amount":self.amount,
            "Description":self.description
        }

        
class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        fileSize = os.path.getsize("expenses.json")
        
        #Writing empty list to json file if it's empty
        if fileSize == 0:
            with open("expenses.json","w") as f:
                f.write(json.dumps(self.expenses,indent=4))

    def add_expense(self,item,amount,description):
        expense = Expense(item,amount,description)
        
        with open("expenses.json","r") as f:
            self.expenses = json.load(f)
            
            #appending expenses to list after converting expenses to dictionary
            self.expenses.append(expense.to_dict())
            
        #Writes the list to the json file      
        self.save()
        
    def save(self):
        json_obj = json.dumps(self.expenses,indent=4)
        with open("expenses.json","w") as f: #using "write" mode because... try using append mode yourself!
            f.write(json_obj)
            
    def view(self):
        with open("expenses.json","r") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            
            # Function to format each cell as a string with fixed width
            def format_cell(cell, width):
                return str(cell).center(width)

            # Determine the maximum width for each column, including the index
            col_widths = {col: max(df[col].astype(str).apply(len).max(), len(col)) for col in df.columns}
            index_width = max(len(str(len(df))), len('Index'))

            # Format each cell and store in a new DataFrame
            formatted_df = df.copy()
            for col in df.columns:
                formatted_df[col] = df[col].astype(str).apply(lambda cell: format_cell(cell, col_widths[col]))

            # Add the index as a formatted column
            formatted_df.insert(0, 'index', [format_cell(i + 1, index_width) for i in range(len(df))])  # Adding index

            # Function to format headers with the same width
            def format_header(header, width):
                return header.center(width)

            # Format headers, including the index header
            formatted_headers = [format_header('S.N.', index_width)] + [format_header(header, col_widths[header]) for header in df.columns]

            # Combine headers and formatted DataFrame to a string
            formatted_string = ' | '.join(formatted_headers) + '\n' + '-' * (sum(col_widths.values()) + index_width + 3 * len(df.columns)) + '\n'
            formatted_string += '\n'.join([' | '.join(row) for row in formatted_df.values])

            # Print the formatted DataFrame
            print(formatted_string)
        
    def delete(self,index):
        with open("expenses.json","r") as f:
            data = json.load(f)
            
            #deleting expense/list element according to index given by user
            del data[index]
            json_obj = json.dumps(data,indent=4)
            
            #writing list to json file after deleting specified element/expense
            with open("expenses.json","w") as f: #using "write" mode because... try using append mode yourself!
                f.write(json_obj)
                
    def edit(self, index, item = "",amount = 1,description = ""):
        with open("expenses.json","r") as f:
            data = json.load(f)
            edit = data.pop(index)
            series = pd.Series(edit)
            print(f"\n{series.to_string()}")
            newItem = input("\n- Item: ")
            newAmount = input("\n- Amount: ")
            newDescription = input("\n- Description: ")
            
            if newItem != "":
                edit["Item"] = newItem
            if newAmount != "":
                edit["Amount"] = int(newAmount)
            if newDescription != "":
                edit["Description"] = newDescription
            
            data.insert(index,edit)
            with open("expenses.json","w") as f:
                f.write(json.dumps(data,indent = 4))
                
    def clear(self):
        with open("expenses.json","r") as f:
            data = json.load(f)
            data.clear()
        with open("expenses.json","w") as f:
            f.write(json.dumps(data,indent = 4))
            
    def summary(self):
        with open("expenses.json","r") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            print(f"\nTotal amount spent: {df["Amount"].sum()}")
            print(f"Average amount spent: {round(df["Amount"].mean(),2)}\n")

print("\t\tExpense Tracker")
print("Enter:\n\nv: To View Expense\na: To Add Expense\ne: To Edit Expense\nd: To Delete Expense\nc: To clear all expenses\ns: Get Summary of Expenses\nq: To Exit\n\n\tEnter 'cmd' for commands!")

while True:
    
    cmd = input("\n--> ").lower()
    print("\n")
    
    if cmd== "v":
        expense = ExpenseTracker()
        expense.view()

    elif cmd == "a":
        item = input("\n- Item: ")
        while True:
            try:
                amount = int(input("\n- Amount: "))
                break
            except:
                print("\nPlease enter amount in digit/number form!")

        description = input("\n- Description: ")
        expense = ExpenseTracker()
        expense.add_expense(item,amount,description)
        print("\n\tExpense has been added to the list!\n")
        expense.view()
        
    elif cmd == "e":
        expense = ExpenseTracker()
        while True:
            try:
                print("\nEnter the S.N. of expense you want to edit:\n")
                expense.view()
                cmd = int(input("\n--> "))
                expense.edit(cmd-1)
                break
            except:
                print("\nPlease enter valid command!")
                continue
        
        print("\nChanges has been saved!\n")
        expense.view()
        
    elif cmd == "d":
        expense = ExpenseTracker()
        expense.view()
        
        while True:
            try:
                cmd = int(input("\nEnter the S.N. of expense you want to delete:\n--> "))
                expense.delete(cmd-1) #index in list starts from 0
                break
                
            except:
                print("\nPlease enter valid command!")
                continue            
        
        print("\tExpense has been deleted!\n")
        expense.view()
        
    elif cmd == "c":
        expense = ExpenseTracker()
        expense.clear()
        print("All the expenses have been cleared!")
        
    elif cmd == "cmd":
        print("Enter:\n\nv: To View Expense\na: To Add Expense\ne: To Edit Expense\nd: To Delete Expense\nc: To clear all expenses\ns: Get Summary of Expenses\nq: To Exit\n\n\tEnter 'cmd' for commands!")

    elif cmd=="q":
        break
    
    elif cmd == "s":
        expense =ExpenseTracker()
        expense.view()
        expense.summary()
    
    else:
        print("\nPlease enter a valid command!\n")
        print("Enter:\n\nv: To View Expense\na: To Add Expense\ne: To Edit Expense\nd: To Delete Expense\nc: To clear all expenses\ns: Get Summary of Expenses\nq: To Exit\n\n\tEnter 'cmd' for commands!")