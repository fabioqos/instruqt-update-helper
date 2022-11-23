# Instruqt Update Helper

This script performs 2 functions.

* Update the vm in each lab.
* Push the updated lab to instruqt.

The update operation will log the update in the instruqt.log file and make backups of the config file in backup/. If a mistake is made, you can also revert all changes through git.

## Instructions

### Installation

Clone this repo. In this example, we're running `git clone` from `/home/myee/instruqt_dev/`.

```bash
git clone https://github.com/myee111/instruqt-update-helper.git /home/myee/instruqt_dev/
```

This script uses a venv.

```bash
python3 -m venv /Users/myee/repos/instruqt-update-helper/venv
```

Activate the venv.

```bash
source /Users/myee/repos/instruqt-update-helper/venv/bin/activate
```

Install the required python modules with pip.

```bash
pip3 install -r /home/myee/instruqt_dev/instruqt-update-helper/requirements.txt
```

### Configuration

#### Configuration Overview

1. Configure the instruqt root directory. The instruqt root directory contains all the instruqt labs you want to update.
2. Add the labs you wish to have this script modify.
3. Configure the old image name `oldimage`. This is the name of the image you want to replace.
4. Configure the new image name `newimage`. This is the name of the latest image you want your labs to use.

#### 1. Configure the instruqt root directory

Inside the `config/config.yml` file under the `instruqt` section, there is a key `instruqt_root_dir`. Set this to the location in your filesystem where you are storing your instruqt labs.

```ini
instruqt_root_dir = /home/myee/instruqt_dev/instruqt
```

#### 2. Add the labs you wish to have this script modify

In the `instruqt` section of `config.yml`, add the labs you wish to modify. This script was designed to force the user to explictly specify the labs to change in order to prevent accidental overwrites.

```ini
labs: [
  "test",
  "unixisms",
  "openscap"
  ]
```

#### 3. Configure the old image name

This script will search for a specified `oldimage` name before replacing it with the `newimage` name. This key can be found under the `oldimage` section.

```ini
image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1
```

