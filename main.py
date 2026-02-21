from generator.generate_blog_list import generate_blog_list
from generator.generate_blog_page import generate_all_blog_pages
from generator.generate_music_list import generate_music_list
from generator.generate_stage_list import generate_stage_list
from generator.generate_stage_page import generate_all_stage_pages
import logging
import time

if __name__ == "__main__":

    start_time = time.time()

    logging.info("Generating blog pages...")
    generate_blog_list()
    generate_all_blog_pages()
    logging.info("Blog pages generated.")
    logging.info("Generating stage pages...")
    generate_stage_list()
    generate_all_stage_pages()
    logging.info("Stage pages generated.")
    logging.info("Generating music pages...")
    generate_music_list()
    logging.info("Music pages generated.")

    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Total time: {total_time:.2f} seconds.")
