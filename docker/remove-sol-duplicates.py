import os
import hashlib

def hash_file(file_path):
    """Return SHA256 hash of the file contents."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
    except (OSError, UnicodeDecodeError) as e:
        print(f"[SKIP] Cannot read file '{file_path}': {e}")
        return None
    return sha256.hexdigest()


def remove_duplicate_solidity_files(folder):
    """Recursively remove duplicate .sol files in a folder."""
    hashes = {}
    removed_count = 0

    for root, _, files in os.walk(folder):
        for file in files:
            if not file.endswith(".sol"):
                continue

            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)
            if not file_hash:
                continue

            if file_hash in hashes:
                # Duplicate found: remove the file
                try:
                    os.remove(file_path)
                    print(f"[REMOVED] Duplicate: {file_path}")
                    removed_count += 1
                except OSError as e:
                    print(f"[ERROR] Cannot remove '{file_path}': {e}")
            else:
                hashes[file_hash] = file_path

    print(f"\n=== Finished ===")
    print(f"Total duplicates removed: {removed_count}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python remove_duplicate_solidity.py folder_path")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"[ERROR] '{folder_path}' is not a valid folder.")
        sys.exit(1)

    remove_duplicate_solidity_files(folder_path)
