'''
    This class is used to model a PhoneBook object to store a list of contacts, 
    to facilitate CRUD operations on the contact list, and to keep track of an audit log of operations.
'''
from contact import Contact
from datetime import datetime
import csv
import re
import os

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

class PhoneBook:
    '''Constructor to create a new phone book with an empty contact list and audit log.'''
    def __init__(self):
        self.contacts_list = []
        self.audit_log_file = 'audit_log.txt'

    def log_operation(self, operation):
        '''Logs an operation with a timestamp into the audit log file.'''
        with open(self.audit_log_file, 'a') as log_file:
            log_file.write(f"{datetime.now()} - {operation}\n")

    '''Add a new contact to the phone book list and log the operation.'''
    def add_contact(self, contact):
        self.contacts_list.append(contact)
        self.log_operation(f"Added contact: {contact.first_name} {contact.last_name}")

    '''Delete a contact from the phone book list and log the operation.'''
    def delete_contact(self, full_name):
        # Convert the input full name to lowercase for case-insensitive comparison
        full_name = full_name.lower()
        contact_to_delete = None

        # Search for the exact full name match in the contacts
        for contact in self.contacts_list:
            contact_full_name = f"{contact.first_name} {contact.last_name}".lower()

            if contact_full_name == full_name:  # Exact match for full name
                contact_to_delete = contact
                break

        if contact_to_delete:
            self.contacts_list.remove(contact_to_delete)
            print(f"{GREEN}Contact '{full_name}' deleted successfully.{RESET}")
            self.log_operation(f"Deleted contact: {contact_full_name}")
        else:
            print(f"{RED}Error: No contact found with the full name '{full_name}'.{RESET}")
            self.log_operation(f"Failed to delete contact: {full_name}")
    
    '''Batch add a group of contacts to the phone book list from a CSV file and log the operation.'''
    def batch_add_contacts(self, filename):
        filepath = os.path.join('data', filename)
        if os.path.exists(filepath):
            with open(filepath, mode='r') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader, None)  # Read headers if they exist, else None
                for row in csv_reader:
                    # Handle optional fields
                    first_name = row[0]
                    last_name = row[1]
                    phone_number = row[2]
                    email = row[3] if len(row) > 3 else None
                    address = row[4] if len(row) > 4 else None
                    
                    contact = Contact(first_name, last_name, phone_number, email, address)
                    self.contacts_list.append(contact)
            print(f"{GREEN}Contacts added successfully from CSV.{RESET}")
            self.log_operation(f"Batch added contacts from file: {filename}")

    '''Batch delete a group of contacts from the phone book list from a CSV file and log the operation.'''
    def batch_delete_contacts(self, filename):
        filepath = os.path.join('data', filename)
        if os.path.exists(filepath):
            with open(filepath, mode='r') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader, None)  # Read headers if they exist, else None
                for row in csv_reader:
                    # Handle optional fields
                    first_name = row[0]
                    last_name = row[1]
                    phone_number = row[2]
                    email = row[3] if len(row) > 3 else None
                    address = row[4] if len(row) > 4 else None
                    
                    contact = Contact(first_name, last_name, phone_number, email, address)
                    try:
                        self.contacts_list.remove(contact)
                    except ValueError:
                        print(f'Error: Contact {contact.first_name} {contact.last_name} does not exist.')
            print(f"{GREEN}Contacts added successfully batch removed from CSV.{RESET}")
            self.log_operation(f"Batch deleted contacts from file: {filename}")


    
    '''Update a contact in the phone book list, log the operation and track the change history.'''
    def update_contact(self, contact, first_name=None, last_name=None, phone_number=None, email=None, address=None):
        # Define helper functions for validation
        def is_valid_phone(phone):
            return re.fullmatch(r"\(\d{3}\) \d{3}-\d{4}", phone) is not None

        def is_valid_email(email):
            return re.fullmatch(r".+@.+\..+", email) is not None or not email  # Allow empty email

        # Backup the old values before updating
        old_values = {
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'phone_number': contact.phone_number,
            'email': contact.email,
            'address': contact.address
        }

        # Validate the phone number if provided
        if phone_number and not is_valid_phone(phone_number):
            print(f"{RED}Error: Invalid phone number format. It must be (###) ###-####.{RESET}")
            return
        
        # Validate the email if provided
        if email and not is_valid_email(email):
            print(f"{RED}Error: Invalid email format. It must be in the format username@domain.com.{RESET}")
            return

        try:
            # Update the contact with validated values
            contact.first_name = first_name if first_name else contact.first_name
            contact.last_name = last_name if last_name else contact.last_name
            contact.phone_number = phone_number if phone_number else contact.phone_number
            contact.email = email if email else contact.email
            contact.address = address if address else contact.address

            self.log_operation(f"Updated contact: {old_values} to {contact.__dict__}")
            print(f"{GREEN}Contact updated successfully!{RESET}")
        except Exception as e:
            print(f"{RED}Error: Invalid contact or update failed.{RESET}")
            self.log_operation(f"Attempted to update non-existent contact: {contact.first_name} {contact.last_name}. Error: {str(e)}")
    
    '''Display all contacts in the phone book list.'''
    def display_contacts(self):
        if not self.contacts_list:
            print("\nNo contacts available in the phonebook.")
            return

        print("\nPhonebook Contacts:")
        print("="*90)

        for idx, contact in enumerate(self.contacts_list, 1):
            # Display each contact's details on one line
            print(f"{idx}. {contact.first_name} {contact.last_name} | Phone: {contact.phone_number} | Email: {contact.email if contact.email else 'N/A'} | Address: {contact.address if contact.address else 'N/A'}")

        print("="*90)
        print(f"Total contacts: {len(self.contacts_list)}")

    '''Wildcard searching with support for partial matches in names, phone numbers, and full names.'''
    def search_contacts(self, search_string, start_date=None, end_date=None):
        matches = []
        search_string = search_string.lower()  # Make search case-insensitive

        for contact in self.contacts_list:
            full_name = f"{contact.first_name} {contact.last_name}".lower()  # Full name for matching

            # Check for matches in first name, last name, full name, or phone number
            if (re.search(search_string, contact.first_name.lower()) or
                re.search(search_string, contact.last_name.lower()) or
                re.search(search_string, full_name) or
                re.search(search_string, contact.phone_number)):

                # Filter by date range if provided
                if start_date and end_date:
                    if start_date <= contact.time_created <= end_date:
                        matches.append(contact)
                else:
                    matches.append(contact)

        # Print matches
        if matches:
            for contact in matches:
                print(contact)
                print()
        else:
            print(f"{RED}No contacts found matching the search criteria: {search_string}{RESET}")
        
        # Log the search operation
        self.log_operation(f"Searched for contacts with query: {search_string}, found {len(matches)} matches")
        
        return matches
    
    '''Sort and group contacts based on various parameters like alphabetical sorting, or grouping by the initial letter of the last name and logs the operation.'''
    def sort_contacts(self, sort_type):
        if sort_type == 'alphabetical':
            self.contacts_list.sort(key=lambda x: x.last_name)
            self.log_operation("Sorted contacts alphabetically by last name.")
        elif sort_type == 'group':
            self.contacts_list.sort(key=lambda x: x.last_name[0])
            self.log_operation("Grouped contacts by last name initial.")
        else:
            print('Error: Invalid sort type.')
            self.log_operation("Attempted to sort contacts with invalid sort type.")

    '''View the history of operations (audit log).'''
    def view_audit_log(self):
        with open(self.audit_log_file, 'r') as log_file:
            print("\n" + BLUE + "--- Audit Log ---" + RESET)
            for line in log_file:
                print(" " + BLUE + line.strip() + RESET)
    
    '''Helper function to clear the audit log.'''
    def clear_audit_log(self):
        '''Clears the audit log file.'''
        open(self.audit_log_file, 'w').close()  # Clear the content of the file
        print(f"{GREEN}Audit log has been cleared.{RESET}")