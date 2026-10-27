
import logging
import psutil
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def measure_ram(path):
    try:
        memory = psutil.Process().memory_info().rss / (1024 * 1024)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info("RAM usage: %.2f MB", memory)
        with open(path, "a") as file:
            file.write(f"{timestamp} RAM usage: {memory:.2f} MB, \n")
        return memory
    except (psutil.Error, OSError) as error:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(path, "a") as file:
            file.write(f"{timestamp} Could not measure RAM: {error}\n")
        return None