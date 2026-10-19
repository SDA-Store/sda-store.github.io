import glob
import re
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATCHES_DIR = os.path.join(BASE_DIR, 'data', 'patches')

count = 0
for toml_path in glob.glob(os.path.join(PATCHES_DIR, '*.toml')):
    with open(toml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(r'brand\s*=\s*"[^"]+"', 'brand = "SDA Store"', content)
    new_content = re.sub(r'\[([a-zA-Z0-9_-]+)-Paresh\]', r'[\1-SDA]', new_content)

    if new_content != content:
        with open(toml_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Updated brand in: {os.path.basename(toml_path)}")

# Also duplicate paresh.toml to cricbuzz.toml for seamless build_app.sh lookup
paresh_file = os.path.join(PATCHES_DIR, 'paresh.toml')
cricbuzz_file = os.path.join(PATCHES_DIR, 'cricbuzz.toml')
if os.path.exists(paresh_file) and not os.path.exists(cricbuzz_file):
    shutil.copy2(paresh_file, cricbuzz_file)
    print("Created data/patches/cricbuzz.toml")

print(f"Sanitized {count} patch configuration files to 'SDA Store'.")
