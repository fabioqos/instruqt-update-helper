from distutils.command.config import config
import logging
import json
import os
from threading import ExceptHookArgs
import yaml

logger = logging.getLogger(__name__)

def getlabs(config):
    # Set the list of labs. 
    labs_string = config.get('instruqt', 'labs')
    labs = json.loads(labs_string)
    return labs

def getlabrootdir(config):
    # Set the lab root directory.
    labrootdir = config.get('instruqt', 'rhel_labs_root_dir')
    return labrootdir

def get_old_vm_image(config):
    return config.get('oldimage', 'image').split()

def get_new_vm_image(config):
    return config.get('newimage', 'image').split()

def UpdateImageNames(config):
    logging.info('Updating image names.')

    labs = getlabs(config)
    logging.debug("Labs: {}".format(' '.join(map(str, labs))))
    listdirectory(config)

    labrootdir = getlabrootdir(config)
    logging.debug("Lab root directory: {}".format(labrootdir))

    oldvm = get_old_vm_image(config)
    logging.debug("Old VM image: {}".format(oldvm))

    newvm = get_new_vm_image(config)
    logging.debug("New VM image: {}".format(newvm))

    configyml = parsetrackconfig('test', labrootdir)
    logging.debug('Config YML: {}'.format(configyml))

    newconfigyml = changevmimage(oldvm, newvm, configyml)
    logging.debug('New Config YML: {}'.format(newconfigyml))
    
    return

def listdirectory(config):
    dir = config.get('instruqt', 'rhel_labs_root_dir')
    logging.debug('Directory list: {}'.format(os.listdir(dir)))
    return

def changevmimage(oldvm, newvm, configyaml):
    # This method will search and replace the instruqtconfigyaml for the oldimage and replace it with newimage.
    # Returns YAML with new VMs where the oldvm is matched and replaced with newvm.
    
    for vm in configyaml["virtualmachines"]:
        if vm["image"] == oldvm:
            vm["image"] = newvm

    return yaml.dump(configyaml)

def parsetrackconfig(labname, labrootdir, configyml="config.yml"):
    with open(labrootdir+labname+'/'+configyml, 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)
    return parsed_yaml