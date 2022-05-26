import logging
import json
import os
import yaml
import time
import sys
import shutil

logger = logging.getLogger(__name__)

class UpdateImageName:
    def __init__(self, config) -> None:
        self.config = config

        self.labs = self.getlabs()
        logging.debug("Labs: {}".format(' '.join(map(str, self.labs))))

        self.dirlisting = self.listdirectory()
        logging.debug('Directory list: {}'.format(self.dirlisting))

        self.labrootdir = self.getlabrootdir()
        logging.debug("Lab root directory: {}".format(self.labrootdir))

        self.oldvm = self.get_old_vm_image()
        logging.debug("Old VM image: {}".format(self.oldvm))

        self.newvm = self.get_new_vm_image()
        logging.debug("New VM image: {}".format(self.newvm))

        self.configfind = self.findconfig()
        logging.debug('Labs {} found.'.format(self.configfind))

        self.labstoupdate = self.needsupdating()
        logging.debug('Labs to update {}.'.format(self.labstoupdate))

    def getlabs(self):
        # Get the list of labs. 
        labs_string = self.config.get('instruqt', 'labs')
        labs = json.loads(labs_string)
        return labs

    def getlabrootdir(self):
        # Get the lab root directory.
        labrootdir = self.config.get('instruqt', 'rhel_labs_root_dir')
        return labrootdir

    def get_old_vm_image(self):
        return self.config.get('oldimage', 'image').split()[0]

    def get_new_vm_image(self):
        return self.config.get('newimage', 'image').split()[0]

    def get_backup_dir(self):
        return self.config.get('general', 'backupdir')

    def UpdateImageNames(self):
        logging.info('Updating image names.')

        backupdir = self.createbackupdir(self.get_backup_dir())
        logging.debug('New backup dir {} created.'.format(backupdir))

        for lab in self.labstoupdate:

            configyml = self.parsetrackconfig(lab)
            logging.debug('Config YML: {}'.format(configyml))

            newconfigyml = self.changevmimage(configyml)
            logging.debug('New Config YML: {}'.format(newconfigyml))

            backup = self.createbackupconfig(lab, backupdir)
            logging.debug('Backup created at {}'.format(backup))

            writtenconfig = self.writeconfig(newconfigyml, lab)
            logging.debug(writtenconfig)
        
        return

    def listdirectory(self):
        dir = self.config.get('instruqt', 'rhel_labs_root_dir')
        return os.listdir(dir)

    def changevmimage(self, configyml):
        # This method will search and replace the instruqtconfigyaml for the oldimage and replace it with newimage.
        # Returns YAML with new VMs where the oldvm is matched and replaced with newvm.
        
        for vm in configyml["virtualmachines"]:
            if vm["image"] == self.oldvm:
                vm["image"] = self.newvm

        return yaml.dump(configyml)

    def parsetrackconfig(self, labname, configyml="config.yml"):
        with open(self.labrootdir+'/'+labname+'/'+configyml, 'r') as stream:
            try:
                parsed_yaml = yaml.safe_load(stream)
                return(parsed_yaml)
            except yaml.YAMLError as exc:
                logging.error(exc)
                sys.exit()

    def writeconfig(self, newconfigyml, lab, configyml="config.yml"):
        # Overwrite the config.yml file with the new config.
        try:
            file = open(self.labrootdir+'/'+lab+'/'+configyml, "w")
            file.write(newconfigyml)
            file.close
            return('Config for lab {} written.'.format(lab)) 
        except Exception as exc:
            return(exc)

    def createbackupdir(self, backupdir):
        # Create a directory under backup/ with the date and time in the name.
        try:
            directory = backupdir+'/'+time.strftime("%Y%m%d-%H%M%S")
            os.mkdir(directory)
            return(directory)
        except OSError as exc:
            logging.error(exc)
            sys.exit()

    def createbackupconfig(self, lab, backupdir):
        return shutil.copy2(self.labrootdir+'/'+lab+'/'+'config.yml', backupdir+'/'+lab+'_config.yml')

    def findconfig(self):
        matchedlabs = []
        try:
            for lab in self.labs:
                for dir in self.dirlisting:
                    if lab == dir:
                        matchedlabs.append(dir)
            return matchedlabs
        except Exception as exc:
            return exc

    def needsupdating(self):
        labstoupdate = []
        for lab in self.configfind:
            configyml = self.parsetrackconfig(lab)
            for vm in configyml['virtualmachines']:
                if vm['image'] != self.newvm:
                    logging.info("Lab - {} - contains a vm - {} - that is using the wrong image - {}.".format(lab, vm['name'], vm['image']))
                    labstoupdate.append(lab)
                else:
                    logging.info("Lab - {} - contains a vm - {} - that is using the right image - {}.".format(lab, vm['name'], vm['image']))
        return labstoupdate
