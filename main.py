from module import *

def main():
    file_path = 'finance_records.csv'
    finance_manager = FinanceManager(file_path)
    while True:
        output = (
            "\n1. Показать текущий баланс",
            "2. Добавить запись",
            "3. Редактировать запись",
            "4. Поиск записи",
            "5. Показать все записи",
            "6. Выйти"
            )
        
        print("\n".join(output))


        choice = input("\nВыберите действие: ")

        if choice == '1':
            print(finance_manager.show_current_balance())
        elif choice == '2':
            category = input("Введите категорию (Доход/Расход): ")
            amount = float(input("Введите сумму: "))
            description = input("Введите описание: ")
            finance_manager.add_record(category, amount, description)
        elif choice == '3':
            pk = int(input("Введите индекс записи для редактирования: "))
            category = input("Введите новую категорию (оставьте пустым, если не хотите изменять): ")
            amount = input("Введите новую сумму (оставьте пустым, если не хотите изменять): ")
            description = input("Введите новое описание (оставьте пустым, если не хотите изменять): ")
            if amount:
                amount = float(amount)
            finance_manager.update_records(pk, category, amount, description)
        elif choice == '4':
            date = input("Введите дату для поиска в формате YYYY-MM-DD (оставьте пустым, если не хотите искать по дате): ")
            if date:
                date = datetime.strptime(date, '%Y-%m-%d').date()
            category = input("Введите категорию для поиска (оставьте пустым, если не хотите искать по категории): ")
            amount = input("Введите сумму для поиска (оставьте пустым, если не хотите искать по сумме): ")
            if amount:
                amount = float(amount)
            results = finance_manager.search_record(date, category, amount)
            print("Результаты поиска:")
            for result in results:
                print(result)
        elif choice == '5':
            print("\n\n")
            print(finance_manager.show_records())
        elif choice == '6':
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()