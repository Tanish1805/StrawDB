import pickle
from btree import BTree

DB_FILENAME = 'data/strawdb.bin'
btree = BTree(order=3)  # Order can be adjusted based on your requirement

def load_database():
    global btree
    try:
        with open(DB_FILENAME, 'rb') as file:
            btree = pickle.load(file)
    except FileNotFoundError:
        btree = BTree(order=3)

def save_database():
    with open(DB_FILENAME, 'wb') as file:
        pickle.dump(btree, file)

def validate_record(record):
    if 'id' not in record or not isinstance(record['id'], int):
        raise ValueError("Record must have an integer 'id'.")
    if 'first_name' not in record or not isinstance(record['first_name'], str):
        raise ValueError("Record must have a string 'first_name'.")
    if 'last_name' not in record or not isinstance(record['last_name'], str):
        raise ValueError("Record must have a string 'last_name'.")

def validate_updated_record(record):
    if 'id' in record:
        raise ValueError(f"ID should not be present in the data.")
    if 'first_name' not in record or not isinstance(record['first_name'], str):
        raise ValueError("Record must have a string 'first_name'.")
    if 'last_name' not in record or not isinstance(record['last_name'], str):
        raise ValueError("Record must have a string 'last_name'.")

def create_record(record):
    validate_record(record)  # Validate record before adding
    if btree.search(record['id']) is not None:
        raise ValueError(f"Record with ID {record['id']} already exists.")
    btree.insert(record['id'], record)  # Using id as key
    save_database()

def read_record(record_id):
    return btree.search(record_id)

def update_record(record_id, updated_record):
    validate_updated_record(updated_record)
    if btree.search(record_id) is not None:
        updated_record_with_id = {"id": record_id, **updated_record}
        print(f"Updating the record: {updated_record_with_id} at id: {record_id}")
        btree.update(record_id, updated_record_with_id)  # Update the record
        save_database()
    else:
        print(f"Record with ID {record_id} not found.")

def delete_record(record_id):
    print("Yet to be implemented")
    # if btree.search(record_id) is not None:
    #     btree.delete(record_id)
    #     save_database()
    # else:
    #     print(f"Record with ID {record_id} not found.")

def search_records(query):
    results = []
    # Search by ID
    if isinstance(query, int):
        record = btree.search(query)
        if record:
            results.append(record)
    # Search by first_name and last_name
    else:
        for node in btree.traverse():
            if node['first_name'] == query or node['last_name'] == query:
                results.append(node)
    return results
