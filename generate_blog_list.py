import re
import sys
from pathlib import Path
from generator_help_functions import *
sys.stdout.reconfigure(encoding='utf-8') # type: ignore


def get_blog_list_path():
    """
    Get the blog list path.

    :return: a list of blog list path
    """

    return [Path("./blog.html"), Path("./blog-zh.html")]


def write_blog_list_head():
    """
    Write the head of the blog list.

    :return: None
    """

    path_list = get_blog_list_path()

    try:
        with open(path_list[0], "w", encoding="utf-8") as file:
            file.write(blog_list_part_return(0))

        with open(path_list[1], "w", encoding="utf-8") as file:
            file.write(blog_list_part_return(1))

    except Exception as e:
        print(f"Error: When writing head for blog list.")
        raise e


def get_all_blog_folders():
    """
    Get all blog folders.

    :return: a list of blog folder paths in date order
    """

    root = Path("./blogs")

    everything = root.iterdir()

    folder_list = []
    for thing in everything:
        if thing.is_dir():
            if thing.name != "example" :
                folder_list.append(thing)

    def folder_date_key(folder):
        try:
            m, d, y = map(int, folder.name.split('-'))
            return (y, m, d)
        except Exception as e:
            print(f"Error: When parsing date from folder name {folder.name}.")
            return (9999, 99, 99)
        
    folder_list.sort(key=folder_date_key)

    return folder_list


def get_body_part_of_blog_list(folder_path: Path, is_first: bool = False):
    """
    Get the body part of the blog list.
    
    :param folder_path: the folder path
    :param is_first: whether this is the first blog in the list
    :return: a list of en and zh string of the body part
    """

    t_regex = r"^/t\{\}\s*(?P<title>.*)$"  
    #match /t{} title

    t_re = re.compile(t_regex)

    i_regex = (r"^/i\{(?P<image_name>[^,}]*)\s*,"
               r"\s*(?P<image_size>[^,}]*)\s*\}"
               r"\s*(?P<description>.*)$")
    # match /i{image_name, image_size} description

    i_re = re.compile(i_regex)

    txt_path = get_txt_file_path(folder_path)

    file = txt_path[0].read_text(encoding="utf-8").splitlines()
    file_zh = txt_path[1].read_text(encoding="utf-8").splitlines()

    title_match = t_re.match(file[0])
    title_match_zh = t_re.match(file_zh[0])

    if title_match and title_match_zh:
        title = title_match.group("title")
        title_zh = title_match_zh.group("title")
    else:
        raise ValueError("Error: Title not found in the txt file.")

    date = folder_path.name

    slash_date = date.replace("-", "/")

    image_match = i_re.match(file[1])
    image_match_zh = i_re.match(file_zh[1])

    if (image_match and image_match_zh):
        image_name = image_match.group("image_name")
        description = image_match.group("description")
        image_name_zh = image_match_zh.group("image_name")
        description_zh = image_match_zh.group("description")
    else:
        raise ValueError("Error: Image not found in the txt file.")

    if is_first:
        blog_list_class = "blogcontainer firstblogcontainer"
    else:
        blog_list_class = "blogcontainer"
        
    body =f"""\
                <div class="{blog_list_class}">
                    <div class="blogimagecontainer">
                        <a href="/blogs/{date}/{date}.html">
                            <img src="blogs/{date}/{image_name}" alt="{description}" class="blogimage">
                        </a>
                    </div>
                    <div class="blogparagraph">
                        <a href="/blogs/{date}/{date}.html">
                            <div class="blogtitle">
                                {title}
                            </div>
                        </a>
                        <a href="/blogs/{date}/{date}.html">
                            <div class="blogdate">
                                {slash_date}
                            </div>
                        </a>
                    </div>
                </div>\n"""
    
    body_zh = f"""\
                <div class="{blog_list_class}">
                    <div class="blogimagecontainer">
                        <a href="/blogs/{date}/{date}-zh.html">
                            <img src="blogs/{date}/{image_name_zh}" alt="{description_zh}" class="blogimage">
                        </a>
                    </div>
                    <div class="blogparagraph">
                        <a href="/blogs/{date}/{date}-zh.html">
                            <div class="blogtitle">
                                {title_zh}
                            </div>
                        </a>
                        <a href="/blogs/{date}/{date}-zh.html">
                            <div class="blogdate">
                                {slash_date}
                            </div>
                        </a>
                    </div>
                </div>\n"""
    
    return [body, body_zh]


def write_blog_list_body():
    """
    Write the body of the blog list.
    
    :return b_number: the number of blogs written
    """

    b_number = 0

    path_list = get_blog_list_path()

    for i, folder in enumerate(get_all_blog_folders()):

        if i == 0:
            body_part = get_body_part_of_blog_list(folder, is_first= True)
        else:
            body_part = get_body_part_of_blog_list(folder)

        try:
            with open(path_list[0], "a", encoding="utf-8") as file:
                file.write(body_part[0])

            with open(path_list[1], "a", encoding="utf-8") as file:
                file.write(body_part[1])

            b_number += 1

        except Exception as e:
            print(f"Error: When writing body for blog list {folder.name}.")
            raise e
        
    return b_number
    

def write_blog_list_tail():
    """
    Write the tail of the blog list.

    :return: None
    """

    path_list = get_blog_list_path()

    try:
        with open(path_list[0], "a", encoding="utf-8") as file:
            file.write(blog_list_part_return(2))

        with open(path_list[1], "a", encoding="utf-8") as file:
            file.write(blog_list_part_return(2))
    except Exception as e:
        print(f"Error: When writing tail for blog list.")
        raise e


def blog_list_part_return(part_number: int):
    """
    Return head or tail of the blog list HTML.

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
            <div class="bloglist">
                <!-- BLOG LIST STARTS HERE -->\n\n"""

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
            <div class="bloglist">
                <!-- BLOG LIST STARTS HERE -->\n\n"""

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
        

def generate_blog_list():
    """
    Generate both blog and blog_zh files
    
    :return: None
    """

    save_temp_file(get_blog_list_path())

    try:
        write_blog_list_head()
        b_number = write_blog_list_body()
        write_blog_list_tail()
        delete_temp_file(get_blog_list_path())
        print(f"Added {b_number} blog(s) to the blog list.")

    except Exception as e:
        print(f"Error: When generating blog list: {e}")
        restore_temp_file(get_blog_list_path())
        print("Restored the backup file.")
        sys.exit(1)


if __name__ == "__main__":
    generate_blog_list()