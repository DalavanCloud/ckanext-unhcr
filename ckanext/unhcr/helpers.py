import logging
from ckan import model
from ckan.plugins import toolkit
from ckanext.unhcr import utils
log = logging.getLogger(__name__)


def render_tree(top_nodes=None):
    '''Returns HTML for a hierarchy of all data containers'''
    context = {'model': model, 'session': model.Session}
    if not top_nodes:
        top_nodes = toolkit.get_action('group_tree')(
            context,
            data_dict={'type': 'data-container'})
    return _render_tree(top_nodes)


def _render_tree(top_nodes):
    html = '<ul class="hierarchy-tree-top">'
    for node in top_nodes:
        html += _render_tree_node(node)
    return html + '</ul>'


def _render_tree_node(node):
    html = '<a href="/data-container/{}">{}</a>'.format(
        node['name'], node['title'])
    if node['children']:
        html += '<ul class="hierarchy-tree">'
        for child in node['children']:
            html += _render_tree_node(child)
        html += '</ul>'

    if node['highlighted']:
        html = '<li id="node_{}" class="highlighted">{}</li>'.format(
            node['name'], html)
    else:
        html = '<li id="node_{}">{}</li>'.format(node['name'], html)
    return html


def page_authorized():

    if (toolkit.c.controller == 'error' and
            toolkit.c.action == 'document' and
            toolkit.c.code and toolkit.c.code[0] != '403'):
        return True

    # TODO: remove request_reset and perform_reset when LDAP is integrated
    return (
        toolkit.c.userobj or
        (toolkit.c.controller == 'user' and
            toolkit.c.action in [
                'login', 'logged_in', 'request_reset', 'perform_reset',
                'logged_out', 'logged_out_page', 'logged_out_redirect'
                ]))


def get_linked_datasets_for_form(selected_ids=[], exclude_ids=[], context=None, user_id=None):
    context = context or {'model': model}
    user_id = user_id or toolkit.c.userobj.id

    # Prepare search query
    fq_list = []
    get_containers = toolkit.get_action('organization_list_for_user')
    containers = get_containers(context, {'id': user_id})
    for container in containers:
        fq_list.append('owner_org:{}'.format(container['id']))

    # Get search results
    search_datasets = toolkit.get_action('package_search')
    search = search_datasets(context, {
        'fq': ' OR '.join(fq_list),
        'include_private': True,
        'sort': 'organization asc, title asc',
    })

    # Get datasets
    orgs = []
    current_org = None
    selected_ids = selected_ids if isinstance(selected_ids, list) else selected_ids.strip('{}').split(',')
    for package in search['results']:

        if package['id'] in exclude_ids:
            continue
        if package['owner_org'] != current_org:
            current_org = package['owner_org']

            orgs.append({'text': package['organization']['title'], 'children': []})

        dataset = {'text': package['title'], 'value': package['id']}
        if package['id'] in selected_ids:
            dataset['selected'] = 'selected'
        orgs[-1]['children'].append(dataset)

    return orgs


def get_linked_datasets_for_display(value, context=None):
    context = context or {'model': model}

    # Get datasets
    datasets = []
    ids = utils.normalize_list(value)
    for id in ids:
        dataset = toolkit.get_action('package_show')(context, {'id': id})
        href = toolkit.url_for('dataset_read', id=dataset['name'], qualified=True)
        datasets.append({'text': dataset['title'], 'href': href})

    return datasets
