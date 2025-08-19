def sort_files_by_date(file_list):
    from datetime import datetime
    import os

    def extract_date(file_name):
        # Assuming the date is in the format YYYYMMDD
        date_str = file_name.split('_')[-1][:8]
        return datetime.strptime(date_str, '%Y%m%d')

    sorted_files = sorted(file_list, key=extract_date)
    return sorted_files

def organize_files_in_directory(directory_path):
    files = os.listdir(directory_path)
    sorted_files = sort_files_by_date(files)

    for file_name in sorted_files:
        # Logic to move or organize files can be added here
        print(f"Organizing file: {file_name}")

# Example usage
if __name__ == "__main__":
    directory = "path_to_your_directory"
    organize_files_in_directory(directory)