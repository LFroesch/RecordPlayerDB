import json

def load_records():
    try:
        with open("rcords.json", "r") as file:
            records = json.load(file)
            # Convert old format records to new format
            normalized_records = []
            for record in records:
                if isinstance(record, list):
                    # Old format [Artist, Record] - convert to dict
                    normalized_record = {
                        "Artist": record[0] if len(record) > 0 else "",
                        "Record": record[1] if len(record) > 1 else "",
                        "Year": record[2] if len(record) > 2 else "",
                        "Rating": record[3] if len(record) > 3 else "",
                        "Notes": record[4] if len(record) > 4 else "",
                        "Price": record[5] if len(record) > 5 else ""
                    }
                    normalized_records.append(normalized_record)
                elif isinstance(record, dict):
                    # New format - ensure all fields exist
                    normalized_record = {
                        "Artist": record.get("Artist", ""),
                        "Record": record.get("Record", ""),
                        "Year": record.get("Year", ""),
                        "Rating": record.get("Rating", ""),
                        "Notes": record.get("Notes", ""),
                        "Price": record.get("Price", "")
                    }
                    normalized_records.append(normalized_record)
            return normalized_records
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error reading records file - file may be corrupted")
        return []

records = load_records()

def search_records(records, search_term):
    """Search records by artist name, album name, or notes"""
    search_results = []
    search_term_lower = search_term.lower()
    
    for record in records:
        if isinstance(record, dict):
            # Search in artist, record name, and notes
            searchable_text = f"{record.get('Artist', '')} {record.get('Record', '')} {record.get('Notes', '')}"
            if search_term_lower in searchable_text.lower():
                search_results.append(record)
        elif isinstance(record, list) and len(record) >= 2:
            # Handle old format for backward compatibility
            searchable_text = f"{record[0]} {record[1]}"
            if search_term_lower in searchable_text.lower():
                # Convert to dict format for consistency
                normalized_record = {
                    "Artist": record[0],
                    "Record": record[1],
                    "Year": record[2] if len(record) > 2 else "",
                    "Rating": record[3] if len(record) > 3 else "",
                    "Notes": record[4] if len(record) > 4 else "",
                    "Price": record[5] if len(record) > 5 else ""
                }
                search_results.append(normalized_record)
    
    return search_results

def save_records(records):
    """Save records in the new dictionary format"""
    try:
        # Ensure all records are in the proper dictionary format
        formatted_records = []
        for record in records:
            if isinstance(record, dict):
                # Clean up empty fields for cleaner JSON
                clean_record = {}
                for key, value in record.items():
                    if value:  # Only include non-empty fields
                        clean_record[key] = value
                    else:
                        clean_record[key] = ""  # Keep structure but with empty string
                formatted_records.append(clean_record)
            elif isinstance(record, list):
                # Convert old format to new format
                clean_record = {
                    "Artist": record[0] if len(record) > 0 else "",
                    "Record": record[1] if len(record) > 1 else "",
                    "Year": record[2] if len(record) > 2 else "",
                    "Rating": record[3] if len(record) > 3 else "",
                    "Notes": record[4] if len(record) > 4 else "",
                    "Price": record[5] if len(record) > 5 else ""
                }
                formatted_records.append(clean_record)
        
        # Sort by artist name (case insensitive)
        formatted_records.sort(key=lambda x: x.get("Artist", "").lower())
        
        with open("rcords.json", "w") as file:
            json.dump(formatted_records, file, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error saving records: {e}")
        return False

def add_to_records(records, artist, record, year="", rating="", notes="", price=""):
    """Add a new record with all possible fields"""
    new_record = {
        "Artist": artist,
        "Record": record,
        "Year": year,
        "Rating": rating,
        "Notes": notes,
        "Price": price
    }
    
    # Check for duplicates
    for existing_record in records:
        if isinstance(existing_record, dict):
            if (existing_record.get("Artist", "").lower() == artist.lower() and 
                existing_record.get("Record", "").lower() == record.lower()):
                print(f"Record already exists: {artist} - {record}")
                return False
        elif isinstance(existing_record, list) and len(existing_record) >= 2:
            if (existing_record[0].lower() == artist.lower() and 
                existing_record[1].lower() == record.lower()):
                print(f"Record already exists: {artist} - {record}")
                return False
    
    records.append(new_record)
    return save_records(records)

def del_from_records(records, artist, record):
    """Delete a record by artist and record name"""
    records_to_remove = []
    
    for i, existing_record in enumerate(records):
        if isinstance(existing_record, dict):
            if (existing_record.get("Artist", "") == artist and 
                existing_record.get("Record", "") == record):
                records_to_remove.append(i)
        elif isinstance(existing_record, list) and len(existing_record) >= 2:
            if existing_record[0] == artist and existing_record[1] == record:
                records_to_remove.append(i)
    
    # Remove records in reverse order to maintain indices
    for i in reversed(records_to_remove):
        records.pop(i)
    
    if records_to_remove:
        return save_records(records)
    return False

def update_record(records, old_artist, old_record, new_data):
    """Update an existing record with new data"""
    for i, existing_record in enumerate(records):
        if isinstance(existing_record, dict):
            if (existing_record.get("Artist", "") == old_artist and 
                existing_record.get("Record", "") == old_record):
                records[i] = new_data
                return save_records(records)
        elif isinstance(existing_record, list) and len(existing_record) >= 2:
            if existing_record[0] == old_artist and existing_record[1] == old_record:
                records[i] = new_data
                return save_records(records)
    return False

def get_record_by_artist_and_name(records, artist, record_name):
    """Get a specific record by artist and name"""
    for record in records:
        if isinstance(record, dict):
            if (record.get("Artist", "") == artist and 
                record.get("Record", "") == record_name):
                return record
        elif isinstance(record, list) and len(record) >= 2:
            if record[0] == artist and record[1] == record_name:
                # Convert to dict format
                return {
                    "Artist": record[0],
                    "Record": record[1],
                    "Year": record[2] if len(record) > 2 else "",
                    "Rating": record[3] if len(record) > 3 else "",
                    "Notes": record[4] if len(record) > 4 else "",
                    "Price": record[5] if len(record) > 5 else ""
                }
    return None

def get_statistics(records):
    """Get collection statistics"""
    stats = {
        "total_records": len(records),
        "artists": set(),
        "years": set(),
        "ratings": {},
        "total_price": 0.0
    }
    
    for record in records:
        if isinstance(record, dict):
            # Count unique artists
            if record.get("Artist"):
                stats["artists"].add(record["Artist"])
            
            # Count years
            if record.get("Year"):
                stats["years"].add(record["Year"])
            
            # Count ratings
            rating = record.get("Rating")
            if rating:
                stats["ratings"][rating] = stats["ratings"].get(rating, 0) + 1
            
            # Sum prices
            price = record.get("Price")
            if price:
                try:
                    stats["total_price"] += float(price)
                except ValueError:
                    pass  # Skip invalid prices
    
    stats["unique_artists"] = len(stats["artists"])
    stats["year_range"] = f"{min(stats['years'])} - {max(stats['years'])}" if stats["years"] else "Unknown"
    
    return stats