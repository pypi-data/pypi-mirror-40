============
Jira To Vsts
============

Synchronize Jira issues to VSTS (Azure Devops)

Usage
-----

Commands::

    Usage: jira2vsts [OPTIONS]

      CLI for Jira2Vsts

    Options:
      -v, --validate
      -l, --logfile FILE    Path to logfile  [required]
      -c, --config FILE     Path to the configuration file  [required]
      --loop-every INTEGER  Loop every X minutes
      --help                Show this message and exit.



Launch synchronization::

    jira2vsts -c config.yml -l /var/log/jira2vsts.log

Check validy of the configuration file and for authentification information::

    jira2vsts.py -c config.yml -l /var/log/jira2vsts.log --validate

Launch the synchronization every 60 minutes::

    jira2vsts.py -c config.yml -l /var/log/jira2vsts.log --loop-every=60

Installation
------------

Simply run ::

    pip install jira2vsts

Format of config file  
---------------------

Configuration file::

    jira:  
      password: {JIRA_PASSWORD}  
      url: {JIRA_FULL_URL}  
      username: {JIRA_USERNAME}  
    projects:  
      {CODE_JIRA_PROJECT}:  
        active: {TRUE_OR_FALSE}
        name: {NAME_OF_VSTS_PROJECT}  
        type: {VSTS_DEFAULT_TYPE}  
        states:
          - {LIST_VSTS_STATES_IN_ORDER} 
        default_values:
            {VSTS_FIELD}: {VSTS_VALUE}
    states:
      {JIRA_STATE}: {VSTS_STATE}  
    vsts:  
      access_token: {VSTS_ACCESS_TOKEN}  
      url: {VSTS_FULL_URL}

Todos
-----
  
- Add default assignee
- Add default followers
- Add attachments