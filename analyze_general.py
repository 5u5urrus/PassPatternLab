#Author: Vahe Demirkhanyan / Atom

from collections import Counter
import sys

def analyzeCharacterFrequency(file_path):
    character_counter = Counter()
    total_characters = 0

    with open(file_path, 'r', errors='ignore') as file:
        for line in file:
            password = line.strip()
            character_counter.update(password)
            total_characters += len(password)

    # Convert counts to percentages
    character_percentages = {char: (count / total_characters) * 100 for char, count in character_counter.items()}

    # Sort characters by highest percentage
    sorted_characters = sorted(character_percentages.items(), key=lambda item: item[1], reverse=True)

    return sorted_characters

def printCharacterFrequencies(sorted_characters, columns=4):
    print("Characters sorted by how common they occurred (highest to lowest percentage):")
    # Determine the number of rows needed
    rows = len(sorted_characters) // columns + (1 if len(sorted_characters) % columns else 0)
    for row in range(rows):
        output = ""
        for col in range(columns):
            index = row + col * rows
            if index < len(sorted_characters):
                char, percentage = sorted_characters[index]
                output += f"{char}: {percentage:.2f}%".ljust(15)  # Adjust width as needed
        print(output)

# Example usage
if len(sys.argv) > 1:
    file_path = str(sys.argv[1])
    sorted_characters = analyzeCharacterFrequency(file_path)
    printCharacterFrequencies(sorted_characters)
else:
    print("Usage: python analyze_general.py <file_path>")

