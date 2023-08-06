import pprint
from ximilar.client.recognition import RecognitionClient, Image, Task
from ximilar.client.tagging import FashionTaggingClient, GenericTaggingClient
from ximilar.client.colors import DominantColorGenericClient, DominantColorProductClient
from ximilar.base.logger import Logger

client = RecognitionClient('eaa27e4de24f3d2c0c9abc91bd2a395fdb3c4385')

task, status = client.get_task('185c2019-1181-439c-900b-9f29c3c35926')
print(task.get_labels())
result = task.classify([{"_file": "../../tests/ximilar.png"}])
pprint.pprint(result)
print('client')
print(task.get_all_tasks())

try:
    fashion = FashionTaggingClient('eaa27e4de24f3d2c0c9abc91bd2a395fdb3c4385')
    result = fashion.tags([{"_file": "../../tests/ximilar.png"}])
    pprint.pprint(result)
except Exception as e:
    print(e)

try:
    generic = GenericTaggingClient('eaa27e4de24f3d2c0c9abc91bd2a395fdb3c4385')
    result = generic.tags([{"_file": "../../tests/ximilar.png"}])
    pprint.pprint(result)
except Exception as e:
    print(e)

try:
    generic = DominantColorGenericClient('eaa27e4de24f3d2c0c9abc91bd2a395fdb3c4385')
    result = generic.dominantcolor([{"_file": "../../tests/ximilar.png"}])
    pprint.pprint(result)
except Exception as e:
    print(e)

try:
    product = DominantColorProductClient('eaa27e4de24f3d2c0c9abc91bd2a395fdb3c4385')
    result = generic.dominantcolor([{"_file": "../../tests/ximilar.png"}])
    pprint.pprint(result)
except Exception as e:
    print(e)
