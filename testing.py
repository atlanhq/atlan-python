from typing import cast

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AuthPolicy

# Initialize the Atlan client
client = AtlanClient()

# Example to retrieve all persona-related policies
request = (
    client.search()
    .where(asset_type=AuthPolicy)
    .where(AuthPolicy.POLICY_CATEGORY.eq("persona"))
    .include_on_results(
        AuthPolicy.NAME, AuthPolicy.POLICY_RESOURCES, AuthPolicy.POLICY_TYPE
    )
    .to_request()
)

# Execute the search and process the results
response = client.asset.search(request)
for p in response:
    policy = cast(AuthPolicy, p)
    print(
        f"Policy Name: {policy.name}, Resources: {policy.policy_resources}, Type: {policy.policy_type}"
    )
