import logging
import json
import os
import time
import sys
import shutil
import yaml

logger = logging.getLogger(__name__)

class UpdateImageName:
    """Changes the "image:name" to the latest image specified in config/config.yml. 
    """
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
            # "lab" is the lab which contains VMs that need to have their images updated.
            # 1. Parse the config file of the lab. 
            # 2. Using the VM names in the lab kv pair, search for the VM in the config file. 
            # 3. Replace the image name for the vm in the config file.
            # 4. Backup the old config.yml.
            # 5. Write the new config.yml file.

            # 1. Parse the config file of the lab.
            configyml = self.parsetrackconfig(lab)
            logging.debug('Config YML: {}'.format(configyml))

            # 2. Using the VM names from the lab KV pair, search for the VM in the config file.
            vm_array = self.labstoupdate[lab]
            
            # 3. Replace the image name for the vm in the config file.
            newconfigyml = self.changevmimage(configyml, vm_array)
            logging.debug('New Config YML: {}'.format(newconfigyml))

            # 4. Backup the old config.yml.
            backup = self.createbackupconfig(lab, backupdir)
            logging.debug('Backup created at {}'.format(backup))

            # 5. Write the new config.yml file.
            writtenconfig = self.writeconfig(newconfigyml, lab)
            logging.debug(writtenconfig)

        return

    def listdirectory(self):
        dir = self.config.get('instruqt', 'rhel_labs_root_dir')
        return os.listdir(dir)

    def changevmimage(self, configyml, vm_array):
        # This method will search and replace the instruqtconfigyaml for the oldimage and replace it with newimage.
        # Returns YAML with new VMs where the oldvm is matched and replaced with newvm.

        for vm in vm_array:
            for i, vm_in_conf in enumerate(configyml["virtualmachines"]):
                if vm_in_conf["name"] == vm:
                    configyml["virtualmachines"][i]["image"] = self.newvm

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
        labstoupdate = {}
        for lab in self.configfind:
            configyml = self.parsetrackconfig(lab)
            vm_list = []
            for vm in configyml['virtualmachines']:
                if vm['image'] == self.oldvm:
                    logging.info("Lab - {} - contains a vm - {} - that is using the old image - {}.".format(lab, vm['name'], vm['image']))
                    vm_list.append(vm['name'])
                elif vm['image'] == self.newvm:
                    logging.info("Lab - {} - contains a vm - {} - that is using the current image - {}.".format(lab, vm['name'], vm['image']))
                else: 
                    logging.info("Lab - {} - contains a vm - {} - that is using neither the old or current image - {}.".format(lab, vm['name'], vm['image']))
            if vm_list == False:
                logging.debug("Lab {} is up to date.".format(lab))
            else:
                labstoupdate[lab] = vm_list
        return labstoupdate

    def createchecklist(self):
        try:
            file = open("status_"+time.strftime("%Y%m%d-%H%M%S")+".json", "w")
            file.writelines(json.dumps(self.labstoupdate))
            file.close
            return
        except Exception as exc:
            return(exc)
