# XL Release Endevor plugin v1.0.0 -- Under construction #

## CI status ##

[![Build Status][xlr-endevor-plugin-travis-image]][xlr-endevor-plugin-travis-url]
[![License: MIT][xlr-endevor-plugin-license-image]][xlr-endevor-plugin-license-url]
![Github All Releases][xlr-endevor-plugin-downloads-image]

[xlr-endevor-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-endevor-plugin.svg?branch=master
[xlr-endevor-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-endevor-plugin
[xlr-endevor-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-endevor-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-endevor-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-endevor-plugin/total.svg


## Functionality ##

**Assumes the CA Endevor SCM Web Services component is installed.
Code returns dummy values for now pending testing against a live installation of CA Endevor.
**

### Approve Package ###

This action approves a package.

##### Input: #####

##### Output: #####

### Backin Package ###

This action backs in a package.

##### Input: #####

##### Output: #####

### Backout Package ###

This action backs out a package.

##### Input: #####

##### Output: #####

### Cast Package ###

This action casts a package.

##### Input: #####

##### Output: #####

### Commit Package ###

This action commits a package.

##### Input: #####

##### Output: #####

### Delete Package ###

This action deletes a package.

##### Input: #####

##### Output: #####

### Execute Package ###

This action executes a package.

##### Input: #####

##### Output: #####


### List All Configurations ###

This action lists all the available CA Endevor SCM configurations on the server.

##### Input: #####
None

##### Output: #####
List of available CA Endevor SCM instances that are defined by configuration files on the server in JSON format.

### List Parameters of a Configuration ###

This action lists all the parameters of a specific CA Endevor SCM configuration.

#####Input: #####
Configuration instance

##### Output: #####
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

### Reset Package ###

This action resets a package.

##### Input: #####

##### Output: #####

### Ship Package ###

This action ships a package.

##### Input: #####

##### Output: #####

### Update Package ###

This action updates a package.

##### Input: #####

##### Output: #####



