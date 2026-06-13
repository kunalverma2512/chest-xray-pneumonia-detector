import os
import re
from pathlib import Path

BACKEND_APP = Path(__file__).resolve().parent.parent / "app" / "ml"

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content
    lines = content.split('\n')
    new_lines = []
    
    # Simple logic to drop specific lines
    for line in lines:
        if 'unchanged' in line.lower() or 'original author' in line.lower() or 'generated' in line.lower() or 'refactored' in line.lower():
            # If it's a docstring or comment line, we can just skip it if it mostly contains these words
            if '#' in line or '"""' in line:
                # If the line is just a comment, skip it
                if line.strip().startswith('#') or line.strip().startswith('"""') or line.strip().endswith('"""'):
                    # To be safe, if it's a single line docstring, we just strip the bad words
                    if '"""' in line:
                        line = re.sub(r'\(?unchanged from original\)?', '', line, flags=re.IGNORECASE)
                        line = re.sub(r'unchanged', '', line, flags=re.IGNORECASE)
                        line = re.sub(r'original author', '', line, flags=re.IGNORECASE)
                        line = line.replace(' ()', '').replace('  ', ' ')
                    else:
                        continue
        new_lines.append(line)
        
    content = '\n'.join(new_lines)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath.name}")

def main():
    for root, _, files in os.walk(BACKEND_APP):
        for file in files:
            if file.endswith('.py'):
                process_file(Path(root) / file)

if __name__ == "__main__":
    main()
