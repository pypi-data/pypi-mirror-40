# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import logging

from horizon import exceptions
from openstack_dashboard.api import neutron
from openstack_dashboard.api.neutron import NeutronAPIDictWrapper

LOG = logging.getLogger(__name__)

# initialized by core horizon app
neutronclient = neutron.neutronclient


def check_ext_raise_exc(request):
    """Check if bsn-service-extension for bsn_service_plugin is enabled.

    If not, raise an exception with appropriate message to enabled the
    bsn_service_plugin

    :param request:
    :return: None
    """
    if not neutron.is_extension_supported(request, "bsn-service-extension"):
        raise Exception("bsn_service_plugin extension is not enabled in "
                        "neutron.conf service_plugins. Please update and "
                        "restart neutron server.")


def reachabilitytest_list(request, **params):
    """Return a list of reachability tests under current tenant

    src_tenant and src_segment display strings are patched.
    :param request: request context
    :param params:
    :return: list of NeutronAPIDictWrapper(<test>)
    """
    LOG.debug("reachabilitytest_list(): params=%s", params)
    reachabilitytests = neutronclient(request)\
        .list_reachabilitytests(**params)

    object_list = []
    for obj in reachabilitytests['reachabilitytests']:
        add_tenant_and_segment_display(obj)
        object_list.append(NeutronAPIDictWrapper(obj))

    return object_list


def convert_to_cli(result_detail):
    l = []
    l.append("{0:20} {1:20} {2:50}".format("Path Index", "Hop Index",
                                           "Hop"))
    if result_detail:
        for hop in result_detail:
            l.append("{0:20} {1:20} {2:50}".format(hop["path-index"],
                                                   hop["hop-index"],
                                                   hop["hop-name"]))
    command_line = '\n'.join(l)
    return command_line


def convert_logicalpath_to_cli(result_logical_path):
    l = []
    l.append("{:15s} {:30s} {:30s} {:30s} {:30s} {:30s}".format(
        "Hop Index",
        "Hop",
        "Ingress Interface",
        "Policy",
        "Route",
        "Egress Interface"))

    if result_logical_path:
        for hop in result_logical_path:
            l.append("{:15s} {:30s} {:30s} {:30s} {:30s} {:30s}".format(
                str(hop.get("hop-index", '')),
                hop.get("hop", ''),
                hop.get("ingress-interface-name", ''),
                hop.get("policy", ''),
                hop.get("route", ''),
                hop.get("egress-interface-name", '')))

    command_line = '\n'.join(l)
    return command_line


def add_tenant_and_segment_display(obj):
    """Add src_tenant and src_tenant to obj

    src_tenant:
        eg1. tenant_name (tenant_id)
        eg2. tenant_name (Unknown_ID)
        name can not be empty
    src_segment:
        eg1. segment_name (segment_id)
        eg2. (segment_id)
        eg3. segment_name (Unknown_ID)
        name can be empty
    Adds Unknown_ID in case of upgrade from old Horzion version
    :param obj: obj that contains src_tenant and src_segment info
    :return:
    """
    if not obj.get('src_tenant_id'):
        tenant_id = 'Unknown_ID'
    else:
        tenant_id = obj.get('src_tenant_id')

    if not obj.get('src_segment_id'):
        segment_id = 'Unknown_ID'
    else:
        segment_id = obj.get('src_segment_id')

    obj['src_tenant'] \
        = '%s (%s)' % (obj['src_tenant_name'], tenant_id)

    if obj.get('src_segment_name'):
        obj['src_segment'] \
            = '%s (%s)' % (obj['src_segment_name'], segment_id)
    else:
        obj['src_segment'] \
            = '(%s)' % segment_id


