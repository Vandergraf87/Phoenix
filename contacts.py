from collections import UserDict
from datetime import datetime
import re
import pickle

class Field:
    def __init__(self, value):
        self.value = value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone_number):
        if not self.validate_phone_number(phone_number):
            raise ValueError("Invalid phone number format")
        super().__init__(phone_number)

    @staticmethod
    def validate_phone_number(phone_number):
        return len(phone_number) == 10 and phone_number.isdigit()

    @Field.value.setter
    def value(self, new_phone_number):
        if not self.validate_phone_number(new_phone_number):
            raise ValueError("Invalid phone number format")
        self._value = new_phone_number


class Email(Field):
    def __init__(self, contact_email):
        if not self.validate_contact_email(contact_email):
            raise ValueError("Invalid email format")
        super().__init__(contact_email)

    @staticmethod
    def validate_contact_email(contact_email):
        email_pattern = r"[A-Za-z]+[\.?\w+]+@\w+\.\w{2,}"
        return len(re.findall(email_pattern, contact_email)) > 0
    
    @Field.value.setter
    def value(self, new_contact_email):
        if not self.validate_contact_email(new_contact_email):
            raise ValueError("Invalid email format")
        self._value = new_contact_email


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_email(self, contact_email):
        email = Email(contact_email)
        self.emails.append(email)

    def edit_email(self, old_contact_email, new_contact_email):
        if not Email.validate_contact_email(new_contact_email):
            raise ValueError("Invalid email format")
        
        found = False
        for email in self.emails:
            if email.value == old_contact_email:
                email.value = new_contact_email
                found = True
        
        if not found:
            raise ValueError("Such email not found in the record")

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        if not Phone.validate_phone_number(new_phone_number):
            raise ValueError("Invalid phone number format")
        
        found = False
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                found = True
        
        if not found:
            raise ValueError("Phone number not found in the record")
            

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def days_to_birthday(self):
        if not self.birthday:
            return None                   
        birthday = self.birthday
        today = datetime.today()
        year, month, day = map(int, birthday.split('-'))
        next_birthday = datetime(today.year, month, day)

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, month, day)

        delta = next_birthday - today
        days_until_birthday = delta.days
        
        return f"There are {days_until_birthday} days to next birthday."

class Birthday(Field):
    def __init__(self, birthday):
        if not self.validate_birthday(birthday):
            raise ValueError("Invalid birthday format")
        super().__init__(birthday)

    @staticmethod
    def validate_birthday(birthday):
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if re.match(pattern, birthday):
            return True
        else:
            return False

    @Field.value.setter
    def value(self, new_birthday):
        if not self.validate_birthday(new_birthday):
            raise ValueError("Invalid birthday format")
        self._value = new_birthday

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
        self.page_size = 10  

    def iterator(self):
        page = 0  
        while page * self.page_size < len(self.data):
            start = page * self.page_size
            end = (page + 1) * self.page_size
            yield list(self.data.values())[start:end]
            page += 1

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def save_to_file(self, filename):
        data = {"contacts": self.data}
        with open(filename, "wb") as f:
            pickle.dump(data, f)

    def load_data(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                if "contacts" in data:
                    self.data = data["contacts"]
        except FileNotFoundError:
            print("File not found")

    def search(self, query):
        search_match = []
        for name, record in self.data.items():
            if query in name or any(query in phone.value for phone in record.phones):
                search_match.append(record)
        return search_match


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Invalid command"

    return inner

phone_book = {}

@input_error
def hello():
    return "How can I help you?"

@input_error
def add_contact(name, phone):
    phone_book[name] = phone
    return f"Added {name.title()} with phone {phone}"

@input_error
def change_contact(name, phone):
    if name in phone_book:
        phone_book[name] = phone
        return f"Changed phone for {name.title()} to {phone}"
    else:
        return f"Contact {name.title()} not found"

@input_error
def get_phone(name):
    if name in phone_book:
        return f"The phone for {name.title()} is {phone_book[name]}"
    else:
        return f"Contact {name.title()} not found"
@input_error
def show_all():
    if not phone_book:
        return "Phone book is empty"
    else:
        return "\n".join([f"{name.title()}: {phone}" for name, phone in phone_book.items()])

@input_error
def goodbye():
    return "Good bye!"