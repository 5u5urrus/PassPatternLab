import sys
from collections import defaultdict, Counter
import re

def analyzePasswords(file_path):
    #Initialize a dictionary to hold counters for each position
    position_counters = defaultdict(Counter)
    total_passwords = 0

    # Maximum password length to consider
    max_password_length = 32

    # read the file and update counters
    with open(file_path, 'r', errors='ignore') as file:
        for line in file:
            password = line.strip().lower()  # Consider passwords in lowercase for uniformity
            if len(password) <= max_password_length:
                total_passwords += 1
                for position, char in enumerate(password):
                    position_counters[position][char] += 1

    # Analyze and print the most common characters for each position
    for position, counter in sorted(position_counters.items()):
        if position > max_password_length:
            break
        most_common_char, count = counter.most_common(1)[0]
        print(f"Position {position + 1}: Most common character is '{most_common_char}' with {count} appearances ({(count / total_passwords) * 100:.2f}% of passwords).")

# Example usage
#file_path = '/home/atom/shared/gmail-leaks/gmail.txt'  # not good
file_path = str(sys.argv[1])
analyzePasswords(file_path)
