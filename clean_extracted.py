import os
import ast

out_dir = r"c:\Users\heath\oceanmovers"
for filename in ['downloader.py', 'fix_integrity.py']:
    filepath = os.path.join(out_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        print(f"{filename} start repr: {repr(content[:100])}")
        if content.startswith('"') or content.startswith("'"):
            try:
                code = ast.literal_eval(content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)
                print(f"Fixed {filename}")
            except Exception as e:
                print(f"Error parsing {filename}: {e}")
        else:
            print(f"{filename} does not start with quote.")

