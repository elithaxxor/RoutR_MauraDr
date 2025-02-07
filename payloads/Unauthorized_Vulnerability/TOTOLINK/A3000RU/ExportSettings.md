## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://totolink.com.my/products/a3000ru/

## Affected version

A3000RU_Firmware V5.9c.5185

## Vulnerability details

In TOTOLINK A3000RU_Firmware V5.9c.5185, an attacker can obtain the apmib configuration file without authorization through /cgi-bin/ExportSettings.sh. When making a request to `/cgi-bin/ExportSettings.sh`, the attacker can obtain the `apmib` configuration file Config--xxxxxxxx.dat without authorization. The username and password can be found in the decoded file.

## POC

![image-20240719214410842](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719214410842.png)
