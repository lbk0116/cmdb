# -*- coding: utf-8 -*-

import json,sys
import urllib2,requests
import cookielib
from urllib import urlencode
import os
import traceback
import logging
from lxml import etree
import re
#from .. import my_pexpect

'''
Show version*
Show ip interface brief*
Show module 只出现一部分数据没有全部出来*
Show interface*
show interface status*
Show inventory*
Show cdp neighbors/Show cdp neighbor

Show arp/show ip arp
show mac address-table
show mac address-table count
Show interface trunk / show environment temperature 可以使用,有数据，但是xml没有数据无法匹配,show redundancy status  可以使用,有数据，但是xml没有数据无法匹配
Show port-channel summary ／ 可以执行，没数据

／Show standby/show hsrp／show ip eigrp neighbor／Show vpc roles／无效的命令
／Show vpc／Show failover ／Show xlate／show resource usage／show access-list <acl_name> brief 无效命令
/show vpc peer_keepalive/Show pvc 无效命令
show nameif
show environment fan*
show ip route *
show ip ospf neighbor*
show spanning-tree summary*
show spanning-tree summary totals *没找到需要的数据,需要的数据在show spanning-tree summary*中就能找到
show fex 没开启服务

show vdc *
Show vdc resource*
show redundancy status  可以使用,有数据，但是xml没有数据无法匹配
show license usage*
show environment power*
show resource usage 无效命令
'''

def main():
    try:
        # file_object = open('/Users/yu/Desktop/od/server/pexpect_sh/ycmd_log/show_redundancy_status.txt','r')
        file_object = open('D:\odoo\server\pexpect_sh\ycmd_log\show_interface.xml','r')
        html = file_object.read()
        # lines = text.splitlines()
        # 无论哪个平台都以换行为分隔符#三种平台下换行符是不一样的
    except:
        print "Got error! "
    file_object.close()
    return html


def show_version():
    html = main()
    page = etree.HTML(html)
    print type(page)
    print 10 * '*'
    dic = {}
    # 以下是network_management_ip表需要的信息
    # hrefs = page.xpath("//host_name")[0].text  # 取设备名称
    # hrefs = page.xpath("//chassis_id")[0].text  # 取设备型号

    # 以下是Network_software_table表需要的信息
    dic['system_image'] = page.xpath("//san_file_name")[0].text  #
    dic['config_register'] = ' '   # Nexus平台没有config_register值，置为空
    dic['uptime_days'] = page.xpath("//kern_uptm_days")[0].text  #
    dic['uptime_hours'] = page.xpath("//kern_uptm_hrs")[0].text  #
    dic['uptime_minutes'] = page.xpath("//kern_uptm_mins")[0].text  #
    dic['kickstart_image'] = page.xpath("//kick_file_name")[0].text  #
    memory = page.xpath("//memory")[0].text  #
    mem_type = page.xpath("//mem_type")[0].text  #
    bootflash = page.xpath("//bootflash_size")[0].text  #
    dic['memory_size'] = memory + mem_type    #(mb)
    # print memory_size
    dic['bootflash_size'] = bootflash + mem_type   #(MB)
    return dic


def show_ip_interface_brief():
    html = main()
    page = etree.HTML(html)
    print type(page)
    print 10 * '*'
    row_intf = page.xpath("//row_intf")
    count_intf = len(row_intf)
    print count_intf
    interface_name  = []
    interface_ip_address  = []
    interface_line_protocol_status = []
    interface_link_status  = []
    dic = {}
    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        child = row_intf[x].getchildren()
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        interface_name.append(dict.get('intf-name'))
        interface_ip_address.append(dict.get('prefix'))
        interface_line_protocol_status.append(dict.get('proto-state'))
        interface_link_status.append(dict.get('link-state'))
    dic['interface_name'] = interface_name
    dic['interface_ip_address'] = interface_ip_address
    dic['interface_line_protocol_status'] = interface_line_protocol_status
    dic['interface_link_status'] = interface_link_status
    return dic


