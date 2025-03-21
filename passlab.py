#!/usr/bin/env python3
# Unified Password Analyzer
# Author: Vahe Demirkhanyan

import sys
import os
import string
import argparse
import re
import math
import json
import itertools
from collections import defaultdict, Counter
from datetime import datetime
from prettytable import PrettyTable

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BRIGHT_GREEN = '\033[92m'

def is_ascii_printable(s):
    return all(32 <= ord(c) <= 126 for c in s)

def get_char_category(char):
    if char in string.ascii_lowercase:
        return 'lowercase'
    elif char in string.ascii_uppercase:
        return 'uppercase'
    elif char in string.digits:
        return 'digit'
    else:
        return 'special'

def pattern_to_regex(pattern):
    translation = {
        'L': '[A-Z]',
        'l': '[a-z]',
        'd': '[0-9]',
        's': '[!@#$%^&*()_+\\-=\\[\\]{};:\'",.<>/?\\\\|`~]'
    }
    regex_pattern = '^'
    for char in pattern:
        if char in translation:
            regex_pattern += translation[char]
        else:
            regex_pattern += re.escape(char)
    regex_pattern += '$'
    return regex_pattern

def get_entropy(password):
    char_sets = {
        'lowercase': 26,
        'uppercase': 26,
        'digit': 10, 
        'special': 33
    }
    
    char_categories = set(get_char_category(c) for c in password)
    char_space = sum(char_sets[category] for category in char_categories)
    
    return len(password) * (char_space.bit_length() - 1)

def detect_keyboard_pattern(password, keyboard_layouts):
    for layout_name, layout in keyboard_layouts.items():
        for row in layout:
            window_size = min(len(password), len(row))
            for i in range(len(row) - window_size + 1):
                window = row[i:i+window_size]
                if window.lower() in password.lower():
                    return (layout_name, window)
                if window.lower()[::-1] in password.lower():
                    return (layout_name, window[::-1])
    return None

def detect_numerical_sequence(s):
    if len(s) < 3:
        return False
    
    if all(c.isdigit() for c in s):
        digits = [int(c) for c in s]
        if all(digits[i] == digits[i-1] + 1 for i in range(1, len(digits))):
            return True
        if all(digits[i] == digits[i-1] - 1 for i in range(1, len(digits))):
            return True
    
    return False

def detect_date_patterns(s):
    date_patterns = [
        r'\b(19|20)\d{2}[01]\d[0-3]\d\b',
        r'\b[0-3]\d[01]\d(19|20)\d{2}\b',
        r'\b[01]\d[0-3]\d(19|20)\d{2}\b',
        r'\b(19|20)\d{2}[01]\d\b',
        r'\b[01]\d(19|20)\d{2}\b',
        r'\b[01]\d[0-3]\d\d{2}\b'
    ]
    
    for pattern in date_patterns:
        if re.search(pattern, s):
            return True
    return False

def is_leetspeak(word):
    leet_map = {
        '4': 'a', '@': 'a', '8': 'b', '(': 'c', '3': 'e', 
        '6': 'g', '9': 'g', '1': 'i', '!': 'i', '0': 'o',
        '5': 's', '$': 's', '7': 't', '+': 't', '2': 'z'
    }
    
    if any(c in leet_map for c in word):
        return True
    return False

