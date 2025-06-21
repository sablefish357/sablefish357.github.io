from pathlib import Path


def save_temp_file(file_path: list[Path]):
    """
    Save old file if exists as .bak file
    
    :param file_path: a list of file path
    :return: None
    """

    for file_path in file_path:
        if file_path.exists():
            try:
                backup_path = file_path.with_suffix('.bak')
                file_path.rename(backup_path)
            except Exception as e:
                print(f"Error creating backup for {file_path.name}: {e}")
                raise e
            

def restore_temp_file(file_path: list[Path]):
    """
    Delete created html file if exists and restore the backup file from .bak 
    file

    :param folder_path: the folder path
    :return: None
    """

    for file_path in file_path:
        backup_path = file_path.with_suffix('.bak')
        if backup_path.exists():
            try:
                file_path.unlink(missing_ok=True)
                backup_path.rename(file_path)
            except Exception as e:
                print(f"Error restoring {file_path.name} from backup: {e}")
                raise e
            
            
def delete_temp_file(file_path: list[Path]):
    """
    Delete temporary .bak file

    :param file_path: a list of file path
    :return: None
    """

    for file_path in file_path:
        backup_path = file_path.with_suffix('.bak')
        if backup_path.exists():
            try:
                backup_path.unlink(missing_ok=True)
            except Exception as e:
                print(f"Error deleting backup {backup_path.name}: {e}")
                raise e


def get_html_file_path(folder_path: Path):
    """
    Use folder path to get html file path with same name as the folder.

    :param folder_path: the folder path
    :return: a list of both en and zh file path
    """

    folder_name = folder_path.name
    file_name = folder_name + ".html"
    file_name_zh = folder_name + "-zh.html"

    file_path = folder_path / file_name
    file_path_zh = folder_path / file_name_zh

    return [file_path, file_path_zh]


def get_txt_file_path(folder_path: Path):
    """
    Use folder path to get txt file path with same name as the folder.

    :param folder_path: the folder path
    :return: a list of en and zh file path
    """

    folder_name = folder_path.name
    file_name = folder_name + ".txt"
    file_name_zh = folder_name + "-zh.txt"

    file_path = folder_path / file_name
    file_path_zh = folder_path / file_name_zh

    return [file_path, file_path_zh]


if __name__ == "__main__":
    print("This module is not meant to be run directly. It contains helper" +  "functions for generating music and blog pages and lists.")