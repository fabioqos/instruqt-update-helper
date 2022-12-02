import argparse
import logging
from configparser import SafeConfigParser

logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse arguments from config/config.yml.

    Returns:
        config: config file
        check_labs: boolean
        modify_labs: boolean
        push_labs: boolean
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--DEBUG', '-d', action='store_true', default=False, dest='level',
                        help='Set logging level to DEBUG.')
    parser.add_argument('--config', '-c', action='store', type=str, dest='config_file', default='config/instruqt.conf',
                        help='Specify the config file.  The default is config/instruqt.conf')
    parser.add_argument('--check', '-k', action='store_true', default=False, dest='check_labs',
                        help='Specify whether to just run a check for whether images require updating. The script will check the image field in the lab config.yml to see whether it matches the newvm key in the instruqt.conf file.')
    parser.add_argument('--modify', '-m', action='store_true', default=False, dest='modify_labs',
                        help='Modify the config.yml files so that the old image (specified in the config.yml) is replaced with the new image.')
    parser.add_argument('--push', '-p', action='store_true', default=False, dest='push_labs',
                        help='Push the modified labs to Instruqt, initiating a lab rebuild.')
    parser.add_argument('--list', '-l', action='store_true', default=False, dest='list_labs',
                        help='List labs found in specified lab directory.')
    parser.add_argument('--pull', '-x', action='store_true', default=False, dest='pull_labs',
                        help='Pull all labs found in the instruqt root dir .')
    parser.add_argument('--arbitrary-push', '-ap', action='store_true', default=False, dest='arb_push_labs',
                        help='Arbitrarily push lab(s) to Instruqt, initiating a lab rebuild.')

    results = parser.parse_args()
    config = SafeConfigParser()
    config.read(results.config_file)
    
    set_debug = results.level
    log_file = config['general']['log']
    check_labs = results.check_labs
    modify_labs = results.modify_labs
    push_labs = results.push_labs
    list_labs = results.list_labs
    pull_labs = results.pull_labs
    arb_push = results.arb_push_labs

    if not config:
        logger.info('Config file is empty.  Exiting.')
        exit()
    else:
        log_file = config['general']['log']
        set_debug = config['general']['debug']
        
    log_format = '%(asctime)s %(levelname)s %(message)s'
    console = logging.StreamHandler()

    if set_debug:
        console.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG,
                            filename=log_file,
                            format=log_format,
                            )
    else:
        console.setLevel(logging.INFO)
        logging.basicConfig(level=logging.INFO,
                            filename=log_file,
                            format=log_format
                            )

    formatter = logging.Formatter(log_format)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    return config, check_labs, modify_labs, push_labs, list_labs, pull_labs, arb_push