def analyzePasswordsFromFile(file_path, max_length=20):
    positionCounters = defaultdict(lambda: Counter({'lower': 0, 'upper': 0, 'number': 0, 'special': 0}))
    charCounters = defaultdict(Counter)
    specialCharacters = set('!@#$%^&*()-_=+[]{};:\'",.<>/?\\|~`')
    
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
    specialCharacters = set('!@#$%^&*()-_=+[]{};:\'",.<>/?\\|~`')
    bright_green = '\033[92m'
    reset = '\033[0m'
    
    headers = ['Position', 'Lower', 'Upper', 'Number', 'Special', 'Most Common', 'Least Common', 'Least Used Letter', 'Least Used Number', 'Least Used Special']
    print(' '.join(f"{header:>15}" for header in headers))
    
    for i in range(max_length):
        highest_percentage = max(typeAnalysisResult[i].values(), default=0)
        row = [f"{i + 1:>15}"]
        
        for char_type in ['lower', 'upper', 'number', 'special']:
            percentage = typeAnalysisResult[i].get(char_type, 0)
            formatted_percentage = f"{percentage:.2f}%"
            if percentage == highest_percentage:
                row.append(f"{bright_green}{formatted_percentage:>15}{reset}")
            else:
                row.append(f"{formatted_percentage:>15}")
        
        # Fix the syntax error in the original code
        most_common_chars = ' '.join([char for char, count in charAnalysisResult[i].most_common(5)])
        
        least_common_chars = ' '.join([char for char, count in sorted(charAnalysisResult[i].items(), key=lambda item: item[1]) 
                                      if char.isalnum() or char in specialCharacters][:5])
        
        least_used_letters = ' '.join([char for char, count in sorted(charAnalysisResult[i].items(), key=lambda item: item[1]) 
                                      if char in string.ascii_letters][:5])
        
        least_used_numbers = ' '.join([char for char, count in sorted(charAnalysisResult[i].items(), key=lambda item: item[1]) 
                                      if char.isdigit()][:5])
        
        least_used_specials = ' '.join([char for char, count in sorted(charAnalysisResult[i].items(), key=lambda item: item[1]) 
                                       if char in specialCharacters][:5])
        
        row.extend([f"{most_common_chars:>15}", f"{least_common_chars:>15}", f"{least_used_letters:>15}", 
                   f"{least_used_numbers:>15}", f"{least_used_specials:>15}"])
        
        print(' '.join(row))

