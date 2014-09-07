Beardo Control
==============

![Docker](http://www.linux.com/news/galleries/image/docker?format=image&thumbnail=small)
![Appengine](http://bkarak.wizhut.com/blog/wp-content/uploads/2012/01/app_engine-64.png)
![Python](http://blog.magiksys.net/sites/default/files/pictures/python-logo-64.png)

This repository provides the control server for a beardo installation. A
beardo-control install lives at the centre of an installation, providing a
single point of control/information.


***

This server uses [Docker][docker] to provide a standard development
environment for all developers on the project, this is the preferred method of
installation/development. No support is provided for non-docker setups.


## Features (for now)
***

- Gitlab sync
    - user accounts
    - SSH keys
    - projects (with webhooks, but not project-users yet)
- Accepts webhooks on push to any attached git repo, enqueing a build job.
- Queue API allowing build tasks to be leased/marked complete by a build worker.
- Basic dashboard
    - User management
    - Project management
    - View build logs


## Before you start
***

- You must have a working Gitlab server set up (preferably dedicated to beardo
  use, as beardo will remove projects/users without confirmation).
- You must have a valid `secrets.py` file in the `app/` folder. You can copy
  the `secrets.example.py` file to get started.


## Using the server with Docker
***

The easiest way to use this skeleton is with [Docker][docker]. With Docker
installed, running your application should be as simple as:

    $ make run

To run your application's tests, use the command:

    $ make test

Visit the running application [http://localhost:8080](http://localhost:8080)

Check out the `Makefile` in the repository root for all available commands.


### Installing Libraries
***

See the [Third party libraries][thrdprty] page for libraries that are already
included in the SDK.  To include SDK libraries, add them in your `app.yaml`
file. Other than libraries included in the SDK, only pure python libraries may
be added to an App Engine project.

Any third-party Python modules added to the `app/vendor/` directory will be
added to Python's `sys.path` at runtime.


## Licensing
***

See [LICENSE](LICENSE)


[docker]: https://docker.io  "Docker"
[thrdprty]: https://developers.google.com/appengine/docs/python/tools/libraries27  "Appengine third-party libraries"
[gae-secure-scaffold-python]: https://github.com/google/gae-secure-scaffold-python  "GAE Secure Scaffold Python"
