import sys
import re
from tkinter import Tk, filedialog
from pathlib import Path
from generator_help_functions import *
sys.stdout.reconfigure(encoding='utf-8')

p_number = 0
i_number = 0

def choose_folder():
    """
    Get the folder path to translate.

    :return: the path of the folder.
    """

    try:
        folder = filedialog.askdirectory(
            title="Please choose the blog file path",
            initialdir="./blogs"
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


def write_html_head(folder_path: Path):
    """
    Write both head of the html file

    :param folder_path: the folder path
    :return: None
    """
    path_list = get_html_file_path(folder_path)
    try:
        with open(path_list[0], "w", encoding="utf-8") as file:
            file.write(blog_part_return(0))

        with open(path_list[1], "w", encoding="utf-8") as file:
            file.write(blog_part_return(1))
    except Exception as e:
        print(f"Error writing head for {folder_path.name}: {e}")
        restore_temp_file(path_list)
        print("Restored the backup file.")
        sys.exit(1)


def txt_to_body_translate(folder_path: Path, file_path: Path):
    """
    Translate the choose file to html body

    :param folder_path: the folder path
    :param file_path: the txt file path
    :return: html body
    """

    global p_number, i_number

    p_regex = r"^/p\{(?P<p_position>[^}]+)\}\s*(?P<content>.*)$"  
    #match /p{p_position} content

    p_re = re.compile(p_regex)

    i_regex = (r"^/i\{(?P<image_name>[^,}]+)\s*,"
               r"\s*(?P<image_size>[^,}]+)\s*\}"
               r"\s*(?P<description>.*)$")  
    # match /i{image_name, image_size} description

    i_re = re.compile(i_regex)

    try:
        file = file_path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"Error reading file {file_path.name}: {e}")
        raise e
    
    body = ""

    for i, line in enumerate(file):
        if i == 0:
            continue

        line = line.strip()
        if not line:
            continue

        i_match = i_re.match(line)

        p_match = p_re.match(line)

        if i_match:
            image_name = i_match.group("image_name").strip()
            image_size = i_match.group("image_size").strip()
            description = i_match.group("description").strip()

            i_number += 1

            if i == 1:
                body += f"""\
                <div class="image-container">
                    <img src="/blogs/{folder_path.name}/{image_name}" alt="{description}" class="showimg img-topless">
                </div>\n\n"""

            if i != 1:

                if "70" in image_size:
                    image_class = "blogimgsize70"
                elif "50" in image_size:
                    image_class = "blogimgsize50"
                else:
                    image_class = ""
            
                body += f"""\
                <div class="blogparagraphimg">
                    <img src="/blogs/{folder_path.name}/{image_name}" alt="{description}" class="blogshowimg {image_class}">
                    <figcaption>{description}</figcaption>
                </div>\n\n"""

        elif p_match:
            p_position = p_match.group("p_position")
            content = p_match.group("content")

            p_number += 1

            if "end" in p_position:
                if "start" in p_position:
                    position = "blogparagraphstart blogparagraphend"
                else:
                    position = "blogparagraphend"
            else:
                if "start" in p_position:
                    position = "blogparagraphstart"
                else:
                    position = ""

            body +=f"""\
                <div class="blogpageparagraph {position}">
                    <p>
                        {content}
                    </p>
                </div>\n\n"""

    return body


def write_html_body(folder_path: Path):
    """
    Write html body

    :param folder_path: the folder path
    :return: None
    """

    global p_number, i_number

    file_path = get_txt_file_path(folder_path)

    body = txt_to_body_translate(folder_path, file_path[0])
    print(f"Number of paragraphs: {p_number}  " +
          f"Number of images: {i_number}  in {file_path[0].name}")

    p_number = 0
    i_number = 0
    body_zh = txt_to_body_translate(folder_path, file_path[1])
    print(f"Number of paragraphs: {p_number}  " +
          f"Number of images: {i_number}  in {file_path[1].name}")

    path_list = get_html_file_path(folder_path)

    try:
        with open(path_list[0], "a", encoding="utf-8") as file:
            file.write(body)

        with open(path_list[1], "a", encoding="utf-8") as file:
            file.write(body_zh)
    except Exception as e:
        print(f"Error writing body for {folder_path.name}: {e}")
        restore_temp_file(path_list)
        print("Restored the backup file.")
        sys.exit(1)


def write_html_tail(folder_path: Path):
    """
    Write html tail

    :param folder_path: the folder path
    :return: None
    """

    path_list = get_html_file_path(folder_path)

    try:
        with open(path_list[0], "a", encoding="utf-8") as file:
            file.write(blog_part_return(2))

        with open(path_list[1], "a", encoding="utf-8") as file:
            file.write(blog_part_return(2))
    except Exception as e:
        print(f"Error writing tail for {folder_path.name}: {e}")
        restore_temp_file(path_list)
        print("Restored the backup file.")
        sys.exit(1)


def blog_part_return(part_number: int):
    """
    Return head or tail of the blog html

    :param part_number: 0 for head, 1 for head-zh, 2 for tail
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
            <div class="blogpagemain">\n"""

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
            <div class="blogpagemain">\n"""

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


def translate_blog():
    """
    Translate the choose folder to html blog

    :return: None
    """
    
    folder_path = choose_folder()
    save_temp_file(get_html_file_path(folder_path))
    
    try:
        write_html_head(folder_path)
        write_html_body(folder_path)
        write_html_tail(folder_path)
        delete_temp_file(get_html_file_path(folder_path))
        print("Translation completed successfully.\n")

        from generate_blog_list import generate_blog_list
        generate_blog_list() 

    except Exception as e:
        print(f"Error translating blog in {folder_path.name}: {e}")
        restore_temp_file(get_html_file_path(folder_path))
        print("Restored the backup file.")
        sys.exit(1)


if __name__ == "__main__":
    Tk().withdraw()
    translate_blog()
