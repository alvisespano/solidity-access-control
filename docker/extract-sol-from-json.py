import json
import os
import sys

def extract_solidity_sources(json_file):

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
        print(f"[SKIP] Cannot read JSON '{json_file}': {e}")
        return 0

    language = data.get("language", "")
    if not isinstance(language, str) or language.lower() != "solidity":
        print(f"[SKIP] '{json_file}': language is not Solidity (found '{language}')")
        return 0

    sources = data.get("sources")
    if not sources or not isinstance(sources, dict):
        print(f"[SKIP] '{json_file}': no valid 'sources' found")
        return 0

    # Output directory in the same folder as the JSON
    json_dir = os.path.dirname(os.path.abspath(json_file))
    output_dir = os.path.join(json_dir, "extracted_contracts")
    os.makedirs(output_dir, exist_ok=True)

    extracted_count = 0
    for path, info in sources.items():
        if not isinstance(info, dict) or "content" not in info:
            print(f"[SKIP] {path}: missing 'content'")
            continue

        path = path.replace("\n", "")

        content = info["content"]
        if not isinstance(content, str) or not content.strip():
            print(f"[SKIP] {path}: empty content")
            continue

        output_path = os.path.join(output_dir, path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            with open(output_path, "w", encoding="utf-8") as sol_file:
                sol_file.write(content)
            extracted_count += 1
        except (UnicodeEncodeError, IOError) as e:
            print(f"[SKIP] Failed to write {path}: {e}")

    return extracted_count


def main(txt_file):
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            json_files = [line.strip() for line in f if line.strip()]
    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"[ERROR] Cannot read list file '{txt_file}': {e}")
        return

    total_files = len(json_files)
    total_extracted = 0

    for idx, json_file in enumerate(json_files, start=1):
        print(f"\n[{idx}/{total_files}] Processing: {json_file}")
        count = extract_solidity_sources(json_file)
        total_extracted += count
        print(f"[{idx}/{total_files}] Done. Extracted {count} Solidity file(s).")

    print(f"\n=== Finished ===")
    print(f"Total Solidity files extracted: {total_extracted}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python batch_extract_solidity.py json_file_list.txt")
        sys.exit(1)

    main(sys.argv[1])
