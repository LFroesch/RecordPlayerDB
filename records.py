import json

def load_records():
    try:
        with open("rcords.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return records

records = load_records()



def save_records(records):
    with open("rcords.json", "w") as file:
        json.dump(records, file)


def search_records(records, artist_name):
    search_results = []
    for record in records:
        if artist_name.lower() in record["Artist"].lower():
            search_results.append(record)
    return search_results

def save_records(records):
    formatted_records = []
    for record in records:
        if isinstance(record, list):
            formatted_records.append({"Artist": record[0], "Record": record[1]})
        elif isinstance(record, dict):
            formatted_records.append(record)
    with open("rcords.json", "w") as file:
        json.dump(formatted_records, file, indent=2)

def add_to_records(records, artist, record):
    records.append([artist, record])
    save_records(records)  # Save after each add
    return records