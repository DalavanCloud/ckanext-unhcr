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


class DepositedDatasetController(toolkit.BaseController):

    def approve(self, id):

        # Check access and get dataset
        _raise_not_authz_or_not_deposited(id)
        pkg_dict = get_core.package_show({'model': model}, {'id': id})

        # Change to regural dataset
        pkg_dict = helpers.convert_deposited_dataset_to_regular_dataset(pkg_dict)

        # Update package
        # TODO: Validation errors are impossible here for normal flow
        # We also set type in context to allow type switching by ckan patch
        context = {'model': model, 'user': toolkit.c.user, 'type': pkg_dict['type']}
        pkg_dict = update_core.package_update(context, pkg_dict)

        # Send approval email
        #  mail_data_container_update_to_user({}, pkg_dict, event='approval')

        # Show flash message and redirect
        toolkit.h.flash_success('Datasest "{}" is approved'.format(pkg_dict['title']))
        toolkit.redirect_to('deposited-dataset_read', id=id)

    def reject(self, id, *args, **kwargs):

        # Check access and get dataset
        _raise_not_authz_or_not_deposited(id)
        pkg_dict = get_core.package_show({'model': model}, {'id': id})

        # Send rejection email
        #  mail_data_container_update_to_user({}, pkg_dict, event='rejection')

        # Purge rejected dataset
        delete_core.dataset_purge({'model': model}, {'id': id})

        # Show flash message and redirect
        toolkit.h.flash_error('Datasest "{}" is rejected'.format(pkg_dict['title']))
        toolkit.redirect_to('data-container_index')


def _raise_not_authz_or_not_deposited(id):
    depo = helpers.get_data_container_for_depositing()

    # Check dataset exists and it's deposited
    pkg_dict = get_core.package_show({'model': model}, {'id': id})
    if pkg_dict.get('owner_org') == depo['id']:
        raise toolkit.ObjectNotFound('Deposited dataset "%s" not found' % id)

    # Check the user is sysadmin or data curator
    granted = lib_helpers.check_access('sysadmin')
    if not granted:
        granted = lib_helpers.user_in_org_or_group(depo['id'])
    if not granted:
        raise toolkit.ObjectNotFound('Deposited dataset "%s" is forbidden' % id)
