import sys
import re
from pathlib import Path
from tkinter import Tk, filedialog
from generator_help_functions import *
sys.stdout.reconfigure(encoding='utf-8')

p_number = 0

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

    return [Path("./stages/README.txt"), Path("./stages/README-zh.txt")]


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

def readme_translate(readme_file: Path):
    """
    Translate the README file to HTML part.

    :param readme_file: the readme file path
    :return: the HTML part of the README file
    """

    p_regex = r"^/p\{(?P<default>[^}]*)\}\s*(?P<content>.*)$"  
    #match /p{default} content
    p_re = re.compile(p_regex)

    readme_part = ""

    try:
        file = readme_file.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"Error reading file {readme_file.name}")
        raise e

    for line in file:

        line = line.strip()

        if not line:
            continue

        p_match = p_re.match(line)

        if p_match:
            content = p_match.group("content").strip()

            readme_part += f"""\
                    <p>
                        {content}
                    </p>\n"""
        else:
            print(f"Undefined line found [{line}] in {readme_file.stem}")
            

    return readme_part



def txt_to_stage_body_translate(folder_path: Path, file_path: Path, 
                                zh: bool = False):
    """
    Translate the chosen file to HTML body.

    :param folder_path: the folder path
    :param file_path: the file path
    :return: None
    """

    global p_number

    p_regex = r"^/p\{(?P<default>[^}]*)\}\s*(?P<content>.*)$"  
    #match /p{default} content
    p_re = re.compile(p_regex)

    i_regex = (r"^/i\{(?P<image_name>[^,}]+)\s*,"
               r"\s*(?P<image_size>[^,}]+)\s*\}"
               r"\s*(?P<description>.*)$")  
    # match /i{image_name, image_size} description
    i_re = re.compile(i_regex)

    v_regex = r"^/v\{\}\s*(?P<version>.*)$"
    # match /t{} version
    v_re = re.compile(v_regex)

    d_regex = r"^/d\{(?P<link>[^}]+)\}\s*(?P<source>.*)$"
    # match /d{link} source
    d_re = re.compile(d_regex)

    try:
        file = file_path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"Error reading file {file_path.name}")
        raise e
    
    image_part = ""
    paragraph_part = ""
    download_part = ""
    paragraph_version = ""

    have_default = False

    for i, line in enumerate(file):
        if i == 0:
            continue

        line = line.strip()
        if not line:
            continue

        i_match = i_re.match(line)
        p_match = p_re.match(line)
        v_match = v_re.match(line)
        d_match = d_re.match(line)

        if i_match:
            if i == 1:
                image_name = i_match.group("image_name").strip()
                description = i_match.group("description").strip()

                image_part += f"""\
                <div class="image-container">
                    <img src="/stages/{folder_path.name}/{image_name}" alt="{description}" class="showimg img-topless">
                </div>\n\n"""

            else:
                continue
            
        elif p_match:
            default = p_match.group("default").strip()
            content = p_match.group("content").strip()

            if "default" in default:
                have_default = True

            paragraph_part += f"""\
                    <p>
                        {content}
                    </p>\n"""
            
            p_number += 1

        elif v_match:
            version = v_match.group("version").strip()

            paragraph_version = f"""\
                    <p>
                        {version}
                    </p>\n"""

        elif d_match:
            link = d_match.group("link").strip()
            source = d_match.group("source").strip()

            download_part += f"""\
                    <a href="{link}" target="_blank">
                        <p>
                            {source}
                        </p>
                    </a>\n"""
        else:
            print(f"Undefined line found [{line}] in {file_path.stem}")

    if not image_part:
        print(f"No cover image found in {file_path.stem}.")

    paragraph_start = """\
                <div class="stagepageparagraph">
                    <p id="readme">
                        ReadMe
                    </p>\n"""
    
    if have_default:
        if zh:
            paragraph_default = readme_translate(get_default_readme_path()[1])
        else:
            paragraph_default = readme_translate(get_default_readme_path()[0])
    else:
        paragraph_default = ""
    
    paragraph_end = """\
                </div>\n"""
    
    download_start = """\
                <div class="download">
                    <p>
                        下载链接:
                    </p>
                </div>
                <div class="downloadlink">\n\n"""
    
    download_end = """\
                </div>\n"""
    
    return (image_part + paragraph_start + paragraph_default + paragraph_part + 
            paragraph_version + paragraph_end + download_start + download_part + 
            download_end)
    

def write_stage_page_body(folder_path: Path):
    """
    Write the body of the stage page HTML file.

    :param folder_path: the folder path
    :return: None
    """

    global p_number

    file_path = get_txt_file_path(folder_path)

    body = txt_to_stage_body_translate(folder_path, file_path[0])
    print(f"Number of additional paragraphs: {p_number} in {file_path[0].name}")

    p_number = 0
    body_zh = txt_to_stage_body_translate(folder_path, file_path[1], True)
    print(f"Number of additional paragraphs: {p_number} in {file_path[1].name}")

    path_list = get_html_file_path(folder_path)
    
    try:
        with open(path_list[0], "a", encoding="utf-8") as file:
            file.write(body)

        with open(path_list[1], "a", encoding="utf-8") as file:
            file.write(body_zh)
    except Exception as e:
        print(f"Error writing body for stage {folder_path.name}: {e}")
        restore_temp_file(path_list)
        print("Restored the backup file.")
        sys.exit(1)


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