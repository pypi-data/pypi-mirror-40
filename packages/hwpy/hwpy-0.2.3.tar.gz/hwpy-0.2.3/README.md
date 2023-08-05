# install(python2.7 and python3.x)

#### lastest psutil maybe required
```
# yum install -y gcc python-devel
# pip install -U setuptools 
# pip install -U psutil
```

```
# pip install hwpy
```

# usage
```
# python -m hwpy
```
```
from hwpy import info
info.main()
info.hwlist
```
```
info.cpu
info.net    
info.disk
info.part   
info.host
info.mem
```
