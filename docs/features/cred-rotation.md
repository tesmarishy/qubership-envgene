
# Credentials Rotation

- [Credentials Rotation](#credentials-rotation)
  - [Problem Statement](#problem-statement)
  - [Proposed Approach](#proposed-approach)
    - [Requirements](#requirements)
    - [Instance Repository Pipeline Parameters](#instance-repository-pipeline-parameters)

## Problem Statement

## Proposed Approach

### Requirements

### Instance Repository Pipeline Parameters

| Attribute | Type | Mandatory | Description | Default | Example |
|---|---|---|---|---|---|
| `CRED_ROTATE` | string | no | TBD | None |TBD |

```yaml
update_shared_creds: <true|false> # Optional, Default - false
sensitive_parameters:
  namespaces:
    <namespace>:
      parameter_keys: # Optional
        - <param-key>: <param-value>
          context: <value>
      applications: # Optional
        <app-name>:
          parameter_keys:
            - <param-key>: <param-value>
              context: <value>
```

```yaml
  - # Mandatory
    # Affected parameter key
    parameter_key: string
    # Mandatory
    # Effective Set context where the parameter is located.
    context: enum(`pipeline`,`deployment`,`runtime`)
    # Mandatory
    # Environment id (in cluster-name/env-name notation) where affected parameter is located
    environment: string
    # Mandatory
    # Namespace where affected parameter is located
    namespace: string
    # Mandatory. Default `""`
    # Application where affected parameter is located
    application: string
    # Mandatory
    # Path to file containing the common Credential
    cred-filepath: string
    # Mandatory
    # Common Credential ID. Located in `cred-filepath`
    cred-id: credX
```