def reachabilitytest_get(request, reachabilitytest_id):
    """Return a reachability test's info

    src_tenant and src_segment display strings are patched.
    :param request: request context
    :param reachabilitytest_id: id of the test
    :return: NeutronAPIDictWrapper(<test>)
    """
    LOG.debug("reachabilitytest_get(): id=%s",
              reachabilitytest_id)
    reachabilitytest = neutronclient(request)\
        .show_reachabilitytest(reachabilitytest_id)\
        .get('reachabilitytest')
    # add field command_line to put CLI representation
    reachabilitytest['command_line'] = \
        convert_to_cli(reachabilitytest['detail'])
    # field for CLI repr of logical-path
    reachabilitytest['logical_path_cli'] = convert_logicalpath_to_cli(
        reachabilitytest['logical_path'])

    add_tenant_and_segment_display(reachabilitytest)

    return NeutronAPIDictWrapper(reachabilitytest)


def reachabilitytest_create(request, **params):
    """Create a reachability test.

    :param request: request context
    :param tenant_id: (optional) tenant id of the reachability test created
    :param name: name of the reachability test
    :param src_tenant_id: source tenant id
    :param src_tenant_name: source tenant name
    :param src_segment_id: source segment id
    :param src_segment_name: source segment name
    :param src_ip: source ip of the reachability test
    :param dst_ip: destination ip of the reachability test
    :param expected_result: expected result of the reachability test
    """
    LOG.debug("reachabilitytest_create(): params=%s", params)
    try:
        check_ext_raise_exc(request)
        if 'tenant_id' not in params:
            params['tenant_id'] = request.user.project_id
        body = {'reachabilitytest': params}
        reachabilitytest = neutronclient(request) \
            .create_reachabilitytest(body) \
            .get('reachabilitytest')
        return NeutronAPIDictWrapper(reachabilitytest)

    except Exception as e:
        msg = e.message
        exceptions.handle(request, msg, escalate=True)


def reachabilitytest_update(request, reachabilitytest_id, **params):
    """Update a reachability test.

    :param request: request context
    :param tenant_id: (optional) tenant id of the reachability test modified
    :param name: name of the reachability test
    :param src_tenant_id: source tenant id
    :param src_tenant_name: source tenant name
    :param src_segment_id: source segment id
    :param src_segment_name: source segment name
    :param src_ip: source ip of the reachability test
    :param dst_ip: destination ip of the reachability test
    :param expected_result: expected result of the reachability test
    :param run_test: boolean flag to run the test
    """
    LOG.debug("reachabilitytest_update(): params=%s", params)
    try:
        if 'tenant_id' in params:
            LOG.debug("Removing tenant_id from params, it cannot be changed")
            params.pop('tenant_id')
        if 'id' in params:
            LOG.debug("Removing id from params, it cannot be changed")
            params.pop('id', None)
        body = {'reachabilitytest': params}
        reachabilitytest = neutronclient(request)\
            .update_reachabilitytest(reachabilitytest_id, body)\
            .get('reachabilitytest')
        return NeutronAPIDictWrapper(reachabilitytest)

    except Exception as e:
        msg = e.message
        exceptions.handle(request, msg, escalate=True)


def reachabilitytest_delete(request, reachabilitytest_id):
    LOG.debug("reachabilitytest_delete(): reachabilitytest_id=%s",
              reachabilitytest_id)
    neutronclient(request).delete_reachabilitytest(reachabilitytest_id)


def networktemplate_list(request, **params):
    LOG.debug("networktemplate_list(): params=%s", params)
    networktemplates = neutronclient(request)\
        .list_networktemplates(**params)
    object_list = [NeutronAPIDictWrapper(obj)
                   for obj in networktemplates['networktemplates']]
    return object_list


def networktemplate_get(request, networktemplate_id):
    LOG.debug("networktemplate_get(): networktemplate_id=%s",
              networktemplate_id)
    networktemplate = neutronclient(request)\
        .show_networktemplate(networktemplate_id)\
        .get('networktemplate')
    return NeutronAPIDictWrapper(networktemplate)


