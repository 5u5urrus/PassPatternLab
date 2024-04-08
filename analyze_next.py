import sys
from collections import defaultdict, Counter

def isAsciiPrintable(s):
    return all(32 <= ord(c) <= 126 for c in s)

def analyzePasswords(file_path):
    followers = defaultdict(Counter)
    charOccurrences = defaultdict(int)
    totalPasswords, filteredPasswords = 0, 0  # Add counters for diagnostics

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:  # Ensure proper handling of encoding
        for line in file:
            totalPasswords += 1
            password = line.strip()
            if not isAsciiPrintable(password):
                filteredPasswords += 1
                continue  # Skip non-ASCII printable passwords
            for i in range(len(password) - 1):
                currentChar = password[i]
                nextChar = password[i + 1]
                followers[currentChar].update([nextChar])
                charOccurrences[currentChar] += 1

    # diagnose the problem
    print(f"Total passwords processed: {totalPasswords}")
    print(f"Passwords filtered out (non-ASCII printable): {filteredPasswords}")

    for char, counter in followers.items():
        if counter:
            mostCommonFollower, occurrences = counter.most_common(1)[0]
            percentage = (occurrences / charOccurrences[char]) * 100
            print(f"Character '{char}' most often followed by: '{mostCommonFollower}' (Occurrences: {occurrences}, {percentage:.2f}%)")
        else:
            print(f"Character '{char}' is not followed by any character.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_next.py [password_file]")
        sys.exit(1)

    passwordFile = sys.argv[1]
    analyzePasswords(passwordFile)
