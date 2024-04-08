import sys
from collections import defaultdict

def analyzePasswords(filePath, maxLength=16):
    positionFollowers = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    totalFollowers = defaultdict(lambda: defaultdict(int))

    with open(filePath, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            password = line.strip()
            for i in range(min(len(password) - 1, maxLength - 1)):
                currentChar = password[i]
                nextChar = password[i + 1]
                positionFollowers[i][currentChar][nextChar] += 1
                totalFollowers[i][currentChar] += 1

    for position in range(maxLength - 1):
        print(f"\nPosition {position + 1}:")
        results = []
        for char in positionFollowers[position]:
            followers = positionFollowers[position][char]
            if followers:
                mostCommonFollower, occurrences = max(followers.items(), key=lambda item: item[1])
                percentage = (occurrences / totalFollowers[position][char]) * 100
                results.append((char, mostCommonFollower, occurrences, percentage))
        
        sortedResults = sorted(results, key=lambda x: x[2], reverse=True)

        for char, mostCommonFollower, occurrences, percentage in sortedResults:
            print(f"  Character '{char}' most often followed by '{mostCommonFollower}' (Occurrences: {occurrences}, {percentage:.2f}%)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_next_each.py [password_file]")
        sys.exit(1)

    passwordFile = sys.argv[1]
    analyzePasswords(passwordFile, maxLength=16)
