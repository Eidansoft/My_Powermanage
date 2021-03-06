# A Visonic PowerManage personal solution #

The Visonic PowerMaster alarm is a home/office alarm. The main device connects to a centralized events servers.

The main ports used are 5001 for events notification and the 8080 for events and video images.

The information regarding ports has been found [here](http://www.smarttech.ro/files/powermanageprofessional_pre-installation_requireme.pdf).

Some more info on [Voksenlia](http://voksenlia.net/powerlink/) and on [securitybydefault](http://www.securitybydefault.com/2012/01/alarma-visonic-powermax-pro-un-estudio.html).

A guy has written a couple scripts to mimmic the visonic server in order to avoid it. The documentation is [available for download](https://www.dropbox.com/s/s2zkjko0ihhfvcm/Configuring%20an%20in-house%20notification%20service%20for%20Visonic%20PowerLink2.pdf?dl=0).

# Main idea
I pretend to build a docker container to run a web server to act as the original centralised event server, in order to avoid use one belonging to a company. This way I can maintain my own infrastructure to get the notifications as I want and without costs.

# Use #
To instantiate the server and listen your Powermaster:

```docker run -ti -p 8080:8080 --rm eidansoft/powermanage```

# Use of the old code #
To create the docker image with the old PHP code:

```docker build powermanage_simply_mock/ -t oldpowermanage```

To launch the service:

```docker run -ti -p 8080:80 --rm oldpowermanage```