def show_module(config_text):
    html = main()
    page = etree.HTML(html)
    # print type(page)
    # print 10 * '*'
    # 以下是Network_hardware_table表需要的信息
    row_modinfo = page.xpath("//row_modinfo")
    count_intf = len(row_modinfo)
    print count_intf
    dic = {}
    modinf = []
    portsdic = []
    modtype = []
    model = []
    status = []
    sw = []
    hw = []
    for x in range(count_intf):
        dict = {}
        child = row_modinfo[x].getchildren()
        count_child = len(row_modinfo[x].getchildren())
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        #以下是Network_hardware_table表需要的信息
        modinf.append(dict.get("modinf"))  # 取模块所在槽号
        portsdic.append(dict.get("ports"))  # 取端口数量
        modtype.append(dict.get("modtype"))  # 取模块描述
        model.append(dict.get("model"))  # 取产号品型
        status.append(dict.get("status"))  # 取模块状态
        sw.append(dict.get("sw"))  # 取软件版本
        hw.append(dict.get("hw"))  # 取硬件版本
        #is_pass.append(dict.get(""))#联机检测状态$没有显示
    dic['modinf'] = modinf
    dic['portsdic'] = portsdic
    dic['modtype'] = modtype
    dic['model'] = model
    dic['status'] = status
    dic['sw'] = sw
    dic['hw'] = hw
    #dic['is_pass'] = is_pass
    return dic
    #以下字段服务于Network_inventory_table6表
    #以下是Network_XBAR_table表需要的信息:但是未解出来


