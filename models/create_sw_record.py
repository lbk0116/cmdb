#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmlrpclib
import my_pexpect
import sw_parsing
import sw_parsing_xml
import logging

def connect_create_server(create_model,fields_dict_list):
    url = 'http://10.10.48.90:8069'
    db = 'test'
    username = 'admin'
    password = '1'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    for fields_dict in fields_dict_list:
        # print fields_dict
        models.execute_kw(db, uid, password, create_model, 'create', [fields_dict])


def connect_search_server(search_model, os_id_search_domain):
    url = 'http://10.10.48.90:8069'
    db = 'test'
    username = 'admin'
    password = '1'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return models.execute_kw(db, uid, password, search_model, 'search', [os_id_search_domain], {'limit': 1})


def create_network_management_ip(os_id):
    _logger = logging.getLogger(__name__)
    command1 = 'show version'
    command2 = 'show ip interface brief '
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username,os_id.device_id.manage_ip,os_id.device_id.password,command1)
        _logger.info(text)
        show_version_list = sw_parsing.show_version(before)
        before = my_pexpect.ssh_command(os_id.device_id.username,os_id.device_id.manage_ip,os_id.device_id.password,command2)
        _logger.info(before)
        show_ip_int_brief_list = sw_parsing.show_ip_interface_brief(before)
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,os_id.device_id.password,command1)
        _logger.info(child_after)
        show_version_list = sw_parsing.show_version(child_after)
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,os_id.device_id.password,command2)
        show_ip_int_brief_list = sw_parsing.show_ip_interface_brief(child_after)
    else:
        pass
    # soft = show_version_list['software']   # os_id_search_domain =[['software_id.name','like',soft],['device','=',os_id.device_id.id]]
    # search_model = 'cmdb.os_instance'
    # os_id = connect_search_server(search_model,os_id_search_domain)
    # print show_version_list[0]['name']
    print os_id.device_id.manage_ip
    for i in range(len(show_ip_int_brief_list['name'])):
        if show_ip_int_brief_list['ip_ids'][i] == os_id.device_id.manage_ip:
            manage_interface = show_ip_int_brief_list['name'][i]
            print manage_interface
    fields_dict = {'os_instance_id': os_id.id,'manage_ip': os_id.device_id.manage_ip,'manage_interface': manage_interface,'device_id':os_id.device_id.id,'type':os_id.device_id.ass_type}
    create_model = 'cmdb.network_management_ip'
    fields_dict_list.append(fields_dict)
    connect_create_server(create_model,fields_dict_list)


def create_interface(os_id):
    _logger = logging.getLogger(__name__)
    command = 'show ip interface brief'
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command)
        show_ip_int_brief_list = sw_parsing.show_ip_interface_brief(before)
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,os_id.device_id.password,command)
        show_ip_int_brief_list = sw_parsing.show_ip_interface_brief(child_after)
    else:
        pass
    for i in range(len(show_ip_int_brief_list['name'])):
        _logger.info(show_ip_int_brief_list['link_status'][i])
        fields_dict = {
                       'name': show_ip_int_brief_list['name'][i], 'os_id': os_id.id,
                       'ip_ids': show_ip_int_brief_list['ip_ids'][i],
                       'link_status': show_ip_int_brief_list['link_status'][i],
                       'line_protocol_status': show_ip_int_brief_list['line_protocol_status'][i]
        }

        fields_dict_list.append(fields_dict)

    create_model = 'cmdb.interface'
    connect_create_server(create_model, fields_dict_list)


