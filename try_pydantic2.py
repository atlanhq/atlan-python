import time

start = time.time()
from pyatlan.model.assets.asset00 import Referenceable
end = time.time()
print("The time to import Referenceable is:", (end-start), "seconds")