class PasswordAnalyzer:
    def __init__(self, file_path, max_length=32, min_length=1, output_dir=None, 
                 exclude_non_ascii=False, pattern=None, verbose=False,
                 dictionary=None, enhanced=False):
        self.file_path = file_path
        self.max_length = max_length
        self.min_length = min_length
        self.output_dir = output_dir
        self.exclude_non_ascii = exclude_non_ascii
        self.pattern = pattern
        self.verbose = verbose
        self.enhanced = enhanced
        self.dictionary_file = dictionary
        self.dictionary_words = set()
        
        self.total_passwords = 0
        self.filtered_passwords = 0
        self.valid_passwords = 0
        self.length_distribution = Counter()
        self.special_chars = set('!@#$%^&*()-_=+[]{};:\'",.<>/?\\|~`')
        
        self.position_character_counters = defaultdict(Counter)
        self.position_type_counters = defaultdict(lambda: Counter({'lowercase': 0, 'uppercase': 0, 'digit': 0, 'special': 0}))
        self.followers = defaultdict(Counter)
        self.position_followers = defaultdict(lambda: defaultdict(Counter))
        self.character_overall_counter = Counter()
        self.total_chars = 0
        self.patterns = Counter()
        self.password_entropy = []
        
        self.repetitive_sequences = Counter()
        self.keyboard_sequences = Counter()
        self.date_patterns = Counter()
        self.common_words = Counter()
        self.leetspeak_count = 0
        self.numeric_sequences = 0
        self.capitalization_patterns = Counter()
        self.word_boundaries = Counter()
        self.password_pairs = Counter()
        self.trigram_frequency = Counter()
        self.english_words_detected = 0
        self.number_suffix_patterns = Counter()
        self.special_char_positions = defaultdict(int)
        self.complexity_distribution = defaultdict(int)
        
        self.keyboard_layouts = {
            'QWERTY': ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'],
            'AZERTY': ['azertyuiop', 'qsdfghjklm', 'wxcvbn'],
            'Numeric': ['123', '456', '789', '0']
        }
        
        self.pattern_matcher = None
        if pattern:
            try:
                self.pattern_matcher = re.compile(pattern_to_regex(pattern))
            except re.error:
                self.pattern_matcher = None
        
        if dictionary:
            try:
                with open(dictionary, 'r', encoding='utf-8', errors='ignore') as f:
                    self.dictionary_words = set(word.strip().lower() for word in f)
            except:
                print(f"{Colors.RED}Error loading dictionary file.{Colors.RESET}")
    
    def analyze(self):
        start_time = datetime.now()
        
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    password = line.strip()
                    self.total_passwords += 1
                    
                    if self.exclude_non_ascii and not is_ascii_printable(password):
                        self.filtered_passwords += 1
                        continue
                    
                    if len(password) < self.min_length or len(password) > self.max_length:
                        self.filtered_passwords += 1
                        continue
                    
                    if self.pattern_matcher and not self.pattern_matcher.match(password):
                        self.filtered_passwords += 1
                        continue
                    
                    self.valid_passwords += 1
                    self.length_distribution[len(password)] += 1
                    self._analyze_password(password)
                    
                    if self.enhanced:
                        self._enhanced_analysis(password)
                    
                    if self.verbose and self.total_passwords % 100000 == 0:
                        print(f"Processed {self.total_passwords} passwords...")
        
        except FileNotFoundError:
            print(f"{Colors.RED}Error: File '{self.file_path}' not found.{Colors.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"{Colors.RED}Error processing file: {e}{Colors.RESET}")
            sys.exit(1)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        print(f"{Colors.GREEN}Analysis completed in {processing_time:.2f} seconds.{Colors.RESET}")
        print(f"Total passwords: {self.total_passwords}")
        print(f"Valid passwords processed: {self.valid_passwords}")
        print(f"Filtered passwords: {self.filtered_passwords}")
        
    def _analyze_password(self, password):
        pattern = ''.join(self._get_pattern_char(c) for c in password)
        self.patterns[pattern] += 1
        
        entropy = get_entropy(password)
        self.password_entropy.append((password, entropy))
        
        for position, char in enumerate(password):
            if position < self.max_length:
                self.position_character_counters[position][char] += 1
                
                char_category = get_char_category(char)
                self.position_type_counters[position][char_category] += 1
                
                if position < len(password) - 1:
                    next_char = password[position + 1]
                    self.followers[char][next_char] += 1
                    self.position_followers[position][char][next_char] += 1
        
        self.character_overall_counter.update(password)
        self.total_chars += len(password)
        
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in self.special_chars for c in password)
        
        complexity = sum([has_lower, has_upper, has_digit, has_special])
        self.complexity_distribution[complexity] += 1
        
        for i in range(len(password) - 2):
            trigram = password[i:i+3]
            self.trigram_frequency[trigram] += 1
    
    def _enhanced_analysis(self, password):
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                rep_seq = password[i] * 3
                j = i + 3
                while j < len(password) and password[j] == password[i]:
                    rep_seq += password[i]
                    j += 1
                if len(rep_seq) >= 3:
                    self.repetitive_sequences[rep_seq] += 1
        
        keyboard_pattern = detect_keyboard_pattern(password, self.keyboard_layouts)
        if keyboard_pattern:
            self.keyboard_sequences[keyboard_pattern[1]] += 1
        
        for i in range(len(password) - 2):
            substr = password[i:i+3]
            if detect_numerical_sequence(substr):
                self.numeric_sequences += 1
                break
        
        if detect_date_patterns(password):
            self.date_patterns[password] += 1
        
        if is_leetspeak(password):
            self.leetspeak_count += 1
        
        alpha_prefix = re.match(r'^([a-zA-Z]+)([0-9]+)$', password)
        if alpha_prefix:
            prefix, suffix = alpha_prefix.groups()
            self.number_suffix_patterns[suffix] += 1
        
        for i, char in enumerate(password):
            if char in self.special_chars:
                self.special_char_positions[i] += 1
        
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            if password[0].isupper() and all(c.islower() for c in password[1:] if c.isalpha()):
                self.capitalization_patterns['First letter'] += 1
            elif all(c.isupper() for c in password if c.isalpha()):
                self.capitalization_patterns['ALL CAPS'] += 1
            elif password[0].islower() and any(password[i].isupper() and password[i-1].islower() for i in range(1, len(password))):
                self.capitalization_patterns['camelCase'] += 1
            else:
                self.capitalization_patterns['Random'] += 1
        
        if self.dictionary_words:
            password_lower = password.lower()
            for word in self.dictionary_words:
                if len(word) >= 4 and word in password_lower:
                    self.common_words[word] += 1
                    self.english_words_detected += 1
                    idx = password_lower.find(word)
                    if idx > 0:
                        prefix = password[idx-1]
                        self.word_boundaries[f"prefix_{prefix}"] += 1
                    if idx + len(word) < len(password):
                        suffix = password[idx+len(word)]
                        self.word_boundaries[f"suffix_{suffix}"] += 1
        
        if len(password) > 1:
            for i in range(1, min(5, len(password))):
                self.password_pairs[f"{password[:-i]}|{password}"] += 1
    
    def _get_pattern_char(self, char):
        if char in string.ascii_lowercase:
            return 'l'
        elif char in string.ascii_uppercase:
            return 'L'
        elif char in string.digits:
            return 'd'
        else:
            return 's'
    
    def print_summary(self):
        print(f"\n{Colors.BOLD}{Colors.UNDERLINE}PASSWORD ANALYSIS SUMMARY{Colors.RESET}")
        print(f"\nAnalyzed {self.valid_passwords} passwords from {self.file_path}")
        
        if self.valid_passwords > 0:
            avg_length = sum(length * count for length, count in self.length_distribution.items()) / self.valid_passwords
            print(f"\n{Colors.BOLD}Password Length Statistics:{Colors.RESET}")
            print(f"Average length: {avg_length:.2f} characters")
            print(f"Minimum length: {min(self.length_distribution.keys())} characters")
            print(f"Maximum length: {max(self.length_distribution.keys())} characters")
            
            print(f"\n{Colors.BOLD}Most Common Lengths:{Colors.RESET}")
            for length, count in self.length_distribution.most_common(5):
                percentage = (count / self.valid_passwords) * 100
                print(f"Length {length}: {count} passwords ({percentage:.2f}%)")
        
        print(f"\n{Colors.BOLD}Most Common Patterns:{Colors.RESET}")
        for pattern, count in self.patterns.most_common(5):
            percentage = (count / self.valid_passwords) * 100
            print(f"Pattern '{pattern}': {count} passwords ({percentage:.2f}%)")
            
        if self.password_entropy:
            entropies = [e for _, e in self.password_entropy]
            avg_entropy = sum(entropies) / len(entropies)
            min_entropy = min(entropies)
            max_entropy = max(entropies)
            
            print(f"\n{Colors.BOLD}Password Entropy:{Colors.RESET}")
            print(f"Average entropy: {avg_entropy:.2f} bits")
            print(f"Minimum entropy: {min_entropy:.2f} bits")
            print(f"Maximum entropy: {max_entropy:.2f} bits")
        
        print(f"\n{Colors.BOLD}Password Complexity Distribution:{Colors.RESET}")
        complexity_table = PrettyTable()
        complexity_table.field_names = ["Complexity Level", "Description", "Count", "Percentage"]
        
        complexity_desc = {
            0: "No character type (should not occur)",
            1: "Single character type (e.g., only lowercase)",
            2: "Two character types (e.g., lowercase + digits)",
            3: "Three character types (e.g., lower + upper + digits)",
            4: "All character types (lower + upper + digits + special)"
        }
        
        for complexity, count in sorted(self.complexity_distribution.items()):
            percentage = (count / self.valid_passwords) * 100
            complexity_table.add_row([
                complexity, 
                complexity_desc.get(complexity, "Unknown"), 
                count, 
                f"{percentage:.2f}%"
            ])
        
        print(complexity_table)
    
    def print_character_analysis(self):
        print(f"\n{Colors.BOLD}{Colors.UNDERLINE}CHARACTER ANALYSIS{Colors.RESET}")
        
        if self.total_chars > 0:
            print(f"\n{Colors.BOLD}Overall Character Frequency:{Colors.RESET}")
            character_percentages = {char: (count / self.total_chars) * 100 
                                    for char, count in self.character_overall_counter.items()}
            sorted_characters = sorted(character_percentages.items(), key=lambda item: item[1], reverse=True)
            
            table = PrettyTable()
            table.field_names = ["Character", "Count", "Percentage"]
            for char, percentage in sorted_characters[:20]:
                count = self.character_overall_counter[char]
                table.add_row([char, count, f"{percentage:.2f}%"])
            print(table)
            
            # Print character category distribution
            lowercase_count = sum(self.character_overall_counter[c] for c in string.ascii_lowercase)
            uppercase_count = sum(self.character_overall_counter[c] for c in string.ascii_uppercase)
            digit_count = sum(self.character_overall_counter[c] for c in string.digits)
            special_count = sum(self.character_overall_counter[c] for c in self.special_chars)
            
            print(f"\n{Colors.BOLD}Character Category Distribution:{Colors.RESET}")
            category_table = PrettyTable()
            category_table.field_names = ["Category", "Count", "Percentage"]
            
            categories = [
                ("Lowercase", lowercase_count),
                ("Uppercase", uppercase_count),
                ("Digits", digit_count),
                ("Special", special_count)
            ]
            
            for category, count in categories:
                percentage = (count / self.total_chars) * 100
                category_table.add_row([category, count, f"{percentage:.2f}%"])
            
            print(category_table)
    
    def print_position_analysis(self, max_positions=10, top_chars=5):
        print(f"\n{Colors.BOLD}{Colors.UNDERLINE}POSITION ANALYSIS{Colors.RESET}")
        
        positions_to_show = min(max_positions, max(self.position_character_counters.keys()) + 1)
        
        print(f"\n{Colors.BOLD}Character Type Distribution by Position:{Colors.RESET}")
        type_table = PrettyTable()
        type_table.field_names = ["Position", "Lowercase %", "Uppercase %", "Digit %", "Special %", "Most Common Type"]
        
        for position in range(positions_to_show):
            total = sum(self.position_type_counters[position].values())
            if total > 0:
                lowercase_pct = (self.position_type_counters[position]['lowercase'] / total) * 100
                uppercase_pct = (self.position_type_counters[position]['uppercase'] / total) * 100
                digit_pct = (self.position_type_counters[position]['digit'] / total) * 100
                special_pct = (self.position_type_counters[position]['special'] / total) * 100
                
                most_common_type = max(self.position_type_counters[position].items(), key=lambda x: x[1])[0]
                
                type_table.add_row([
                    position + 1,
                    f"{lowercase_pct:.2f}%",
                    f"{uppercase_pct:.2f}%",
                    f"{digit_pct:.2f}%",
                    f"{special_pct:.2f}%",
                    most_common_type
                ])
        
        print(type_table)
        
        print(f"\n{Colors.BOLD}Most Common Characters by Position:{Colors.RESET}")
        for position in range(positions_to_show):
            total = sum(self.position_character_counters[position].values())
            if total > 0:
                print(f"\n{Colors.BOLD}Position {position + 1}:{Colors.RESET}")
                table = PrettyTable()
                table.field_names = ["Character", "Count", "Percentage"]
                
                for char, count in self.position_character_counters[position].most_common(top_chars):
                    percentage = (count / total) * 100
                    table.add_row([char, count, f"{percentage:.2f}%"])
                
                print(table)
    
    def print_follower_analysis(self, top_followers=5):
        print(f"\n{Colors.BOLD}{Colors.UNDERLINE}CHARACTER SEQUENCE ANALYSIS{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}Most Common Character Followers (Overall):{Colors.RESET}")
        table = PrettyTable()
        table.field_names = ["Character", "Most Common Follower", "Count", "Percentage"]
        
        for char, char_count in self.character_overall_counter.most_common(15):
            if char in self.followers and char_count > 0:
                most_common = self.followers[char].most_common(1)
                if most_common:
                    follower, count = most_common[0]
                    percentage = (count / char_count) * 100
                    table.add_row([char, follower, count, f"{percentage:.2f}%"])
        
        print(table)
        
        print(f"\n{Colors.BOLD}Position-Specific Character Followers:{Colors.RESET}")
        for position in range(min(5, max(self.position_followers.keys()) + 1)):
            print(f"\n{Colors.BOLD}Position {position + 1}:{Colors.RESET}")
            position_table = PrettyTable()
            position_table.field_names = ["Character", "Most Common Follower", "Count", "Percentage"]
            
            for char, counter in self.position_followers[position].items():
                char_count = self.position_character_counters[position][char]
                if counter and char_count > 0:
                    follower, count = counter.most_common(1)[0]
                    percentage = (count / char_count) * 100
                    position_table.add_row([char, follower, count, f"{percentage:.2f}%"])
            
            position_table.sortby = "Percentage"
            position_table.reversesort = True
            
            rows = position_table._rows
            if len(rows) > top_followers:
                position_table._rows = rows[:top_followers]
            
            print(position_table)
        
        if self.trigram_frequency:
            print(f"\n{Colors.BOLD}Most Common 3-Character Sequences:{Colors.RESET}")
            trigram_table = PrettyTable()
            trigram_table.field_names = ["Trigram", "Count", "Percentage"]
            
            total_trigrams = sum(self.trigram_frequency.values())
            for trigram, count in self.trigram_frequency.most_common(10):
                percentage = (count / total_trigrams) * 100
                trigram_table.add_row([trigram, count, f"{percentage:.2f}%"])
            
            print(trigram_table)
    
    def print_enhanced_analysis(self):
        if not self.enhanced:
            return
            
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{Colors.UNDERLINE}ENHANCED PATTERN ANALYSIS{Colors.RESET}")
        
        if self.repetitive_sequences:
            print(f"\n{Colors.BOLD}Repetitive Character Sequences:{Colors.RESET}")
            rep_table = PrettyTable()
            rep_table.field_names = ["Sequence", "Count", "Percentage"]
            
            for seq, count in self.repetitive_sequences.most_common(10):
                percentage = (count / self.valid_passwords) * 100
                rep_table.add_row([seq, count, f"{percentage:.2f}%"])
            
            print(rep_table)
        
        if self.keyboard_sequences:
            print(f"\n{Colors.BOLD}Keyboard Pattern Sequences:{Colors.RESET}")
            key_table = PrettyTable()
            key_table.field_names = ["Sequence", "Count", "Percentage"]
            
            for seq, count in self.keyboard_sequences.most_common(10):
                percentage = (count / self.valid_passwords) * 100
                key_table.add_row([seq, count, f"{percentage:.2f}%"])
            
            print(key_table)
            
        print(f"\n{Colors.BOLD}Date Pattern Detection:{Colors.RESET}")
        date_percentage = (len(self.date_patterns) / self.valid_passwords) * 100
        print(f"Passwords containing date patterns: {len(self.date_patterns)} ({date_percentage:.2f}%)")
        
        print(f"\n{Colors.BOLD}Numeric Sequence Detection:{Colors.RESET}")
        num_seq_percentage = (self.numeric_sequences / self.valid_passwords) * 100
        print(f"Passwords containing numeric sequences: {self.numeric_sequences} ({num_seq_percentage:.2f}%)")
        
        print(f"\n{Colors.BOLD}Leetspeak Usage:{Colors.RESET}")
        leetspeak_percentage = (self.leetspeak_count / self.valid_passwords) * 100
        print(f"Passwords using leetspeak: {self.leetspeak_count} ({leetspeak_percentage:.2f}%)")
        
        if self.capitalization_patterns:
            print(f"\n{Colors.BOLD}Capitalization Patterns:{Colors.RESET}")
            cap_table = PrettyTable()
            cap_table.field_names = ["Pattern", "Count", "Percentage"]
            
            cap_passwords = sum(self.capitalization_patterns.values())
            for pattern, count in self.capitalization_patterns.most_common():
                percentage = (count / cap_passwords) * 100
                cap_table.add_row([pattern, count, f"{percentage:.2f}%"])
            
            print(cap_table)
        
        if self.number_suffix_patterns:
            print(f"\n{Colors.BOLD}Number Suffix Patterns:{Colors.RESET}")
            suffix_table = PrettyTable()
            suffix_table.field_names = ["Suffix", "Count", "Percentage"]
            
            for suffix, count in self.number_suffix_patterns.most_common(10):
                percentage = (count / self.valid_passwords) * 100
                suffix_table.add_row([suffix, count, f"{percentage:.2f}%"])
            
            print(suffix_table)
        
        if self.special_char_positions:
            print(f"\n{Colors.BOLD}Special Character Positions:{Colors.RESET}")
            special_pos_table = PrettyTable()
            special_pos_table.field_names = ["Position", "Count", "Percentage"]
            
            total_special = sum(self.special_char_positions.values())
            if total_special > 0:
                for position, count in sorted(self.special_char_positions.items()):
                    percentage = (count / total_special) * 100
                    special_pos_table.add_row([position + 1, count, f"{percentage:.2f}%"])
                
                print(special_pos_table)
        
        if self.dictionary_words and self.common_words:
            print(f"\n{Colors.BOLD}Common Dictionary Words in Passwords:{Colors.RESET}")
            print(f"Passwords containing English dictionary words: {self.english_words_detected} ({(self.english_words_detected/self.valid_passwords)*100:.2f}%)")
            
            word_table = PrettyTable()
            word_table.field_names = ["Word", "Count", "Percentage"]
            
            for word, count in self.common_words.most_common(15):
                percentage = (count / self.valid_passwords) * 100
                word_table.add_row([word, count, f"{percentage:.2f}%"])
            
            print(word_table)
            
            if self.word_boundaries:
                print(f"\n{Colors.BOLD}Word Boundaries Analysis:{Colors.RESET}")
                print("Characters commonly found before or after dictionary words:")
                
                boundary_table = PrettyTable()
                boundary_table.field_names = ["Position", "Character", "Count"]
                
                for boundary, count in self.word_boundaries.most_common(10):
                    pos, char = boundary.split('_')
                    boundary_table.add_row([pos, char, count])
                
                print(boundary_table)
    
    def print_classic_analysis(self):
        print(f"\n{Colors.BOLD}{Colors.UNDERLINE}CLASSIC TYPE ANALYSIS{Colors.RESET}")
        positionCounters, charAnalysisResult = analyzePasswordsFromFile(self.file_path, self.max_length)
        printAnalysisResults(positionCounters, charAnalysisResult, self.max_length)
    
    def export_results(self):
        if not self.output_dir:
            return
        
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            with open(os.path.join(self.output_dir, f'password_summary_{timestamp}.txt'), 'w') as f:
                f.write(f"Password Analysis Summary\n")
                f.write(f"File: {self.file_path}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total passwords: {self.total_passwords}\n")
                f.write(f"Valid passwords: {self.valid_passwords}\n")
                f.write(f"Filtered passwords: {self.filtered_passwords}\n\n")
                
                f.write("Length Distribution:\n")
                for length, count in sorted(self.length_distribution.items()):
                    percentage = (count / self.valid_passwords) * 100
                    f.write(f"Length {length}: {count} ({percentage:.2f}%)\n")
            
            with open(os.path.join(self.output_dir, f'character_frequency_{timestamp}.csv'), 'w') as f:
                f.write("Character,Count,Percentage\n")
                if self.total_chars > 0:
                    for char, count in self.character_overall_counter.most_common():
                        percentage = (count / self.total_chars) * 100
                        char_escaped = f'"{char}"' if ',' in char or '"' in char else char
                        f.write(f"{char_escaped},{count},{percentage:.4f}\n")
            
            with open(os.path.join(self.output_dir, f'position_analysis_{timestamp}.csv'), 'w') as f:
                f.write("Position,Character,Count,Percentage\n")
                for position in sorted(self.position_character_counters.keys()):
                    total = sum(self.position_character_counters[position].values())
                    if total > 0:
                        for char, count in self.position_character_counters[position].most_common():
                            percentage = (count / total) * 100
                            char_escaped = f'"{char}"' if ',' in char or '"' in char else char
                            f.write(f"{position+1},{char_escaped},{count},{percentage:.4f}\n")
            
            with open(os.path.join(self.output_dir, f'patterns_{timestamp}.csv'), 'w') as f:
                f.write("Pattern,Count,Percentage\n")
                for pattern, count in self.patterns.most_common():
                    percentage = (count / self.valid_passwords) * 100
                    f.write(f"{pattern},{count},{percentage:.4f}\n")
            
            if self.enhanced:
                enhanced_data = {
                    "repetitive_sequences": dict(self.repetitive_sequences.most_common(20)),
                    "keyboard_sequences": dict(self.keyboard_sequences.most_common(20)),
                    "date_patterns_count": len(self.date_patterns),
                    "numeric_sequences_count": self.numeric_sequences,
                    "leetspeak_count": self.leetspeak_count,
                    "capitalization_patterns": dict(self.capitalization_patterns),
                    "number_suffix_patterns": dict(self.number_suffix_patterns.most_common(20)),
                    "special_char_positions": {str(k+1): v for k, v in self.special_char_positions.items()},
                    "common_words": dict(self.common_words.most_common(50)),
                    "trigram_frequency": dict(self.trigram_frequency.most_common(50))
                }
                
                with open(os.path.join(self.output_dir, f'enhanced_analysis_{timestamp}.json'), 'w') as f:
                    json.dump(enhanced_data, f, indent=2)
            
            print(f"{Colors.GREEN}Results exported to directory: {self.output_dir}{Colors.RESET}")
        
        except Exception as e:
            print(f"{Colors.RED}Error exporting results: {e}{Colors.RESET}")

