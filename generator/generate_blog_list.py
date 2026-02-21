import re
import sys
from pathlib import Path
import logging
from generator.generator_help_functions import save_temp_file, delete_temp_file, restore_temp_file, general_part_return, get_txt_file_path


def get_blog_list_path() -> list[Path]:
    """
    Get the blog list path.

    :return: a list of blog list path
    """

    return [Path("./blog.html"), Path("./blog-zh.html")]


def write_blog_list_head() -> None:
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
        logging.exception(f"Error: When writing head for blog list.")
        raise


def get_all_blog_folders() -> list[Path]:
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
            logging.exception(f"Error: When parsing date from folder name {folder.name}.")
            return (9999, 99, 99)
        
    folder_list.sort(key=folder_date_key)

    return folder_list


def get_body_part_of_blog_list(folder_path: Path, is_first: bool = False) -> list[str]:
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
        error_message = "Error: Title not found in the txt file." + str(folder_path)
        logging.error(error_message)
        raise ValueError(error_message)

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
        error_message = "Error: Image not found in the txt file." + str(folder_path)
        logging.error(error_message)
        raise ValueError(error_message)

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
                </div>\n\n"""
    
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
                </div>\n\n"""
    
    return [body, body_zh]


def write_blog_list_body() -> int:
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
            logging.exception(f"Error: When writing body for blog list {folder.name}.")
            raise
        
    return b_number
    

def write_blog_list_tail() -> None:
    """
    Write the tail of the blog list.

    :return: None
    """

    path_list = get_blog_list_path()

    try:
        with open(path_list[0], "a", encoding="utf-8") as file:
            file.write(blog_list_part_return(2))

        with open(path_list[1], "a", encoding="utf-8") as file:
            file.write(blog_list_part_return(3))
    except Exception as e:
        logging.exception(f"Error: When writing tail for blog list.")
        raise


def blog_list_part_return(part_number: int) -> str:
    """
    Return head or tail of the blog list HTML.

    :param part_number: 0 for head, 1 for head-zh, 2 for tail, 3 for tail-zh
    :return: str of head or tail
    """

    title = ("Blog | SableFiSh Studio", "文章 | SableFiSh Studio")
    description = ("A personal archive of thoughts and experiments.", "个人文章与创作实验档案。")
    
    class_name = "bloglist"
    file_path = "/blog"

    return general_part_return(part_number, file_path, title, description, class_name)

def generate_blog_list() -> None:
    """
    Generate the blog list HTML files.
    
    :return: None
    """

    save_temp_file(get_blog_list_path())

    try:
        write_blog_list_head()
        b_number = write_blog_list_body()
        write_blog_list_tail()
        delete_temp_file(get_blog_list_path())
        logging.info(f"Added {b_number} blog(s) to the blog list.")

    except Exception as e:
        logging.exception(f"Error: When generating blog list: {e}")
        restore_temp_file(get_blog_list_path())
        logging.info("Restored the backup file.")
        sys.exit(1)


if __name__ == "__main__":
    generate_blog_list()