def networktemplate_create(request, **params):
    """Create a network template.

    :param request: request context
    :param tenant_id: (optional) tenant id of the network template created
    :param name: name of the network template
    :param body: body of the network template
    """
    LOG.debug("networktemplate_create(): params=%s", params)
    check_ext_raise_exc(request)
    if 'tenant_id' in params:
        LOG.debug("Removing tenant_id from params, "
                  "not present in network template")
        params.pop('tenant_id', None)
    # remove id when creating object. it is autogenerated
    if 'id' in params:
        LOG.debug("Removing id from params, it cannot be changed")
        params.pop('id', None)
    body = {'networktemplate': params}
    networktemplate = neutronclient(request)\
        .create_networktemplate(body)\
        .get('networktemplate')
    return NeutronAPIDictWrapper(networktemplate)


def networktemplate_update(request, networktemplate_id, **params):
    """Update a network template.

    :param request: request context
    :param networktemplate_id: id of the network template
    :param tenant_id: (optional) tenant id of the network template updated
    :param name: name of the network template
    :param body: body of the network template
    """
    LOG.debug("networktemplate_update(): params=%s", params)
    # cannot update tenant_id
    if 'tenant_id' in params:
        LOG.debug("Removing tenant_id from params, "
                  "not present in network template")
        params.pop('tenant_id')
    # remove id when modifying object. it cannot be changed
    if 'id' in params:
        LOG.debug("Removing id from params, it cannot be changed")
        params.pop('id', None)
    body = {'networktemplate': params}
    networktemplate = neutronclient(request)\
        .update_networktemplate(networktemplate_id, body)\
        .get('networktemplate')
    return NeutronAPIDictWrapper(networktemplate)


def networktemplate_delete(request, networktemplate_id):
    LOG.debug("networktemplate_delete(): networktemplate_id=%s",
              networktemplate_id)
    neutronclient(request).delete_networktemplate(networktemplate_id)


def networktemplateassignment_list(request, **params):
    LOG.debug("networktemplateassignment_list(): params=%s", params)
    networktemplateassignments = neutronclient(request)\
        .list_networktemplateassignments(**params)
    assignlist = \
        [NeutronAPIDictWrapper(obj)
         for obj in networktemplateassignments['networktemplateassignments']]
    return assignlist


def networktemplateassignment_get(request, networktemplateassignment_id):
    LOG.debug("networktemplateassignment_get(): id=%s",
              networktemplateassignment_id)
    networktemplateassignment = neutronclient(request)\
        .show_networktemplateassignment(networktemplateassignment_id)\
        .get('networktemplateassignment')
    return NeutronAPIDictWrapper(networktemplateassignment)


def networktemplateassignment_delete(request, networktemplateassignment_id):
    LOG.debug("networktemplateassignment_delete(): networktemplate_id=%s",
              networktemplateassignment_id)
    neutronclient(request)\
        .delete_networktemplateassignment(networktemplateassignment_id)


def networktemplateassignment_update(request,
                                     networktemplateassignment_id,
                                     **params):
    """Update a network template assignemnt.

    :param request: request context
    :param networktemplate_id: id of the network template
    :param tenant_id: (optional) tenant id of the network template updated
    :param stack_id: id of the heat stack
    """
    LOG.debug("networktemplateassignment_update(): id=%s params=%s",
              networktemplateassignment_id,
              params)
    # cannot update tenant_id
    if 'tenant_id' in params:
        LOG.debug("Removing tenant_id from params, it cannot be changed")
        params.pop('tenant_id')
    # remove id when modifying object. it cannot be changed
    if 'id' in params:
        LOG.debug("Removing id from params, it cannot be changed")
        params.pop('id', None)
    body = {'networktemplateassignment': params}
    networktemplateassignment = neutronclient(request)\
        .update_networktemplateassignment(networktemplateassignment_id, body)\
        .get('networktemplateassignment')
    return NeutronAPIDictWrapper(networktemplateassignment)


