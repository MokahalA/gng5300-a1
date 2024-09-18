''' This file contains the code for the command-line interface of the phonebook application.  
    The user can interact with the phonebook by adding, viewing, searching, updating, and deleting contacts.
    To run the application: python main.py
'''

from phonebook import PhoneBook
from contact import Contact
import os
import re

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


''' Helper functions for the command-line interface main menu. '''
def display_menu():
    '''Display the menu options for the user.'''
    print("\n--- Phonebook Main Menu ---")
    print(" 1. Add Contact")
    print(" 2. View All Contacts")
    print(" 3. Search Contacts")
    print(" 4. Update Contact")
    print(" 5. Delete Contact")
    print(" 6. Batch Add Contacts (from CSV)")
    print(" 7. Batch Delete Contacts (from CSV)")
    print(" 8. Sort Contacts Alphabetically")
    print(" 9. Group Contacts by Last Name Initial")
    print(" 10. View Audit Log")
    print(" 11. Exit")
    print()


''' Helper function for validating input phone number format: (###) ###-#### '''
def is_valid_phone(phone):
    '''Check if the phone number is in the correct format.'''
    return re.fullmatch(r"\(\d{3}\) \d{3}-\d{4}", phone) is not None


''' Helper function for validating input email'''
def is_valid_email(email):
    '''Check if the email is in the correct format.'''
    return re.fullmatch(r".+@.+\.com", email) is not None or not email  # Allow empty email


''' Helper function for getting and validating input from the user.'''
def get_valid_input(prompt, validation_func, error_message):
    '''Helper function to get and validate input from the user.'''
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        else:
            print(f"{RED}{error_message}{RESET}")


'''Function to get contact details from the user with validation.'''
def get_contact_details():
    first_name = get_valid_input(
        "Enter first name: ",
        lambda x: bool(x.strip()),  # Non-empty check
        "Error: First name cannot be empty."
    )
    last_name = get_valid_input(
        "Enter last name: ",
        lambda x: bool(x.strip()),  # Non-empty check
        "Error: Last name cannot be empty."
    )
    phone_number = get_valid_input(
        "Enter phone number (format: (###) ###-####): ",
        is_valid_phone,
        "Error: Invalid phone number format. It must be (###) ###-####."
    )
    email = input("Enter email (optional): ")
    if email and not is_valid_email(email):
        print(f"{RED}Error: Invalid email format. It must be in the format username@domain.com.{RESET}")
        email = input("Enter email (optional): ")
    address = input("Enter address (optional): ")
    
    return Contact(first_name, last_name, phone_number, email, address)


''' Adding a contact to the phonebook '''
def add_contact(phonebook):
    contact = get_contact_details()
    phonebook.add_contact(contact)
    print(f"{GREEN}Contact added successfully!{RESET}")


'''View all contacts currently in the phonebook.'''
def view_contacts(phonebook):
    phonebook.display_contacts()


'''Search contacts by name or phone number.'''
def search_contacts(phonebook):
    search_string = input("Enter name or phone number to search: ")
    phonebook.search_contacts(search_string)


