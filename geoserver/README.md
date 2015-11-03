Provisioning the Geoserver
==========================

Provisioning a brand new geoserver.
-----------------------------------
1.  Set up ssh keys and ensure the provisioning user account can ssh into the new machine.
2.  Remove password request for the provisioning user account in `/etc/sudoers`.
3   Install [docker](https://docs.docker.com/installation/ubuntulinux/) on the machine if it's not installed.
4.  Clone the repository into your dev box by running `git clone https://github.com/unicefuganda/necoc.git`
5.  Change current working directory to `<PROJECT_ROOT>/geoserver/provision`
6.  Provision the geoserver by running `ansible-playbook -i production provision.yaml --extra-vars "ansible_ssh_user=<YOUR_SSH_USERNAME>"`  

> Note: Ansible deployment scripts have been tested on Debian Linux distributions.

Configuring the Geoserver
-------------------------
1.  Access the provisioned geoserver via `http://<YOUR_PUBLIC_IP>:8080/geoserver/web/`
2.  Login with your geoserver credentials
3.  Click `Work Spaces` on the left nav and then click `Add new workspace`.
4.  Click `Stores` on the left nav and then click `Add new store`.
5.  Select `Shape file` from the Vector Data Sources and enter the information as shown below.
6.  Click Publish Action
7.  Under the `Coordinate Reference System` form section change the Declared SRS to `EPSG:102113` by searching `WGS84`
8.  Under the `Bounding Boxes` form section click `Compute from data` and `Compute from native bounds`
9   Click Save.