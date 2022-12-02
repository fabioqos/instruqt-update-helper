import logging
import subprocess
import lib.update_image_name as update_image_name
from colorama import init, Fore

init(autoreset=True)

logger = logging.getLogger(__name__)

def PushLabs(config):
    logger.info('Pushing labs.')

    updates = update_image_name.UpdateImageName(config)
    instruqtpushcommand = updates.config.get('instruqt', 'instruqt_push_command')
    
    # Change directory to the root of instruqt repo.
    for lab in updates.labstoupdate:
        # Run the instruqt push command.
        if updates.labstoupdate[lab]:
            try:
                result = subprocess.Popen(instruqtpushcommand, shell=True, cwd=updates.labrootdir +
                                          '/'+lab, stdout=subprocess.PIPE, universal_newlines=True)
                out = result.communicate()[0]
                if 'OK\n==> Building track' in out:
                    logging.info(Fore.GREEN + 'Build result successful for lab {}'.format(lab))
                elif 'OK\n    \x1b[1;31m[ERROR]\x1b[0m Unauthorized, please login to continue\n ' in out:
                    logging.error(Fore.RED + 'Authenticate with Instruqt: instruqt auth login')
                elif 'Everything up-to-date\n' in out:
                    logging.info(Fore.GREEN + 'Lab {} is up to date'.format(lab))
                else:
                    logging.info(Fore.RED + 'Build failed: {}'.format(result.communicate()[0]))
            except Exception as exc:
                logging.info(Fore.RED + 'Can\'t push {}'.format(lab))
        else:
            logging.info('No VM image changes to push in lab {}.'.format(lab))
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

def ArbitraryPush(config):
    logger.info('Performing Arbitrary Push')
    # Push labs listed in "labs:[]". This method does not check for lab name changes. 
    updates = update_image_name.UpdateImageName(config)
    instruqtpushcommand = updates.config.get(
        'instruqt', 'instruqt_push_command')
    
    labs = updates.getlabs()
    for lab in labs:
        try:
            result = subprocess.Popen(instruqtpushcommand, shell=True, cwd=updates.labrootdir +
                                        '/'+lab, stdout=subprocess.PIPE, universal_newlines=True)
            out = result.communicate()[0]
            if 'OK\n==> Building track' in out:
                logging.info(
                    Fore.GREEN + 'Build result successful for lab {}'.format(lab))
            elif 'OK\n    \x1b[1;31m[ERROR]\x1b[0m Unauthorized, please login to continue\n ' in out:
                logging.error(
                    Fore.RED + 'Authenticate with Instruqt: instruqt auth login')
            elif 'Everything up-to-date\n' in out:
                logging.info(
                    Fore.GREEN + 'Lab - {} - is up to date'.format(lab))
            else:
                logging.info(
                    Fore.RED + 'Build failed: {}'.format(result.communicate()[0]))
        except Exception as exc:
            logging.info(Fore.RED + 'Can\'t push {}'.format(lab))
    return