#### 4. Configure the new image name

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
```

### Running instruqt_update.py

#### Authenticate with Instruqt

```bash
instruqt auth login
```

#### Activate the venv

This command will vary depending on the tool used. See `Installation` above for more details.

```bash
source .venv/bin/activate
```

#### Run the script on the cli

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

```bash
(.venv) [myee@DESKTOP-L2GNENL instruqt-update-helper]$ python instruqt_update.py -k
2022-05-31 07:54:49,623 INFO Starting.
2022-05-31 07:54:49,624 DEBUG Labs: test unixisms openscap
2022-05-31 07:54:49,624 DEBUG Directory list: ['service-admin', 'sql-server-cstore', 'installing-software-yum', 'sql-server-session-recording', 'customize-crypto-policy', '.gitignore', 'kpatch-apply', 'edge-management', 'sql-server-ansible', 'README.md', 'openscap', 'ebpf-tracing', 'webconsole-perf', 'insights-workshop', 'maintenance', '.git', 'podman-deploy', 'rhel-system-roles', 'webconsole-software', 'pcp-intro', 'file-access-policy', 'pcp-flamegraphs', 'sql-server-ubi', 'rhel-session-recording-tlog', 'session-recording-tlog', 'containerize-app', 'appstream-manage', 'sandbox', 'helpful-commands', 'user-basics', 'test', 'file-permissions', 'crypto-policy', 'buildah', 'sql-server-crypto-policy', 'unixisms', 'selinux-containers', 'satellite-basics', 'sql-server-insights']
2022-05-31 07:54:49,624 DEBUG Lab root directory: /home/myee/instruqt_dev/instruqt
2022-05-31 07:54:49,624 DEBUG Old VM image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1
2022-05-31 07:54:49,625 DEBUG New VM image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
2022-05-31 07:54:49,625 DEBUG Labs ['test', 'unixisms', 'openscap'] found.
2022-05-31 07:54:49,628 INFO Lab - test - contains a vm - rhel - that is using neither the old or current image - projects/tmm-instruqt-11-26-2021/global/images/satellite-2-15-22.
2022-05-31 07:54:49,628 INFO Lab - test - contains a vm - rhel2 - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:54:49,628 INFO Lab - test - contains a vm - rhel3 - that is using the old image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1.
2022-05-31 07:54:49,629 INFO Lab - unixisms - contains a vm - rhel - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:54:49,631 INFO Lab - openscap - contains a vm - rhel - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:54:49,631 DEBUG Labs to update {'test': ['rhel3'], 'unixisms': [], 'openscap': []}.
2022-05-31 07:54:49,632 INFO Completed.
```

Next, modify the config file.

```bash
python instruqt_update --modify
```

```bash
(.venv) [myee@DESKTOP-L2GNENL instruqt-update-helper]$ python instruqt_update.py --modify
2022-05-31 07:56:24,564 INFO Starting.
2022-05-31 07:56:24,565 DEBUG Labs: test unixisms openscap
2022-05-31 07:56:24,565 DEBUG Directory list: ['service-admin', 'sql-server-cstore', 'installing-software-yum', 'sql-server-session-recording', 'customize-crypto-policy', '.gitignore', 'kpatch-apply', 'edge-management', 'sql-server-ansible', 'README.md', 'openscap', 'ebpf-tracing', 'webconsole-perf', 'insights-workshop', 'maintenance', '.git', 'podman-deploy', 'rhel-system-roles', 'webconsole-software', 'pcp-intro', 'file-access-policy', 'pcp-flamegraphs', 'sql-server-ubi', 'rhel-session-recording-tlog', 'session-recording-tlog', 'containerize-app', 'appstream-manage', 'sandbox', 'helpful-commands', 'user-basics', 'test', 'file-permissions', 'crypto-policy', 'buildah', 'sql-server-crypto-policy', 'unixisms', 'selinux-containers', 'satellite-basics', 'sql-server-insights']
2022-05-31 07:56:24,565 DEBUG Lab root directory: /home/myee/instruqt_dev/instruqt
2022-05-31 07:56:24,565 DEBUG Old VM image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1
2022-05-31 07:56:24,565 DEBUG New VM image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
2022-05-31 07:56:24,566 DEBUG Labs ['test', 'unixisms', 'openscap'] found.
2022-05-31 07:56:24,568 INFO Lab - test - contains a vm - rhel - that is using neither the old or current image - projects/tmm-instruqt-11-26-2021/global/images/satellite-2-15-22.
2022-05-31 07:56:24,568 INFO Lab - test - contains a vm - rhel2 - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:56:24,568 INFO Lab - test - contains a vm - rhel3 - that is using the old image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1.
2022-05-31 07:56:24,569 INFO Lab - unixisms - contains a vm - rhel - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:56:24,570 INFO Lab - openscap - contains a vm - rhel - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:56:24,570 DEBUG Labs to update {'test': ['rhel3'], 'unixisms': [], 'openscap': []}.
2022-05-31 07:56:24,570 INFO Updating image names.
2022-05-31 07:56:24,570 DEBUG New backup dir backup/20220531-075624 created.
2022-05-31 07:56:24,572 DEBUG Config YML: {'version': '3', 'virtualmachines': [{'environment': {'TERM': 'xterm'}, 'image': 'projects/tmm-instruqt-11-26-2021/global/images/satellite-2-15-22', 'machine_type': 'n1-highmem-4', 'name': 'rhel', 'shell': '/bin/bash'}, {'environment': {'TERM': 'xterm'}, 'image': 'projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1', 'machine_type': 'n1-highmem-2', 'name': 'rhel2', 'shell': '/bin/bash'}, {'environment': {'TERM': 'xterm'}, 'image': 'projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1', 'machine_type': 'n1-highmem-2', 'name': 'rhel3', 'shell': '/bin/bash'}]}
2022-05-31 07:56:24,573 DEBUG New Config YML: version: '3'
virtualmachines:
- environment:
    TERM: xterm
  image: projects/tmm-instruqt-11-26-2021/global/images/satellite-2-15-22
  machine_type: n1-highmem-4
  name: rhel
  shell: /bin/bash
- environment:
    TERM: xterm
  image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
  machine_type: n1-highmem-2
  name: rhel2
  shell: /bin/bash
- environment:
    TERM: xterm
  image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
  machine_type: n1-highmem-2
  name: rhel3
  shell: /bin/bash

2022-05-31 07:56:24,573 DEBUG Backup created at backup/20220531-075624/test_config.yml
2022-05-31 07:56:24,574 DEBUG Config for lab test written.
2022-05-31 07:56:24,575 DEBUG Config YML: {'version': '3', 'virtualmachines': [{'environment': {'TERM': 'xterm'}, 'image': 'projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1', 'machine_type': 'n1-standard-1', 'name': 'rhel', 'shell': '/bin/bash'}]}
2022-05-31 07:56:24,575 DEBUG New Config YML: version: '3'
virtualmachines:
- environment:
    TERM: xterm
  image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
  machine_type: n1-standard-1
  name: rhel
  shell: /bin/bash

