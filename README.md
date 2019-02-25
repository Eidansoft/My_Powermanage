The Visonic PowerMaster 10 connects to a centralized events servers.

The main ports used are 5001 for events notification and the 8080 for events and video images.

The information regarding ports has been found [here](http://www.smarttech.ro/files/powermanageprofessional_pre-installation_requireme.pdf).
Some more info on [Voksenlia](http://voksenlia.net/powerlink/) and on [securitybydefault](http://www.securitybydefault.com/2012/01/alarma-visonic-powermax-pro-un-estudio.html).
A guy has written a couple scripts to mimmic the visonic server in order to avoid it. The documentation is [available for download](https://www.dropbox.com/s/s2zkjko0ihhfvcm/Configuring%20an%20in-house%20notification%20service%20for%20Visonic%20PowerLink2.pdf?dl=0).

To test all readings I have lauched a docker container with the previously commented scripts.