def show_interface(config_text):
    html = main()
    page = etree.HTML(html)
    # print type(page)
    # print 10 * '*'
    row_intf = page.xpath("//row_interface")
    count_intf = len(row_intf)
    print count_intf
    interface_name = []
    interface_rate_mode = []
    interface_admin_state = []
    interface_line_protocol_state = []
    interface_ip_address = []  #
    interface_mac_address = []  #
    interface_description_string = []  #
    interface_mtu = []  #
    interface_bandwidth = []  #
    interface_delay = []  #
    interface_reliability = []  #
    interface_txload = []  #
    interface_rxload = []
    interface_speed = []
    interface_duplex = []
    interface_input_flow_control = []
    interface_output_flow_control = []
    interface_input_rate_5_minute = []
    interface_output_rate_5_minute = []
    interface_input_rate_30_second = []
    interface_output_rate_30_second = []
    interface_rx_unicast_packets = []
    interface_rx_multicast_packets = []
    interface_rx_broadcast_packets = []
    interface_rx_input_packets = []
    interface_rx_input_bytes = []
    interface_rx_jumbo_packets = []
    interface_rx_storm_suppression_packets = []
    interface_rx_runts = []
    interface_rx_giants = []
    interface_rx_crc = []
    interface_rx_no_buffer = []
    interface_rx_input_error = []
    interface_rx_short_frame = []
    interface_rx_overrun = []
    interface_rx_underrun = []
    interface_rx_ignored = []
    interface_rx_watchdog = []
    interface_rx_bad_ethertype_drop = []
    interface_rx_bad_protocol_drop = []
    interface_rx_if_down_drop = []
    interface_rx_input_with_dribble = []
    interface_rx_input_discard = []
    interface_rx_rx_pause = []
    interface_tx_unicast_packets = []
    interface_tx_multicast_packets = []
    interface_tx_broadcast_packets = []
    interface_tx_output_packets = []
    interface_tx_output_bytes = []
    interface_tx_jumbo_packets = []
    interface_tx_output_error = []
    interface_tx_collision = []
    interface_tx_deferred = []  #
    interface_tx_late_collision = []  #
    interface_tx_lost_carrier = []  #
    interface_tx_no_carrier = []  #
    interface_tx_babble = []  #
    interface_tx_output_discard = []  #
    interface_tx_tx_pause = []
    dic = {}
    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        interface_name.append(dict.get('interface'))  #
        interface_rate_mode.append(dict.get("eth_mode"))  #
        interface_admin_state.append(dict.get("admin_state"))  #
        interface_line_protocol_state.append(dict.get("state"))  #
        interface_ip_address.append(dict.get("eth_ip_addr"))  #
        interface_mac_address.append(dict.get("eth_hw_addr"))  #
        interface_description_string.append(dict.get("eth_hw_desc"))  #
        interface_mtu.append(dict.get("eth_mtu"))  #
        interface_bandwidth.append(dict.get("eth_bw"))  #
        interface_delay.append(dict.get("eth_dly"))  #
        interface_reliability.append(dict.get("eth_reliability"))  #
        interface_txload.append(dict.get("eth_txload"))  #
        interface_rxload.append(dict.get("eth_rxload"))  #
        interface_speed.append(dict.get("eth_speed"))  #
        interface_duplex.append(dict.get("eth_duplex"))  #
        interface_input_flow_control.append(dict.get("eth_in_flowctrl"))  #
        interface_output_flow_control.append(dict.get("eth_out_flowctrl"))  #
        interface_input_rate_5_minute.append(dict.get("interface"))  #
        interface_output_rate_5_minute.append(dict.get("interface"))  #
        interface_input_rate_30_second.append(dict.get("interface"))  #
        interface_output_rate_30_second.append(dict.get("interface"))  #
        interface_rx_unicast_packets.append(dict.get("eth_inucast"))  #
        interface_rx_multicast_packets.append(dict.get("eth_inmcast"))  #
        interface_rx_broadcast_packets.append(dict.get("eth_inbcast"))  #
        interface_rx_input_packets.append(dict.get("eth_inpkts"))  #
        interface_rx_input_bytes.append(dict.get("eth_inbytes"))  #
        interface_rx_jumbo_packets.append(dict.get("eth_jumbo_inpkts"))  #
        interface_rx_storm_suppression_packets.append(dict.get("eth_storm_supp"))  #
        interface_rx_runts.append(dict.get("eth_runts"))  #
        interface_rx_giants.append(dict.get("eth_giants"))  #
        interface_rx_crc.append(dict.get("eth_crc"))  #
        interface_rx_no_buffer.append(dict.get("eth_nobuf"))  #
        interface_rx_input_error.append(dict.get("eth_inerr"))  #
        interface_rx_short_frame.append(dict.get("eth_frame"))  #
        interface_rx_overrun.append(dict.get("eth_overrun"))  #
        interface_rx_underrun.append(dict.get("eth_underrun"))  #
        interface_rx_ignored.append(dict.get("eth_ignored"))  #
        interface_rx_watchdog.append(dict.get("eth_watchdog"))  #
        interface_rx_bad_ethertype_drop.append(dict.get("eth_bad_eth"))  #
        interface_rx_bad_protocol_drop.append(dict.get("eth_bad_proto"))  #
        interface_rx_if_down_drop.append(dict.get("eth_in_ifdown_drops"))  #
        interface_rx_input_with_dribble.append(dict.get("eth_dribble"))  #
        interface_rx_input_discard.append(dict.get("eth_indiscard"))  #
        interface_rx_rx_pause.append(dict.get("eth_inpause"))  #
        interface_tx_unicast_packets.append(dict.get("eth_outucast"))  #
        interface_tx_multicast_packets.append(dict.get("eth_outmcast"))  #
        interface_tx_broadcast_packets.append(dict.get("eth_outbcast"))  #
        interface_tx_output_packets.append(dict.get("eth_outpkts"))  #
        interface_tx_output_bytes.append(dict.get("eth_outbytes"))  #
        interface_tx_jumbo_packets.append(dict.get("eth_jumbo_outpkt"))  #
        interface_tx_output_error.append(dict.get("eth_outerr"))  #
        interface_tx_collision.append(dict.get("eth_coll"))  #
        interface_tx_deferred.append(dict.get("eth_deferred"))  #
        interface_tx_late_collision.append(dict.get("eth_latecoll"))  #
        interface_tx_lost_carrier.append(dict.get("eth_lostcarrier"))  #
        interface_tx_no_carrier.append(dict.get("eth_nocarrier"))  #
        interface_tx_babble.append(dict.get("eth_babbles"))  #
        interface_tx_output_discard.append(dict.get("eth_outdiscard"))  #
        interface_tx_tx_pause.append(dict.get("eth_outpause"))  #
    dic['interface_name'] = interface_name
    dic['interface_rate_mode'] = interface_rate_mode
    dic['interface_admin_state'] = interface_admin_state
    dic['interface_line_protocol_state'] = interface_line_protocol_state
    dic['interface_ip_address'] = interface_ip_address    #
    dic['interface_mac_address'] = interface_mac_address    #
    dic['interface_description_string'] = interface_description_string    #
    dic['interface_mtu'] = interface_mtu    #
    dic['interface_bandwidth'] = interface_bandwidth    #
    dic['interface_delay'] = interface_delay    #
    dic['interface_reliability'] = interface_reliability    #
    dic['interface_txload'] = interface_txload    #
    dic['interface_rxload'] = interface_rxload
    dic['interface_speed'] = interface_speed
    dic['interface_duplex'] = interface_duplex
    dic['interface_input_flow_control'] = interface_input_flow_control
    dic['interface_output_flow_control'] = interface_output_flow_control
    dic['interface_input_rate_5_minute'] = interface_input_rate_5_minute
    dic['interface_output_rate_5_minute'] = interface_output_rate_5_minute
    dic['interface_input_rate_30_second'] = interface_input_rate_30_second
    dic['interface_output_rate_30_second'] = interface_output_rate_30_second
    dic['interface_rx_unicast_packets'] = interface_rx_unicast_packets
    dic['interface_rx_multicast_packets'] = interface_rx_multicast_packets
    dic['interface_rx_broadcast_packets'] = interface_rx_broadcast_packets
    dic['interface_rx_input_packets'] = interface_rx_input_packets
    dic['interface_rx_input_bytes'] = interface_rx_input_bytes
    dic['interface_rx_jumbo_packets'] = interface_rx_jumbo_packets
    dic['interface_rx_storm_suppression_packets'] = interface_rx_storm_suppression_packets
    dic['interface_rx_runts'] = interface_rx_runts
    dic['interface_rx_giants'] = interface_rx_giants
    dic['interface_rx_crc'] = interface_rx_crc
    dic['interface_rx_no_buffer'] = interface_rx_no_buffer
    dic['interface_rx_input_error'] = interface_rx_input_error
    dic['interface_rx_short_frame'] = interface_rx_short_frame
    dic['interface_rx_overrun'] = interface_rx_overrun
    dic['interface_rx_underrun'] = interface_rx_underrun
    dic['interface_rx_ignored'] = interface_rx_ignored
    dic['interface_rx_watchdog'] = interface_rx_watchdog
    dic['interface_rx_bad_ethertype_drop'] = interface_rx_bad_ethertype_drop
    dic['interface_rx_bad_protocol_drop'] = interface_rx_bad_protocol_drop
    dic['interface_rx_if_down_drop'] = interface_rx_if_down_drop
    dic['interface_rx_input_with_dribble'] = interface_rx_input_with_dribble
    dic['interface_rx_input_discard'] = interface_rx_input_discard
    dic['interface_rx_rx_pause'] = interface_rx_rx_pause
    dic['interface_tx_unicast_packets'] = interface_tx_unicast_packets
    dic['interface_tx_multicast_packets'] = interface_tx_multicast_packets
    dic['interface_tx_broadcast_packets'] = interface_tx_broadcast_packets
    dic['interface_tx_output_packets'] = interface_tx_output_packets
    dic['interface_tx_output_bytes'] = interface_tx_output_bytes
    dic['interface_tx_jumbo_packets'] = interface_tx_jumbo_packets
    dic['interface_tx_output_error'] = interface_tx_output_error
    dic['interface_tx_collision'] = interface_tx_collision
    dic['interface_tx_deferred'] = interface_tx_deferred    #
    dic['interface_tx_late_collision'] = interface_tx_late_collision    #
    dic['interface_tx_lost_carrier'] = interface_tx_lost_carrier    #
    dic['interface_tx_no_carrier'] = interface_tx_no_carrier    #
    dic['interface_tx_babble'] = interface_tx_babble    #
    dic['interface_tx_output_discard'] = interface_tx_output_discard    #
    dic['interface_tx_tx_pause'] = interface_tx_tx_pause    #
    return dic #以下是Network_platform_interface_info_table5表需要的信息


