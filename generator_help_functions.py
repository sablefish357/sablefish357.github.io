from pathlib import Path


def save_temp_file(file_path: list[Path]):
    """
    Save old file if exists as .bak file
    
    :param file_path: a list of file path
    :return: None
    """

    for file in file_path:
        if file.exists():
            try:
                backup_path = file.with_suffix('.bak')
                file.rename(backup_path)
            except Exception as e:
                print(f"Error: When creating backup for {file.name}: {e}")
                raise e
            

def restore_temp_file(file_path: list[Path]):
    """
    Delete created html file if exists and restore the backup file from .bak 
    file

    :param file_path: a list of file path
    :return: None
    """

    for file in file_path:
        backup_path = file.with_suffix('.bak')
        if backup_path.exists():
            try:
                file.unlink(missing_ok=True)
                backup_path.rename(file)
            except Exception as e:
                print(f"Error: When restoring {file.name} from backup: {e}")
                raise e
            
            
def delete_temp_file(file_path: list[Path]):
    """
    Delete temporary .bak file

    :param file_path: a list of file path
    :return: None
    """

    for file in file_path:
        backup_path = file.with_suffix('.bak')
        if backup_path.exists():
            try:
                backup_path.unlink(missing_ok=True)
            except Exception as e:
                print(f"Error: When deleting backup {backup_path.name}: {e}")
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

def general_part_return(part_number: int, folder_Path: Path, page_title: str, class_name: str):
    """
    Return head or tail of the general HTML.

    :param part_number: 0 for head, 1 for head-zh, 2 for tail, 3 for tail-zh
    :param folder_Path: the folder path
    :param page_title: the title of the page
    :param class_name: the class name for CSS
    :return: str of head or tail
    """

    is_en = part_number in [0, 2]

    context = {
        "lang" : "en" if is_en else "zh-CN"
    }

    head = f"""\
<!DOCTYPE html>
<html lang="{context['lang']}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="This is SableFiSh's personal page.">
        <meta name="keywords" content="Blender,SableFiSh,MMD,mikumikudance ">

        <title>
            {page_title}
        </title>

        <link rel="icon" type="image/jpg" href="/image/favicon.jpg">
        <link rel="stylesheet" href="/style.css">
    </head>
     
    <body>
        <main>
            <div class="{class_name}">\n\n"""
    
    tail = f"""\
            </div>
            
        </main>

        <script src="/script.js"></script>
        
    </body>
</html>"""
    
    match part_number:
        case 0 | 1:
            return head
        case 2 | 3:
            return tail
        case _:
            raise ValueError("Error: Wrong part number.")

if __name__ == "__main__":
    print("This module is not meant to be run directly. It contains helper " +  
          "functions for generating music and blog pages and lists.")