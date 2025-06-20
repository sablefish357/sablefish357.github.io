from pathlib import Path
from generate_blog_page import *

def get_music_folder_path():
    """
    Get the path of the music folder.
    
    :return: a Path object for the music folder
    """

    return Path("./music")


def get_music_list_path():
    """
    Get the path of the music list HTML files.
    
    :return: a list of Path objects for the music list HTML files
    """

    return [Path("./music.html"), Path("./music-zh.html")]


def write_music_list_head():
    """
    Write music list head
    
    :return: None
    """

    path_list = get_music_list_path()

    try:
        with open(path_list[0], "w", encoding="utf-8") as file:
            file.write(music_list_part_return(0))

        with open(path_list[1], "w", encoding="utf-8") as file:
            file.write(music_list_part_return(1))

    except Exception as e:
        print(f"Error writing head for music_list: {e}")
        restore_temp_file(path_list)
        print("Restored the backup file.")
        sys.exit(1)

def generate_music_picture(music_path: Path):
    """
    Generate the music cover under ./music/cover
     
    :param music_path: the music file path
    :return: None
    """


def get_body_part_of_music_list(music_path: Path, is_first: bool = False):
    """Get the body part of the music list
    
    :param music_path: the music file path
    :param is_first: whether this is the first music in the list
    
    :return: a list of en and zh string of the body part
    """


def write_music_list_body():
    """
    Write music list body
    
    :return: None
    """


def write_music_list_tail():
    """Write music list tail
    
    :return: None
    """

    path_list = get_music_list_path()

    try:
        with open(path_list[0], "a", encoding="utf-8") as file:
            file.write(music_list_part_return(2))

        with open(path_list[1], "a", encoding="utf-8") as file:
            file.write(music_list_part_return(2))

    except Exception as e:
        print(f"Error writing tail for music_list: {e}")
        restore_temp_file(path_list)
        print("Restored the backup file.")
        sys.exit(1)


def music_list_part_return(part_number: int):
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

        <link rel="icon" type="image/jpg" href="image/favicon.jpg">
        <link rel="stylesheet" href="style.css">

        <script src="/addelements.js" defer></script>
    </head> 

    <body>
        <main>
            <div class="musiclist">
                <!-- MUSIC LIST STARTS HERE-->\n\n"""

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
        
            <div class="musiclist">
                <!-- MUSIC LIST STARTS HERE-->\n\n"""

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


def generate_music_list():
    """Generate the music list HTML files from music folder.
    
    :return: None
    """
    
    save_temp_file(get_music_list_path())

    try:
        write_music_list_head()
        write_music_list_body()
        write_music_list_tail()
        delete_temp_file(get_music_list_path())
        print("Music list generated successfully.")
    except Exception as e:
        print(f"Error generating music list: {e}")
        restore_temp_file(get_music_list_path())
        print("Restored the backup file.")
        sys.exit(1)


if __name__ == "__main__":
    generate_music_list()