# def create_xbar(os_id):
#     command = "show module"
#     fields_dict_list = []
#     if os_id.software_id.name == 'IOS':
#         # child = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                os_id.device_id.password, command)
#         # before = child.before
#         show_module_list = sw_parsing.show_module()
#     elif os_id.software_id.name == 'Nexus':
#         # child_after = my_pexpect.telnet_command(os_id.device_id.username,
#                                           os_id.device_id.manage_ip,os_id.device_id.password,command)
#         show_module_list = sw_parsing_xml.show_module()
#     # 等待show module 的数据
#     for i in range(1,len(show_module_list['interface'])):
#         fields_dict = {'number': show_module_list['number'][i],
#                        'os_id': os_id,
#                        'module_type': show_module_list['module_type'][i],
#                        'model': show_module_list['model'][i],
#                        'status': show_module_list['status'][i]
#                        }
#         fields_dict_list.append(fields_dict)
#     create_model = 'cmdb.xbar'
#     connect_create_server(create_model, fields_dict_list)


def create_interface_info(os_id):
    command1 = "show interface"
    command2 = "show interface status"
    if os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command2)
        show_interface_status = sw_parsing.show_interface_status(before)
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                        os_id.device_id.password, command1)
        fields_dict_list = sw_parsing.show_interface(before)
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,os_id.device_id.password,command1)
        fields_dict_list = sw_parsing.show_interface(child_after)
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,os_id.device_id.password,command2)
        show_interface_status = sw_parsing.show_interface_status(child_after)

    for line in fields_dict_list:
        for line2 in show_interface_status:
            line_int_name = line['interface_name'].split('/')
            line2_int_name = line2['port'].split('/')
            if line['interface_name'][0] == line2['port'][0] and line2['port'][0] != 'P':

                if line_int_name[1] == line2_int_name[1] and line_int_name[2] == line2_int_name[2]:
                    print line_int_name
                    print line2_int_name
                    line['sfp_type'] = line2['sfp_type']
                # print line['interface_name']
                    continue
        line['os_instance_id']= os_id.id
    create_model = 'cmdb.interface_info'
    connect_create_server(create_model, fields_dict_list)


def create_neighbor(os_id):
    command = "show cdp neighbors"
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command)
        show_neighbor_list = sw_parsing.show_neighbor(before)   # 等待show module 的数据
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,
                                                os_id.device_id.password,command)
        show_neighbor_list = sw_parsing.show_neighbor(child_after)

    for i in range(len(show_neighbor_list['local_interface'])):
        device_name = show_neighbor_list['peer_device_name']
        search_model = 'cmdb.os_instance'
        os_id_search_domain = [['device_id.name','=',device_name]]
        peer_os_id = connect_search_server(search_model, os_id_search_domain)

        fields_dict = {
                       'local_interface': show_neighbor_list['local_interface'][i],
                       'os_instance_id': os_id.id,
                       'local_interface_model': '' ,
                       'peer_os_id': peer_os_id,
                       'peer_interface': show_neighbor_list['peer_interface'][i],
                       'peer_interface_model': ''}
        fields_dict_list.append(fields_dict)
    create_model = 'cmdb.neighbor'
    connect_create_server(create_model, fields_dict_list)


def create_arp(os_id):
    command = "show ip arp"
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command)
        show_arp_list = sw_parsing.show_ip_arp(before)   # 等待show module 的数据
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,
                                                os_id.device_id.password,command)
        show_arp_list = sw_parsing.show_ip_arp(child_after)

    for i in range(len(show_arp_list['ip'])):
        # device_name = show_neighbor_list['peer_device_name']
        # search_model = 'cmdb.os_instance'
        # os_id_search_domain = [['device_id.name','=',device_name]]
        # peer_os_id = connect_search_server(search_model, os_id_search_domain)

        fields_dict = {
                       'ip': show_arp_list['ip'][i],
                       'os_instance_id': os_id.id,
                       'mac_id':show_arp_list['mac_id'][i] ,
                       'interface_id': show_arp_list['interface_id'][i],
                       }
        fields_dict_list.append(fields_dict)
    create_model = 'cmdb.arp'
    connect_create_server(create_model, fields_dict_list)