def networktemplateassignment_create(request, **params):
    """Create a network template.

    :param request: request context
    :param tenant_id: (optional) tenant id of the user
    :param template_id: ID of the network template
    :param stack_id: ID of the heat stack
    """
    LOG.debug("networktemplateassignment_create(): params=%s", params)
    check_ext_raise_exc(request)
    if 'tenant_id' not in params:
        params['tenant_id'] = request.user.project_id
    # remove id when creating object. it is autogenerated
    if 'id' in params:
        LOG.debug("Removing id from params, it cannot be changed")
        params.pop('id', None)
    body = {'networktemplateassignment': params}
    networktemplateassignment = neutronclient(request)\
        .create_networktemplateassignment(body)\
        .get('networktemplateassignment')
    return NeutronAPIDictWrapper(networktemplateassignment)


def reachabilityquicktest_list(request, **params):
    """Return a list of reachability quick tests under current tenant

    src_tenant and src_segment display strings are patched.
    :param request: request context
    :param params:
    :return: list of NeutronAPIDictWrapper(<quick_test>)
    """
    LOG.debug("reachabilityquicktest_list(): params=%s", params)
    reachabilityquicktests = neutronclient(request)\
        .list_reachabilityquicktests(**params)

    object_list = []
    for obj in reachabilityquicktests['reachabilityquicktests']:
        add_tenant_and_segment_display(obj)
        object_list.append(NeutronAPIDictWrapper(obj))

    return object_list


def reachabilityquicktest_get(request, reachabilityquicktest_id):
    """Return a quick test info

    src_tenant and src_segment display strings are patched.
    :param request: request context
    :param reachabilityquicktest_id: id of the quick test
    :return: NeutronAPIDictWrapper(<quick_test>)
    """
    LOG.debug("reachabilityquicktest_get(): id=%s",
              reachabilityquicktest_id)
    reachabilityquicktest = neutronclient(request)\
        .show_reachabilityquicktest(reachabilityquicktest_id)\
        .get('reachabilityquicktest')
    # add field command_line to put CLI representation
    reachabilityquicktest['command_line'] = \
        convert_to_cli(reachabilityquicktest['detail'])

    add_tenant_and_segment_display(reachabilityquicktest)

    return NeutronAPIDictWrapper(reachabilityquicktest)


def reachabilityquicktest_create(request, **params):
    """Create a reachability quick test.

    :param request: request context
    :param tenant_id: (optional) tenant id of the reachability quick test
    :param name: name of the reachability test
    :param src_tenant_id: source tenant id
    :param src_tenant_name: source tenant name
    :param src_segment_id: source segment id
    :param src_segment_name: source segment name
    :param src_ip: source ip of the reachability test
    :param dst_ip: destination ip of the reachability test
    :param expected_result: expected result of the reachability test
    """
    LOG.debug("reachabilityquicktest_create(): params=%s", params)
    try:
        check_ext_raise_exc(request)
        if 'tenant_id' not in params:
            params['tenant_id'] = request.user.project_id
        body = {'reachabilityquicktest': params}
        reachabilityquicktest = neutronclient(request)\
            .create_reachabilityquicktest(body)\
            .get('reachabilityquicktest')
        return NeutronAPIDictWrapper(reachabilityquicktest)
    except Exception as e:
        msg = e.message
        exceptions.handle(request, msg, escalate=True)


