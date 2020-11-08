# Hands-on Ansible-06 : Using Roles
The purpose of this hands-on training is to give students knowledge of basic Ansible skills.

## Learning Outcomes

At the end of this hands-on training, students will be able to;

- Explain what is Ansible role
- Learn how to create, find and use a role.  

## Outline

- Part 1 - Install Ansible

- Part 2 - Using Ansible Roles

## Part 1 - Install Ansible


- Spin-up 3 Amazon Linux 2 instances and name them as:
    1. control node -->(SSH PORT 22)
    2. node1 ----> (SSH PORT 22, HTTP PORT 80)
    3. node2 ----> (SSH PORT 22, HTTP PORT 80)


- Connect to the control node via SSH and run the following commands.

```bash
sudo yum update -y
sudo amazon-linux-extras install ansible2
```

### Confirm Installation

- To confirm the successful installation of Ansible, run the following command.

```bash
$ ansible --version
```
Stdout:
```
ansible 2.9.12
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ec2-user/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.18 (default, Aug 27 2020, 21:22:52) [GCC 7.3.1 20180712 (Red Hat 7.3.1-9)]
```

### Configure Ansible on the Control Node

- Connect to the control node for building a basic inventory.

- Edit ```/etc/ansible/hosts``` file by appending the connection information of the remote systems to be managed.

- Along with the hands-on, public or private IPs can be used.

```bash
$ sudo su
$ cd /etc/ansible
$ ls
$ vim hosts
[webservers]
node1 ansible_host=<node1_ip> ansible_user=ec2-user
node2 ansible_host=<node2_ip> ansible_user=ec2-user

[all:vars]
ansible_ssh_private_key_file=/home/ec2-user/<pem file>
```


- Copy your pem file to the /etc/ansible/ directory. First, go to your pem file directory on your local PC and run the following command.

```bash
$ scp -i <pem file> <pem file> ec2-user@<public DNS name of Control Node>:/home/ec2-user
```
- Check if the file is transferred to the remote machine. 

- As an alternative way, create a file on the control node with the same name as the <pem file> in ```/etc/ansible``` directory. 

- Then copy the content of the pem file and paste it in the newly created pem file on the control node.


```bash
$ ansible all -m ping

```


## Part 2 - Using Ansible Roles

- Go to Ansible Galaxy web site (www.galaxy.ansible.com)

- Click the Search option

- Write ngnx

- Explane the difference beetween collections and roles

- Evaluate the results (stars, number of download, etc.)

- Go to command line and write:

```bash
$ ansible-galaxy search nginx
```

Stdout:
```
Found 1494 roles matching your search. Showing first 1000.

 Name                                                         Description
 ----                                                         -----------
 0x0i.prometheus                                              Prometheus - a multi-dimensional time-series data mon
 0x5a17ed.ansible_role_netbox                                 Installs and configures NetBox, a DCIM suite, in a pr
 1davidmichael.ansible-role-nginx                             Nginx installation for Linux, FreeBSD and OpenBSD.
 1it.sudo                                                     Ansible role for managing sudoers
 1mr.zabbix_host                                              configure host zabbix settings
 1nfinitum.php                                                PHP installation role.
 2goobers.jellyfin                                            Install Jellyfin on Debian.
 2kloc.trellis-monit                                          Install and configure Monit service in Trellis.
 ```


 - there are lots of. Lets filter them.

 ```bash
 $ ansible-galaxy search nginx --platform EL
```
"EL" for centos 

- Lets go more specific :

```bash
$ ansible-galaxy search nginx --platform EL | grep geerl

Stdout:
```
geerlingguy.nginx                                            Nginx installation for Linux, FreeBSD and OpenBSD.
geerlingguy.php                                              PHP for RedHat/CentOS/Fedora/Debian/Ubuntu.
geerlingguy.pimpmylog                                        Pimp my Log installation for Linux
geerlingguy.varnish                                          Varnish for Linux.

