import os
import csv
import shutil

from datetime import datetime
from tempfile import NamedTemporaryFile



tempfile = NamedTemporaryFile(mode='w', delete=False, encoding="utf-8-sig")

class FinanceManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.records = []
        self.show_records()


    def show_records(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                output = ""
                for row in reader:
                    sign = '+' if row['category'] == 'Доход' else '-'
                    output += f"{row['pk']}.{row['date']}: {sign + str(row['amount'])}\n"
                return output


    def save_records(self):
        with open(self.file_path, 'r+', encoding='utf-8-sig', newline='') as file:
            fieldnames = ['pk', 'date', 'category', 'amount', 'description']
            write = csv.DictWriter(file, fieldnames=fieldnames)
            write.writeheader()
            for pk, record in enumerate(self.records):
                record['pk'] = pk
                record['date'] = datetime.now().strftime('%Y-%m-%d')
                write.writerow(record)
    

    def update_records(self, pk, category=None, amount=None, description=None):
        up_dt = []
        with open(self.file_path, 'r+', encoding='utf-8-sig', newline='') as file, tempfile:
            fieldnames = ['pk', 'date', 'category', 'amount', 'description']
            reader = csv.DictReader(file, fieldnames=fieldnames)
            writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
            print("pk", pk)
            if 0 <= pk < len(self.records):    
                for row in reader:
                    if row['pk'] == str(pk):
                        print(f"updating row with pk {pk}")
                        if category:
                            row['category'] = category
                        elif amount:
                            row['amount'] = amount
                        elif description:
                            row['description'] = description
                        up_dt.append(row)
                    else:
                        row = {
                            "pk": row['pk'],
                            "date": row['date'],
                            "category": row['category'],
                            "amount": row['amount'],
                            "description": row['description']
                        }
                        up_dt.append(row)
                writer.writerows(up_dt)
                shutil.move(tempfile.name, self.file_path)
            else:
                return "Invalid record pk"


    def add_record(self, category, amount, description):
        date = datetime.now().date()
        
        #Валидация категории
        if not isinstance(category, str) or not category.strip():
            print("Ошибка: Некорректно введена категория.")
            return
        
        #Валидация суммы
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Ошибка: Некорректно введена сумма.")
            return
        
        #Валидация описания
        if not isinstance(description, str) or not description.strip():
            print("Ошибка: Некорректно введено описание.")

        self.records.append({'date': date, 'category': category, 'amount': amount, 'description': description})
        self.save_records()
    

    def search_record(self, date=None, category=None, amount=None):
        with open(self.file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            results = []
            for row in reader:
                if (not date or row['date'] == date) and \
                    (not category or row['category'] == category) and \
                    (not amount or row['amount'] == amount):
                    results.append(row)
            return results
    
    
    def show_current_balance(self):
        total_income = 0
        total_expense = 0 

        with open(self.file_path, 'r', encoding='utf-8-sig') as file:
            fieldnames = ['pk', 'date', 'category', 'amount', 'description']
            reader = csv.DictReader(file, fieldnames=fieldnames)
            
            for row in reader:
                if row['category'] == "Доход":
                    total_income += float(row['amount'])
                elif row['category'] == "Расход":
                    total_expense += float(row['amount'])

            total_balance = total_income - total_expense
            
            output = ("Ваш текущий баланс:",
                    f"Баланс: {total_balance}",
                    f"Доходы: {total_income}",
                    f"Расходы: {total_expense}")
            
            return "\n".join(output)
