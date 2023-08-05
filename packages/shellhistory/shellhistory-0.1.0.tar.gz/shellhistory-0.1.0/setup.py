# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['shellhistory']

package_data = \
{'': ['*'],
 'shellhistory': ['static/css/*',
                  'static/js/*',
                  'templates/*',
                  'templates/admin/*']}

install_requires = \
['Flask-Admin>=1.5,<2.0',
 'flask>=1.0,<2.0',
 'python-dateutil>=2.7,<3.0',
 'sqlalchemy>=1.2,<2.0']

entry_points = \
{'console_scripts': ['shellhistory-location = shellhistory.cli:location']}

setup_kwargs = {
    'name': 'shellhistory',
    'version': '0.1.0',
    'description': ' Visualize your shell usage with Highcharts!',
    'long_description': '# Shell History\n[![pipeline status](https://gitlab.com/Pawamoy/shell-history/badges/master/pipeline.svg)](https://gitlab.com/Pawamoy/shell-history/commits/master)\n\nInspired by https://github.com/bamos/zsh-history-analysis.\n\nVisualize your usage of Bash/Zsh through a web app\nthanks to Flask and Highcharts.\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [How it looks](#how-it-looks)\n- [How it works](#how-it-works)\n- [History file format](#history-file-format)\n- [Chart ideas](#chart-ideas)\n- [License](#license)\n\n## Installation\nClone the repo with `git clone https://github.com/Pawamoy/shell-history`.\n\nRun `make install` or `./scripts/setup.sh` to install the dependencies in\nthe current directory.\n\n`shell-history` needs a lot of info to be able to display various charts.\nThe basic shell history is not enough. In order to generate the necessary\ninformation, you have to source the `shellhistory.sh` script, and activate\n`shell-history`.\n\nSo, at shell startup, in `.bashrc` or `.zshrc`, put the following:\n\n```bash\n# make sure nothing is prepended to PROMPT_COMMAND or precmd after this line\n. \'/path/to/shell-history/shellhistory.sh\'\nshellhistory enable\n```\n\n... and now use your shell normally!\n\nIf you want to stop `shell-history`, simply run `shellhistory disable`.\n\n## Usage\nLaunch the web app with `make run` or `./scripts/run.sh`.\nNow go to http://127.0.0.1:5000/ and enjoy!\n\nFor more convenience, you can put a script in your PATH, for example in\n`/usr/bin/`, with the following contents:\n\n```bash\n#!/usr/bin/env bash\n\nSHELLHISTORY_DIR=/path/to/shell-history  # update this line\nexport SHELLHISTORY_VENV=${SHELLHISTORY_DIR}/venv\nexport SHELLHISTORY_FILE=~/.shell_history/history\nexport SHELLHISTORY_DB=~/.shell_history/db\n\ncd ${SHELLHISTORY_DIR} || exit 1\n./scripts/run.sh\n```\n\nYou will need Internet connection since assets are not bundled.\n\n## How it looks\n![length chart](pictures/length.png)\n![markov chart](pictures/markov.png)\n![daily chart](pictures/daily.png)\n![type chart](pictures/type.png)\n\n## How it works\nIn order to append a line each time a command is entered, the `PROMPT_COMMAND`\nvariable and the `precmd` function are used, respectively for Bash and Zsh.\nThey allow us to execute arbitrary instructions just before command execution,\nor before the command prompt is displayed, meaning, just after the last command\nhas returned.\n\nThis is where we compute the start and stop time, return code, working\ndirectory and command type, and append the line into our history file.\nStart and stop time are obtained with `$(date \'+%s%N\')`, return code is passed\ndirectly with `$?`, working directory is obtained with `$PWD` and command\ntype with `$(type -t arg)` for Bash and `$(type -w arg)` for Zsh.\n\nValues for UUID, parents, hostname, and TTY are computed only once, when\n`shellhistory.sh` is sourced. Indeed they do not change during usage of the current\nshell process. Hostname and TTY are obtained through commands `$(hostname)` and\n`$(tty)`. UUID is generated with command `$(uuidgen)`. Also note that UUID\nis exported in subshells so we know which shell is a subprocess of another, and\nso we are able to group shell processes by "sessions", a session being an opened\nterminal (be it a tab, window, pane or else). Parents are obtained with a\nfunction that iteratively greps `ps` result with PIDs (see `shellhistory.sh`).\n\nValues for user, shell, and level are simply obtained through environment\nvariables: `$USER`, `$SHELL`, and `$SHLVL`.\n\nStart time is computed just before the entered command is run by the shell,\nthanks to a trap on the DEBUG signal. From Bash manual about `trap`:\n\n>If a sigspec is DEBUG, the command arg is executed before every simple command.\n\nThe last command is obtained with the command `fc`. It will feel like your\nhistory configuration is mimic\'d by the extended history. If the commands\nbeginning with a space are ignored, `shell-history` will notice it and will not\nappend these commands. Same for ignored duplicates. If you enter an empty line,\nor hit Control-C before enter, nothing will be appended either. The trick behind\nthis is to check the command number in the current history (see `shellhistory.sh`\nfor technical details). Note however that if you type the same command in an\nother terminal, it will still be appended, unless you manage to synchronize your\nhistory between terminals.\n\n## History file format\nFields saved along commands are start and stop timestamps, hostname, username,\nuuid (generated), tty, process\' parents, shell, shell level, command type,\nreturn code, and working directory (path), in the following format:\n`:start:stop:uuid:parents:host:user:tty:path:shell:level:type:code:command`.\n\n- multiline commands are prepended with a semi-colon `;` instead of a colon `:`,\n  starting at second line\n- start and stop timestamps are in microseconds since epoch\n- process\' parents and working directory are encoded in base64 to avoid\n  delimiter corruption\n\nExample (multiline command):\n\n```\n:1510588139930150:1510588139936608:40701d9b-1807-4a3e-994b-dde68692aa14:L2Jpbi9iYXNoCi91c3IvYmluL3B5dGhvbiAvdXNyL2Jpbi94LXRlcm1pbmFsLWVtdWxhdG9yCi91c3IvYmluL29wZW5ib3ggLS1zdGFydHVwIC91c3IvbGliL3g4Nl82NC1saW51eC1nbnUvb3BlbmJveC1hdXRvc3RhcnQgT1BFTkJPWApsaWdodGRtIC0tc2Vzc2lvbi1jaGlsZCAxMiAyMQovdXNyL3NiaW4vbGlnaHRkbQovc2Jpbi9pbml0Cg==:myhost:pawamoy:/dev/pts/1:L21lZGlhL3Bhd2Ftb3kvRGF0YS9naXQvc2hlbGxoaXN0Cg==:/bin/bash:1:builtin:0:echo \'a\n;b\n;c\' | wc -c\n```\n\n## Chart ideas\nYou can post your ideas in this issue: https://github.com/Pawamoy/shell-history/issues/9.\n\n## License\nSoftware licensed under the\n[ISC](https://www.isc.org/downloads/software-support-policy/isc-license/)\nlicense.\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'url': 'https://github.com/pawamoy/shell-history',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
