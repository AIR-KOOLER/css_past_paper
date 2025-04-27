import os
import re

# CONFIGURE
GITHUB_USER = "AIR-KOOLER"
REPO_NAME = "css_past_paper"
BRANCH = "main"
START_YEAR = 2000
END_YEAR = 2024
OUTPUT_FILE = "output.txt"
TARGET_FOLDER = "."  # "." means root folder

# Function to safely encode spaces
def url_encode_path(path):
    return path.replace(" ", "%20")

# Start scanning folders from the target folder
base_path = os.path.join(".", TARGET_FOLDER)
folders = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

lines = []

lines.append("{")  # Open the JS object

for idx, folder in enumerate(folders):
    folder_path = os.path.join(base_path, folder)
    folder_url = url_encode_path(folder)

    # Auto-detect if filenames use " - " or " " between subject and year
    files = os.listdir(folder_path)
    uses_dash = False
    for file in files:
        # Check if there's a file matching "Subject - 2024.html"
        pattern = re.escape(folder) + r" - \d{4}\.html"
        if re.match(pattern, file):
            uses_dash = True
            break

    # Debug print (you can remove later)
    print(f"📂 {folder} uses {'DASH' if uses_dash else 'SPACE'} between name and year.")

    lines.append(f"  '{folder}': Object.fromEntries(")
    lines.append(f"    Array.from({{ length: {END_YEAR} - {START_YEAR} + 1 }}, (_, i) => {{")
    lines.append(f"      const year = {START_YEAR} + i;")

    if uses_dash:
        filename = f"{folder} - ${{year}}.html"
    else:
        filename = f"{folder} ${{year}}.html"

    filename_url = url_encode_path(filename)

    lines.append(f"      return [")
    lines.append(f"        year,")
    lines.append(f"        {{")
    lines.append(f"          url: `https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{folder_url}/{filename_url}`")
    lines.append(f"        }}")
    lines.append(f"      ];")
    lines.append(f"    }})")

    if idx == len(folders) - 1:
        lines.append(f"  )")  # last item, no comma
    else:
        lines.append(f"  ),")  # comma between objects

lines.append("}")  # Close the JS object

# Write everything to output.txt
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n✅ JavaScript code has been saved to {OUTPUT_FILE}!")
