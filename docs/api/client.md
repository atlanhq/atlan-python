# Client

## AtlanClient

::: pyatlan.client.atlan

## Asset Client

::: pyatlan.client.asset

## Audit Client

::: pyatlan.client.audit

## File Client

::: pyatlan.client.file

## Group Client

::: pyatlan.client.group

## Role Client

::: pyatlan.client.role

## Token Client

::: pyatlan.client.token

## User Client

::: pyatlan.client.user

## Typedef Client

::: pyatlan.client.typedef

## Workflow Client

> **Deprecated.** Targets the legacy workflow surface, which no longer runs on
> newer Atlan tenants. Use the **App Client** below for app workflows.

::: pyatlan.client.workflow

## App Client

The app-workflow client (`client.app`). Creates and manages app workflows from an
`app_id` plus a generic `inputs` dict validated server-side against the app's live
input contract — replacing the hand-maintained `model.packages` builders. Discover
inputs at runtime via `client.app.get_input_contract(...)`.

::: pyatlan.client.app

## Credential Client

::: pyatlan.client.credential

## Contract Client

::: pyatlan.client.contract

## Query Client

::: pyatlan.client.query

## Search Log Client

::: pyatlan.client.search_log

## Task Client

::: pyatlan.client.task

## SSO Client

::: pyatlan.client.sso

## Open Lineage Client

::: pyatlan.client.open_lineage

## Impersonation Client

::: pyatlan.client.impersonate

## Admin Client

::: pyatlan.client.admin

## OAuth

::: pyatlan.client.oauth

::: pyatlan.client.oauth_client
