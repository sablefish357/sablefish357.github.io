from pathlib import Path
import re

def save_temp_file(file_path: list[Path]) -> None:
    """
    Save old file if exists as .bak file
    
    :param file_path: a list of file path
    :return: None
    """

    for file in file_path:
        if file.exists():
            try:
                backup_path = file.with_suffix('.bak')
                file.rename(backup_path)
            except Exception as e:
                print(f"Error: When creating backup for {file.name}: {e}")
                raise e
            

def restore_temp_file(file_path: list[Path]) -> None:
    """
    Delete created html file if exists and restore the backup file from .bak 
    file

    :param file_path: a list of file path
    :return: None
    """

    for file in file_path:
        backup_path = file.with_suffix('.bak')
        if backup_path.exists():
            try:
                file.unlink(missing_ok=True)
                backup_path.rename(file)
            except Exception as e:
                print(f"Error: When restoring {file.name} from backup: {e}")
                raise e
            
            
def delete_temp_file(file_path: list[Path]) -> None:
    """
    Delete temporary .bak file

    :param file_path: a list of file path
    :return: None
    """

    for file in file_path:
        backup_path = file.with_suffix('.bak')
        if backup_path.exists():
            try:
                backup_path.unlink(missing_ok=True)
            except Exception as e:
                print(f"Error: When deleting backup {backup_path.name}: {e}")
                raise e


def get_html_file_path(folder_path: Path) -> list[Path]:
    """
    Use folder path to get html file path with same name as the folder.

    :param folder_path: the folder path
    :return: a list of both en and zh file path
    """

    folder_name = folder_path.name
    file_name = folder_name + ".html"
    file_name_zh = folder_name + "-zh.html"

    file_path = folder_path / file_name
    file_path_zh = folder_path / file_name_zh

    return [file_path, file_path_zh]


def get_txt_file_path(folder_path: Path) -> list[Path]:
    """
    Use folder path to get txt file path with same name as the folder.

    :param folder_path: the folder path
    :return: a list of en and zh file path
    """

    folder_name = folder_path.name
    file_name = folder_name + ".txt"
    file_name_zh = folder_name + "-zh.txt"

    file_path = folder_path / file_name
    file_path_zh = folder_path / file_name_zh

    return [file_path, file_path_zh]

def get_title_from_folder(folder_path: Path) -> tuple[str, str]:
    """
    Get title from txt files in the folder.

    :param folder_path: the folder path
    :return: a tuple of (en_title, zh_title)
    """

    t_regex = r"^/t\{\}\s*(?P<title>.*)$"  
    #match /t{} title

    t_re = re.compile(t_regex)

    txt_path = get_txt_file_path(folder_path)

    file = txt_path[0].read_text(encoding="utf-8").splitlines()
    file_zh = txt_path[1].read_text(encoding="utf-8").splitlines()

    title_match = t_re.match(file[0])
    title_match_zh = t_re.match(file_zh[0])

    if title_match and title_match_zh:
        title = title_match.group("title")
        title_zh = title_match_zh.group("title")
    else:
        raise ValueError("Error: Title not found in the txt file." + str(folder_path))
    
    return (title, title_zh)

def get_title_image_from_folder(file_path: str) -> str:
    """
    Get title image from txt files in the folder.

    :param file_path: the file path without language and .html
    :return: image name
    """
    i_regex = (r"^/i\{(?P<image_name>[^,}]*)\s*,"
               r"\s*(?P<image_size>[^,}]*)\s*\}"
               r"\s*(?P<description>.*)$")  
    # match /i{image_name, image_size} description

    i_re = re.compile(i_regex)

    txt_path = Path("." + file_path + ".txt")

    file = txt_path.read_text(encoding="utf-8").splitlines()

    image_match = i_re.match(file[1])

    if image_match:
        image_name = image_match.group("image_name")
        return image_name
    else:
        raise ValueError("Error: Image not found in the txt file." + file_path)
    
def get_og_image_url(file_path: str) -> str:
    """
    Get og image url for the page.

    :param file_path: the file path without language.html
    :return: the og image url
    """

    
    base_url = "https://sablefish357.github.io"

    if file_path == "/index":
        return base_url + "/image/og_image_index.jpg"
    
    if file_path == "/stages":
        return base_url + "/image/og_image_stages.jpg"
    
    if file_path == "/blog":
        return base_url + "/image/og_image_blog.jpg"
    
    if file_path == "/music":
        return base_url + "/image/og_image_music.jpg"
    
    if file_path.startswith("/stages/"):
        image_name = get_title_image_from_folder(file_path)
        return base_url + f"/stages/{file_path.split('/')[-1]}/{image_name}"
    
    if file_path.startswith("/blogs/"):
        image_name = get_title_image_from_folder(file_path)
        return base_url + f"/blogs/{file_path.split('/')[-1]}/{image_name}"
    
    raise ValueError("Error: Unrecognized file path for og image url." + file_path)

