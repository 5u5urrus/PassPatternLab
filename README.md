**The Character Frequency Analysis Tool**

**analyze_general.py**: The Character Frequency Analysis Tool examines password datasets to identify and rank the frequency of character occurrences. By analyzing the distribution of characters within passwords, it provides insights into common patterns, highlighting potential security implications. This tool outputs characters sorted by their prevalence, offering a statistical foundation to assess password strength and complexity.

Example: python3 analyze_general.py /usr/share/seclists/Passwords/Leaked-Databases/Ashley-Madison.txt

<img width="550" alt="analyze_general" src="https://github.com/5u5urrus/PassPatternLab/assets/165041037/4abb1dd1-5660-4f9a-9253-886433333614">
<br><br>

**The Positional Character Analysis Tool**

**analyze_1.py**: The Positional Character Analysis Tool delves into password datasets to identify the most common character at each position, offering insights into prevalent patterns at various password positions. By analyzing character frequency and distribution at each position, this script highlights tendencies in password composition in a more detailed way, uncovering hidden patterns, revealing potential weaknesses and areas for strengthening password policies. 

Example: python3 analyze_1.py /usr/share/seclists/Passwords/Leaked-Databases/rockyou-75.txt

<img width="550" alt="analyze_1" src="https://github.com/5u5urrus/PassPatternLab/assets/165041037/e78c99ed-8541-42c4-a8df-c2c762cda132">


