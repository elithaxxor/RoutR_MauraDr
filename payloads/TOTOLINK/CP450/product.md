## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/data/upload/20200414/2254ce90058da1a549566852c86031db.zip

## Affected version

CP450 v4.1.0cu.747_B20191224

## Vulnerability details

TOTOLINK CP450 v4.1.0cu.747_B20191224 has hard code password for telnet in /web_cste/cgi-bin/product.ini.

## POC

```c
[PRODUCT]
Csid=C8B193C
Model=C8B193C
HostName=none
webTitle=
Vendor=
CopyRight=
webTitle=
Vendor=
CopyRight=
IpAddress=192.168.0.254
DhcpStart=192.168.0.2
DhcpEnd=192.168.0.250
Language=cn
MultiLang="cn,en"
SoftVersion=V6.0c
TelnetHost=Carystudio
TelnetKey=cs2012
TimeZone=UTC-8
StatisticsModel=C8B193C
StatisticsDomain=esas.carystudio.com,totolinkc.com
DomainAccess=
LoginPassword=

[WLAN]
Ssid_5G=wifi_5G
FixedMac=
WlanKey_5G=
Channel_5G=149
MaxSta=32
CountryCodeSupport=1
CountryCode_5G=CN
```
