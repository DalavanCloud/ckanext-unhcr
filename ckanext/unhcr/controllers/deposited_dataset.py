import logging
from ckan import model
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as lib_helpers
import ckan.logic.action.get as get_core
import ckan.logic.action.update as update_core
import ckan.logic.action.delete as delete_core
from ckanext.unhcr.mailer import mail_data_container_update_to_user
from ckanext.unhcr import helpers
log = logging.getLogger(__name__)


# Module API

class DepositedDatasetController(toolkit.BaseController):

    def approve(self, id):

        # Get access and check authz
        context = _get_no_authz_context()
        pkg_dict = get_core.package_show(context, {'id': id})
        _raise_not_authz_or_not_deposited(pkg_dict)

        # Change to regural dataset
        pkg_dict = helpers.convert_deposited_dataset_to_regular_dataset(pkg_dict)

        # Update package
        # TODO: Validation errors are impossible here for normal flow
        # We also set type in context to allow type switching by ckan patch
        update_context = _get_no_authz_context(type=pkg_dict['type'])
        pkg_dict = update_core.package_update(update_context, pkg_dict)

        # Send approval email
        #  mail_data_container_update_to_user({}, pkg_dict, event='approval')

        # Show flash message and redirect
        toolkit.h.flash_success('Datasest "{}" is approved'.format(pkg_dict['title']))
        toolkit.redirect_to('deposited-dataset_read', id=id)

    def reject(self, id, *args, **kwargs):

        # Check access and get dataset
        context = _get_no_authz_context()
        pkg_dict = get_core.package_show(context, {'id': id})
        _raise_not_authz_or_not_deposited(pkg_dict)

        # Send rejection email
        #  mail_data_container_update_to_user({}, pkg_dict, event='rejection')

        # Purge rejected dataset
        delete_core.dataset_purge(context, {'id': id})

        # Show flash message and redirect
        toolkit.h.flash_error('Datasest "{}" is rejected'.format(pkg_dict['title']))
        toolkit.redirect_to('data-container_index')


# Internal

def _get_no_authz_context(**patch):
    context = {'model': model, 'user': toolkit.c.user, 'ignore_auth': True}
    context.update(patch)
    return context


def _raise_not_authz_or_not_deposited(pkg_dict):
    depo = helpers.get_data_container_for_depositing()

    # Check dataset exists and it's deposited
    if pkg_dict.get('owner_org') != depo['id']:
        message = 'Deposited dataset "%s" not found' % pkg_dict['id']
        raise toolkit.ObjectNotFound(message)

    # Check the user is sysadmin or data curator
    granted = lib_helpers.check_access('sysadmin')
    if not granted:
        granted = lib_helpers.user_in_org_or_group(depo['id'])
    if not granted:
        message = 'Deposited dataset "%s" is forbidden' % pkg_dict['id']
        raise toolkit.ObjectNotFound(message)
