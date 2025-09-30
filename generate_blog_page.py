import sys
import re
from pathlib import Path
from generator_help_functions import *
sys.stdout.reconfigure(encoding='utf-8') # type: ignore

def write_blog_page_head(folder_path: Path):
    """
    Write the head of the blog page.

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
        print(f"Error: When writing head for {folder_path.name}.")
        raise e


def txt_to_body_translate(folder_path: Path, file_path: Path):
    """
    Translate the chosen file to HTML body.

    :param folder_path: the folder path
    :param file_path: the txt file path
    :return: tuple (body, p_number, i_number)
        body: the HTML body as a string
        p_number: the number of paragraphs
        i_number: the number of images
    """

    i_number = 0
    p_number = 0

    p_regex = r"^/p\{(?P<p_position>[^}]+)\}\s*(?P<content>.*)$"  
    #match /p{p_position} content

    p_re = re.compile(p_regex)

    i_regex = (r"^/i\{(?P<image_name>[^,}]*)\s*,"
               r"\s*(?P<image_size>[^,}]*)\s*\}"
               r"\s*(?P<description>.*)$")  
    # match /i{image_name, image_size} description

    i_re = re.compile(i_regex)

    try:
        file = file_path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"Error: When reading file {file_path.name}.")
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

    return body, p_number, i_number


def write_blog_page_body(folder_path: Path):
    """
    Write the body of the blog page.

    :param folder_path: the folder path
    :return: tuple (p_number, i_number, p_number_zh, i_number_zh)
        p_number: the number of paragraphs in English version
        i_number: the number of images in English version
        p_number_zh: the number of paragraphs in Chinese version
        i_number_zh: the number of images in Chinese version
    """

    file_path = get_txt_file_path(folder_path)

    body, p_number, i_number = txt_to_body_translate(folder_path, 
                                                     file_path[0])

    body_zh, p_number_zh, i_number_zh = txt_to_body_translate(folder_path, 
                                                              file_path[1])

    path_list = get_html_file_path(folder_path)

    try:
        with open(path_list[0], "a", encoding="utf-8") as file:
            file.write(body)

        with open(path_list[1], "a", encoding="utf-8") as file:
            file.write(body_zh)
    except Exception as e:
        print(f"Error: When writing body for {folder_path.name}.")
        raise e
    
    return p_number, i_number, p_number_zh, i_number_zh


def write_blog_page_tail(folder_path: Path):
    """
    Write the tail of the blog page.

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
        print(f"Error: When writing tail for {folder_path.name}.")
        raise e


def blog_part_return(part_number: int):
    """
    Return head or tail of the blog HTML.

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
            <div class="blogpagemain">\n\n"""

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
            <div class="blogpagemain">\n\n"""

    tail = """\
            </div>
            
        </main>

        <script src="/script.js"></script>
        
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
            raise ValueError("Error: Wrong part number.")

def generate_blog_page(folder_path: Path):
    """
    Generate the blog page.

    :param folder_path: the folder path
    :return: None
    """

    save_temp_file(get_html_file_path(folder_path))
    
    try:
        write_blog_page_head(folder_path)
        (p_number, i_number, 
         p_number_zh, i_number_zh) = write_blog_page_body(folder_path)
        write_blog_page_tail(folder_path)
        delete_temp_file(get_html_file_path(folder_path))

        print(f"Translated blog page {folder_path.stem}: " +
              f"added {p_number} paragraphs {i_number} images (en), " +
              f"{p_number_zh} paragraphs {i_number_zh} images (zh).")

    except Exception as e:
        print(f"Error: When translating blog in {folder_path.name}: {e}.")
        restore_temp_file(get_html_file_path(folder_path))
        print("Restored the backup file.")
        sys.exit(1)

def generate_all_blog_pages():
    """
    Generate all blog pages in the blogs folder.

    :return: None
    """
    blogs_path = Path("./blogs")

    for folder_path in blogs_path.iterdir():
        if folder_path.is_dir():
            if folder_path.name != "example":
                generate_blog_page(folder_path)


if __name__ == "__main__":
    generate_all_blog_pages()