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
