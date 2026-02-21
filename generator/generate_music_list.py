import sys
from pathlib import Path
import eyed3
import logging
from generator.generator_help_functions import save_temp_file, delete_temp_file, restore_temp_file, general_part_return

logging.getLogger("eyed3").setLevel(logging.ERROR)

def get_music_folder_path() -> Path:
    """
    Get the path of the music folder.
    
    :return: a Path object for the music folder
    """

    return Path("./music")


def get_music_list_path() -> list[Path]:
    """
    Get the path of the music list HTML files.
    
    :return: a list of Path objects for the music list HTML files
    """

    return [Path("./music.html"), Path("./music-zh.html")]


def write_music_list_head() -> None:
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


def generate_music_picture(music_path: Path) -> Path | None:
    """
    Generate the music cover under ./music/cover
     
    :param music_path: the music file path
    :return: the path of the generated cover image, or None if no cover is found
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
                                is_first: bool = False) -> str | None:
    """Get the body part of the music list
    
    :param music_path: the music file path
    :param is_first: whether this is the first music in the list
    
    :return: a string of the body part or None if metadata is missing
    """

    try:
        audio_file = eyed3.load(music_path)
        if ((audio_file is None) or (audio_file.tag is None)):
            return None
        
        artist = audio_file.tag.artist
        title = audio_file.tag.title
        
        if not artist or not title:
            return None
            
        artist = artist.strip()
        title = title.strip()
        
    except Exception as e:
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
    

def get_all_music_files() -> list[Path]:
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

    def get_track_number(music_file: Path) -> int:
        """
        Extract track number from the file name.
        
        :param music_file: the music file path
        :return: the track number as an integer, or infinity if not found
        """

        try:
            audio_file = eyed3.load(music_file)
            if audio_file and audio_file.tag and audio_file.tag.track_num:
                return audio_file.tag.track_num[0]
            else:
                return int('inf')
        except Exception as e:
            return int('inf')

    music_files.sort(key=get_track_number)
    return music_files


def write_music_list_body() -> int:
    """
    Write music list body
    
    :return: the number of music files added to the list
    """

    s_number = 0

    path_list = get_music_list_path()
    music_files = get_all_music_files()

    if not music_files:
        print("Error: No music files found in the music folder.")
        return 0
    
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


def write_music_list_tail() -> None:
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


def music_list_part_return(part_number: int) -> str:
    """
    Return head or tail of the music list html

    :param part_number: 0 for head, 1 for head-zh, 2 for tail, 3 for tail-zh
    :return: str of head or tail
    """

    title = ("FiShMuSic | SableFiSh Studio", "FiShMuSic 音乐精选 | SableFiSh Studio")
    description = ("A personal archive of my favorite music.", "个人音乐精选档案。")

    class_name = "musiclist"
    file_path = "/music"

    return general_part_return(part_number, file_path, title, description, class_name)

def generate_music_list() -> None:
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