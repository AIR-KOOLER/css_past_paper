import os
import re

# CONFIGURE
GITHUB_USER = "AIR-KOOLER"
REPO_NAME = "css_past_paper"
BRANCH = "main"
START_YEAR = 2000
END_YEAR = 2024
OUTPUT_FILE = "analysis_output.txt"
TARGET_FOLDER = "analysis"

# Function to safely encode spaces
def url_encode_path(path):
    return path.replace(" ", "%20")

# Start scanning files inside the target folder
base_path = os.path.join(".", TARGET_FOLDER)

# Get all .html files inside the folder
files = [f for f in os.listdir(base_path) if f.endswith(".html")]

lines = []
lines.append("{")  # Open the JS object

last_subject = None

for idx, file in enumerate(files):
    # Match files like "Subject - 2024.html" or "Subject 2024.html"
    match = re.match(r"(.+?)(?: -)? (\d{4})\.html", file)
    if not match:
        print(f"⚠️ Skipping unexpected file: {file}")
        continue

    subject = match.group(1).strip()
    year = match.group(2)

    # Encode folder/subject name for URL
    subject_url = url_encode_path(subject)
    file_url = url_encode_path(file)

    if idx > 0 and subject != last_subject:
        lines.append(f"  ),")  # close previous subject block

    if idx == 0 or subject != last_subject:
        lines.append(f"  '{subject}': Object.fromEntries(")
        lines.append(f"    Array.from({{ length: {END_YEAR} - {START_YEAR} + 1 }}, (_, i) => {{")
        lines.append(f"      const year = {START_YEAR} + i;")
        
        # Check if the filename has a dash or not
        if " - " in file:
            filename = f"{subject} - ${{year}}.html"
        else:
            filename = f"{subject} ${{year}}.html"
        filename_url = url_encode_path(filename)

        lines.append(f"      return [")
        lines.append(f"        year,")
        lines.append(f"        {{ url: `https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{TARGET_FOLDER}/{filename_url}` }}")
        lines.append(f"      ];")
        lines.append(f"    }})")

    last_subject = subject

lines.append("  )")
lines.append("}")  # Close the JS object

# Write to output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ JavaScript code has been saved to {OUTPUT_FILE}!")
