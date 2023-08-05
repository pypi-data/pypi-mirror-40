======
macapi
======

|Python 27|

**What is macapi?** macapi is a tool used to easily access MongoDB Atlas by leverating its resful api. It's primarily used to easilty adminsiter Atlas clusters and groups.



.. figure:: https://github.com/dmcna005/macapi/blob/master/macapi.png
   :alt: macapi
--------------------------------------------------

Installation
------------

.. code-block:: console

    $ pip install macapi

**The toolkit constists of the following tools**:


``alerts``
~~~~~~~~~~

Used to get and create alert configuration for a single group.

.. code-block:: console

    $ alerts -h
    
    usage: alerts [-h] [-G] [-U] [-C] [-D] [-f FILE] -g GROUP_ID -u API_USER -k
              API_KEY
              
    optional arguments:
     -h, --help            show this help message and exit
     -G, --get             get a group alert and monitoring configuration
     -U, --update          update current alerts configuration
     -C, --create          replace current alerts confifuration
     -D, --delete          delte a single alert
     -f FILE, --file FILE  write file to current directory unless absolute path
                           is provided
     -g GROUP_ID, --group_id GROUP_ID
     -u API_USER, --api_user API_USER
     -k API_KEY, --api_key API_KEY

  
``cluster``
~~~~~~~~~~~

Used to create and modify cluster configurations for a given group.

.. code-block:: console

    $ cluster -h
    
    usage: cluster [-h] [-G] [-C] [-f FILE] -n NAME -g GROUP_ID -u API_USER -k
               API_KEY [-D] [--resize] [--size SIZE] [--nodes NODES]
               [--shards SHARDS]
               
    optional arguments:

  -h, --help            show this help message and exit
  -G, --get             get's the currnet group cluster configuration
  -C, --create          creates a new cluster
  -f FILE, --file FILE  write file to current directy or path
  -n NAME, --name NAME  the name of the cluster
  -g GROUP_ID, --group_id GROUP_ID
                        id of the group that you are trying to make the
                        changes for
  -u API_USER, --api_user API_USER
                        the email address you use to login
  -k API_KEY, --api_key API_KEY
                        Your Atlas api key
  -D, --delete          deletes a cluster from a project
  --resize              resizes an instace
  --size SIZE           size of an instance in ['M10',...,'M60']
  --nodes NODES         number of nodes per shard or replicaSet
  --shards SHARDS       number of replicaSets to deploy
      
   
``ip_whitelist``
~~~~~~~~~~~~~~~~

 Used to create, delete, update and getip whitelist information for a single group in Atlas.
 
 .. code-block:: console
      
      $ ipwhitelist -h
         usage: ipwhitelist [-h] [-G] [-C] [-D] [-f FILE] -g GROUP_ID -u API_USER -k
                   API_KEY

      optional arguments:
        -h, --help            show this help message and exit
        -G, --get             get's the currnet group IP Whitelist
        -C, --create          replace current alerts confifuration

        -D, --delete          delte a single alert
        -f FILE, --file FILE  write file to current directory unless absolute path
                              is provided
        -g GROUP_ID, --group_id GROUP_ID
                              id of the group that you are trying to make the
                              changes for
        -u API_USER, --api_user API_USER
                              the email address you use to login
        -k API_KEY, --api_key API_KEY
                              Your Atlas api key
      




.. |Python 27| image:: https://img.shields.io/badge/Python-2.7-brightgreen.svg?style=flat
   :target: http://python.org
