import sys
from tkinter import Tk, filedialog
from generator_help_functions import *
sys.stdout.reconfigure(encoding='utf-8')

def choose_folder():
    """
    Get the folder path to translate.
    
    :return: the path of the folder.
    """

    try:
        folder = filedialog.askdirectory(
            title="Please choose the stage file path",
            initialdir="./stages"
        )
    except Exception as e:
        print(f"Error selecting folder: {e}")
        raise e

    if not folder:
        raise FileNotFoundError("No folder selected.")

    try:
        folder = Path(folder).relative_to(Path().resolve())

    except Exception as e:
        print(f"Error: The selected folder is not within the project root: {e}")
        raise e
    
    return folder


def get_default_readme_path():
    """
    Get the default README file path.
    
    :return: the path of the default README file.
    """

    return Path("./stages/README.txt")


def write_stage_page_head(folder_path: Path):
    """
    Write both head of the stage page HTML file.

    :param folder_path: the folder path
    :return: None
    """

    path_list = get_html_file_path(folder_path)

    try:
        with open(path_list[0], "w", encoding="utf-8") as file:
            file.write(stage_part_return(0))

        with open(path_list[1], "w", encoding="utf-8") as file:
            file.write(stage_part_return(1))

    except Exception as e:
        print(f"Error writing head for {folder_path.name}: {e}")
        restore_temp_file(path_list)
        print("Restored the backup file.")
        sys.exit(1)


def txt_to_stage_body_translate(folder_path: Path, file_path: Path):
    """
    Translate the chosen file to HTML body.

    :param folder_path: the folder path
    :param file_path: the file path
    :return: None
    """


def write_stage_page_body(folder_path: Path):
    """
    Write the body of the stage page HTML file.

    :param folder_path: the folder path
    :return: None
    """


def write_stage_page_tail(folder_path: Path):
    """
    Write the tail of the stage page HTML file.

    :param folder_path: the folder path
    :return: None
    """

    path_list = get_html_file_path(folder_path)

    try:
        with open(path_list[0], "a", encoding="utf-8") as file:
            file.write(stage_part_return(2))

        with open(path_list[1], "a", encoding="utf-8") as file:
            file.write(stage_part_return(2))
    except Exception as e:
        print(f"Error writing tail for {folder_path.name}: {e}")
        restore_temp_file(path_list)
        print("Restored the backup file.")
        sys.exit(1)

    
def stage_part_return(part_number: int):
    """
    Return the head or tail of the stage page HTML.

    :param part: 0 for head, 1 for head-zh, 2 for tail
    :return: str of head or tail
    """

    head = """\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="This is SableFiSh's personal page.">
        <meta name="keywords" content="Blender,SableFiSh,MMD,mikumikudance ">

        <title>
            SableFiSh
        </title>

        <link rel="icon" type="image/jpg" href="/image/favicon.jpg">
        <link rel="stylesheet" href="/style.css">

        <script src="/addelements.js" defer></script>
    </head>
     
    <body>
        <main>
            <div class="stagepagemain">\n\n"""

    head_zh = """\
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="This is SableFiSh's personal page.">
        <meta name="keywords" content="Blender,SableFiSh,MMD,mikumikudance ">

        <title>
            SableFiSh
        </title>

        <link rel="icon" type="image/jpg" href="/image/favicon.jpg">
        <link rel="stylesheet" href="/style.css">

        <script src="/addelements_zh.js" defer></script>
    </head>
     
    <body>
        <main>
            <div class="stagepagemain">\n\n"""

    tail = """\
            </div>
            
        </main>

        <script src="script.js"></script>
        
    </body>
</html>"""

    match part_number:
        case 0:
            return head
        case 1:
            return head_zh
        case 2:
            return tail
        case _:
            raise ValueError("Wrong part number.")

def generate_stage_page():
    """
    Generate the stage page.
    
    :return: None
    """

    folder_path = choose_folder()
    save_temp_file(get_html_file_path(folder_path))
    
    try:
        write_stage_page_head(folder_path)
        write_stage_page_body(folder_path)
        write_stage_page_tail(folder_path)
        delete_temp_file(get_html_file_path(folder_path))
        print("Translation completed successfully.\n")

        from generate_stage_list import generate_stage_list
        generate_stage_list() 

    except Exception as e:
        print(f"Error translating stage page in {folder_path.name}: {e}")
        restore_temp_file(get_html_file_path(folder_path))
        print("Restored the backup file.")
        sys.exit(1)
    

if __name__ == "__main__":
    generate_stage_page()