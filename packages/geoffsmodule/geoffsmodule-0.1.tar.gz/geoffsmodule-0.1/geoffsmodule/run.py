import gpu, mymath
import logging
import numpy as np

def main():
    logging.basicConfig(filename='/Users/gw/Dropbox/2018w/mbptechtalk/main.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Started')
    a = np.ones((5,100000))
    b = np.ones((100000,3))
    mymath.mm(a,b)
    logging.info('mymath.mm Finished')
    gpu.mm_jit(a,b)
    logging.info('gpu.mm_jit Finished')
    np.dot(a,b)
    logging.info('np.dot Finished')
    logging.info('All done')

if __name__ == "__main__":
    main()