import sys
from pathlib import Path
import eyed3
import logging
import re
from generator_help_functions import *
sys.stdout.reconfigure(encoding='utf-8') # type: ignore

logging.getLogger("eyed3").setLevel(logging.ERROR)

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
        print(f"Error: When writing head for music_list.")
        raise e


def generate_music_picture(music_path: Path):
    """
    Generate the music cover under ./music/cover
     
    :param music_path: the music file path
    :return: the path of the generated cover image, or an empty string if no cover is found
    """

    cover_path = get_music_folder_path() / "cover"
    cover_path.mkdir(exist_ok=True)

    cover_file = cover_path / (music_path.stem + ".jpg")
    if cover_file.exists():
        return cover_file
    
    try:
        audio_file = eyed3.load(music_path)
        if ((audio_file is None) or (audio_file.tag is None) or 
            (not audio_file.tag.images)): # type: ignore
            return None
        
        image_data = audio_file.tag.images[0].image_data # type: ignore
        with open(cover_file, "wb") as img_file:
            img_file.write(image_data)

        return cover_file
    
    except Exception as e:
        return None
        

def get_body_part_of_music_list(music_path: Path, music_cover: Path,
                                is_first: bool = False):
    """Get the body part of the music list
    
    :param music_path: the music file path
    :param is_first: whether this is the first music in the list
    
    :return: a string of the body part or None if metadata is missing
    """

    m_regex = r"^(?P<artist>[^-]+)\s*-\s*(?P<title>.+)$"
    # match "artist - title"

    m_re = re.compile(m_regex)

    m_match = m_re.match(music_path.stem)

    if m_match:
        artist = m_match.group("artist").strip()
        title = m_match.group("title").strip()
    else:
        return None
    
    if is_first:
        music_class = "musiccontainer firstmusiccontainer"
    else:
        music_class = "musiccontainer"
    
    body = f"""\
                <!--{title}-->
                <div class="{music_class}">
                    <div class="musicimagecontainer">
                            <img src="{music_cover}" alt="{title}" class="musicimage">
                    </div>
                    <div class="musicparagraphcontainer">
                        <audio controls class="invis">
                            <source src="/music/Eye In The Sky - The Alan Parsons Project.mp3" type="audio/mp3">。
                        </audio>
                        <div class="musicparagraph">
                        
                            <div class="musicproducer">
                                &nbsp
                            </div>
                            <div class="musictitle">
                                {title}
                            </div>
    
                            <div class="musicproducer">
                                {artist}
                            </div>
                        </div>
                        <audio controls>
                            <source src="{music_path}" type="audio/mp3">。
                        </audio>
                    </div>
                </div>\n\n"""
    
    return body
    

def get_all_music_files():
    """
    Get all music files in the music folder.
    
    :return: a list of Path objects for all music files
    """

    root = get_music_folder_path()
    everything = root.iterdir()
    music_files = []
    for thing in everything:
        if thing.is_file() and thing.suffix.lower() in {".mp3"}:
            music_files.append(thing)

    music_files.sort(key=lambda f: f.stat().st_ctime)
    return music_files


def write_music_list_body():
    """
    Write music list body
    
    :return: the number of music files added to the list
    """

    s_number = 0

    path_list = get_music_list_path()
    music_files = get_all_music_files()

    if not music_files:
        print("Error: No music files found in the music folder.")
        return
    
    for i, music in enumerate(music_files):
        music_cover = generate_music_picture(music)

        if music_cover is None:
            print(f"Error: Skipping {music.name} due to missing cover.")
            continue

        if i == 0:
            body_part = get_body_part_of_music_list(music,music_cover, 
                                                    is_first=True)
        else:
            body_part = get_body_part_of_music_list(music, music_cover)

        if body_part is None:
            print(f"Error: Skipping {music.name} due to missing metadata.")
            continue

        try:
            with open(path_list[0], "a", encoding="utf-8") as file:
                file.write(body_part)

            with open(path_list[1], "a", encoding="utf-8") as file:
                file.write(body_part)

            s_number += 1

        except Exception as e:
            print(f"Error: When writing body for music {music.name}.")
            raise e
        
    return s_number


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
        print(f"Error: When writing tail for music_list.")
        raise e


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
            raise ValueError("Error: Wrong part number.")


def generate_music_list():
    """Generate the music list HTML files from music folder.
    
    :return: None
    """
    
    save_temp_file(get_music_list_path())

    try:
        write_music_list_head()
        s_number = write_music_list_body()
        write_music_list_tail()
        delete_temp_file(get_music_list_path())
        print(f"Added {s_number} music(s) to the music list.")
    except Exception as e:
        print(f"Error: When generating music list: {e}")
        restore_temp_file(get_music_list_path())
        print("Restored the backup file.")
        sys.exit(1)


if __name__ == "__main__":
    generate_music_list()