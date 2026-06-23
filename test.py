import os, time
from pyatlan.client.atlan import AtlanClient

client = AtlanClient(
    base_url=os.environ["ATLAN_BASE_URL"],
    api_key=os.environ["ATLAN_API_KEY"],
)

APP_ID, ENTRYPOINT = "bigquery-crawler", "crawler"

# 1) Discover — confirm it's native + see what inputs the app expects
info = client.app.get_app(APP_ID)
print("native_ready:", info.native_ready, "| entrypoints:", [e.name for e in info.entrypoints])
contract = client.app.get_input_contract(APP_ID, entrypoint=ENTRYPOINT)
print("fields:", contract.field_names())
print("credential field:", contract.credential_field())

# 2a) Guided builder — DIRECT (Atlan-vaulted) credential.
#     Swap in a REAL connection qualifiedName + an existing credential_guid.
inputs = (
    client.app.inputs(APP_ID, entrypoint=ENTRYPOINT)
    .connection(
        qualified_name="default/bigquery/<ts>",     # <-- real connection QN
        connector_name="bigquery",
        admin_users=[os.environ.get("USER", "me")],
    )
    .direct_credential(guid="<existing-credential-guid>")  # <-- real cred guid
    .filters(include={}, exclude={})
    .set("enable_nested_columns", True)                    # validated vs contract
    # .set("filter_sharded_tablez", True)  # <-- typo would raise with a suggestion
)

# 2b) ...or SDR/agent mode (no central credential):
# inputs = (client.app.inputs(APP_ID, entrypoint=ENTRYPOINT)
#     .connection(qualified_name="default/bigquery/<ts>", connector_name="bigquery", admin_users=["me"])
#     .agent(agent_name="<your-agent>", secret_manager="vault", secret_path="kv/<path>")
#     .filters(include={}, exclude={}))

# 2c) ...or the raw-dict escape hatch (FE payloads / power users):
# inputs = {"connection": {...}, "credential_guid": "...", "include_filter": "{}", ...}

# 3) Create AND run it (run defaults to True; pass run=True to be explicit)
resp = client.app.create(app_id=APP_ID, entrypoint=ENTRYPOINT, name="pyatlan-smoke", inputs=inputs, run=True)
print("slug:", resp.slug, "| run_id:", resp.run_id)
slug = resp.slug

try:
    # 4) Poll the run to a terminal state
    if resp.run_id:
        for _ in range(60):
            run = client.app.get_run(resp.run_id)
            print("status:", run.status)
            if run.is_terminal:
                print("final:", run.status, "| success:", run.is_success)
                break
            time.sleep(10)

    # 5) Schedule (optional)
    sch = client.app.add_schedule(slug, cron="0 9 * * *", timezone="Asia/Kolkata")
    client.app.remove_schedule(slug, trigger_id=sch.trigger_id)

    # 6) Update inputs → new version on the same slug
    client.app.update(slug, inputs=inputs, entrypoint=ENTRYPOINT)
finally:
    # 7) Clean up
    print("archived:", client.app.delete(slug).archived)