def analyzePasswordsDetailed(file_path):
    position_character_counters = defaultdict(lambda: defaultdict(int))
    total_passwords = 0
    
    max_password_length = 32
    
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
        table = PrettyTable()
        table.field_names = ["Character", "Occurrences", "Percentage"]
        
        sorted_characters = sorted(character_counter.items(), key=lambda item: (item[1] / total_passwords), reverse=True)
        
        for char, count in sorted_characters:
            percentage = (count / total_passwords) * 100
            table.add_row([char, count, f"{percentage:.2f}%"])
        
        print(f"\nPosition {position + 1} (sorted by highest occurrence):")
        print(table)

def analyzePasswords(file_path):
    position_counters = defaultdict(Counter)
    total_passwords = 0
    max_password_length = 32
    
    with open(file_path, 'r', errors='ignore') as file:
        for line in file:
            password = line.strip().lower()
            if len(password) <= max_password_length:
                total_passwords += 1
                for position, char in enumerate(password):
                    position_counters[position][char] += 1
    
    for position, counter in sorted(position_counters.items()):
        if position > max_password_length:
            break
        most_common_char, count = counter.most_common(1)[0]
        print(f"Position {position + 1}: Most common character is '{most_common_char}' with {count} appearances ({(count / total_passwords) * 100:.2f}% of passwords).")