def general_part_return(part_number: int, 
                        file_path: str, 
                        page_title: tuple[str, str],
                        description: tuple[str, str],
                        class_name: str) -> str:
    """
    Return head or tail of the general HTML.

    :param part_number: 0 for head, 1 for head-zh, 2 for tail, 3 for tail-zh
    :param file_path: the file path without language.html
    :param page_title: the title of the page, a tuple of (en_title, zh_title)
    :param description: the description of the page, a tuple of (en_description, zh_description)
    :param class_name: the class name for CSS
    :return: str of head or tail
    """

    is_en = part_number in [0, 2]

    if file_path == "/index":
        is_main_page = True
    else:
        is_main_page = False

    context = {
        "lang_code" : "en" if is_en else "zh-CN",
        "home_link" : "/" if is_en else "/index-zh.html",

        "page_title" : page_title[0] if is_en else page_title[1],
        "description" : description[0] if is_en else description[1],

        "alt_link_en" : (f"https://sablefish357.github.io{file_path}.html" 
                         if not is_main_page else "https://sablefish357.github.io/"),
        "alt_link_zh" : (f"https://sablefish357.github.io{file_path}-zh.html"
                         if not is_main_page else "https://sablefish357.github.io/index-zh.html"),

        "nav_video" : "VIDEOS" if is_en else "视频",
        "nav_video_link" : ("https://www.youtube.com/@SableFiSh" 
                            if is_en else "https://space.bilibili.com/49323671"),

        "nav_stage_text" : "STAGES" if is_en else "场景",
        "nav_stage_link" : "/stages.html" if is_en else "/stages-zh.html",

        "nav_blog_text"  : "BLOG" if is_en else "文章",
        "nav_blog_link"  : "/blog.html" if is_en else "/blog-zh.html",

        "nav_home_text" : "HOME" if is_en else "主页",
        "nav_home_link" : "/" if is_en else "/index-zh.html",

        "nav_contact_text" : "CONTACT" if is_en else "联系我",
        "nav_contact_link" : "#bottom",

        "nav_lang_text" : "CHN" if is_en else "ENG",
        "nav_lang_link" : (f"{file_path}-zh.html" 
                           if is_en else f"{file_path}.html"),
        
        "footer_text" : "Top" if is_en else "回到顶部"
    }

    og_url = context['alt_link_en'] if is_en else context['alt_link_zh']

    og_image_url = get_og_image_url(file_path)

    head = f"""\
<!DOCTYPE html>
<html lang="{context['lang_code']}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="{context['description']}">
        <meta name="keywords" content="Blender,SableFiSh,MMD,mikumikudance ">

        <title>
            {context['page_title']}
        </title>

        <link rel="icon" type="image/jpg" href="/image/favicon.jpg">
        <link rel="stylesheet" href="/style.css">

        <meta property="og:title" content="{context['page_title']}">
        <meta property="og:description" content="{context['description']}">
        <meta property="og:type" content="website">
        <meta property="og:url" content="{og_url}">
        <meta property="og:site_name" content="SableFiSh Studio">
        <meta property="og:image" content="{og_image_url}">

        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@100..900&display=swap" rel="stylesheet">

        <link rel="alternate" hreflang="en" href="{context['alt_link_en']}">
        <link rel="alternate" hreflang="zh" href="{context['alt_link_zh']}">
        <link rel="alternate" hreflang="x-default" href="{context['alt_link_en']}">
    </head>
     
    <body>
        <header id="header"> 
            <a href="{context['home_link']}">
                <div class="SableFiSh">
                    SableFiSh
                </div>
            </a>
            <a href="{context['home_link']}">
                <div class="Studio">
                    STUDIO
                </div>
            </a>
        </header>

        <nav id="top">
            <div class="leftbar">
                <a href="{context['nav_video_link']}">
                    <div>{context['nav_video']}</div>
                </a>
        
                <a href="{context['nav_stage_link']}">
                    <div>{context['nav_stage_text']}</div>
                </a>

                <a href="{context['nav_blog_link']}">
                    <div>{context['nav_blog_text']}</div>
                </a>

            </div>

            <div class="rightbar">
                <a href="{context['nav_home_link']}">
                    <div>{context['nav_home_text']}</div>
                </a>

                <a href="{context['nav_contact_link']}">
                    <div>{context['nav_contact_text']}</div>
                </a>

                <a href="{context['nav_lang_link']}">
                    <div>{context['nav_lang_text']}</div>
                </a>

            </div>
        </nav>

        <main class="show">
            <div class="{class_name}">\n\n"""
    
    tail = f"""\
            </div>  
        </main>

        <footer id="bottom">
            <div class="footer-left">
                <div class="footer-container">
                    <a href="https://www.youtube.com/@SableFiSh">
                        <div>
                            Youtube
                        </div>
                    </a>
                    <a href="https://space.bilibili.com/49323671">
                        <div>
                            Bilibili
                        </div>
                    </a>
                    <a href="https://www.artstation.com/sablefish">
                        <div>
                            ArtStation
                        </div>
                    </a>
                    <a href="mailto:sablefish357@gmail.com">
                        <div>
                            sablefish357@gmail.com
                        </div>
                    </a>
                    <a href="#top">
                        <div>
                            {context['footer_text']}
                        </div>
                    </a>
                </div>
                
                <div class="copyright">
                    <div>
                        © 2026 SableFiSh. All Rights Reserved.
                    </div>
                </div>
            </div>

            <div class="foot-logo-container">
                <a href="#top">
                    <div class="SableFiSh">
                        SableFiSh
                    </div>
                </a>
                <a href="#top">
                    <div class="Studio">
                        STUDIO
                    </div>
                </a>
            </div>

        </footer>

        <script src="/script.js"></script>
        
    </body>
</html>"""
    
    match part_number:
        case 0 | 1:
            return head
        case 2 | 3:
            return tail
        case _:
            raise ValueError("Error: Wrong part number.")

if __name__ == "__main__":
    print("This module is not meant to be run directly. It contains helper " +  
          "functions for generating music and blog pages and lists.")