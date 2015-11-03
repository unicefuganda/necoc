Deployment
==========

Provision a brand new machine.
------------------------------
1.  Set up ssh keys and ensure the provisioning user account can ssh into the new machine.
2.  Remove password request for the provisioning user account in `/etc/sudoers`.
3   Install [docker](https://docs.docker.com/installation/ubuntulinux/) on the machine if it's not installed.
4.  Clone the repository into your dev box by running `git clone https://github.com/unicefuganda/necoc.git`
5.  Change current working directory to `<PROJECT_ROOT>/deployment/ansible`
6.  Provision the machine by running `ansible-playbook -i production provision.yaml --extra-vars "ansible_ssh_user=<YOUR_SSH_USERNAME>"` 
    (Ensure that ansible is installed on your dev box).
7.  Deploy the application for the first time by running `ansible-playbook -i production deploy.yaml --extra-vars "api_token=<RAPID_PRO_API_TOKEN> ansible_ssh_user=<YOUR_SSH_USERNAME> email_password=<EMAIL_PASSWORD> clean_db=True local=True load_data=True"` 

Deploy on a provisioned machine (existing server).
--------------------------------------------------
1.  On your dev box, change current working directory to `<PROJECT_ROOT>/deployment/ansible`
2.  Run `ansible-playbook -i production deploy.yaml --extra-vars "api_token=<RAPID_PRO_API_TOKEN> ansible_ssh_user=<YOUR_SSH_USERNAME> email_password=<EMAIL_PASSWORD> clean_db=False local=True load_data=False"`

> Note: Ansible deployment scripts have been tested on Debian Linux distributions.