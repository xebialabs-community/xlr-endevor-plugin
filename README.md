# xlr-endevor-plugin v1.0.0

### List All Configurations ###

This action lists all the available CA Endevor SCM configurations on the server.

##### Input: #####
None

##### Output:#####
List of available CA Endevor SCM instances that are defined by configuration files on the server in JSON format.

### List Parameters of a Configuration ###

This action lists all the parameters of a specific CA Endevor SCM configuration.

#####Input: #####
Configuration instance

##### Output:#####
List of a specific CA Endevor SCM configuration in JSON format.

### List Packages ###

The List package action lists CA Endevor SCM packages. Name-masking is supported to filter package names.

##### Input: #####

* status, filters by one or more of INEDIT, INAPPROVAL, APPROVED, INEXECUTION, EXECUTED, COMMITTED, DENIED.

* type, filters by Standard or Emergency 

* enterprise, filters by enterprise package parameter, all, enterprise, exclude

* promotion, filters by promotion package parameter, all, promotion or exclude

##### Output: #####
List of Packages in JSON format, which corresponds to the CA Endevor SCM List Package ID function of the CSV utility. 

