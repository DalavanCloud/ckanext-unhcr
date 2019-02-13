import json
from collections import OrderedDict


# Module API

INPUT_JSON = 'ckanext/unhcr/schemas/dataset.json'
OUTPUT_JSON = 'ckanext/unhcr/schemas/curated_dataset.json'

def generate_curated_dataset_schema():

    # Read `dataset` schema
    with open(INPUT_JSON) as file:
        schema = OrderedDict(json.load(file))

    # Update dataset type
    schema['dataset_type'] = 'curated-dataset'

    # Remove required flags
    for field in schema['dataset_fields'] + schema['resource_fields']:
        if field['field_name'] not in ['title', 'type']:
            field['required'] = False

    # Handle organization fields
    for index, field in enumerate(list(schema['dataset_fields'])):
        if field['field_name'] == 'owner_org':

            # owner_org
            field['form_snippet'] = None
            field['display_snippet'] = None
            field['required'] = True

            # owner_org_dest
            schema['dataset_fields'].insert(index + 1, {
                'field_name': 'owner_org_dest',
                'label': 'Organization',
                'form_snippet': 'owner_org_dest.html',
                'validators': 'owner_org_validator unicode',
                'required': True,
            })

    # Write `curated-dataset` schema tweaking order
    with open(OUTPUT_JSON, 'w') as file:
        schema['dataset_fields'] = schema.pop('dataset_fields')
        schema['resource_fields'] = schema.pop('resource_fields')
        json.dump(schema, file, indent=4)

    print('Schema for the `curated-dataset` type has been generated')


# Main script

if __name__ == '__main__':
    generate_curated_dataset_schema()
