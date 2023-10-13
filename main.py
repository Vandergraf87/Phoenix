import contacts
import notebook
import sorter
from collections import UserDict


def main():
    phone_book = contacts.AddressBook() 

    is_running = True

    while is_running:
        user_input = input("Choose (contacts, notes, sorter): ").lower() #тут треба прописати вибір з чим саме будемо працювати. Типу до списку контактів, нотатника чи сортера
        
        if user_input == "contacts":
            while True:
                user_input = input("Enter command: ").lower()

                if user_input == "hello":
                    print(contacts.hello())
                elif user_input.startswith("add"):
                    _, name, phone = user_input.split()
                    print(contacts.add_contact(name, phone))
                elif user_input.startswith("change"):
                    _, name, phone = user_input.split()
                    print(contacts.change_contact(name, phone))
                elif user_input.startswith("phone"):
                    _, name = user_input.split()
                    print(contacts.get_phone(name))
                elif user_input == "show all":
                    print(contacts.show_all())
                elif user_input == "save":
                    filename = input("Enter the filename to save the phone book: ")
                    phone_book.save_to_file(filename)
                    print(f"Phone book saved to {filename}")
                elif user_input == "load":
                    filename = input("Enter the filename to load the phone book: ")
                    phone_book.load_data(filename)
                    print(f"Phone book loaded from {filename}")
                elif user_input.startswith("search"):
                    _, query = user_input.split()
                    results = contacts.phone_book.search(query)
                    if results:
                        for record in results:
                            print(f"Name: {record.name.value}, Phone: {', '.join(contacts.phone.value for phone in contacts.record.phones)}")
                    else:
                        print("No matching contacts found.")
                elif user_input == "back":
                    break
                elif user_input in ["good bye", "close", "exit"]:
                    print(contacts.goodbye())
                    is_running = False
                    break
        elif user_input == "notes":
            pass                      #Сюди додаєм роботу з нотатником

        elif user_input == "sorter":
            pass                      #Тут прописуєм роботу з сортером. Це має бути 1 команда - вказати папку яку будем сортувати
        
        elif user_input in ["good bye", "close", "exit"]:
            print(contacts.goodbye())
            is_running = False
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()