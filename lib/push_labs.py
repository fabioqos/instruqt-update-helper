import logging
import subprocess
from unittest import result
import lib.update_image_name as update_image_name

logger = logging.getLogger(__name__)

def PushLabs(config):
    logger.info('Pushing labs.')

    updates = update_image_name.UpdateImageName(config)
    instruqtpushcommand = updates.config.get('instruqt', 'instruqt_push_command')
    
    # Change directory to the root of instruqt repo.
    for lab in updates.labstoupdate:
        # Run the instruqt push command.
        result = subprocess.Popen(instruqtpushcommand, shell=True, cwd=updates.labrootdir+'/'+lab, stdout=subprocess.PIPE)
        logging.info('Push result: {}'.format(result.communicate()[0]))
        
    return

def PullLabs(config):
    logger.info('Pulling labs.')
    """This method will pull all the labs located in the instruqt root directory.
    """
    
    updates = update_image_name.UpdateImageName(config)
    lablist = updates.createlablist()
    instruqtpullcommand = updates.config.get('instruqt', 'instruqt_pull_command')
    for lab in lablist:
        result = subprocess.Popen(instruqtpullcommand, shell=True,
                                  cwd=updates.labrootdir+'/'+lab, stdout=subprocess.PIPE)
        logging.info('Pull result: {}'.format(result.communicate()[0]))