def create_mac(os_id):
    command = "show mac address-table"
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command)
        show_mac_list = sw_parsing.show_mac_address_table(before)   # 等待show module 的数据
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,
                                                os_id.device_id.password,command)
        show_arp_list = sw_parsing.show_mac_address_table()

    for i in range(len(show_mac_list['interface_id'])):
        # device_name = show_neighbor_list['peer_device_name']
        # search_model = 'cmdb.os_instance'
        # os_id_search_domain = [['device_id.name','=',device_name]]
        # peer_os_id = connect_search_server(search_model, os_id_search_domain)

        fields_dict = {
                       'interface_id': show_mac_list['interface_id'][i],
                       'os_instance_id': os_id.id,
                       'vlan_ids':show_mac_list['vlan_ids'][i] ,
                       'mac': show_mac_list['mac'][i],
                       }
        fields_dict_list.append(fields_dict)
    create_model = 'cmdb.mac'
    connect_create_server(create_model, fields_dict_list)

def trunk_allowed_vlan(os_id):
    command1 = "show cdp neighbors,"
    command2 = "show interface trunk"
    fields_dict_list = []

    if os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command2)
        show_interface_trunk = sw_parsing.show_interface_trunk(before)
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                    os_id.device_id.password, command1)

        show_neighbor_list = sw_parsing.show_neighbor(before)   # 等待show module 的数据
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,
                                                os_id.device_id.password,command2)
        show_interface_trunk = sw_parsing.show_interface_trunk(child_after)
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,
                                                os_id.device_id.password,command1)
        show_interface_trunk = sw_parsing.show_neighbor(child_after)
    else:
        pass
    for i in range(len(show_interface_trunk['local_trunk_interface'])):
        peer_os_id = ''
        peer_trunk_interface = ''
        peer_allowed_vlans = ''
        is_cisco = False

        for j in range(len(show_neighbor_list['local_interface'])):
            if show_interface_trunk['local_trunk_interface'][i] in show_neighbor_list['local_interface']:
                is_cisco = True
            if show_interface_trunk['local_trunk_interface'][i] == show_neighbor_list['local_interface'][j]:
                peer_trunk_interface = show_neighbor_list['peer_trunk_interface'][j]
                device_name = show_neighbor_list['peer_device_name']
                search_model = 'cmdb.os_instance'
                os_id_search_domain = [['device_id.name','=',device_name]]
                peer_os_id = connect_search_server(search_model, os_id_search_domain)
                if peer_os_id:
                    # before = my_pexpect.ssh_command(peer_os_id.device_id.username, peer_os_id.device_id.manage_ip,
                    #                                peer_os_id.device_id.password, command2)
                    peer_show_interface_trunk = sw_parsing.show_interface_trunk()
                    for k in range(len(peer_show_interface_trunk['local_trunk_interface'])):
                        if peer_trunk_interface ==  peer_show_interface_trunk['local_trunck_interface'][k]:
                            peer_allowed_vlans = peer_show_interface_trunk['local_allowed_vlans'][k]

        if peer_allowed_vlans == show_interface_trunk['local_allowed_vlans'][i]:
            consistency = True
        else:
            consistency = True

        fields_dict = {
                       'os_id': os_id.id,
                       'local_trunck_interface': show_interface_trunk['local_trunk_interface'][i],
                       'native_vlan': show_interface_trunk['native_vlan'][i],
                       'local_allowed_vlans': show_interface_trunk['local_allowed_vlans'][i],
                       'peer_trunk_interface': peer_trunk_interface,
                       'peer_os_id':peer_os_id,
                       'peer_allowed_vlans':peer_allowed_vlans,
                       'consistency':consistency,
                       'is_cisco': is_cisco
                       }
        fields_dict_list.append(fields_dict)
    create_model = 'cmdb.trunk_allowed_vlan'
    connect_create_server(create_model, fields_dict_list)


