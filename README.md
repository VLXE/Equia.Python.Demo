# Use cases of Equia Python SDK

This repository contains a collection of samples showcasing some typical uses of [Equia Python SDK](https://vlxe.com/).

> All samples use Python 3.10.

## What is Equia?

Equia is the cloud version of VLXE. It supports all the calculations and systems from the Excel version of VLXE but also much more.
[Equia Python SDK](https://vlxe.com/) integrates the Equia platform by letting you write code that invokes functionality exposed by OnlinePVT API.

## Prerequisites

To be able to run these samples, you need to install the following packages

- [equia](https://pypi.org/project/equia/)
- [aiohttp](https://pypi.org/project/aiohttp/)
- [matplotlib](https://pypi.org/project/matplotlib/)

## Before you start

All samples assume you have set the two values in the file: shared_settings

```
user_id=
access_secret=
```

You can get these values by contacting us at [VLXE](https://vlxe.com/contact)

!!! Please do not share or expose these values !!!

## What is a fluid?
In the Excel version of VLXE you store the parameters in a VLXE project sheet. In Equia this information is contained in a 'Fluid'
A fluid in Equia holds the same information as a VLXE project sheet. So in order to perform any calculations using Equia a fluid has to be provided.
This can be done in two ways:

### Taken from the webserver
Here a fluid has been predefined and send to the webserver and a id to this fluid has been returned. See example in the file: 'fluid_add_sample.py'
This id can then be send as a argument in the flash call

### Provide fluid with the flash call
A user can also provide a fluid as a argument when calling the flash routine. See example in the file: 'flash_sample.py'
 
## Run the flash sample

First edit the file: shared_settings.py with the user id and access secret you obtained from VLXE
Open the file flash_sample and have a look at the code.
The pypi library: Equia provided by VLXE containes a lot of helper classes to get you started fast.
First we obtaine an instance of the class: 'FlashCalculationInput'. It holds all the input arguments needed to perform a flash.
We call it: 'input'
We provide a fluid using the 'Fluid' argument that works just like a project sheet in the Excel version of VLXE
Temperature and pressure is set.
Then we set the type of flash calculation. Here we select: "Fixed Temperature/Pressure" 
Composition is set for each of the three components in the fluid
Last the units are set.

If you have been using the Excel version of VLXE all those arguments will look familiar.


Now just run any sample like any Python script

```
python3 flash_sample.py
```