def reachabilityquicktest_update(request, reachabilityquicktest_id, **params):
    """Update a reachability quick test.

    :param request: request context
    :param tenant_id: (optional) tenant id of the reachability test modified
    :param name: name of the reachability test
    :param src_tenant_id: source tenant id
    :param src_tenant_name: source tenant name
    :param src_segment_id: source segment id
    :param src_segment_name: source segment name
    :param src_ip: source ip of the reachability test
    :param dst_ip: destination ip of the reachability test
    :param expected_result: expected result of the reachability test
    :param run_test: boolean flag to run the test
    """
    LOG.debug("reachabilityquicktest_update(): params=%s", params)
    try:
        if 'tenant_id' in params:
            LOG.debug("Removing tenant_id from params, it cannot be changed")
            params.pop('tenant_id')
        if 'id' in params:
            LOG.debug("Removing id from params, it cannot be changed")
            params.pop('id', None)
        body = {'reachabilityquicktest': params}
        reachabilityquicktest = neutronclient(request)\
            .update_reachabilityquicktest(reachabilityquicktest_id, body)\
            .get('reachabilityquicktest')
        return NeutronAPIDictWrapper(reachabilityquicktest)
    except Exception as e:
        msg = e.message
        exceptions.handle(request, msg, escalate=True)


def reachabilityquicktest_delete(request, reachabilityquicktest_id):
    LOG.debug("reachabilityquicktest_delete(): reachabilitytest_id=%s",
              reachabilityquicktest_id)
    neutronclient(request).delete_reachabilityquicktest(
        reachabilityquicktest_id)


def tenantpolicy_list(request, **params):
    LOG.debug("tenantpolicy_list(): params=%s", params)
    tenantpolicies = neutronclient(request).list_tenantpolicies(**params)
    object_list = [NeutronAPIDictWrapper(obj)
                   for obj in tenantpolicies['tenantpolicies']]
    return object_list


def tenantpolicy_get(request, tenantpolicy_id):
    LOG.debug("tenantpolicy_get(): id=%s", tenantpolicy_id)
    tenantpolicy = (neutronclient(request)
                    .show_tenantpolicy(tenantpolicy_id)
                    .get('tenantpolicy'))
    return NeutronAPIDictWrapper(tenantpolicy)


def tenantpolicy_create(request, **params):
    """Create a tenant policy.

    :param request: request context
    :param tenant_id: (optional) tenant id of the reachability test created
    :param priority:
    :param source: source IP or range
    :param source_port: (optional)
    :param destination: destination IP or range
    :param destination_port: (optional)
    :param protocol: (optional) TCP or UDP
    :param action: permit or deny
    :param nexthops: [] list of nexthop IPs
    """
    LOG.debug("tenantpolicy_create(): params=%s", params)
    check_ext_raise_exc(request)
    if 'tenant_id' not in params:
        params['tenant_id'] = request.user.project_id
    body = {'tenantpolicy': params}
    tenantpolicy = (neutronclient(request)
                    .create_tenantpolicy(body)
                    .get('tenantpolicy'))
    return NeutronAPIDictWrapper(tenantpolicy)


def tenantpolicy_update(request, tenantpolicy_id, **params):
    """Update a tenant policy.

    :param request: request context
    :param tenant_id: (optional) tenant id of the reachability test created
    :param priority:
    :param source: source IP or range
    :param source_port: (optional)
    :param destination: destination IP or range
    :param destination_port: (optional)
    :param protocol: (optional) TCP or UDP
    :param action: permit or deny
    :param nexthops: [] list of nexthop IPs
    """
    LOG.debug("tenantpolicy_update(): params=%s", params)
    if 'tenant_id' in params:
        LOG.debug("Removing tenant_id from params, it cannot be changed")
        params.pop('tenant_id')
    if 'id' in params:
        LOG.debug("Removing id from params, it cannot be changed")
        params.pop('id', None)
    body = {'tenantpolicy': params}
    tenantpolicy = (neutronclient(request)
                    .update_tenantpolicy(tenantpolicy_id, body)
                    .get('tenantpolicy'))
    return NeutronAPIDictWrapper(tenantpolicy)


def tenantpolicy_delete(request, tenantpolicy_id):
    LOG.debug("tenantpolicy_delete(): tenantpolicy_id=%s", tenantpolicy_id)
    neutronclient(request).delete_tenantpolicy(tenantpolicy_id)
