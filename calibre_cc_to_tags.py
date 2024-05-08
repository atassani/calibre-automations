import subprocess
import json
import os

# Function to execute calibredb command and capture output
def run_calibredb_command(command):
    try:
        # Execute the command and capture output
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout
        else:
            print("Error:", result.stderr)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# Path to Calibre library
library_path = "/Users/toni.tassani/CalibreLibrary"

# Function to update tags based on custom column values
def update_tags(book_id, original_tags, read_order, read_status):
    read_order_tag = f"readorder:{read_order}"
    read_status_tag = "readstatus:read" if read_status else None

    # Remove existing tags with specified prefixes
    tags = [tag for tag in original_tags if not tag.startswith(('readorder:', 'readstatus:'))]

    # Add tags based on column values
    if read_order:
        tags.append(read_order_tag)
    if read_status:
        tags.append(read_status_tag)

    # Update tags for the book, if the tags are different
    if (set(original_tags) != set(tags)):
        tags_str = ", ".join(tags)
        command = f"calibredb set_metadata {book_id} --field tags:\"{tags_str}\" --library-path={library_path}"
        print(f'{book_id} "{tags_str}"')
        run_calibredb_command(command)

# Iterate through books in the library
command = f"calibredb list --library-path={library_path} --for-machine --fields title,tags,\\*readorder,\\*read"
output = run_calibredb_command(command)
if output:
    books = json.loads(output)
    for book in books:
        book_id = book['id']
        tags= book.get('tags', [])
        read_order = book.get('*readorder', None)
        read_status = book.get('*read', False)
        update_tags(book_id, tags, read_order, read_status)