Sirius CALDAV
=============
This project is plugin for https://radicale.org/.

With this plugin you can connect to CVUT Sirius API using CALDAV protocol. This allows you to edit or remove already existing events in sirius.

Documentation
------------------
https://radicale-sirius-plugin.readthedocs.io/en/latest/

GitHub
------------------
https://github.com/bezstpav/radicale-sirius-plugin

Pypi
------------------
??????


Supported Features
------------------

* Show Personal Timetable
* Change Summary
* Change Location
* Change Time
* Change URL
* Change Attendace (transp)
* Remove Events

Data Source
------------------
This plugin uses Sirius ical export to load data into radicale. Calendar events are cached in memory for faster access.

Authorization
------------------
Due to internal limitation of application Local Sirus token and CVUT username in format "{username}|{token}" is passed to username login.

Sirius Token can be found in URL link for ical export on timetable website::

    https://sirius.fit.cvut.cz/api/v1/people/{username}/events.ical?access_token={token}

Example::

    https://sirius.fit.cvut.cz/api/v1/people/pepazdepa/events.ical?access_token=xxxxxxx-7dfe-40b5-xxxx-43c82c858fb1

    CVUT username -> pepazdpapa
    Sirius Token -> xxxxxxx-7dfe-40b5-xxxx-43c82c858fb1

    Radicale Username -> pepazdpapa|xxxxxxx-7dfe-40b5-xxxx-43c82c858fb1
    Radicale Password -> {anything}
    
Instalation
------------------
    
    pip install radicale-sirius-plugin

Configuartion
------------------

It is needed to set correct types plugins (auth and storage). 

For configuration is posible to use radicale config file::

    [auth]
    type = radicale_sirius_plugin.auth
    cache_expire = 600 (Optional set timelife of Credintial cache in sec )

    [storage]
    type = radicale_sirius_plugin.storage
    cache_expire = 3000 (Optional set timelife of Sirius Event cache in sec )

Plugin uses original multifilesystem for datastoring. For more information see https://radicale.org/.

Running
------------------

Example radicale.config::

    [auth]
    type = radicale_sirius_plugin.auth
    cache_expire = 600

    [storage]
    type = radicale_sirius_plugin.storage
    cache_expire = 3000
    filesystem_folder = ./radicale/collections

    [server]
    timeout = 300

Run::

    python3 -m radicale --config "radicale.conf"
