import logging
import wavegenerator
import random

def randList(n):
    return [random.randint(1, 50) for _ in range(n)]

logging.basicConfig(filename='../soundmixture.log', level='DEBUG', format='%(asctime)s %(levelname)s %(message)s')
wlog = logging.getLogger(__name__)
wlog.info("Initiating mixing audio and noise files")



