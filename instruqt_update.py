import logging
import logging.handlers
import lib.parse_args as parse_args
import lib.update_image_name as update_image_name
import lib.push_labs as push_labs

logger = logging.getLogger(__name__)

def main():
    """This script will do each of the following separately:
    1. Check to see which instruqt labs are out of date. 
    2. Update the image for instruqt labs specified in the config/config.yml.
    3. Push labs to instruqt.
    """
    logger.info('Starting.')

    if check_labs:
        update_image_name.UpdateImageName(config).createchecklist()
    elif modify_labs:
        update_image_name.UpdateImageName(config).UpdateImageNames()
    elif push:
        push_labs.PushLabs(config)
    elif list_labs:
        update_image_name.UpdateImageName(config).createlablist()
    elif pull_labs:
        push_labs.PullLabs(config)
    elif arb_push:
        push_labs.ArbitraryPush(config)
    else:
        logger.info('No options specified. Please run "python Instruqtupdate -h" for more information.')

    logger.info('Completed.')

if __name__ == '__main__':
    config, check_labs, modify_labs, push, list_labs, pull_labs, arb_push = parse_args.parse_arguments()
    main()
