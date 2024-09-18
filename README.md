# subby.py
subdomain enumeration with simple data aggregators built in

## Installation

In order to rub Subby, you need the following Python and Golang packages:

```bash
  requests (python)
  beautifulsoup4 (python)
  httpx (go)
```

To install these packages, do the following: 

### Python

```bash
pip install -r requirements.txt
```

### Go

```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
```

## Running the script

After installing all of the required packages and binaries, you can either scan a singular domain or run multiple from a text file. 

```bash
python3 subpy.py -d example.com
```
or 
```
python3 subpy.py -f file.txt
```

## Visual Demo
![image_example](https://i.ibb.co/NWdYz5w/image.png)

![image_example](https://i.ibb.co/ng6F2VC/image.png)


## Credits

- developed with ❤️ from [criminal.sh](https://criminal.sh)
- credits go respectfully and with love to [Project Discovery](https://github.com/projectdiscovery/httpx) for the httpx go binary, and for the developers of the [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) and [requests](https://pypi.org/project/requests/) python modules!
- credits also go to [myssl.com](https://myssl.com), [rapiddns.io](https://rapiddns.io), [hackertarget.com](https://hackertarget.com), [jldc.me](https://jldc.me), and [alienvault.com](https://alienvault.com) for providing the APIs needed for the data aggregation.
- shoutout to c (providing original modules) and wazzy for the idea, wouldn't be here without you both.

## TODO 

- improve regex rules
- add sitedossier, crt.sh, archive.org as aggregators
- multiprocessing for multiple domains (chunk each domain scan into a seperate process to run concurrent with the rest)
