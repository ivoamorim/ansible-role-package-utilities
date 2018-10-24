package-utilities
=========

Configure package repository list and Install package utility tools

Requirements
------------

None

Role Variables
--------------
```
epel_enabled: boolean
```
Enable EPEL repository if target OS is RedHat family.

Dependencies
------------

None

Example Playbook
----------------
```
- hosts: all
  vars:
    epel_enabled: true

  roles:
    - role: ivoamorim.package-utilities
```

License
-------

BSD
