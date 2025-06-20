from pathlib import Path

def get_music_folder_path():
    """
    Get the path of the music folder.
    
    :return: a Path object for the music folder
    """


def get_music_list_path():
    """
    Get the path of the music list HTML files.
    
    :return: a list of Path objects for the music list HTML files
    """


def write_music_list_head():
    """
    Write music list head
    
    :return: None
    """


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


def music_list_part_return(part_number: int):
    """
    Return head or tail of the blog html

    :param part_number: 0 for head, 1 for head-zh, 2 for tail
    :return: str of head or tail
    """


def generate_music_list():
    """Generate the music list HTML files from music folder.
    
    :return: None
    """


if __name__ == "__main__":
    generate_music_list()