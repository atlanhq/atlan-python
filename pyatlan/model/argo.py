from typing import Optional, List
from pydantic import BaseModel, Field , validator


#These are classes for data that directly comes from the Argo through Heracles API
#while workflow models data comes via ES.

class Label(BaseModel):
    package_installer: Optional[str] = Field(None, alias='package.argoproj.io/installer')
    package_name: Optional[str] = Field(None, alias='package.argoproj.io/name')
    package_parent: Optional[str] = Field(None, alias='package.argoproj.io/parent')
    package_registry: Optional[str] = Field(None, alias='package.argoproj.io/registry')
    package_version: Optional[str] = Field(None, alias='package.argoproj.io/version')
    workflows_creator: Optional[str] = Field(None, alias='workflows.argoproj.io/creator')
    workflows_creator_email: Optional[str] = Field(None, alias='workflows.argoproj.io/creator-email')
    workflows_creator_username: Optional[str] = Field(None, alias='workflows.argoproj.io/creator-preferred-username')


class Annotation(BaseModel):
    last_used_schedule: Optional[str] = Field(None, alias='cronworkflows.argoproj.io/last-used-schedule')
    last_applied_configuration: Optional[str] = Field(None, alias='kubectl.kubernetes.io/last-applied-configuration')
    package_author: Optional[str] = Field(None, alias='package.argoproj.io/author')
    package_description: Optional[str] = Field(None, alias='package.argoproj.io/description')


class Metadata(BaseModel):
    name: Optional[str]
    namespace: Optional[str]
    uid: Optional[str]
    resource_version: Optional[str] = Field(None, alias='resourceVersion')
    generation: Optional[int]
    creation_timestamp: Optional[str] = Field(None, alias='creationTimestamp')
    labels: Optional[Label]
    annotations: Optional[Annotation] = {} # Default to an empty dict if missing


class WorkflowTemplateRef(BaseModel):
    name: Optional[str]
    # cluster_scope: Optional[bool] = Field(None, alias='clusterScope')


class WorkflowSpec(BaseModel):
    arguments: Optional[dict] = {}  # Default to an empty dict if missing
    workflow_template_ref: Optional[WorkflowTemplateRef] = Field(None, alias='workflowTemplateRef')

class Spec(BaseModel):
    workflow_spec: Optional[WorkflowSpec] = Field(None, alias='workflowSpec')
    schedule: Optional[str]
    concurrency_policy: Optional[str] = Field(None, alias='concurrencyPolicy')
    starting_deadline_seconds: Optional[int] = Field(None, alias='startingDeadlineSeconds')
    timezone: Optional[str] = Field(None, alias='timezone')
    nextRun: Optional[str] = Field(None, alias='nextRun')
    successful_jobs_history_limit: Optional[int] = Field(None, alias='successfulJobsHistoryLimit')
    failed_jobs_history_limit: Optional[int] = Field(None, alias='failedJobsHistoryLimit')


class Status(BaseModel):
    active: Optional[bool] = False # Default to False if missing
    last_scheduled_time: Optional[str] = Field(None, alias='lastScheduledTime')
    conditions: Optional[dict] = {} #Default to an empty dict if missing


class Item(BaseModel):
    metadata: Optional[Metadata]
    spec: Optional[Spec]
    status: Optional[Status]


class RootModel(BaseModel):
    items: Optional[List[Item]]
