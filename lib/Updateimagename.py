import logging
import json
import os
import yaml
import time
import sys
import shutil

logger = logging.getLogger(__name__)

def getlabs(config):
    # Get the list of labs. 
    labs_string = config.get('instruqt', 'labs')
    labs = json.loads(labs_string)
    return labs

def getlabrootdir(config):
    # Get the lab root directory.
    labrootdir = config.get('instruqt', 'rhel_labs_root_dir')
    return labrootdir

def get_old_vm_image(config):
    return config.get('oldimage', 'image').split()[0]

def get_new_vm_image(config):
    return config.get('newimage', 'image').split()[0]

def get_backup_dir(config):
    return config.get('general', 'backupdir')

def UpdateImageNames(config):
    logging.info('Updating image names.')

    labs = getlabs(config)
    logging.debug("Labs: {}".format(' '.join(map(str, labs))))
    
    dirlisting = listdirectory(config)
    logging.debug('Directory list: {}'.format(dirlisting))

    labrootdir = getlabrootdir(config)
    logging.debug("Lab root directory: {}".format(labrootdir))

    oldvm = get_old_vm_image(config)
    logging.debug("Old VM image: {}".format(oldvm))

    newvm = get_new_vm_image(config)
    logging.debug("New VM image: {}".format(newvm))

    configfind = findconfig(labs, dirlisting)
    logging.debug('Labs {} found.'.format(configfind))

    labstoupdate = needsupdating(configfind, newvm,labrootdir)
    logging.debug('Labs to update {}.'.format(labstoupdate))

    backupdir = createbackupdir(get_backup_dir(config))
    logging.debug('New backup dir {} created.'.format(backupdir))

    for lab in labstoupdate:

        configyml = parsetrackconfig(lab, labrootdir)
        logging.debug('Config YML: {}'.format(configyml))

        newconfigyml = changevmimage(oldvm, newvm, configyml)
        logging.debug('New Config YML: {}'.format(newconfigyml))

        backup = createbackupconfig(lab, labrootdir, backupdir)
        logging.debug('Backup created at {}'.format(backup))

        writtenconfig = writeconfig(newconfigyml, lab, labrootdir)
        logging.debug(writtenconfig)
    
    return

def listdirectory(config):
    dir = config.get('instruqt', 'rhel_labs_root_dir')
    return os.listdir(dir)

def changevmimage(oldvm, newvm, configyaml):
    # This method will search and replace the instruqtconfigyaml for the oldimage and replace it with newimage.
    # Returns YAML with new VMs where the oldvm is matched and replaced with newvm.
    
    for vm in configyaml["virtualmachines"]:
        if vm["image"] == oldvm:
            vm["image"] = newvm

    return yaml.dump(configyaml)

def parsetrackconfig(labname, labrootdir, configyml="config.yml"):
    with open(labrootdir+'/'+labname+'/'+configyml, 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
            return(parsed_yaml)
        except yaml.YAMLError as exc:
            logging.error(exc)
            sys.exit()

def writeconfig(newconfigyml, labname, labrootdir, configyml="config.yml"):
    # Overwrite the config.yml file with the new config.
    try:
        file = open(labrootdir+'/'+labname+'/'+configyml, "w")
        file.write(newconfigyml)
        file.close
        return('Config for lab {} written.'.format(labname)) 
    except Exception as exc:
        return(exc)

def createbackupdir(backupdir):
    # Create a directory under backup/ with the date and time in the name.
    try:
        directory = backupdir+'/'+time.strftime("%Y%m%d-%H%M%S")
        os.mkdir(directory)
        return(directory)
    except OSError as exc:
        logging.error(exc)
        sys.exit()

def createbackupconfig(labname, sourcedir, backupdir):
    return shutil.copy2(sourcedir+'/'+labname+'/'+'config.yml', backupdir+'/'+labname+'_config.yml')

def findconfig(labs, dirlisting):
    matchedlabs = []
    try:
        for lab in labs:
            for dir in dirlisting:
                if lab == dir:
                    matchedlabs.append(dir)
        return matchedlabs
    except Exception as exc:
        return exc

def needsupdating(configsthatexist, newvm, labrootdir):
    labstoupdate = []
    for lab in configsthatexist:
        configyml = parsetrackconfig(lab, labrootdir)
        for vm in configyml['virtualmachines']:
            if vm['image'] != newvm:
                logging.info("Lab - {} - contains a vm - {} - that is using the wrong image - {}.".format(lab, vm['name'], vm['image']))
                labstoupdate.append(lab)
            else:
                logging.info("Lab - {} - contains a vm - {} - that is using the right image - {}.".format(lab, vm['name'], vm['image']))
    return labstoupdate
