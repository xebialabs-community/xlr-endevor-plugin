# XL Release Endevor plugin v1.0.0 -- <span style="color:red">Under construction</span>

[![Build Status][xlr-endevor-plugin-travis-image]][xlr-endevor-plugin-travis-url]
[![License: MIT][xlr-endevor-plugin-license-image]][xlr-endevor-plugin-license-url]
![Github All Releases][xlr-endevor-plugin-downloads-image]

[xlr-endevor-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-endevor-plugin.svg?branch=master
[xlr-endevor-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-endevor-plugin
[xlr-endevor-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-endevor-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-endevor-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-endevor-plugin/total.svg

## Preface

This document describes the functionality provided by the xlr-endevor-plugin.

See the **[XL Release Documentation](https://docs.xebialabs.com/xl-release/index.html)** for background information on XL Release and release concepts.

## Overview

This is a plugin allows XL Release to interact with Endevor for deploying, promoting and managing applications on the mainframe.

## Installation

* Copy the xlr-endevor-plugin by copying the plugin jar to the **XL-RELEASE-HOME/plugin** folder.
* On the Mainframe install the following:
	* 	SMID Web Services 
	*  CISQ103
	*  Tomcat under Unix services
	*  Communications EAX
	*  RESTful client or SOAP
*  Restart XL Release


## Functionality

<span style="color:red">**Assumes the CA Endevor SCM Web Services component is installed.
Code returns dummy values for now pending testing against a live installation of CA Endevor.**</span>

### Approve Package

This action approves a package.

![Approve_Package](images/Endevor_Approve_Package.png)

##### Input: 

| Variable | Description  |
|----------|--------------|
| instance | Name of a specific Endevor instance to validate instead of all available Endevor instances. |
| Package  | The package  |

##### Output: 

### Backin Package

This action backs in a package.

##### Input: 

##### Output: 

### Backout Package

This action backs out a package.

##### Input: 

##### Output: 

### Cast Package

This action casts a package.

##### Input:

##### Output:

### Commit Package

The COMMIT PACKAGE action removes all backout/backin data while retaining package event information. You can use the COMMIT action against a package only if the package has a status of **Executed** or **Exec-failed**.

##### Input:

##### Output:

### Delete Package

This action deletes a package.

##### Input: 

##### Output: 

### Execute Package

This action executes a package.

![Execute_Package](images/Endevor_Execute_Pacakage.png)

##### Input:

| Variable | Description  |
|----------|--------------|
| instance | Name of a specific Endevor instance to validate instead of all available Endevor instances. |
| Package  | The package  |
| Ewfromdate | Specifies the time frame within which to execute the package (Execution window). You can only use the execution window parameters if the package is fully qualified and the existing execution window is closed. |
| Ewfromtime | Specifies the time frame within which to execute the package (Execution window). You can only use the execution window parameters if the package is fully qualified and the existing execution window is closed. |
| Ewtodate | Specifies the time frame within which to execute the package (Execution window). You can only use the execution window parameters if the package is fully qualified and the existing execution window is closed. |
| Ewtotime | Specifies the time frame within which to execute the package (Execution window). You can only use the execution window parameters if the package is fully qualified and the existing execution window is closed.| 
| Status | Specifies the statuses of the package you want to execute. You can only use this clause when you wildcard the package ID. The default is to execute packages that have a status of Approved. ( Valid statuses are: **APPROVED**, **EXECFAILED** |

##### Output:


### List All Configurations

This action lists all the available CA Endevor SCM configurations on the server.

##### Input:
None

##### Output:
List of available CA Endevor SCM instances that are defined by configuration files on the server in JSON format.

### List Parameters of a Configuration

This action lists all the parameters of a specific CA Endevor SCM configuration.

#####Input: 
Configuration instance

##### Output: 
List of a specific CA Endevor SCM configuration in JSON format.

### List Packages

The List package action lists CA Endevor SCM packages. Name-masking is supported to filter package names.

##### Input:

| Variable | Description  |
|----------|--------------|
| instance | Name of a specific Endevor instance to validate instead of all available Endevor instances. |
| Package  | The package  |
| status   | filters by one or more of **INEDIT**, **INAPPROVAL**, **APPROVED**, **INEXECUTION**, **EXECUTED**, **COMMITTED**, **DENIED**.|
| type     | filters by Standard or Emergency |
| enterprise  | filters by enterprise package parameter, all, enterprise, exclude |
| promotion | filters by promotion package parameter, all, promotion or exclude |

##### Output:
List of Packages in JSON format, which corresponds to the CA Endevor SCM List Package ID function of the CSV utility. 

### Reset Package

This action resets a package.

##### Input: 

##### Output: 

### Ship Package

The SHIP PACKAGE action is used to ship a package to a remote site. You can ship the package output members or the package backout members. The Ship Package task will let you indicate the package that you wnat to ship, the destination to ship the package to and if you want to ship output or backout members as well as set the data set name prefix in the XCOM or CONNECT:DIRECT transmission methods.

![Ship_Package](images/Endevor_Ship_Package.png)

##### Input:

| Variable | Description  |
|----------|--------------|
| instance | Name of a specific Endevor instance to validate instead of all available Endevor instances. |
| Package  | The package  |
| destination | Indicates the name of the remote site to which you want to ship the specified package. This parameter is mandatory. |
| option   | Indicates whether you want to ship output members, or backout members to the remote site. |
| prefix   | Indicates the data set name prefix to be used in the XCOM or CONNECT:DIRECT transmission methods.

##### Output:

### Update Package

This action updates a package.

##### Input: 

##### Output:

## References
* [Restful API Clients](https://docops.ca.com/ca-endevor-SCM/18/en/web-services-and-eclipse-based-ui/restful-api-clients)
* 

