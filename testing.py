from pyatlan.client.atlan import AtlanClient
from pyatlan.model.enums import AtlanWorkflowPhase

client = AtlanClient()
runs_status = client.workflow.find_by_status_and_interval(
    [AtlanWorkflowPhase.RUNNING], 1
)
print(runs_status)