def create_route(os_id):
    command = "show ip route"
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command)
        show_ip_route_dict = sw_parsing.show_ip_route(before)   # 等待show module 的数据
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,
                                                os_id.device_id.password,command)
        show_ip_route_dict = sw_parsing.show_ip_route(child_after)

    # return {'dst_ip': route_subnet, 'dst_netmask': masks, 'interface_id': route_interface,
    #  'metric': route_metric, 'next_hop': route_next_hop}

    for i in range(len(show_ip_route_dict['dst_ip'])):
        fields_dict = {
                       'dst_ip': show_ip_route_dict['dst_ip'][i],
                       'os_id': os_id.id,
                       'dst_netmask':show_ip_route_dict['dst_netmask'][i] ,
                       'interface_id': show_ip_route_dict['interface_id'][i],
                       'metric': show_ip_route_dict['metric'][i],
                       'next_hop': show_ip_route_dict['next_hop'][i],
                       }
        fields_dict_list.append(fields_dict)
    create_model = 'cmdb.route'
    connect_create_server(create_model, fields_dict_list)


# def create_vpcgroup(os_id):
#     # Show vpc 无效的命令 xml
#     pass
#
#
# def create_hsrp(os_id):
#     # Show standby/show hsrp 无效的命令 xml
#     # Show ip interface brief
#
#     pass
#
#
# def create_port_channel(os_id):
#     # Show cdp neighbor 对端设备名称 无效的命令 xml
#     # Show port-channel summary
#     pass
#
#
# # def create_bgp_neighbor(os_id):
# #     pass
#
#
def create_ospf_neighbor(os_id):
    # show ip ospf neighbor
    command = "show ip ospf neighbor"
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'ssh':
         pass # 等待show module 的数据
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,
                                                os_id.device_id.password,command)
        show_ip_ospf_neighbor = sw_parsing.show_ip_ospf_neighbor(child_after)
    for i in len(show_ip_ospf_neighbor['port_type_default']):
        fields_dict = {
                       'neighbor_router_id': show_ip_ospf_neighbor['neighbor_router_id'][i],
                       'os_instance_id': os_id,
                       'priority': show_ip_ospf_neighbor['priority'][i],
                       'neighbor_state':show_ip_ospf_neighbor['neighbor_state'][i],
                       'neighbor_ip_address': show_ip_ospf_neighbor['neighbor_ip_address'][i],
                       'local_interface_name': show_ip_ospf_neighbor['local_interface_name'][i],

                       }
        fields_dict_list.append(fields_dict)
    create_model = 'cmdb.stp_summary'
    connect_create_server(create_model,fields_dict_list)


# def create_eigrp_neighbor(os_id):
#     # show ip eigrp neighbor 无效的命令
#     pass
#
#
def create_stp_summary(os_id):
    command = "show spanning-tree summary"
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command)
        show_spanning_tree_summary = sw_parsing.show_spanning_tree_summary(before)   # 等待show module 的数据
    elif os_id.software_id.manage_mode == 'telnet':
        child_after = my_pexpect.telnet_command_sw(os_id.device_id.username,os_id.device_id.manage_ip,
                                                os_id.device_id.password,command)
        show_spanning_tree_summary = sw_parsing.show_spanning_tree_summary(child_after)
    for i in range(len(show_spanning_tree_summary['port_type_default'])):
        fields_dict = {
                       'stp_mode': show_spanning_tree_summary['stp_mode'],
                       'os_instance_id': os_id.id,
                       'port_type_default': show_spanning_tree_summary['port_type_default'][i],
                       'root_bridge_for_vlans': show_spanning_tree_summary['root_bridge_for_vlans'][i],
                       'bpdu_guard_default': show_spanning_tree_summary['bpdu_guard_default'][i],
                       'bpdu_filter_default': show_spanning_tree_summary['bpdu_filter_default'][i],
                       'bridge_assurance': show_spanning_tree_summary['bridge_assurance'][i],
                       'loopguard_default': show_spanning_tree_summary['loopguard_default'][i],
                       'pathcost_method_used': show_spanning_tree_summary['pathcost_method_used'][i],
                       }
        fields_dict_list.append(fields_dict)
    create_model = 'cmdb.stp_summary'
    connect_create_server(create_model,fields_dict_list)