def analyzeCharacterFrequency(file_path):
    character_counter = Counter()
    total_characters = 0
    with open(file_path, 'r', errors='ignore') as file:
        for line in file:
            password = line.strip()
            character_counter.update(password)
            total_characters += len(password)
    
    character_percentages = {char: (count / total_characters) * 100 for char, count in character_counter.items()}
    sorted_characters = sorted(character_percentages.items(), key=lambda item: item[1], reverse=True)
    return sorted_characters

def printCharacterFrequencies(sorted_characters, columns=4):
    print("Characters sorted by how common they occurred (highest to lowest percentage):")
    rows = len(sorted_characters) // columns + (1 if len(sorted_characters) % columns else 0)
    for row in range(rows):
        output = ""
        for col in range(columns):
            index = row + col * rows
            if index < len(sorted_characters):
                char, percentage = sorted_characters[index]
                output += f"{char}: {percentage:.2f}%".ljust(15)
        print(output)

def isAsciiPrintable(s):
    return all(32 <= ord(c) <= 126 for c in s)

def analyzePasswordsNext(file_path):
    followers = defaultdict(Counter)
    charOccurrences = defaultdict(int)
    totalPasswords, filteredPasswords = 0, 0
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            totalPasswords += 1
            password = line.strip()
            if not isAsciiPrintable(password):
                filteredPasswords += 1
                continue
            for i in range(len(password) - 1):
                currentChar = password[i]
                nextChar = password[i + 1]
                followers[currentChar].update([nextChar])
                charOccurrences[currentChar] += 1
    
    print(f"Total passwords processed: {totalPasswords}")
    print(f"Passwords filtered out (non-ASCII printable): {filteredPasswords}")
    for char, counter in followers.items():
        if counter:
            mostCommonFollower, occurrences = counter.most_common(1)[0]
            percentage = (occurrences / charOccurrences[char]) * 100
            print(f"Character '{char}' most often followed by: '{mostCommonFollower}' (Occurrences: {occurrences}, {percentage:.2f}%)")
        else:
            print(f"Character '{char}' is not followed by any character.")

