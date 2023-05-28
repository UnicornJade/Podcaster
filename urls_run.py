import os

with open('urls.txt', 'r') as file:  
    for line in file:
        os.system(f"python -U {line.strip()}" --headless --moimg)