Command used to generate file

```
poetry run datamodel-codegen --snake-case-field --output-model-type pydantic_v2.BaseModel --set-default-enum-member --input-file-type openapi --input src/task_tracker/contract/spec.yaml --output src/task_tracker/contract/spec.py --field-constraints --allow-population-by-field-name --allow-extra-fields
```
