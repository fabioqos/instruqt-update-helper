import logging
import json
import logging.handlers
from pickle import TRUE
import parseargs

logger = logging.getLogger(__name__)

def main():
    config = parseargs.parse_arguments()
    logger.info('Starting.')
    labs = config.get('instruqt', 'labs')
    print(json.loads(labs)[2])
    
    
if __name__ == '__main__':
    main()