**The Character Frequency Analysis Tool**

**analyze_general.py**: The Character Frequency Analysis Tool examines password datasets to identify and rank the frequency of character occurrences. By analyzing the distribution of characters within passwords, it provides insights into common patterns, highlighting potential security implications. This tool outputs characters sorted by their prevalence, offering a statistical foundation to assess password strength and complexity.

Example: python3 analyze_general.py /usr/share/seclists/Passwords/Leaked-Databases/Ashley-Madison.txt

<img width="550" alt="analyze_general" src="https://github.com/5u5urrus/PassPatternLab/assets/165041037/4abb1dd1-5660-4f9a-9253-886433333614">
<br><br>

**The Positional Character Analysis Tool**

**analyze_1.py**: The Positional Character Analysis Tool delves into password datasets to identify the most common character at each position, offering insights into prevalent patterns at various password positions. By analyzing character frequency and distribution at each position, this script highlights tendencies in password composition in a more detailed way, uncovering hidden patterns, revealing potential weaknesses and areas for strengthening password policies. 

Example: python3 analyze_1.py /usr/share/seclists/Passwords/Leaked-Databases/rockyou-75.txt

<img width="550" alt="analyze_1" src="https://github.com/5u5urrus/PassPatternLab/assets/165041037/e78c99ed-8541-42c4-a8df-c2c762cda132">
<br><br>

**The Detailed Positional Character Analysis Tool**

**analyze.py**: The Detailed Positional Character Analysis Tool offers an in-depth examination of password character composition by mapping the frequency and percentage of each character's occurrence for each specific position within a dataset. Utilizing the PrettyTable library for clear and organized output, this script not only identifies the most prevalent characters at each position but also presents a detailed statistical breakdown, enabling a granular understanding of password patterns and tendencies. This analysis aids in reinforcing password strength and policy development by uncovering potential vulnerabilities linked to common character use.

Example: python3 analyze.py /usr/share/seclists/Passwords/Leaked-Databases/rockyou-75.txt

  <img src="https://github.com/5u5urrus/PassPatternLab/assets/165041037/404a1373-b7bf-4395-9e39-34575f908341" width="442" alt="analyze">
  <img src="https://github.com/5u5urrus/PassPatternLab/assets/165041037/98f30cf0-0c2a-439b-929f-9ad06580d404" width="224" alt="analyze2">
<br><br>

**The Enhanced Password Composition Analysis Tool**

**analyze_type.py**: The Enhanced Password Composition Analysis Tool scrutinizes the intricacies of password structures, emphasizing the frequency and distribution of character types/categories at each position within passwords. It shows for each position what type of characters are most commonly use - lowercase letters, uppsercase, numbers, special symbols? What are the most common characters for each position? Least common? Least common for each category? All displayed in a compact concise way.

Example: python3 analyze_type.py /usr/share/seclists/Passwords/Leaked-Databases/rockyou-75.txt

<img width="750" alt="analyze_type" src="https://github.com/5u5urrus/PassPatternLab/assets/165041037/8244cdaf-a7f2-4720-946d-9d85eb2b4a82">

