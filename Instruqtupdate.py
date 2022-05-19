import logging
import logging.handlers
import lib.Parseargs as Parseargs
import lib.Updateimagename as Updateimagename
import lib.Pushlabs as Pushlabs

logger = logging.getLogger(__name__)

def main():
    logger.info('Starting.')
    
    Updateimagename.UpdateImageNames(config)
    Pushlabs.PushLabs(config)
        
    logger.info('Completed.')
    
    
if __name__ == '__main__':
    config = Parseargs.parse_arguments()
    main()