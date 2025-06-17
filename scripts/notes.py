import os
import glob
import json


def update_json_with_md_content(json_file_path, md_folder_path, output_file_path=None):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    md_files = glob.glob(os.path.join(md_folder_path, '*.md'))

    md_mapping = {
        os.path.splitext(os.path.basename(md_file))[0]: md_file
        for md_file in md_files
    }

    for key in list(data.keys()):
        if key in md_mapping:
            try:
                with open(md_mapping[key], 'r', encoding='utf-8') as md_file:
                    data[key]['content'] = md_file.read()
            except Exception as e:
                print(f"Error reading {md_mapping[key]}: {e}")
                continue

    if output_file_path is None:
        output_file_path = json_file_path

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully updated JSON file at {output_file_path}")


if __name__ == "__main__":
    json_file_path = '../static/notes/notes.json'
    md_folder_path = '../static/notes'

    update_json_with_md_content(json_file_path, md_folder_path)
