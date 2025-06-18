import re
import textwrap
from tkinter import Tk, filedialog
from pathlib import Path


def choose_folder():
    """
    Get the folder path to translate.

    :return: the path of the folder.
    """
    folder = filedialog.askdirectory(
        title="Please choose the blog file path",
        initialdir="./blogs"
    )

    if not folder:
        raise FileNotFoundError("Please choose a folder")

    folder = Path(folder)
    return folder


def get_html_file_path(folder_path: Path):
    """
    Use folder path to get file path

    :param folder_path: the folder path
    :return: a list of both en and zh file path
    """

    folder_name = folder_path.name
    file_name = folder_name + ".html"
    file_name_zh = folder_name + "-zh.html"

    file_path = folder_path / file_name
    file_path_zh = folder_path / file_name_zh

    return [file_path, file_path_zh]


def write_html_head(folder_path: Path):
    """
    Write both head of the html file

    :param folder_path: the folder path
    :return: None
    """
    path_list = get_html_file_path(folder_path)

    with open(path_list[0], "w", encoding="utf-8") as file:
        file.write(blog_part_return(0))

    with open(path_list[1], "w", encoding="utf-8") as file:
        file.write(blog_part_return(1))

    print("Successfully wrote the header\n")


def get_txt_file_path(folder_path: Path):
    """
    Get the txt file path

    :param folder_path: the folder path
    :return: a list of en and zh file path
    """

    folder_name = folder_path.name
    file_name = folder_name + ".txt"
    file_name_zh = folder_name + "-zh.txt"

    file_path = folder_path / file_name
    file_path_zh = folder_path / file_name_zh

    return [file_path, file_path_zh]


def txt_to_body_translate(folder_path: Path, file_path: Path):
    """
    Translate the choose file to html body

    :param folder_path: the folder path
    :param file_path: the txt file path
    :return: html body
    """

    p_regex = r"^/p\{(?P<p_position>[^}]+)\}\s*(?P<content>.*)$"  
    #match /p{p_position} content

    p_re = re.compile(p_regex)

    i_regex = (r"^/i\{(?P<image_name>[^,}]+)\s*,"
               r"\s*(?P<image_size>[^,}]+)\s*\}"
               r"\s*(?P<description>.*)$")  
    # match /i{image_name, image_size} description

    i_re = re.compile(i_regex)

    file = file_path.read_text(encoding="utf-8").splitlines()
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

            print("Image added")

        elif p_match:
            p_position = p_match.group("p_position")
            content = p_match.group("content")

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

            print("Paragraph added")

    return body


def write_html_body(folder_path: Path):
    """
    Write html body

    :param folder_path: the folder path
    :return: None
    """
    file_path = get_txt_file_path(folder_path)

    body = txt_to_body_translate(folder_path, file_path[0])

    print("Successfully translated the body-en\n")

    body_zh = txt_to_body_translate(folder_path, file_path[1])

    print("Successfully translated the body-zh\n")

    path_list = get_html_file_path(folder_path)

    with open(path_list[0], "a", encoding="utf-8") as file:
        file.write(body)

    with open(path_list[1], "a", encoding="utf-8") as file:
        file.write(body_zh)

    print("Successfully wrote the body")


def write_html_tail(folder_path: Path):
    """
    Write html tail

    :param folder_path: the folder path
    :return: None
    """

    path_list = get_html_file_path(folder_path)

    with open(path_list[0], "a", encoding="utf-8") as file:
        file.write(blog_part_return(2))

    with open(path_list[1], "a", encoding="utf-8") as file:
        file.write(blog_part_return(2))

    print("Successfully wrote the tail")


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
    write_html_head(folder_path)
    write_html_body(folder_path)
    write_html_tail(folder_path)


if __name__ == "__main__":
    Tk().withdraw()
    translate_blog()
