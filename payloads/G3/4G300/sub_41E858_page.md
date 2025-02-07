## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2227.html

## Affected version

4G300 V1.01.42

## Vulnerability details

The Tenda 4G300 V1.01.42 firmware has a stack overflow vulnerability in the `sub_41E858` function. The `v4` variable receives the `page` parameter from a POST request. However, since the user can control the input of `page `, the statement can cause a buffer overflow. The user-provided `page` can exceed the capacity of the `v10` array, triggering this security vulnerability.

![image-20240418105305100](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418105305100.png)

## POC

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)
