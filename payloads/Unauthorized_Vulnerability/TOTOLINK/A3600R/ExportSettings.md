## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.cn/home/menu/detail.html?menu_listtpl=download&id=63&ids=36

## Affected version

A3600R V4.1.2cu.5182_B20201102

## Vulnerability details

In TOTOLINK A3600R V4.1.2cu.5182_B20201102, an attacker can obtain the apmib configuration file without authorization through /cgi-bin/ExportSettings.sh. When making a request to `/cgi-bin/ExportSettings.sh`, the attacker can obtain the `apmib` configuration file Config--xxxxxxxx.dat without authorization. The username and password can be found in the decoded file.

## POC

![image-20240719214410842](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719214410842.png)