'''Update an existing contact in the phonebook.'''
def update_contact(phonebook):
    search_string = input("Enter the full name of the contact to update: ")
    matches = phonebook.search_contacts(search_string)
    
    if matches:
        print("\n--- Select Contact to Update ---")
        for idx, contact in enumerate(matches, 1):
            print(f"{idx}. {contact.first_name} {contact.last_name} | {contact.phone_number}")
        
        # Validate input for contact selection
        while True:
            try:
                choice = int(input("\nEnter the number of the contact to update: ")) - 1
                
                if 0 <= choice < len(matches):
                    contact = matches[choice]
                    break
                else:
                    print(f"{RED}Error: Please enter a valid number from the list.{RESET}")
            except ValueError:
                print(f"{RED}Error: Invalid input. Please enter a number.{RESET}")

        # Define validation functions
        def is_valid_phone(phone):
            return re.fullmatch(r"\(\d{3}\) \d{3}-\d{4}", phone) is not None

        def is_valid_email(email):
            return re.fullmatch(r".+@.+\.com", email) is not None or not email  # Allow empty email

        def get_valid_input(prompt, validation_func, error_message):
            while True:
                value = input(prompt)
                if validation_func(value):
                    return value
                else:
                    print(f"{RED}{error_message}{RESET}")

        # Validate and get new details
        print("\n--- Enter New Details (Leave blank to keep current values) ---")
        first_name = input(f"Enter new first name (current: {contact.first_name}): ") or contact.first_name
        last_name = input(f"Enter new last name (current: {contact.last_name}): ") or contact.last_name
        
        phone_number_prompt = f"Enter new phone number (current: {contact.phone_number}): "
        phone_number = get_valid_input(
            phone_number_prompt,
            is_valid_phone,
            "Error: Invalid phone number format. It must be (###) ###-####."
        ) or contact.phone_number

        email_prompt = f"Enter new email (current: {contact.email}): "
        email = get_valid_input(
            email_prompt,
            is_valid_email,
            "Error: Invalid email format. It must be in the format username@domain.com."
        ) or contact.email
        
        address = input(f"Enter new address (current: {contact.address}): ") or contact.address
        
        # Update contact with validated values
        phonebook.update_contact(contact, first_name, last_name, phone_number, email, address)
    else:
        print(f"{RED}Error: No contact found with the name {search_string}.{RESET}")


'''Delete an existing contact from the phonebook based on the full name.'''
def delete_contact(phonebook):
    full_name = input("Enter the full name of the contact to delete (First Last): ").strip()
    phonebook.delete_contact(full_name)


'''Batch add contacts from an input CSV file. File must be placed in the data folder'''
def batch_add_contacts(phonebook):
    filename = input("Place your CSV file in the 'data' folder and enter the name of the file (e.g: testing.csv): ")
    filepath = os.path.join('data', filename)
    if os.path.exists(filepath):
        phonebook.batch_add_contacts(filename)
    else:
        print(f"{RED}Error: File not found in the 'data' folder.{RESET}")


'''Batch delete contacts from an input CSV file. File must be placed in the data folder'''
def batch_delete_contacts(phonebook):
    filename = input("Place your CSV file in the 'data' folder and enter the name of the file (e.g: testing.csv): ")
    filepath = os.path.join('data', filename)
    if os.path.exists(filepath):
        phonebook.batch_delete_contacts(filename)
    else:
        print(f"{RED}Error: File not found in the 'data' folder.{RESET}")


'''Sort contacts alphabetically by last name.'''
def sort_contacts(phonebook):
    phonebook.sort_contacts('alphabetical')
    print(f"{GREEN}Contacts sorted alphabetically by last name.{RESET}")
    phonebook.display_contacts()


'''Group contacts by the initial letter of the last name.'''
def group_contacts(phonebook):
    phonebook.sort_contacts('group')
    print(f"{GREEN}Contacts grouped by the first letter of last name.{RESET}")
    phonebook.display_contacts()


'''View the audit log of operations.'''
def view_audit_log(phonebook):
    phonebook.view_audit_log()


'''Main function to run the phonebook application command-line loop.'''
def main():
    phonebook = PhoneBook()

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            add_contact(phonebook)
        elif choice == '2':
            view_contacts(phonebook)
        elif choice == '3':
            search_contacts(phonebook)
        elif choice == '4':
            update_contact(phonebook)
        elif choice == '5':
            delete_contact(phonebook)
        elif choice == '6':
            batch_add_contacts(phonebook)
        elif choice == '7':
            batch_delete_contacts(phonebook)
        elif choice == '8':
            sort_contacts(phonebook)
        elif choice == '9':
            group_contacts(phonebook)
        elif choice == '10':
            view_audit_log(phonebook)
        elif choice == '11':
            phonebook.clear_audit_log()  # Clear the audit log
            print(f"{GREEN}Exiting the phonebook system. Goodbye!{RESET}")
            print("")
            break
        else:
            print(f"{RED}Invalid option. Please try again.{RESET}")

if __name__ == "__main__":
    main()
