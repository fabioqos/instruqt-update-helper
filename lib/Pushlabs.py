import logging
import subprocess
from unittest import result
import lib.Updateimagename as Updateimagename

logger = logging.getLogger(__name__)

def PushLabs(config):
    logger.info('Pushing labs.')

    updates = Updateimagename.UpdateImageName(config)
    instruqtpushcommand = updates.config.get('instruqt', 'instruqt_push_command')
    
    # Change directory to the root of instruqt repo.
    for lab in updates.labstoupdate:
        # Run the instruqt push command.
        result = subprocess.Popen("instruqt track checksum", shell=True, cwd=updates.labrootdir+'/'+lab, stdout=subprocess.PIPE)
        logging.info('Push result: {}'.format(result.communicate()[0]))
