import os
import re

# CONFIGURE
GITHUB_USER = "AIR-KOOLER"
REPO_NAME = "css_past_paper"
BRANCH = "main"
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
    full_path = os.path.join(base_path, file)

    # Match files like "Subject - Summary.html" or "Subject Summary.html"
    match = re.match(r"(.+?)(?: -)? (.+)\.html", file)
    if not match:
        print(f"⚠️ Skipping unexpected file: {file}")
        continue

    subject = match.group(1).strip()
    paper_summary = match.group(2).strip()

    # Encode folder/subject name for URL
    subject_url = url_encode_path(subject)
    paper_url = url_encode_path(file)

    # Add the new subject to the object if it's different from the previous subject
    if last_subject != subject:
        if last_subject is not None:
            lines.append("  ],")  # Close previous subject list
        lines.append(f"  '{subject}': [")  # Start a new subject list

    # Add the paper summary link for the current subject
    lines.append(f"    {{")
    lines.append(f"      title: '{paper_summary}',")
    lines.append(f"      url: `https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{TARGET_FOLDER}/{paper_url}`")
    lines.append(f"    }},")

    last_subject = subject

# Ensure the last subject list is properly closed
lines.append("  ]")
lines.append("}")  # Close the JS object

# Write to output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ JavaScript code has been saved to {OUTPUT_FILE}!")