# vdc_state - VDC状态表#加一个os_id.method # 获取配置文件的方法
# def create_vdc_state(os_id):
#     command_a = "show vdc state"
#     command_b = "show vdc state | xml | nomore"
#     fields_dict_list = []
#     if os_id.software_id.manage_mode == 'telnet':
#         # command = command_b
#         # child_config = my_pexpect.telnet_command_sw(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                os_id.device_id.password, command)
#         # dict = sw_parsing.show_vdc_state(child_config)
#         pass
#
#     elif os_id.software_id.manage_mode == 'ssh':
#         # command = command_a
#         # child = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                os_id.device_id.password, command)
#         # before = child.before
#         # dict = sw_parsing.show_vdc_state()
#         pass
    # for i in range(len(dict['vdc_name'])):
    #     fields_dict = {
    #                    'name': dict['vdc_name'][i],
    #                    'os_id': os_id,
    #                    'vdc_id': dict['vdc_id'][i],
    #                    'state': dict['vdc_state'][i],
    #                    'supported_linecard': dict['vdc_supported_linecard'][i],
    #                    }
    #     fields_dict_list.append(fields_dict)
    # create_model = 'cmdb.vdc_state'
    # connect_create_server(create_model, fields_dict_list)


# vdc_resource_usage - VDC资源利用表
# def create_vdc_resource_usage(os_id):
#     command_a = "show vdc resource"
#     command_b = "show vdc resource | xml | nomore"
#     fields_dict_list = []
#     if os_id.software_id.manage_mode == 'telnet':
#         command = command_b
          # child_config = my_pexpect.telnet_command_sw(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                os_id.device_id.password, command)
#         dict = sw_parsing_xml.show_vdc_resource()
#     elif os_id.software_id.manage_mode == 'ssh':
#         command = command_a
#         # child = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                os_id.device_id.password, command)
#         # before = child.before
#         # dict = sw_parsing.show_vdc_resource()
#         pass
#     for i in len(dict['vdc_name']):
#         fields_dict = {
#                        'resource_type': dict['resource_type'][i],
#                        'os_id': os_id,
#                        'name': dict['name'][i],
#                        'resource_allocated_minimum_value': dict['resource_allocated_minimum_value'][i],
#                        'resource_allocated_max_value': dict['resource_allocated_max_value'][i],
#                        'used_value': dict['used_value'][i],
#                        'available_value': dict['available_value'][i],
#                        }
#         fields_dict_list.append(fields_dict)
#     create_model = 'cmdb.vdc_resource_usage'
#     connect_create_server(create_model, fields_dict_list)



# redundancy_state - 引擎冗余信息表#加一个os_id.method #获取配置文件的方法
# def create_redundancy_state(os_id):
#     command_a = "show redundancy status"
#     command_b = "show redundancy status | xml | nomore"
#     fields_dict_list = []
#
#     if os_id.software_id.manage_mode == 'telnet':
#         command = command_a
#         # child_config = my_pexpect.telnet_command_sw(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                os_id.device_id.password, command)
#         dict = sw_parsing_xml.show_redundancy_status()
#
#     elif os_id.software_id.manage_mode == 'ssh':
#         command = command_a
#         # child = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                os_id.device_id.password, command)
#         # before = child.before
#         # dict = sw_parsing.show_redundancy_status()
#         pass
#     fields_dict = {
#                    'administrative_redundancy': dict['administrative_redundancy'],
#                    'os_id': os_id,
#                    'operational_redundancy': dict['operational_redundancy'],
#                    'this_supervisor': dict['this_supervisor'],
#                    'this_supervisor_redundancy_state': dict['this_supervisor_redundancy_state'],
#                    'other_supervisor': dict['other_supervisor'],
#                    'other_supervisor_redundancy_state': dict['other_supervisor_redundancy_state'],
#                    'other_supervisor_state': dict['other_supervisor_state'],
#                    }
#     fields_dict_list.append(fields_dict)
#     create_model = 'cmdb.redundancy_state'
#     connect_create_server(create_model, fields_dict_list)
#