```
- Install it:

$ ansible-galaxy install geerlingguy.nginx

Stdout:
```
- downloading role 'nginx', owned by geerlingguy
- downloading role from https://github.com/geerlingguy/ansible-role-nginx/archive/2.8.0.tar.gz
- extracting geerlingguy.nginx to /home/ec2-user/.ansible/roles/geerlingguy.nginx
- geerlingguy.nginx (2.8.0) was installed successfully
```

- Inspect the role:

$ cd /home/ec2-user/.ansible/roles/geerlingguy.nginx

$ ls
defaults  handlers  LICENSE  meta  molecule  README.md  tasks  templates  vars

$ cd tasks
$ ls

main.yml             setup-Debian.yml   setup-OpenBSD.yml  setup-Ubuntu.yml
setup-Archlinux.yml  setup-FreeBSD.yml  setup-RedHat.yml   vhosts.yml

$ vi main.yml

```yml
--
# Variable setup.
- name: Include OS-specific variables.
  include_vars: "{{ ansible_os_family }}.yml"

- name: Define nginx_user.
  set_fact:
    nginx_user: "{{ __nginx_user }}"
  when: nginx_user is not defined

# Setup/install tasks.
- include_tasks: setup-RedHat.yml
  when: ansible_os_family == 'RedHat'

- include_tasks: setup-Ubuntu.yml
  when: ansible_distribution == 'Ubuntu'

- include_tasks: setup-Debian.yml
  when: ansible_os_family == 'Debian'

- include_tasks: setup-FreeBSD.yml
  when: ansible_os_family == 'FreeBSD'

- include_tasks: setup-OpenBSD.yml
  when: ansible_os_family == 'OpenBSD'

- include_tasks: setup-Archlinux.yml
  when: ansible_os_family == 'Archlinux'

# Vhost configuration.
- import_tasks: vhosts.yml

# Nginx setup.
- name: Copy nginx configuration in place.
  template:
    src: "{{ nginx_conf_template }}"
    dest: "{{ nginx_conf_file_path }}"
    owner: root
    group: "{{ root_group }}"
    mode: 0644
  notify:
    - reload nginx
```

- # use it in playbook:

- Create a playbook named "playbook-nginx.yml"

```yml
- name: use galaxy nginx role
  hosts: all
  user: ec2-user
  become: true

  roles:
    - role: geerlingguy.nginx
```

- Run the playbook.

$ ansible-playbook playbook-nginx.yml

- List the roles you have:

$ ansible-galaxy list

Stdout:
```
- geerlingguy.elasticsearch, 5.0.0
- geerlingguy.mysql, 3.3.0
```

- 
$ ansible-config dump | grep ROLE

Stdout:
```
DEFAULT_PRIVATE_ROLE_VARS(default) = False
DEFAULT_ROLES_PATH(default) = [u'/home/ercan/.ansible/roles', u'/usr/share/ansible/roles', u'/etc/ansible/roles']
GALAXY_ROLE_SKELETON(default) = None
GALAXY_ROLE_SKELETON_IGNORE(default) = ['^.git$', '^.*/.git_keep$']
```



- Install Apache server and restart it with using Ansible roles.

```bash
ansible-galaxy init /etc/ansible/roles/apache
cd roles/apache
ll
yum install tree
tree apache/
```

- Create tasks/main.yml with the following.

```bash
vi tasks/main.yml
```

```bash
---
# tasks file for /etc/ansible/roles/apache
- name: installing apache
  apt:
    name: apache2
    state: latest

- name: index.html
  copy:
    content: "<h1>Hello Clarusway</h1>"
    dest: /var/www/html/index.html

- name: restart apache2
  service:
    name: apache2
    state: restarted
    enabled: yes
```

- Create handlers/main.yml with the following.

```bash
vi handlers/main.yml
```

```bash
---
# handlers file for /etc/ansible/roles/apache
- name: restart apache
  service: name=apache2 state=restarted
```

- Create playbook7.yml.

```bash
cd /etc/ansible
vi playbook7.yml
```

```bash
---
- name: Install and Start Apache
  hosts: ubuntuservers
  roles:
    - apache
```
- Run the playbook7.yml

```bash
ansible-playbook -b playbook7.yml
```

