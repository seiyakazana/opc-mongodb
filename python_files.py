import os

def get_files_content(file_list, output_filename):
    """
    Reads a list of files and writes their content into a single text file.
    """
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for file_path in file_list:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    output_file.write(f'----- {file_path} -----\n')
                    output_file.write(content)
                    output_file.write('\n----- end -----\n\n')
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
            else:
                print(f"File not found: {file_path}")

if __name__ == '__main__':
    files_to_process = [
        "migration.py",
        "docker-compose.yml",
        "Dockerfile",
        "test_integrity.py",
        "integrity.py"
    ]
    
    output_file_name = 'codebase.txt'
    get_files_content(files_to_process, output_file_name)
    print(f"Output has been written to {output_file_name}")