# license_status - license信息表
# def create_license_status(os_id):
#     command_a = "show license usage"
#     command_b = "show license usage | xml | nomore"
#     fields_dict_list = []
#
#     if os_id.software_id.manage_mode == 'telnet':
#         command = command_a
#         # child_config = my_pexpect.telnet_command_sw(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                          os_id.device_id.password, command)
#         dict = sw_parsing_xml.show_redundancy_status()
#
#     elif os_id.software_id.manage_mode == 'ssh':
#         command = command_a
#         # child = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                os_id.device_id.password, command)
#         # before = child.before
#         # dict = sw_parsing.show_redundancy_status()
#         pass
#     fields_dict = {
#         'os_instance_id': os_id,
#         'license_feature': dict['license_feature'],
#         'License_installed': dict['License_installed'],
#         'License_status': dict['License_status'],
#         'License_expiry_date': dict['License_expiry_date'],
#     }
#     fields_dict_list.append(fields_dict)
#     create_model = 'cmdb.license_status'
#     connect_create_server(create_model, fields_dict_list)


# 这个他是怎么解出来的
# stp_logical_port - 生成树logical ports数量信息表
def create_stp_logical_port(os_id):
    command = "show spanning-tree summary totals"
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'telnet':
        child_config = my_pexpect.telnet_command_sw(os_id.device_id.username, os_id.device_id.manage_ip,
                                                 os_id.device_id.password, command)
        dict = sw_parsing.show_spanning_tree_summary_total(child_config)

    elif os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command)
        dict = sw_parsing.show_spanning_tree_summary_total(before)
    for i in range(len(dict['logical_ports_available'])):
        fields_dict = {
            'os_instance_id': os_id.id,
            'logical_ports_available': '',
            'logical_ports_current': dict['logical_ports_available'][i],
            'logical_ports_current_percentage': '',
        }
        fields_dict_list.append(fields_dict)
    create_model = 'cmdb.stp_logical_port'
    connect_create_server(create_model, fields_dict_list)


# mac_address_count - MAC地址数量信息表
def create_mac_address_count(os_id):
    command = "show mac address-table count"
    # command_b = "show mac address-table count | xml | nomore"
    fields_dict_list = []
    if os_id.software_id.manage_mode == 'telnet':
            child_config = my_pexpect.telnet_command_sw(os_id.device_id.username, os_id.device_id.manage_ip,
                                                     os_id.device_id.password, command)
            dict = sw_parsing.show_spanning_tree_summary(child_config)

    elif os_id.software_id.manage_mode == 'ssh':
        before = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
                                       os_id.device_id.password, command)
        dict = sw_parsing.show_mac_address_table_count(before)
    # for i in range(len(dict['stp_summary_totals'])):
    fields_dict = {
        'os_instance_id': os_id.id,
        'mac_available': '',
        'mac_current': dict['mac_current'],
        'mac_current_percentage': '',
    }
    fields_dict_list.append(fields_dict)
    create_model = 'cmdb.mac_address_count'
    connect_create_server(create_model, fields_dict_list)


