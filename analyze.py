import sys
from collections import defaultdict
from prettytable import PrettyTable

def analyzePasswordsDetailed(file_path):
    # Initialize a nested defaultdict to hold counters for characters at each position
    position_character_counters = defaultdict(lambda: defaultdict(int))
    total_passwords = 0

    max_password_length = 32  #Define a reasonable maximum length for analysis

    with open(file_path, 'r', errors='ignore') as file:
        for line in file:
            password = line.strip()
            if len(password) <= max_password_length:
                total_passwords += 1
                for position, char in enumerate(password):
                    position_character_counters[position][char] += 1

    return position_character_counters, total_passwords

def printDetailedStats(position_character_counters, total_passwords):
    for position, character_counter in position_character_counters.items():
        # Initialize PrettyTable with headings
        table = PrettyTable()
        table.field_names = ["Character", "Occurrences", "Percentage"]
        
        # Sort characters by occurrence percentage in descending order
        sorted_characters = sorted(character_counter.items(), key=lambda item: (item[1] / total_passwords), reverse=True)
        
        for char, count in sorted_characters:
            percentage = (count / total_passwords) * 100
            # Add each character's stats as a new row in the table
            table.add_row([char, count, f"{percentage:.2f}%"])
        
        print(f"\nPosition {position + 1} (sorted by highest occurrence):")
        print(table)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = str(sys.argv[1])
        position_character_counters, total_passwords = analyzePasswordsDetailed(file_path)
        printDetailedStats(position_character_counters, total_passwords)
    else:
        print("Example: python analyze.py [file_path]")
