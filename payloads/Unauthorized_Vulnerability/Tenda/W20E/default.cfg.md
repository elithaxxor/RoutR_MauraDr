## Overview

- Manufacturer's website information：https://www.tenda.com.cn/
- Firmware download address ：https://www.tenda.com.cn/material/show/102707

## Affected version

W20EV4.0 V15.11.0.6

## Vulnerability details

In W20EV4.0 V15.11.0.6, an attacker can obtain the configuration file without authorization through `/default.cfg`. When making a request to `/default.cfg`, the attacker can obtain the configuration file `default.cfg` without authorization. The login password can be found in the decoded file in parameter `sys.default.userpass`.

## POC

The default password is `admin`, `admin` in base64 code is `YWRtaW4=`

![image-20241214232010541](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20241214232010541.png)
