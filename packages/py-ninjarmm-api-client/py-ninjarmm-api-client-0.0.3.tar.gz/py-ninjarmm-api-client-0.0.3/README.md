# README #

### What is this repository for? ###

Unoffical [NinjaRMM API](https://ninjarmm.com/dev-api/) client for Python

### Requirements ###

* Python 3
* [Requests](https://pypi.org/project/requests/)

### Installation ###

the classic way:

```
pip3 install py-ninjarmm-api-client
```

or directly from GIT repo:

```
pip3 install git+https://bitbucket.org/raptus-it-services/py-ninjarmm-api-client.git
```

### Usage ###

```
import ninjarmm_api
napi = ninjarmm_api.client("YOUR_AccessKeyId", "YOUR_SecretAccessKey", iseu=False, debug=True)
customers = napi.get_customers()
```

If you are on the **EU instance** of NinjaRMM, set `iseu=True`