# environment_power_summary - 环境电源使用情况表
# environment_module_power_supply - 环境电源模块状态表
# environment_power_supply - 环境电源输入表
# def create_environment_power_summary(os_id):
#     command = "show environment power"
#     fields_dict_list = []
#     if os_id.software_id.manage_mode == 'telnet':
#         child_config = my_pexpect.telnet_command_sw(os_id.device_id.username, os_id.device_id.manage_ip,
#                                                  os_id.device_id.password, command)
#         dict = sw_parsing_xml.show_environment_power(child_config)
#
#     elif os_id.software_id.manage_mode == 'ssh':
#         child = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
#                                        os_id.device_id.password, command)
#         before = child.before
#         dict = sw_parsing.show_environment_power()
#         pass
#     fields_dict = {
#         'os_instance_id': os_id,
#         'configured_redundancy': dict['configured_redundancy'],
#         'operational_redundancy': dict['operational_redundancy'],
#         'is_normal': dict['is_normal'],
#         'power_total': dict['power_total'],
#         'Power_available': dict['Power_available'],
#         'Power_available_percentage': dict['Power_available_percentage'],
#     }
#     fields_dict_list.append(fields_dict)
#     create_model = 'cmdb.environment_power_summary'
#     connect_create_server(create_model, fields_dict_list)
#
#     for i in len(dict['module_number']):
#         fields_dict = {
#             'os_instance_id': os_id,
#             'module_number': dict['module_number'][i],
#             'module_model': dict['module_model'][i],
#             'module_power_allocated': dict['module_power_allocated'][i],
#             'module_power_status': dict['module_power_status'][i],
#         }
#         fields_dict_list.append(fields_dict)
#     create_model = 'cmdb.environment_module_power_supply'
#     connect_create_server(create_model, fields_dict_list)
#
#     for i in len(dict['power_supply_number']):
#         fields_dict = {
#             'os_instance_id': os_id,
#             'power_supply_number': dict['power_supply_number'][i],
#             'Power_supply_model': dict['Power_supply_model'][i],
#             'power_supply_total_capacity': dict['power_supply_total_capacity'][i],
#             'power_supply_status': dict['power_supply_status'][i],
#         }
#         fields_dict_list.append(fields_dict)
#     create_model = 'ccmdb.environment_power_supply'
#     connect_create_server(create_model, fields_dict_list)
#

# environment_fan - 环境风扇表
# def create_environment_fan(os_id):
#     command_a = "show environment fan"
#     command_b = "show environment fan | xml | nomore"
#     fields_dict_list = []
#
#     if os_id.software_id.manage_mode == 'telnet':
#         # command = command_b
#         # child_config = my_pexpect.telnet_command_sw(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                          os_id.device_id.password, command)
#         dict = sw_parsing_xml.show_environment_fan()
#
#     elif os_id.software_id.manage_mode == 'ssh':
#         command = command_a
#         # child = my_pexpect.ssh_command(os_id.device_id.username, os_id.device_id.manage_ip,
#         #                                os_id.device_id.password, command)
#         # before = child.before
#         # dict = sw_parsing.show_environment_fan()
#         pass
#     for i in len(dict['fan']):
#         fields_dict = {
#             'fan': dict['fan'][i],
#             'Fan_model': dict['Fan_model'][i],
#             'os_id': os_id,
#             'Fan_status': dict['Fan_status'][i],
#             'Fan_air_filter': dict['Fan_air_filter'][i],
#         }
#         fields_dict_list.append(fields_dict)
#     create_model = 'cmdb.environment_fan'
#     connect_create_server(create_model, fields_dict_list)



# #这个已经匹配完需要把代码移植过来
# #environment_temperature - 环境温度表
# def create_environment_temperature(os_id):
#     command_a = "show environment temperature"
#     command_b = "show environment temperature | xml | nomore"
#     fields_dict_list = []
#     pass
#
#
#
# #nat - NAT映射关系表
# def create_nat(os_id):
#     command_a = "Show xlate"
#     command_b = "Show xlate | xml | nomore"
#     fields_dict_list = []
#     pass


def create_all(os_id):
    create_network_management_ip(os_id)
    create_interface(os_id)
    create_interface_info(os_id)
    create_neighbor(os_id)
    trunk_allowed_vlan(os_id)
    create_route(os_id)
    create_stp_summary(os_id)
    create_stp_logical_port(os_id)
    create_mac_address_count(os_id)
    create_arp(os_id)
    create_mac(os_id)
    print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
