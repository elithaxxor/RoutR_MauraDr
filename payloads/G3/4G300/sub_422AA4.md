## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2227.html

## Affected version

4G300 V1.01.42

## Vulnerability details

The Tenda 4G300 V1.01.42 firmware has a stack overflow vulnerability in the `sub_422AA4` function. The `v5， v6, v7, v8, v9, v16` variable receives the `year, month, day, hour, minute, second` parameter from a POST request. However, since the user can control the input of `year, month, day, hour, minute, second `, the statement can cause a buffer overflow. The user-provided `year, month, day, hour, minute, second` can exceed the capacity of the `v14` array, triggering this security vulnerability.

![image-20240418105925088](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418105925088.png)

## POC

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)
