---
title: Manage apps
description: Create, run, schedule, and manage Atlan app workflows with the AppClient.
---

# Manage apps

Atlan **apps** are connector workflows — crawlers, miners, and enrichment jobs — that
you create and run on your tenant. The `AppClient` (`client.app`) is the single
entry point for the full app lifecycle: create, run, inspect, update, schedule,
and delete.

There are two ways to build the `inputs` for an app:

- **Typed builders** (recommended) — a fluent, UI-equivalent builder per connector
  (see [Supported apps](index.md)). The builder vaults credentials, mints the
  connection, and assembles the full payload for you, so you never hand-build a
  connection object or guess an input key.
- **A raw `inputs` dict** — for any app, including ones without a builder. Pass the
  values dict directly to `client.app.create(...)`; the server validates it against
  the app's input contract.

!!! info "Apps run asynchronously"
    Creating an app with `run=True` (or calling `.run()` on a builder) submits a run
    that executes in the background. Use [`get_run`](#get-a-runs-status) to poll the
    run's status until it is terminal.

## Create an app

A builder's `.create()` builds and publishes the workflow **without** running it;
`.run()` does the same and immediately submits a run. Both return an
`AppResponse` — **persist its `slug`**, which identifies the workflow for every
later operation.

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Create and run an app via a builder"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import BigqueryCrawler

    client = AtlanClient()

    response = (
        BigqueryCrawler(client) # (1)
        .service_account( # (2)
            email="svc@my-project.iam.gserviceaccount.com",
            service_account_json=sa_json,
            project_id="my-project",
        )
        .connection( # (3)
            name="production-bigquery",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include({"my-project": ["analytics", "sales"]}) # (4)
        .run(name="bigquery-prod") # (5)
    )
    print(response.slug, response.run_id) # (6)
    ```

    1. Each connector has its own builder — see [Supported apps](index.md).
    2. **Step 1 — Credential.** Pick the auth method your source uses; the builder
       vaults the secret and never persists it in the workflow.
    3. **Step 2 — Connection.** Provide a display name and at least one admin
       (user, group, or role). The builder mints the connection qualified name.
    4. **Step 3 — Metadata.** Configure what to crawl and how.
    5. `.run(name=...)` creates **and** submits a run. Use `.create(name=...)` to
       create the workflow without running it.
    6. Persist `response.slug` — you need it to inspect, update, schedule, re-run,
       or delete the workflow.

To build an app **without** a builder, pass a raw `inputs` dict:

=== ":lang-python: Python"

    ```python linenums="1" title="Create an app from a raw inputs dict"
    response = client.app.create(
        app_id="bigquery-crawler", # (1)
        entrypoint="crawler", # (2)
        name="bigquery-prod",
        inputs={...}, # (3)
        run=True, # (4)
    )
    ```

    1. The marketplace application id.
    2. Optional — omit to use the app's default entrypoint.
    3. The values dict matching the app's input contract. See
       [Inspect an app's input contract](#inspect-an-apps-input-contract) to
       discover the available keys.
    4. Submit a run on create. The server defaults to `True` when omitted.

## Re-run an existing app

!!! warning "Don't re-create — re-run"
    Calling a builder's `.run()` / `.create()` again creates a **new** connection and
    new assets, which can produce duplicates. To re-crawl, submit a new run of the
    **existing** workflow with its `slug`.

=== ":lang-python: Python"

    ```python linenums="1" title="Submit a new run of an existing workflow"
    run = client.app.submit("bigquery-prod-AbC123") # (1)
    print(run.run_id, run.status)
    ```

    1. The `slug` returned when the workflow was first created.

## List apps

=== ":lang-python: Python"

    ```python linenums="1" title="List published app workflows"
    page = client.app.get_all(limit=50) # (1)
    for app in page.workflows: # (2)
        print(app.slug, app.name)
    # page.has_more / page.next_cursor -> pass cursor= back to paginate
    ```

    1. `limit` is the page size (server default 50).
    2. Iterate `page.workflows`; if `page.has_more`, pass `page.next_cursor` as
       `cursor=` on the next call.

## Get a single app

=== ":lang-python: Python"

    ```python linenums="1" title="Get one workflow by slug"
    summary = client.app.get("bigquery-prod-AbC123") # (1)
    print(summary.app_id, summary.name, summary.version)
    ```

    1. The workflow `slug`.

## Get a run's status

Runs are asynchronous — poll until the run is terminal.

=== ":lang-python: Python"

    ```python linenums="1" title="Poll a run until it finishes"
    import time

    while True:
        run = client.app.get_run("a1b2c3d4-...") # (1)
        print(run.status)
        if run.is_terminal: # (2)
            print("done:", run.status, "success:", run.is_success)
            break
        time.sleep(10)
    ```

    1. The `run_id` from `create(run=True)` / `run()` / `submit()`.
    2. `is_terminal` is `True` once the run has finished (succeeded, failed, or
       cancelled); `is_success` reports the outcome.

## Cancel a run

=== ":lang-python: Python"

    ```python linenums="1" title="Cancel an in-flight run"
    client.app.cancel_run("a1b2c3d4-...") # (1)
    ```

    1. The `run_id` of the run to cancel.

## Update an app

Replace a workflow's inputs and publish a new version on the same `slug`. This is a
full replace — send the complete `inputs`. Omit the credential to keep the
persisted one.

=== ":lang-python: Python"

    ```python linenums="1" title="Update a workflow's inputs"
    updated = client.app.update(
        slug="bigquery-prod-AbC123", # (1)
        inputs={...}, # (2)
    )
    print(updated.version) # (3)
    ```

    1. The workflow `slug`.
    2. The **complete** input-contract values (a dict, or an `AppInput` from a
       builder's `preview()`).
    3. A new `version` is published on the same slug.

## Schedule an app

Attach a cron schedule to the latest published version.

=== ":lang-python: Python"

    ```python linenums="1" title="Add and remove a schedule"
    added = client.app.add_schedule(
        slug="bigquery-prod-AbC123", # (1)
        cron="0 9 * * *", # (2)
        timezone="Asia/Kolkata", # (3)
    )

    client.app.remove_schedule(
        slug="bigquery-prod-AbC123",
        trigger_id=added.trigger_id, # (4)
    )
    ```

    1. The workflow `slug`.
    2. A standard cron expression (here: every day at 09:00).
    3. Optional IANA timezone; defaults to `UTC` when omitted.
    4. Removing a schedule needs the `trigger_id` returned when it was added.

You can also attach a schedule when creating the app, by passing `schedule=` to
`.create()` / `.run()` (builders) or `client.app.create(...)`.

## Delete an app

=== ":lang-python: Python"

    ```python linenums="1" title="Archive (delete) a workflow"
    result = client.app.delete("bigquery-prod-AbC123") # (1)
    print(result.archived)
    ```

    1. The workflow `slug`.

## Inspect an app's input contract

Every app validates its `inputs` against a server-side **input contract**. Fetch it
to discover the available keys, types, and defaults — useful when building a raw
`inputs` dict, or to check whether an app is runnable on your tenant.

=== ":lang-python: Python"

    ```python linenums="1" title="Fetch an app's input contract"
    contract = client.app.get_input_contract("bigquery-crawler") # (1)
    print(contract.properties.keys())
    ```

    1. Returns the JSON-schema-style contract. A `404` means the app does not expose
       a native input contract on this tenant (it isn't runnable via `client.app`
       there yet).

## Describe an app

=== ":lang-python: Python"

    ```python linenums="1" title="Describe an app's metadata"
    info = client.app.describe("bigquery-crawler") # (1)
    print(info.name, info.native_ready, info.entrypoints)
    ```

    1. Returns the app's metadata (display name, whether it is native-ready, and its
       entrypoints).

## Raw REST API

If you aren't using the SDK, call the app endpoints directly. They are served under
the gateway prefix `api/service/` on your tenant, and authenticated with an API key
via the `Authorization: Bearer <api-key>` header.

| Operation | Method & path |
|---|---|
| Create (+ version, publish, optional run) | `POST /api/service/v1/app` |
| List published workflows | `GET /api/service/v1/app` |
| Get one workflow | `GET /api/service/v1/app/{slug}` |
| Update (full-replace inputs, new version) | `PUT /api/service/v1/app/{slug}` |
| Delete (archive) | `DELETE /api/service/v1/app/{slug}` |
| Submit a run | `POST /api/service/v1/app/{slug}/submit` |
| Get a run's status | `GET /api/service/v1/app/runs/{run_id}` |
| Cancel a run | `POST /api/service/v1/app/runs/{run_id}/cancel` |
| Add a schedule | `POST /api/service/v1/app/{slug}/schedule` |
| Remove a schedule | `DELETE /api/service/v1/app/{slug}/schedule/{trigger_id}` |
| Describe an app | `GET /api/service/v1/apps/{app_id}` |
| Get an app's input contract | `GET /api/service/v1/apps/{app_id}/inputs` |

=== ":material-console: cURL"

    ```bash linenums="1" title="Create and run an app"
    curl -X POST "https://<tenant>.atlan.com/api/service/v1/app" \
      -H "Authorization: Bearer $ATLAN_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
            "app_id": "bigquery-crawler",
            "entrypoint": "crawler",
            "name": "bigquery-prod",
            "run": true,
            "inputs": {
              "connection": {
                "typeName": "Connection",
                "attributes": {
                  "qualifiedName": "default/bigquery/1700000000",
                  "connectorName": "bigquery",
                  "name": "production-bigquery",
                  "adminRoles": ["<role-guid>"]
                }
              },
              "extraction_method": "direct",
              "credential": {
                "authType": "basic",
                "connectorConfigName": "atlan-connectors-bigquery",
                "username": "svc@my-project.iam.gserviceaccount.com",
                "password": "<service-account-json>",
                "host": "https://bigquery.googleapis.com",
                "port": 443,
                "extra": {"project_id": "my-project", "connect_type": "public"}
              },
              "credential_guid": "",
              "include_filter": "{\"^my-project$\": [\"^analytics$\"]}"
            }
          }'
    ```

    The response contains the `slug` and (when `run: true`) the `run_id`. A raw
    credential placed in the `credential` key is vaulted server-side and the issued
    guid is routed into `credential_guid`.

=== ":material-console: Poll the run"

    ```bash linenums="1" title="Get a run's status"
    curl "https://<tenant>.atlan.com/api/service/v1/app/runs/<run_id>" \
      -H "Authorization: Bearer $ATLAN_API_KEY"
    # -> {"run_id": "...", "slug": "...", "status": "Running"}
    ```

!!! tip "Discover the input keys"
    `inputs` is validated against the app's input contract. Fetch it with
    `GET /api/service/v1/apps/{app_id}/inputs` to see the available keys, types, and
    defaults before hand-building a payload.
