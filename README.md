# Use cases of Equia Python SDK

This repository contains a collection of samples showcasing some typical uses of [Equia Python SDK](https://vlxe.com/).

> All samples use Python 3.11.

## What is Equia?

Equia is the cloud version of VLXE. It supports all the calculations and systems from the Excel version of VLXE but also much more.
[Equia Python SDK](https://vlxe.com/) integrates the Equia platform by letting you write code that invokes functionality exposed by Equia API.

## Prerequisites

To be able to run these samples, you need to install the following packages

- [equia](https://pypi.org/project/equia/)
- [aiohttp](https://pypi.org/project/aiohttp/)
- [matplotlib](https://pypi.org/project/matplotlib/)

## Before you start

Contact VLXE to obtain your access key.
You can get these values by contacting [VLXE](https://vlxe.com/contact)

!!! Please do not share or expose these values !!!

## Pypi.org library
VLXE provide a Equia library in Pypi that makes it easy to call the Equia API's.
[See mere here](https://pypi.org/project/Equia/)

## What is a fluid?
In the Excel version of VLXE you store the parameters in a VLXE project sheet. 
In Equia this information is contained in a 'Fluid'
This can be handled in two ways:
Taken from the webserver: Id of this fluid is passed as argument
Provide fluid: The fluid can be passes as a argument
 
## Run the flash sample

First edit the file: shared_settings.py with the access key you obtained from VLXE
```
access_key=
```
Open the file flash_sample and have a look at the code.  
The pypi library: Equia provided by VLXE containes a lot of helper classes to get you started fast.  
First we obtaine an instance of the class: 'FlashFixedTemperaturePressureCalculationInput'. It holds all the input arguments needed to perform a flash.
We call it: 'input'  
We provide a fluid using the 'Fluid' argument that works just like a project sheet in the Excel version of VLXE
Temperature and pressure is set.  
Each web API service a specific type of flash. Here we perform a flash at fixed temperature and pressure.   
Composition is set for each of the three components in the fluid  
Last the units are set.

If you have been using the Excel version of VLXE all those arguments will look familiar.


Now just run any sample like any Python script

```
python flash_sample.py
```
