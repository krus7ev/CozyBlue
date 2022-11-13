# CozyBlue
Sensika Hackathon against disinformation solutions submission


## 3.1.2 - subtask 5: Detection of the real (hosting) IP address

The [CloudFail](https://github.com/m0rtem/CloudFail) project mentioned in the suggested [technical alternatives medium article](https://medium.com/@hengky.kaiqi/finding-the-real-ip-address-of-a-website-behind-cloud-flare-c2115be8d163)
) is added to the project in [CloudFail-master](./CloudFail-master) and modified in order to be imported as a python module and re-used iteratively to loop over domains in the `data/` spreadsheet provided (ignored/not added), patching some of the error-handling and some of the steps in the code (cloudfail.py) yielding buggy behaviour.
As a result 160 hits were made showing IP address discoveries different to the ping-able CloudFlare proxy IPs, over the set of 850 domains listed in via its `dnsdumpster` and/or `crimeflare` reccord lookup procedures. Subdomain lookups were not debugged as well as some of `dnsdumpster`'s error prone behaviour (LTBD).
