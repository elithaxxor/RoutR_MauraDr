## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/data/upload/20200414/2254ce90058da1a549566852c86031db.zip

## Affected version

CP450 v4.1.0cu.747_B20191224

## Vulnerability details

In TOTOLINK CP450 v4.1.0cu.747_B20191224, an attacker can obtain the apmib configuration file without authorization through /cgi-bin/ExportSettings.sh. When making a request to `/cgi-bin/ExportSettings.sh`, the attacker can obtain the `apmib` configuration file Config--xxxxxxxx.dat without authorization. The username and password can be found in the decoded file.

## POC

![image-20240719214410842](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719214410842.png)
