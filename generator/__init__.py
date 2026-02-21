import sys
import logging

sys.stdout.reconfigure(encoding='utf-8') # type: ignore

logging.basicConfig(
    level= logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s",

    handlers=[
        logging.FileHandler("./generator/generator.log", mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)