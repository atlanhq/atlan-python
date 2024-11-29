from pyatlan.client.atlan import AtlanClient
import logging
logging. basicConfig (level=logging.DEBUG) #
client = AtlanClient()

groups3 =  client.group.get_all(limit=3)

print(groups3)
