import re
from pathlib import Path
from txt_to_html_blog import *


def get_blog_list_path():
    """
    Get the blog list path

    :return: a list of blog list path
    """

    return ["./blog.html", "./blog-zh.html"]


def write_blog_list_head():
    """
    Write blog head

    :return: None
    """

    path_list = get_blog_list_path()

    with open(path_list[0], "w", encoding="utf-8") as file:
        file.write(blog_list_part_return(0))

    with open(path_list[1], "w", encoding="utf-8") as file:
        file.write(blog_list_part_return(1))

    print("Successfully wrote the blog list header\n")


def get_all_blog_folders():
    """
    Get all blog folders

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
        m, d, y = map(int, folder.name.split('-'))
        return (y, m, d)

    folder_list.sort(key=folder_date_key)

    print(folder_list)

    return folder_list


def get_body_part_of_blog_list(folder_path: Path, is_first: bool = False):
    """
    Get the body part of the blog list
    
    :param folder_path: the folder path
    :return: a list of en and zh string of the body part
    """

    t_regex = r"^/t\{\}\s*(?P<title>.*)$"  
    #match /t{} title

    t_re = re.compile(t_regex)

    i_regex = (r"^/i\{(?P<image_name>[^,}]+)\s*,"
               r"\s*(?P<image_size>[^,}]+)\s*\}"
               r"\s*(?P<description>.*)$")  
    # match /i{image_name, image_size} description

    i_re = re.compile(i_regex)

    txt_path = get_txt_file_path(str(folder_path))

    file = Path(txt_path[0]).read_text(encoding="utf-8").splitlines()
    file_zh = Path(txt_path[1]).read_text(encoding="utf-8").splitlines()

    title_match = t_re.match(file[0])
    title_match_zh = t_re.match(file_zh[0])

    if title_match and title_match_zh:
        title = title_match.group("title")
        title_zh = title_match_zh.group("title")
    else:
        raise ValueError("Title not found in the txt file.")
    
    date = get_folder_name(folder_path)

    slash_date = date.replace("-", "/")

    image_match = i_re.match(file[1])
    image_match_zh = i_re.match(file_zh[1])

    if (image_match and image_match_zh):
        image_name = image_match.group("image_name")
        description = image_match.group("description")
        image_name_zh = image_match_zh.group("image_name")
        description_zh = image_match_zh.group("description")
    else:
        raise ValueError("Image not found in the txt file.")

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
                        <a href="/blogs/{date}/{date}.html">
                            <img src="blogs/{date}/{image_name_zh}" alt="{description_zh}" class="blogimage">
                        </a>
                    </div>
                    <div class="blogparagraph">
                        <a href="/blogs/{date}/{date}.html">
                            <div class="blogtitle">
                                {title_zh}
                            </div>
                        </a>
                        <a href="/blogs/{date}/{date}.html">
                            <div class="blogdate">
                                {slash_date}
                            </div>
                        </a>
                    </div>
                </div>\n"""
    
    return [body, body_zh]


def write_blog_list_body():
    """
    Write blog body
    
    :return: None
    """

    for i, folder in enumerate(get_all_blog_folders()):

        if i == 0:
            body_part = get_body_part_of_blog_list(folder, is_first= True)
        else:
            body_part = get_body_part_of_blog_list(folder)
        
        path_list = get_blog_list_path()

        with open(path_list[0], "a", encoding="utf-8") as file:
            file.write(body_part[0])

        print(f"Successfully wrote the blog list body of {folder.name}\n")

        with open(path_list[1], "a", encoding="utf-8") as file:
            file.write(body_part[1])

        print(f"Successfully wrote the blog list body of {folder.name} in zh\n")
    


def write_blog_list_tail():
    """
    Write blog tail

    :return: None
    """

    path_list = get_blog_list_path()

    with open(path_list[0], "a", encoding="utf-8") as file:
        file.write(blog_list_part_return(2))

    with open(path_list[1], "a", encoding="utf-8") as file:
        file.write(blog_list_part_return(2))

    print("Successfully wrote the blog list tail\n")



def blog_list_part_return(part_number: int):
    """
    Return head or tail of the blog list html

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

        <link rel="icon" type="image/jpg" href="image/favicon.jpg">
        <link rel="stylesheet" href="style.css">

        <script src="/addelements.js" defer></script>
    </head> 
    
    <body>
        <main>
            <div class="bloglist">
                <!-- BLOG LIST STARTS HERE -->\n"""

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

        <link rel="icon" type="image/jpg" href="image/favicon.jpg">
        <link rel="stylesheet" href="style.css">

        <script src="/addelements_zh.js" defer></script>
    </head> 
    
    <body>
        <main>
            <div class="bloglist">
                <!-- BLOG LIST STARTS HERE -->\n"""

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
        

def generate_blog_list():
    """
    Generate both blog and blog_zh files
    
    :param folder_path: the folder path
    :return: None
    """
    write_blog_list_head()
    write_blog_list_body()
    write_blog_list_tail()


if __name__ == "__main__":
    generate_blog_list()