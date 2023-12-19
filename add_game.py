import csv
import os

def add_game(username, game):
    file_path = r"Info\users.csv"
    is_game_added = False

    # Check if the file exists
    file_exists = os.path.exists(file_path)

    # Read existing content if the file exists
    existing_data = []
    if file_exists:
        with open(file_path, mode='r', newline='') as dosya:
            csv_reader = csv.DictReader(dosya)
            existing_data = list(csv_reader)

    # Find the user in the existing data
    user_found = False
    for row in existing_data:
        if row['Username'] == username:
            # Check if the game is already in the list
            if game not in row['Game']:
                # Append the new game to the existing games
                row['Game'] = row.get('Game', '') + ',' + game
                is_game_added = True
            user_found = True
            break

    # If the user is not found, add a new entry
    if not user_found:
        existing_data.append({'Username': username, 'Game': game})
        is_game_added = True

    # Write the updated content back to the file
    with open(file_path, mode='w', newline='') as dosya:
        fields = ['Username', 'Game']
        csv_writer = csv.DictWriter(dosya, fieldnames=fields)
        csv_writer.writeheader()
        csv_writer.writerows(existing_data)

    return is_game_added
