# Instruqt Update Helper

This script performs 2 functions.

* Update the vm in each lab.
* Push the updated lab to instruqt.

The update operation will log the update in the instruqt.log file and make backups of the config file in backup/. If a mistake is made, you can also revert all changes through git.

## Instructions

### Activate the venv

```bash
source .venv/bin/activate
```

### Run the script on the cli

```bash
python Instruqtupdate.py
```

By default, the logging will be set to verbose and the changes will be destructive. Backups of the config.yml for each lab are created in the backup directory (specified in the config/instruqt.conf file).

This script can run in a non-destructive _check_ mode which compares the image key in the config.yml to the newvm key specified in the config/instruqt.conf file. To run a non-destructive check, run the following on the cli.

```bash
python Instruqtupdate.py --check
```

This will output the labs that are not up to date.

## Installation

This script uses a venv.
<stuff about the requirements.txt>

## Configuration

The configuration file looks like this.

```ini
[general]
debug = True
log = instruqt.log
backupdir = backup

[instruqt]
instruqt_push_command = "instruqt track push"
rhel_labs_root_dir = /home/myee/test/instruqt
config_file_name = config.yml
labs: [
  "appstream-manage", 
  "buildah", 
  "containerize-app",
  "test"
  ]

[oldimage]
image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1

[newimage]
image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
```