def show_interface_status(config_text):
    html = main()
    page = etree.HTML(html)
    # print type(page)
    # print 10 * '*'
    row_intf = page.xpath("//row_interface")
    count_intf = len(row_intf)
    print count_intf
    dic = {}
    interface = []
    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        interface.append(dict.get('type'))
    dic['interface'] = interface
    return dic


def show_inventory(config_text):
    html = main()
    page = etree.HTML(html)
    # print type(page)
    # print 10 * '*'
    row_intf = page.xpath("//row_inv")
    count_intf = len(row_intf)
    print count_intf
    dic = {}
    product_id = []
    product_serial_number = []
    product_decription = []

    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        product_id.append(dict.get("productid"))
        product_serial_number.append(dict.get("serialnum"))
        product_decription.append(dict.get("desc"))
    dic['product_id'] = product_id
    dic['product_serial_number'] = product_serial_number
    dic['product_decription'] = product_decription
    return dic


def show_environment_fan(config_text):
    html = main()
    page = etree.HTML(html)
    # print type(page)
    # print 10 * '*'
    row_intf = page.xpath("//row_faninfo")
    fan_filter_status = page.xpath("//fan_filter_status")
    count_intf = len(row_intf)
    print count_intf
    dic = {}
    fan = []
    fan_model = []
    fan_status = []
    fan_air_filter = []

    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        child = row_intf[x].getchildren()
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        fan.append(dict.get("fanname"))
        fan_model.append(dict.get("fanmodel"))
        fan_status.append(dict.get("fanstatus"))
        fan_air_filter.append(fan_filter_status[0].text)#这是共有信息
    dic['fan'] = fan
    dic['fan_model'] = fan_model
    dic['fan_status'] = fan_status
    dic['fan_air_filter'] = fan_air_filter
    return dic


