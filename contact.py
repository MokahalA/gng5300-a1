'''
    This class is used to model a Contact object with the following input attributes:
        - first_name
        - last_name
        - phone_number
        - email (optional attribute)
        - address (optional attribute)
'''
from datetime import datetime

class Contact:
    '''Constructor to create a new contact with the given input attributes.'''
    def __init__(self, first_name, last_name, phone_number, email=None, address=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address

        # Time created and updated are the same when the contact is first created.
        self.time_created = datetime.now().replace(microsecond=0)
        self.time_updated = datetime.now().replace(microsecond=0)

        # Store the history of updates
        self.update_history = []

    '''Update the contact with the given input attributes and store the change history.'''
    def update(self, first_name=None, last_name=None, phone_number=None, email=None, address=None):
        old_values = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'address': self.address
        }

        # Check to see which attributes need to be updated.
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if phone_number:
            self.phone_number = phone_number
        if email:
            self.email = email
        if address:
            self.address = address

        # Modify the updated time to the current time.
        self.time_updated = datetime.now().replace(microsecond=0)

        # Add the changes to update history log
        self.update_history.append({
            'time_updated': self.time_updated,
            'old_values': old_values,
            'new_values': {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'phone_number': self.phone_number,
                'email': self.email,
                'address': self.address
            }
        })

    '''View the update history for the contact.'''
    def view_update_history(self):
        print(f"\n--- Update History for {self.first_name} {self.last_name} ---")
        if not self.update_history:
            print("No updates made to this contact.")
        else:
            for update in self.update_history:
                print(f"Updated on {update['time_updated']}:")
                print(f"  Old values: {update['old_values']}")
                print(f"  New values: {update['new_values']}")

    '''Define equality between two contact objects based on their core attributes.'''
    def __eq__(self, other):
        if not isinstance(other, Contact):
            return False
        return (self.first_name == other.first_name and
                self.last_name == other.last_name and
                self.phone_number == other.phone_number and
                self.email == other.email and
                self.address == other.address)

    '''Return a string representation of the contact.'''
    def __str__(self):
        return (f"\n{'-'*40}\n"
                f"Contact Name : {self.first_name} {self.last_name}\n"
                f"Phone Number : {self.phone_number}\n"
                f"Address      : {self.address if self.address else 'N/A'}\n"
                f"Email        : {self.email if self.email else 'N/A'}\n"
                f"Added on     : {self.time_created}\n"
                f"{'-'*40}\n")