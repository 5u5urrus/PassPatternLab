import sys
import string
from collections import defaultdict, Counter

# Define the set of special characters we're interested in
specialCharacters = set('!@#$%^&*()-_=+[]{};:\'",.<>/?\\|~`')

# ANSI escape code for bright green text
brightGreen = '\033[92m'
reset = '\033[0m'

def analyzePasswordsFromFile(file_path, max_length=20):
    positionCounters = defaultdict(lambda: Counter({'lower': 0, 'upper': 0, 'number': 0, 'special': 0}))
    charCounters = defaultdict(Counter)

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for password in file:
            password = password.strip()[:max_length]
            for i, char in enumerate(password):
                if char in string.ascii_lowercase:
                    positionCounters[i]['lower'] += 1
                elif char in string.ascii_uppercase:
                    positionCounters[i]['upper'] += 1
                elif char in string.digits:
                    positionCounters[i]['number'] += 1
                if char in specialCharacters:
                    positionCounters[i]['special'] += 1
                if char.isalnum() or char in specialCharacters:
                    charCounters[i][char] += 1

    for i in range(max_length):
        total_chars = sum(positionCounters[i].values())
        for char_type in positionCounters[i]:
            if total_chars > 0:
                positionCounters[i][char_type] = (positionCounters[i][char_type] / total_chars) * 100

    return positionCounters, charCounters

def printAnalysisResults(typeAnalysisResult, charAnalysisResult, max_length=20):
    headers = ['Position', 'Lower', 'Upper', 'Number', 'Special', 'Most Common', 'Least Common', 'Least Used Letter', 'Least Used Number', 'Least Used Special']
    print(' '.join(f"{header:>15}" for header in headers))

    for i in range(max_length):
        highest_percentage = max(typeAnalysisResult[i].values(), default=0)
        row = [f"{i + 1:>15}"]
        for char_type in ['lower', 'upper', 'number', 'special']:
            percentage = typeAnalysisResult[i].get(char_type, 0)
            formatted_percentage = f"{percentage:.2f}%"
            if percentage == highest_percentage:
                # Highlight the highest percentage in bright green
                row.append(f"{brightGreen}{formatted_percentage:>15}{reset}")
            else:
                row.append(f"{formatted_percentage:>15}")
        
        most_common_chars = ' '.join([char for char, _ in charAnalysisResult[i].most_common(5)])
        least_common_chars = ' '.join([char for char, count in sorted(charAnalysisResult[i].items(), key=lambda item: item[1]) if char not in specialCharacters or char.isalnum()][:5])
        least_used_letters = ' '.join([char for char, count in sorted(charAnalysisResult[i].items(), key=lambda item: item[1]) if char in string.ascii_letters][:5])
        least_used_numbers = ' '.join([char for char, count in sorted(charAnalysisResult[i].items(), key=lambda item: item[1]) if char.isdigit()][:5])
        least_used_specials = ' '.join([char for char, count in sorted(charAnalysisResult[i].items(), key=lambda item: item[1]) if char in specialCharacters][:5])
        
        row.extend([f"{most_common_chars:>15}", f"{least_common_chars:>15}", f"{least_used_letters:>15}", f"{least_used_numbers:>15}", f"{least_used_specials:>15}"])
        print(' '.join(row))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Example: python analyze_type.py [wordlist-file]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    positionCounters, charAnalysisResult = analyzePasswordsFromFile(file_path)
    printAnalysisResults(positionCounters, charAnalysisResult)
