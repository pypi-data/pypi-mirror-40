# emdata-tools

Something useful in my python apps.

### eureka useage

```python
from emdata_tools import EurekaClient

eureka = EurekaClient('em-eureka-app', 8088,
                      eureka_url='http://localhost:8761/')
eureka.start()
```