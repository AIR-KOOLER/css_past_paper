import os
import subprocess
import urllib.parse

def get_repo_url():
    return "https://raw.githubusercontent.com/AIR-KOOLER/css_past_paper"

def get_branch_name():
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def get_repo_root():
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def list_links():
    repo_url = get_repo_url()
    branch = get_branch_name()
    repo_root = get_repo_root()
    current_folder = os.path.dirname(os.path.abspath(__file__))

    lines = []
    for file in os.listdir(current_folder):
        full_path = os.path.join(current_folder, file)
        if os.path.isfile(full_path):
            rel_path = os.path.relpath(full_path, repo_root).replace(os.sep, "/")
            encoded_path = urllib.parse.quote(rel_path)
            raw_url = f"{repo_url}/{branch}/{encoded_path}"
            entry = f"'{file}': {{\n  url: '{raw_url}',\n}},"
            lines.append(entry)

    return lines

# --- Run and write output ---
if __name__ == "__main__":
    output_file = "links.js"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("{\n")
        for line in list_links():
            f.write("  " + line + "\n")
        f.write("}\n")

    print(f"Links written to: {output_file}")
