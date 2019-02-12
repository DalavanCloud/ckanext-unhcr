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
        if field['field_name'] not in ['title', 'notes', 'type']:
            field['required'] = False

    # Update `owner_ord`
    for field in schema['dataset_fields']:
        if field['field_name'] == 'owner_org':
            field['validators'] = 'validate_curation_data_container'

    # Add `owner_ord_dest`
    schema['dataset_fields'].append({
        'field_name': 'owner_org_dest',
        'label': 'Target Organization',
        'preset': 'dataset_organization',
        'form_snippet': 'owner_org.html',
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
