import logging
import logging.handlers
import lib.Parseargs as Parseargs
import lib.Updateimagename as Updateimagename
import lib.Pushlabs as Pushlabs

logger = logging.getLogger(__name__)

def main():
    logger.info('Starting.')
    
    if check_labs:
        Updateimagename.UpdateImageName(config)
    else:
        # Updateimagename.UpdateImageName(config).UpdateImageNames()
        Pushlabs.PushLabs(config)
        
    logger.info('Completed.')
    
    
if __name__ == '__main__':
    config, check_labs = Parseargs.parse_arguments()
    main()