2022-05-31 07:56:24,576 DEBUG Backup created at backup/20220531-075624/unixisms_config.yml
2022-05-31 07:56:24,576 DEBUG Config for lab unixisms written.
2022-05-31 07:56:24,577 DEBUG Config YML: {'version': '3', 'virtualmachines': [{'environment': {'TERM': 'xterm'}, 'image': 'projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1', 'machine_type': 'n1-standard-1', 'name': 'rhel', 'shell': '/bin/bash'}]}
2022-05-31 07:56:24,578 DEBUG New Config YML: version: '3'
virtualmachines:
- environment:
    TERM: xterm
  image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
  machine_type: n1-standard-1
  name: rhel
  shell: /bin/bash

2022-05-31 07:56:24,578 DEBUG Backup created at backup/20220531-075624/openscap_config.yml
2022-05-31 07:56:24,578 DEBUG Config for lab openscap written.
2022-05-31 07:56:24,578 INFO Completed.
```

Push the changes to instruqt.

```bash
python instruqt_update --push
```

```bash
(.venv) [myee@DESKTOP-L2GNENL instruqt-update-helper]$ python instruqt_update.py --push
2022-05-31 07:57:39,603 INFO Starting.
2022-05-31 07:57:39,603 INFO Pushing labs.
2022-05-31 07:57:39,603 DEBUG Labs: test unixisms openscap
2022-05-31 07:57:39,603 DEBUG Directory list: ['service-admin', 'sql-server-cstore', 'installing-software-yum', 'sql-server-session-recording', 'customize-crypto-policy', '.gitignore', 'kpatch-apply', 'edge-management', 'sql-server-ansible', 'README.md', 'openscap', 'ebpf-tracing', 'webconsole-perf', 'insights-workshop', 'maintenance', '.git', 'podman-deploy', 'rhel-system-roles', 'webconsole-software', 'pcp-intro', 'file-access-policy', 'pcp-flamegraphs', 'sql-server-ubi', 'rhel-session-recording-tlog', 'session-recording-tlog', 'containerize-app', 'appstream-manage', 'sandbox', 'helpful-commands', 'user-basics', 'test', 'file-permissions', 'crypto-policy', 'buildah', 'sql-server-crypto-policy', 'unixisms', 'selinux-containers', 'satellite-basics', 'sql-server-insights']
2022-05-31 07:57:39,603 DEBUG Lab root directory: /home/myee/instruqt_dev/instruqt
2022-05-31 07:57:39,603 DEBUG Old VM image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-5-03-02-2022-1
2022-05-31 07:57:39,603 DEBUG New VM image: projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1
2022-05-31 07:57:39,604 DEBUG Labs ['test', 'unixisms', 'openscap'] found.
2022-05-31 07:57:39,605 INFO Lab - test - contains a vm - rhel - that is using neither the old or current image - projects/tmm-instruqt-11-26-2021/global/images/satellite-2-15-22.
2022-05-31 07:57:39,606 INFO Lab - test - contains a vm - rhel2 - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:57:39,606 INFO Lab - test - contains a vm - rhel3 - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:57:39,607 INFO Lab - unixisms - contains a vm - rhel - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:57:39,607 INFO Lab - openscap - contains a vm - rhel - that is using the current image - projects/tmm-instruqt-11-26-2021/global/images/rhel-8-6-05-10-2022-1.
2022-05-31 07:57:39,607 DEBUG Labs to update {'test': [], 'unixisms': [], 'openscap': []}.
2022-05-31 07:57:54,714 INFO Push result: b"==> Loading track files...\n    OK\n==> Checking challenges\n    OK\n==> Checking tabs\n    OK\n==> Checking scripts\n    OK\n==> Checking for leftover *.remote files\n    OK\n==> Reading track definition\n    OK\n==> Checking deltas\n    OK\n==> Pushing track\n    OK\n==> Pushing assets\n    Everything up-to-date\n    OK\n==> Updating local track:\n    OK\n==> Building track 'rhel/test' (ID: jc35qjmmymau)\n    Track URL: https://play.instruqt.com/rhel/tracks/test\n    OK\n"
2022-05-31 07:57:55,791 INFO Push result: b'==> Loading track files...\n    OK\n==> Checking challenges\n    OK\n==> Checking tabs\n    OK\n==> Checking scripts\n    OK\n==> Checking for leftover *.remote files\n    OK\n==> Reading track definition\n    OK\n==> Checking deltas\n    Everything up-to-date\n    OK\n'
2022-05-31 07:57:57,151 INFO Push result: b'==> Loading track files...\n    OK\n==> Checking challenges\n    OK\n==> Checking tabs\n    OK\n==> Checking scripts\n    OK\n==> Checking for leftover *.remote files\n    OK\n==> Reading track definition\n    OK\n==> Checking deltas\n    Everything up-to-date\n    OK\n'
2022-05-31 07:57:57,151 INFO Completed.
```
