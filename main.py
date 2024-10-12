from db import create_record, load_database, read_record, update_record, delete_record
import json

def main():
    while True:
        print("\nChoose an option:")
        print("1. Create Record")
        print("2. Read Record")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            record = {
                "id": int(input("Enter ID: ")),
                "first_name": input("Enter First Name: "),
                "last_name": input("Enter Last Name: "),
            }
            optional_fields = {}
            email = input("Enter Email (optional): ")
            phone = input("Enter Phone (optional): ")
            if email:
                optional_fields["email"] = email
            if phone:
                optional_fields["phone"] = phone
            record.update(optional_fields)
            try:
                create_record(record)
                print("Record created successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            record_id = int(input("Enter ID of the record to read: "))
            record = read_record(record_id)
            if record:
                print("Record:", json.dumps(record, indent=4))
            else:
                print("Record not found.")

        elif choice == '3':
            record_id = int(input("Enter ID of the record to update: "))
            updated_record = {
                "first_name": input("Enter new First Name: "),
                "last_name": input("Enter new Last Name: "),
            }
            optional_fields = {}
            email = input("Enter new Email (optional): ")
            phone = input("Enter new Phone (optional): ")
            if email:
                optional_fields["email"] = email
            if phone:
                optional_fields["phone"] = phone
            updated_record.update(optional_fields)
            try:
                update_record(record_id, updated_record)
                print("Record updated successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '4':
            record_id = int(input("Enter ID of the record to delete: "))
            delete_record(record_id)
            print("Record deleted successfully.")

        elif choice == '5':
            break

if __name__ == "__main__":
    load_database()
    main()
