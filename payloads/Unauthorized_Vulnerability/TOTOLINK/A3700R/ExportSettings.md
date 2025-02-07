## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/data/upload/20200728/311b3ec5b0a8e61af298aebda158ec9b.zip

## Affected version

A3700R V9.1.2u.5822_B20200513

## Vulnerability details

In TOTOLINK A3700R V9.1.2u.5822_B20200513, an attacker can obtain the apmib configuration file without authorization through /cgi-bin/ExportSettings.sh. When making a request to `/cgi-bin/ExportSettings.sh`, the attacker can obtain the `apmib` configuration file Config--xxxxxxxx.dat without authorization. The username and password can be found in the decoded file.

## POC

![image-20240719214410842](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719214410842.png)
