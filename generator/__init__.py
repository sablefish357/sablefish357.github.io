import sys
import logging

sys.stdout.reconfigure(encoding='utf-8') # type: ignore

logging.basicConfig(
    level= logging.INFO,
    format= "%(asctime)s | %(levelname)-8s | %(module)-20s.%(funcName)-20s | %(message)s",
    datefmt= "%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("./generator/generator.log", mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)