def show_ip_route(config_text):
    html = main()
    page = etree.HTML(html)

    row_prefix = page.xpath("//row_prefix")
    row_path = page.xpath("//row_path")
    #print row_path
    count_prefix = len(row_prefix)
    #print count_prefix

    dic = {}
    route_type = []  # 没找到
    route_subnet = []
    route_metric = []
    route_next_hop = []
    route_interface = []
    for x in range(count_prefix):
        dict = {}
        dict1 = {}
        child_prefix = row_prefix[x].getchildren()
        count_prefix = len(row_prefix[x].getchildren())

        child_path = row_path[x].getchildren()
        count_path = len(row_path[x].getchildren())
        #print count_path
        for y in range(count_prefix):
            dict[child_prefix[y].tag] = child_prefix[y].text
        for z in range(count_path):
            dict[child_path[z].tag] = child_path[z].text

        route_type.append(dict.get(""))#没找到
        route_subnet .append(dict.get("ipprefix"))
        pref = dict.get("pref")
        metric = dict.get("metric")
        route_metric.append(pref + '/'+metric)
        route_next_hop.append(dict.get("ipnexthop"))
        route_interface.append(dict.get("ifname"))
    dic['route_type'] = route_type  # 没找到
    dic['route_subnet'] = route_subnet
    dic['route_metric'] = route_metric
    dic['route_next_hop'] = route_next_hop
    dic['route_interface'] = route_interface
    return dic


