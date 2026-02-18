from generator.generate_blog_list import generate_blog_list
from generator.generate_blog_page import generate_all_blog_pages
from generator.generate_music_list import generate_music_list
from generator.generate_stage_list import generate_stage_list
from generator.generate_stage_page import generate_all_stage_pages
import time

if __name__ == "__main__":

    start_time = time.time()

    print("Generating blog pages...")
    generate_blog_list()
    generate_all_blog_pages()
    print()
    print("Generating stage pages...")
    generate_stage_list()
    generate_all_stage_pages()
    print()
    print("Generating music pages...")
    generate_music_list()
    print()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time: {total_time:.2f} seconds.")
