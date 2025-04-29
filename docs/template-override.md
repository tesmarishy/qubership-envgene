
# Template Override

- [Template Override](#template-override)
  - [Problem Statement](#problem-statement)
  - [Proposed Approach](#proposed-approach)
    - [Template Descriptor](#template-descriptor)
      - [Example](#example)

## Problem Statement

Projects need to deploy the same Solution in several modes, for example DEV, SVT, PROD. Preparing an Env Template for such modes requires creating a large number of duplicates of individual components of the template, which creates difficulties with their management.

Goals:

  1. Be able to define Resource Profile and Resource Profile Override via Environment Inventory
  2. Be able to create group Environment Templates with common and different parts

## Proposed Approach

In the Environment Descriptor, it becomes possible to describe the override of a Namespace template using the `template_override` attribute. This attribute allows defining the **entirety or a portion of the Namespace object**. When generating an Environment Instance, the content of `template_override` is merged into the Namespace object.

`template_override` may contain Jinja expressions. In such cases, the content of `template_override` will be rendered using the same context as the Namespace template and then merged into the rendered Namespace during Environment Instance generation.

If `template_override` contains Jinja expressions, it must be declared as a multi-line string, for example, using the [literal style](https://yaml.org/spec/1.2.2/#812-literal-style) in YAML.

### Template Descriptor

```yaml
tenant: <path-to-tenant-template>
cloud: <path-to-cloud-template>
namespaces:
  - template_path: <path-to-ns-template>
    template_override:     
      <yaml or jinja expression> # entirety or a portion of the Namespace object or a Jinja expression that should render into entirety or a portion of the Namespace object
```

#### Example

```yaml
tenant: "{{ templates_dir }}/env_templates/dev/tenant.yml.j2"
cloud: "{{ templates_dir }}/env_templates/dev/cloud.yml.j2"
namespaces:
  - template_path: "{{ templates_dir }}/env_templates/dev/Namespaces/bss.yml.j2"
    template_override:
      profile:
        name: prod_bss_override
        baseline: prod
```

In this example, the generated Environment Instance will include a namespace object based on the bss namespace template, with the following attribute values under profile:

```yaml
profile:
  name: prod_bss_override
  baseline: prod
```

This will override any values defined in the original bss.yml.j2 template.