#以下这种情况会出现想要的信息没有tag,所以会用None代替
def show_ip_ospf_neighbor(config_text):
    #以下字段服务于Network_OSPF_neighbor_table18表
    html = main()
    page = etree.HTML(html)

    row_intf = page.xpath("//row_nbr")
    count_intf = len(row_intf)
    print count_intf
    dic= {}
    ospf_neighbor_router_id = []
    ospf_priority = []
    ospf_neighbor_state = []
    ospf_neighbor_ip_address = []
    ospf_local_interface_name = []
    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        child = row_intf[x].getchildren()
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        ospf_neighbor_router_id.append(dict.get("rid"))
        ospf_priority.append(dict.get("priority"))
        ospf_neighbor_state.append(dict.get("state"))
        ospf_neighbor_ip_address.append(dict.get("addr"))
        ospf_local_interface_name.append(dict.get("intf"))
    dic['ospf_neighbor_router_id'] = ospf_neighbor_router_id
    dic['ospf_priority'] = ospf_priority
    dic['ospf_neighbor_state'] = ospf_neighbor_state
    dic['ospf_neighbor_state'] = ospf_neighbor_ip_address
    dic['ospf_local_interface_name'] = ospf_local_interface_name
    return dic


def show_spanning_tree_summary(config_text):
    html = main()
    page = etree.HTML(html)
    dic = {}

    #以下字段服务于Network_STP_summary_table21这个表
    dic['stp_mode'] = page.xpath("//stp-mode")[0].text
    dic['root_bridge_for_vlans'] = page.xpath("//tree_root_bmp")[0].text
    dic['port_type_default'] = page.xpath("//port_fast")[0].text
    dic['bpdu_guard_default'] = page.xpath("//bpdu_guard")[0].text
    dic['bpdu_filter_default'] = page.xpath("//bpdu_filter")[0].text
    dic['bridge_assurance'] = page.xpath("//bridge_assurance")[0].text
    dic['loopguard_default'] = page.xpath("//oper_loopguard")[0].text
    dic['pathcost_method_used'] = page.xpath("//oper_pcost_method")[0].text
    #以下字段服务于Network_stp_logical_ports28这个表
    dic['stp_summary_totals'] = page.xpath("//oper_pcost_method")[0].text
    return dic


def show_vdc(config_text):
    html = main()
    page = etree.HTML(html)
    row_intf = page.xpath("//row_vdc")
    count_intf = len(row_intf)
    print count_intf
    dic = {}
    vdc_id =[]
    vdc_name = []
    vdc_state = []
    vdc_supported_linecard = []
    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        child = row_intf[x].getchildren()
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        vdc_id.append(dict.get("vdc_id"))
        vdc_name.append(dict.get("vdc_name"))
        vdc_state.append(dict.get("state"))
        vdc_supported_linecard.append(dict.get("lc-support"))
    dic['vdc_id'] = vdc_id
    dic['vdc_name'] = vdc_name
    dic['vdc_state'] = vdc_state
    dic['vdc_supported_linecard'] = vdc_supported_linecard
    return dic



#这个表已经匹配完需要补充上
def show_vdc_resource(config_text):
    html = main()
    page = etree.HTML(html)
    row_intf = page.xpath("//row_resource")
    count_intf = len(row_intf)
    print count_intf
    dic = {}
    resource_type = []
    vdc_name = []
    resource_allocated_minimum_value = []
    resource_allocated_max_value = []
    used_value = []
    available_value = []
    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        child = row_intf[x].getchildren()
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        resource_type.append(dict.get("resource_name"))
        vdc_name.append(dict.get(""))
        resource_allocated_minimum_value.append(dict.get(""))
        resource_allocated_max_value.append(dict.get(""))
        used_value.append(dict.get(""))
        available_value.append(dict.get(""))
    dic['resource_type'] = resource_type
    dic['vdc_name'] = vdc_name
    dic['resource_allocated_minimum_value'] = resource_allocated_minimum_value
    dic['resource_allocated_max_value'] = resource_allocated_max_value
    dic['used_value'] = used_value
    dic['available_value'] = available_value
    return dic



