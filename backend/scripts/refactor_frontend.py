import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_SRC = PROJECT_ROOT / "frontend" / "src"

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    # Strip all rounded classes: rounded, rounded-sm, rounded-md, rounded-lg, rounded-xl, rounded-2xl, rounded-3xl, rounded-full, rounded-t-xl, etc.
    content = re.sub(r'\brounded(?:-[a-z0-9]+)*\b', '', content)
    # Cleanup multiple spaces left by removal
    content = re.sub(r'  +', ' ', content)
    content = content.replace(' "', '"').replace('" ', '"')

    # Update hardcoded metrics
    content = content.replace('86.0%', '82.7%')
    content = content.replace('96.4%', '97.6%')
    content = content.replace('8.8%', '12.1%')
    content = content.replace('94.8%', '94.8%') # remains the same for internal
    
    # Strip comments
    # Remove standard single line comments that have words like unchanged, original, AI IDE
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if '//' in line:
            if any(keyword in line.lower() for keyword in ['unchanged', 'original author', 'ai ide', 'generated', 'from original']):
                # skip line or strip comment
                if line.strip().startswith('//'):
                    continue
                else:
                    line = line.split('//')[0].rstrip()
        new_lines.append(line)
        
    content = '\n'.join(new_lines)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath.name}")

def main():
    count = 0
    for root, _, files in os.walk(FRONTEND_SRC):
        for file in files:
            if file.endswith('.jsx') or file.endswith('.js'):
                process_file(Path(root) / file)
                count += 1
    print(f"Processed {count} frontend files.")

if __name__ == "__main__":
    main()
