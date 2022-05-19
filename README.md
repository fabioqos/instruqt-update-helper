# Instruqt Update Helper

This script performs 2 functions.

* Update the vm in each lab.
* Push the updated lab to instruqt.

## Instructions

### Run the following on the cli.

```bash
python Instruqtupdate.py
```

## Installation

This script uses a venv.

## Configuration

The configuration file looks like this.

```ini
[general]
debug = True
log = instruqt.log

[instruqt]
rhel_labs_root_dir = /mnt/c/Users/myee/github/instruqt/
vm_image = 'image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1'
labs: [
  "appstream-manage", 
  "buildah", 
  "containerize-app"
  ]
```
