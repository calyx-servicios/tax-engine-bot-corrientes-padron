[![License](https://img.shields.io/badge/Patagon%20IO%201.0-License-lightgrey)](https://patagon.io/licenses/patagon-io-1.0)[![License](https://img.shields.io/badge/Calyx%20Servicios%201.0-License-lightgrey)](https://patagon.io/licenses/patagon-io-1.0)
# Corrientes Bot

Bot de descarga padron corrientes percepciones

### Bot Architecture

    .
    ├── app/                        # Bot Application Folder
    |    ├── __init__.py            
    |    ├── bot.py                 # main Bot script
    |    ├── database.py            # database module
    |    ├── main.py                 
    |    ├── pandas_job.py          # pandas job module
    |    ├── selenium_job.py        # selenium job module
    |    └── test.ipynb             # test notebook for Jupyter Lab
    ├── .env                        # Env vars only for local (not on git)
    ├── bootstrap.sh                # custom boostrap script
    ├── Dockerfile                  # Custom Bot Dockerfile
    └── requirements.txt            # Python requirements for Docker
    
#### Build Bot
```bash
$docker build -t corrientes.bot .
```

#### Run Bot


* notes:
.env environment file

Create it with this variables. (Update cuit and password)

```bash
➜  tax-engine-bot-corrientes-padron git:(fix/BOT-001_db_setup) ✗ cat .env
CUIT=20123456780
PASSWORD=password
SHELL=/bin/bash
PG_HOST=db
PG_PORT=5432
PG_DB=api
PG_USER=api
PG_PASSWORD=api
RETRO=1
COMMAND=init%  
```

### Container Run Notes 
Ports exposure:
-p <your_local_port>:<docker_container_port>

- -p 8889:8888 expose Jupyter Lab port at 8888 into 8889 at your local, access at http://127.0.0.1:8889

Network:
The network parameter is important to reach the docker-compose default network of the project.

- -p 3003:3003 expose debugpy port to use it with Vs Code. debugger port.


Memory limit:
-m 512m  
It will be the assigned memory in K8s, so it is important to code it with this limit

```bash
$docker run -it -p 8889:8888 -m 512m --network tax-engine-api_default --env-file .env --rm -v ${PWD}\downloads:/code/downloads corrientes.bot /bin/bash
```

Inside the container run the jupyter lab service to test and develop

#### Run Jupyter Lab
```bash
$jupyter lab --allow-root --no-browser --ip=0.0.0.0 --ServerApp.allow_password_change=False &
```

#### Run with Debugger

```bash
$docker run -it -p 3003:3003 --network tax-engine-api_default --env-file .env --rm patagon.bot /bin/bash 
```

Then inside the container run the application with debugpy
```bash
$python -m debugpy --listen 0.0.0.0:3003 main.py
```

#### Development requirements

We use pre-commit to control the quality of the code before pushing it to our repository

Install the following tools
- (pre-commit)[https://pre-commit.com]
- (black)[https://pypi.org/project/black/]
- (pylint)[https://pylint.pycqa.org/en/latest/]
- (isort)[https://pycqa.github.io/isort/]

run pre-commit install 

```bash
➜  tax-engine-bot-corrientes-padron git:(fix/BOT-001_db_setup) pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

Everytime you do a commit, the quality controls will run in your local
You won't be able to commit code unless all the test are passed:

```bash
➜  tax-engine-bot-corrientes-padron git:(fix/BOT-001_db_setup) ✗ git commit --amend
seed isort known_third_party.............................................Passed
isort................................................(no files to check)Skipped
black................................................(no files to check)Skipped
- hook id: black
flake8 only __init__.py..............................(no files to check)Skipped
flake8 except __init__.py............................(no files to check)Skipped
pylint...............................................(no files to check)Skipped
- hook id: pylint
Lint Dockerfiles.....................................(no files to check)Skipped
```


### Conventions for GIT commits and branches:


Common CI/CD naming requirements for commit/branch/PR:
Branch:  ^(feature|fix|docs|style|refactor|test|chore|release)/(\w*)-[0-9].*$ , e.g. feature/BACK-666-short-desc
PR/Commit example: BACK-666 (Service) short description

It is very important to start a commit message from the issue number (Jira key). 

Git commits and the commit messages are longer-lived than both JIRA tickets and Pull-Requests. 
They are also available in-context (git blame/praise) when you are doing actual development. 
This means that they are a good - and necessary - place to capture intended behaviour of the change introduced by the commit. There are many good resources on commit message guidelines:
http:////chris.beams.io/posts/git-commit/
http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html


- Structure
Many tools that show git logs depend on commit messages following a particular structure:
Separate subject from body with a blank line
Limit the subject line to 70 characters
If applicable, start subject with Jira ticket number
Capitalize the subject line
Do not end the subject line with a period
Use the imperative (i.e. commanding) mood in the subject, e.g. "BACK-12345 Fix currency validation errors" or "Allow user 
to have more than 2 names". To check your subject virtually add "This commit will " as prefix to subject line - correct 
sentence should be as result. 
Wrap the body at 80 characters per line
- Content 
Have your commit messages be about WHY you changed the code, not about HOW you did it. Point out things that may 
not be obvious to the reader (or even better, document that inside code).
Rewrite history 
- Squash 
squash commits in order to get the commit count per PR to a manageable size - think about the timeline in the 
commit messages. Ideally, each commit (when it is no longer work in progress) is a self-contained changeset. 

```bash
➜  tax-engine-bot-corrientes-padron git:(fix/BOT-001_db_setup) ✗ git log
commit 16359af0c14a1caad8b55fdb07a8b57687628c24 (HEAD -> fix/BOT-001_db_setup)
Author: Agustin Wisky <agustinwisky@gmail.com>
Date:   Tue Jul 26 19:20:27 2022 -0300

    BOT-001 fix (App) Memory usage produced OOKilled

commit f111069b3b6777048c8bf4dae11321e07ad0d8f1
Author: Agustin Wisky <agustinwisky@gmail.com>
Date:   Mon Jul 25 08:10:58 2022 -0300

    BOT-001 fix (App) DB setup

commit eeb556ba09521cef90fd30521f74cfbc25a19f02
Author: Agustin Wisky <agustinwisky@gmail.com>
Date:   Sun Jul 24 21:38:29 2022 -0300

    BOT-001 feature (App) initial setup
```


Copyright © 2022, Patagon IO
http://patagon.io/ 
All rights reserved. 
