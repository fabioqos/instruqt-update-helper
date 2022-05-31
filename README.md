# Instruqt Update Helper

This script performs 2 functions.

* Update the vm in each lab.
* Push the updated lab to instruqt.

The update operation will log the update in the instruqt.log file and make backups of the config file in backup/. If a mistake is made, you can also revert all changes through git.

## Instructions

### Activate the venv

This command will vary depending on the tool used. See `Installation` below for more details.

```bash
source .venv/bin/activate
```

### Run the script on the cli

For help, run `python instruqt_update.py -h`.

```ascii
usage: instruqt_update.py [-h] [--DEBUG] [--config CONFIG_FILE] [--check] [--modify] [--push] [--list] [--pull]

options:
  -h, --help            show this help message and exit
  --DEBUG, -d           Set logging level to DEBUG.
  --config CONFIG_FILE, -c CONFIG_FILE
                        Specify the config file. The default is config/instruqt.conf
  --check, -k           Specify whether to just run a check for whether images require updating. The script will check the image field in the lab config.yml to see whether it matches the newvm key in the instruqt.conf file.
  --modify, -m          Modify the config.yml files so that the old image (specified in the config.yml) is replaced with the new image.
  --push, -p            Push the modified labs to Instruqt, initiating a lab rebuild.
  --list, -l            List labs found in specified lab directory.
  --pull, -x            Pull all labs found in the instruqt root dir .
```

By default, the logging will be set to verbose. Backups of the config.yml for each lab are created in the backup directory (specified in the config/instruqt.conf file).

This script can run in a non-destructive _check_ mode which compares the image key in the config.yml to the newvm key specified in the config/instruqt.conf file. To run a non-destructive check, run the following on the cli.

```bash
python instruqt_update.py --check
```

This will output the labs that are not up to date.

## Installation

Clone this repo. In this example, we're running `git clone` from `/home/myee/instruqt_dev/`.

```bash
git clone https://github.com/myee111/instruqt-update-helper.git /home/myee/instruqt_dev/
```

This script uses a venv.

```bash
virtualenv -p python3 /home/myee/instruqt_dev/instruqt-update-helper/
```

Activate the venv.

```bash
source /home/myee/instruqt_dev/instruqt-update-helper/bin/activate
```

Install the required python modules with pip.

```bash
pip install -r /home/myee/instruqt_dev/instruqt-update-helper/requirements.txt
```

## Configuration

### Configuration Overview

1. Configure the instruqt root directory. The instruqt root directory contains all the instruqt labs you want to update.
2. Add the labs you wish to have this script modify.
3. Configure the old image name `oldimage`. This is the name of the image you want to replace.
4. Configure the new image name `newimage`. This is the name of the latest image you want your labs to use.

### 1. Configure the instruqt root directory

Inside the `config/config.yml` file under the `instruqt` section, there is a key `instruqt_root_dir`. Set this to the location in your filesystem where you are storing your instruqt labs.

```ini
instruqt_root_dir = /home/myee/instruqt_dev/instruqt
```

### 2. Add the labs you wish to have this script modify

In the `instruqt` section of `config.yml`, add the labs you wish to modify. This script was designed to force the user to explictly specify the labs to change in order to prevent accidental overwrites.

```ini
labs: [
  "test",
  "unixisms",
  "openscap"
  ]
```

### 3. Configure the old image name

This script will search for a specified `oldimage` name before replacing it with the `newimage` name. This key can be found under the `oldimage` section.

```ini
image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1
```

### 4. Configure the new image name

The `newimage` key can be found under the `newimage` section.

```ini
[newimage]
image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
```

The full configuration file looks like this.

```ini
[general]
# Set the logging level to debug.
debug = True

# Log file name.
log = instruqt.log

# Location to store the backups.
backupdir = backup

[instruqt]
# instruqt_root_dir specifies the root directory containing all the instruqt labs.
instruqt_root_dir = /home/myee/instruqt_dev/instruqt

# Instruqt commands to push and pull labs.
instruqt_push_command = instruqt track push
instruqt_pull_command = instruqt track pull --force

# Name of the file containing instruqt lab configuration.
config_file_name = config.yml

# Enter the labs you wish to operate on.
# Example:
#
# labs: [
#   "test",
#   "unixisms",
#   "openscap"
#   ]

labs: [
  "test",
  "unixisms",
  "openscap"
  ]

# The oldimage is the name of the image you want the script to replace.
[oldimage]
image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1

# The newimage is the name of the image you wish to update all the labs to.
[newimage]
image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
