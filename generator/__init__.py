import sys
import logging

sys.stdout.reconfigure(encoding='utf-8') # type: ignore

logging.basicConfig(
    filename= "./generator/generator.log",
    filemode= "w",
    level= logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s"
)