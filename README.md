# CozyBlue
Sensika Hackathon against disinformation solutions submission


## 3.1.2 - subtask 5: Detection of the real (hosting) IP address

The [CloudFail](https://github.com/m0rtem/CloudFail) project mentioned in the suggested [technical alternatives medium article](https://medium.com/@hengky.kaiqi/finding-the-real-ip-address-of-a-website-behind-cloud-flare-c2115be8d163)
) is added to the project in [CloudFail-master](./CloudFail-master) and modified in order to be imported as a python module and re-used iteratively in the  [demo notebook](./CloudFail-master/hack_thisinformation.ipynb) to loop over domains in the `data/` spreadsheet provided (ignored/not added), patching some of the error-handling and some of the steps in the code (cloudfail.py) yielding buggy behaviour.

As a result 160 hits were made showing IP address discoveries different to the ping-able CloudFlare proxy IPs, over the set of 850 domains listed in via its `dnsdumpster` and/or `crimeflare` reccord lookup procedures. Subdomain lookups were not debugged as well as some of `dnsdumpster`'s error prone behaviour (LTBD).

The output hits' ip address traces from bot `dnsdumpster` and `crimeflare` stages are stored raw in a list of the same length as the input dataframe to preserve indentation. 

Not much progress was made as most effort was put into converting `cloudfail.py`. Future steps must include results validation by comparison with outer CloudFlare adresses, claimed address databases and comparison of their respective geolocations.

## 3.4 - Excessive Ads

At a conceptual stage using filters from filters.txt

## 3.2.2 Identification of ownership/affiliation cross multiple websites with different domains and visual styles without using structured or semi-structured data from the HTML/CSS/JS

The main idea is to extract meaningful information from html structure By meaningful we assume css selectors(class names, ids, tags) and assets (js, css, etc.) We then encode them and run similarity. Jaro is prefered as it preserves original order which is also important.
- parse.py implements this idea above
- sorted_results.py just sorts the results by similarity so we can easily pick threshold.