def analyzePasswordsNextEach(filePath, maxLength=16):
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

def main():
    parser = argparse.ArgumentParser(description="Unified Password Analyzer - Comprehensive password analysis tool")
    
    parser.add_argument("file", help="Password file to analyze")
    parser.add_argument("-o", "--output", help="Directory to save analysis results", default=None)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    parser.add_argument("--min-length", type=int, default=1, help="Minimum password length to include")
    parser.add_argument("--max-length", type=int, default=32, help="Maximum password length to include")
    parser.add_argument("--ascii-only", action="store_true", help="Exclude non-ASCII printable passwords")
    parser.add_argument("--pattern", help="Filter by pattern (l=lowercase, L=uppercase, d=digit, s=special)")
    
    parser.add_argument("--summary", action="store_true", help="Show overall summary only")
    parser.add_argument("--position", action="store_true", help="Show position-specific analysis")
    parser.add_argument("--followers", action="store_true", help="Show character follower analysis")
    parser.add_argument("--enhanced", action="store_true", help="Enable enhanced pattern detection")
    parser.add_argument("--classic", action="store_true", help="Show classic analysis from original scripts")
    parser.add_argument("--dictionary", help="Path to dictionary file for word detection")
    parser.add_argument("--all", action="store_true", help="Show all analysis types")
    
    args = parser.parse_args()
    
    analyzer = PasswordAnalyzer(
        file_path=args.file,
        max_length=args.max_length,
        min_length=args.min_length,
        output_dir=args.output,
        exclude_non_ascii=args.ascii_only,
        pattern=args.pattern,
        verbose=args.verbose,
        dictionary=args.dictionary,
        enhanced=args.enhanced or args.all
    )
    
    analyzer.analyze()
    
    show_all = args.all or not any([args.summary, args.position, args.followers, args.enhanced, args.classic])
    
    if show_all or args.summary:
        analyzer.print_summary()
        analyzer.print_character_analysis()
    
    if show_all or args.position:
        analyzer.print_position_analysis()
    
    if show_all or args.followers:
        analyzer.print_follower_analysis()
    
    if (show_all and args.enhanced) or (args.enhanced and not args.all):
        analyzer.print_enhanced_analysis()
    
    if show_all or args.classic:
        analyzer.print_classic_analysis()
    
    if args.output:
        analyzer.export_results()

if __name__ == "__main__":
    main()