#正则表达式匹配
def show_redundancy_status(config_text):
    str = main()
    print str
    dic = {}

    dic['administrative_redundancy_mode'] = re.compile('administrative:(.*?)\n').findall(str)[0].strip()

    dic['operational_redundancy_mode'] = re.compile('operational:(.*?)\n').findall(str)[0].strip()#
    pattern3= re.compile('this(.*?)other',re.s).findall(str)[0].strip()#
    dic['this_supervisor']= re.compile(r'supervisor [\(（](.*?)[\)）]').findall(pattern3)[0]#
    dic['this_supervisor_redundancy_state']= re.compile(r'redundancy state:(.*?)\n').findall(pattern3)[0].strip()#
    dic['this_supervisor_state']= re.compile(r'Supervisor state:(.*?)\n').findall(pattern3)[0].strip()#

    pattern4 = re.compile('Other(.*?)System',re.S).findall(str)[0].strip()#(.*?)是非贪心算法匹配到第一个返回结果，(.*)是贪心算法匹配到最多的字符串
    dic['other_supervisor']= re.compile(r'supervisor [\(（](.*?)[\)）]').findall(pattern4)#
    dic['other_supervisor_redundancy_state']= re.compile(r'Redundancy state:(.*?)\n').findall(pattern4)#
    dic['other_supervisor_state']= re.compile(r'Supervisor state:(.*?)\n').findall(pattern4)#
    return dic


def show_license_usage(config_text):
    html = main()
    page = etree.HTML(html)
    row_intf = page.xpath("//row_show_lic_usage")
    count_intf = len(row_intf)
    print count_intf
    dic = {}
    license_feature = []
    license_installed = []
    license_status = []
    license_expiry_date = []
    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        child = row_intf[x].getchildren()
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        license_feature.append(dict.get("feature_name"))
        license_installed.append(dict.get("lic_installed"))
        license_status.append(dict.get("status"))
        license_expiry_date.append(dict.get("expiry_date"))
    dic['license_feature'] = license_feature
    dic['license_installed'] = license_installed
    dic['license_status'] = license_status
    dic['license_expiry_date'] = license_expiry_date
    return dic


def show_environment_power(config_text):
    html = main()
    page = etree.HTML(html)
    # print type(page)
    # print 10 * '*'

    # Network_Environment_Power_Summary_Table30
    Configured_Redundancy_Mode = page.xpath("//ps_redun_mode")
    Operational_Redundancy_Mode = page.xpath("//ps_oper_mode")  #
    Power_Configured_mode_compared_with_operational_mode = '否'  #
    Power_total_Capacity = page.xpath("//tot_pow_capacity")  #
    Power_Available = page.xpath("//available_pow")  #
    Power_available_percentage = '40%'  #

    #Network_ Environment_module_Power_Supply_Table31
    row_intf = page.xpath("//row_mod_pow_info")
    count_intf = len(row_intf)
    print count_intf
    dict_total = {}
    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        child = row_intf[x].getchildren()
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        module_number = dict.get("modnum")
        module_model = dict.get("mod_model")
        module_power_allocated = dict.get("watts_alloced")
        module_power_status = dict.get("modstatus")
        print dict

    #Network_ Environment_Power_Supply_Table32
    row_intf = page.xpath("//row_psinfo")
    count_intf = len(row_intf)
    print count_intf
    dict_total = {}
    for x in range(count_intf):
        dict = {}
        child = row_intf[x].getchildren()
        count_child = len(row_intf[x].getchildren())
        child = row_intf[x].getchildren()
        for y in range(count_child):
            dict[child[y].tag] = child[y].text
        power_supply_number = dict.get("psnum")
        power_supply_model = dict.get("psmodel")
        power_supply_total_capacity = dict.get("watts")#####不确定是这个
        power_supply_status = dict.get("ps_status")
        print dict



if __name__ == "__main__":
    res = show_interface()
    print res