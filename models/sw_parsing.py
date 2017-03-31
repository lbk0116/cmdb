#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import logging

# 解析show_version命令
def show_version(before):
    # f = open(r'C:\Users\nantian\Desktop\command_result\log.txt', 'r')
    # alllines = f.readlines()
    # f.close()
    _logger = logging.getLogger(__name__)
    _logger.info(before)
    _logger.info('************************************************')
    alllines = before.splitlines()
    show_version_list = []
    days = 0
    hours = 0
    minutes = 0
    kickstart_image = ''
    bootflash_size = ''
	# name=''
    for line in alllines:
        if line:
            name_obj = re.search(r'.*(?=uptime)', line)
            if name_obj:
                name = name_obj.group(0).strip()
                day = re.search(r'(?<= )\d+ (?=day)', line)
                years = re.search(r'(?<= )\d+ (?=year)',line)
                month = re.search(r'(?<= )\d+ (?=month)',line)
                weeks = re.search(r'(?<= )\d+ (?=week)', line)
                hour = re.search(r'(?<= )\d+ (?=hour)', line)
                minute = re.search(r'(?<= )\d+ (?=minute)', line)
                if day:
                    days += int(day.group())
                if years:
                    days += int(years.group())*365
                if month:
                    days += int(month.group())*30
                if weeks:
                    days += int(weeks.group())*7
                if hour:
                    hours += int(hour.group())
                if minute:
                    minutes += int(minute.group())
                    continue
            system_image_obj = re.search(r'(?<=^system image file is ").*(?=")', line, re.IGNORECASE)
            if system_image_obj:
                system_image =system_image_obj.group().strip()
                continue

            config_register_obj = re.search(r'(?<=^Configuration register is ).*', line, re.IGNORECASE)
            if config_register_obj:
                config_register = config_register_obj.group().strip()
                continue
            kickstart_image_obj = re.search(r'(?<=^kickstart image file is: ).*', line, re.IGNORECASE)
            if kickstart_image_obj:
                kickstart_image = kickstart_image_obj.group().strip()
                continue
            memory_size_obj = re.search(r'(?<=with )\d+(?=K.*of memory)', line, re.IGNORECASE)
            if memory_size_obj:
                memory_size = int(memory_size_obj.group())/1024
                print memory_size
                continue
            bootflash_size_obj = re.search(r'(?<=bootflash:)\s+\d+(?= KB)', line, re.IGNORECASE)
            if bootflash_size_obj:
                bootflash_size = int(bootflash_size_obj.group().strip()) / 1024
                print bootflash_size
                continue
            software_obj = re.search(r'(?<=cisco).*?(?= Software)', line, re.IGNORECASE)
            if software_obj:
                software = software_obj.group().strip()
                soft_version_obj = re.search(r'(?<=Version)\s+([0-9\(.\)]+)SE', line, re.IGNORECASE)
                if soft_version_obj:
                    soft_version = soft_version_obj.group(0).strip()
                    continue
    show_version_list.append({'name':name,'days':days,'hours':hours,'minutes':minutes,'software':software,'soft_version':soft_version,'system_image':system_image,'kickstart_image':kickstart_image,'config_register':config_register,'memory_size':memory_size,'bootflash_size':bootflash_size})
    return show_version_list


# 解析show ip interface biref
def show_ip_interface_brief(before):
    # f = open(r'C:\Users\nantian\Desktop\command_result\log1.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    interface = []
    ip_address = []
    ok = []
    method = []
    status = []
    protocol = []
    # 利用正则表达式获取需要信息的行
    for index ,line in enumerate(alllines):
        if index>0:
            list = re.split('\s+', line)
            _logger = logging.getLogger(__name__)
            _logger.info(list)
            _logger.info('************************************************')
            for i in range(len(list)):
                _logger.info(list[i])
            if list[4] == 'administratively':
                list[4] = list[4]+' '+list[5]
                list[5] = list[-1]
                list[-1] = ''
            if '' in list:
                list.remove('')
            if '' in list:
                list.remove('')
            interface.append(list[0])
            ip_address.append(list[1])
            ok.append(list[2])
            method.append(list[3])
            status.append(list[4])
            protocol.append(list[5])
    interface_dict = {'name': interface, 'ip_ids': ip_address, 'ok': ok, 'method': method, 'link_status': status,
                      'line_protocol_status': protocol}
    # print interface_dict
    return interface_dict


def show_neighbor(before):
    # f = open(r'C:\Users\nantian\Desktop\command_result\show_neighbor.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    start_index = len(alllines)
    use_lines = []
    use_line = []
    # 利用正则表达式获取需要信息的行
    for index,line in enumerate(alllines):
        if line:
            if index <= start_index:
                m = re.search('PORT ID',line,re.IGNORECASE)
                if m:
                    start_index = index
                    print 'aaaa',start_index
                    continue
            else:
                use_lines.append(line.split(' '))
    # 将相关信息放在一个列表中
    merge_index = 0
    lines = []
    merge_line = []
    for index, line in enumerate(use_lines):
        if len(line) == 1:
            megre_index = index
            for ele in line:
                merge_line.append(ele.strip())
        elif index == merge_index +1:
            for ele in line:
                if ele:
                    merge_line.append(ele.strip())
            lines.append(merge_line)
            merge_line = []
        else:
            for ele in line:
                if ele:
                    merge_line.append(ele.strip())
            lines.append(merge_line)
            merge_line = []
    # print lines
    # [['FI6120XP-cluster-A(SSI134606F2)', 'Gig', '1/0/3', '178', 'S', 'I', 'N10-S6100', 'Eth', '1/5'], ['sw3', 'Fas',
    #  '1/0/48', '140', 'R', 'S', 'I', 'WS-C3750-', 'Fas', '2/0/27'], ['leaf1(SAL18474KM6)', 'Gig', '1/0/2', '168', 'R',
    #  'S', 'N9K-C9396', 'Eth', '1/9']]
    device_id = []
    local_interface = []
    port_id = []
    platform = []
    for line in lines:
        device_id.append(line[0])
        local_interface.append(line[1]+line[2])
        port_id.append(line[-2]+line[-1])
        platform.append(line[-3])
    print device_id, local_interface, port_id, platform
    return{'peer_device_name': device_id, 'local_interface': local_interface, 'peer_interface': port_id,
           'platform': platform}


def show_interface_trunk(before):
    # f = open(r'C:\Users\nantian\Desktop\command_result\show_interface_trunk.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    start_index1 = len(alllines)
    start_index2 = len(alllines)
    start_index3 = len(alllines)
    native_lines = []
    allowed_lines = []
    # 利用正则表达式获取需要信息的行
    for index ,line in enumerate(alllines):
        if len(line)>1:
            if index < start_index1:
                m = re.search('Native vlan\n',line,re.IGNORECASE)
                if m:
                    start_index1 = index
                    print start_index1
                    continue
            if index<start_index2:
                m = re.search('Vlans allowed on trunk\n', line, re.IGNORECASE)
                if m:
                    start_index2 = index
                    print start_index2
                    continue
            if index < start_index3:
                m = re.search('Vlans allowed and active in management domain\n', line, re.IGNORECASE)
                if m:
                    start_index3 = index
                    print start_index3
                    continue
            if index > start_index1 and index < start_index2 -1:
                native_lines.append(re.split('\s\s+',line))
                continue
            if start_index2 < index and index< start_index3-1:
                allowed_lines.append(re.split('\s\s+', line))
                continue
            #print native_lines,allowed_lines
            #将相关信息放在一个列表
            port_native_vlans=[]
            port_allowed_vlans = []
            for line in native_lines:
                if line:
                    port_native_vlans.append([line[0].strip(),line[4].strip()])
            for line in allowed_lines:
                if line:
                    port_allowed_vlans.append([line[0].strip(), line[1].strip()])
    local_trunk_interface = []
    native_vlan = []
    local_allowed_vlans = []

    for index in range(len(port_native_vlans)):
        # print port_native_vlans[index]
        local_trunk_interface.append(port_native_vlans[index][0])
        native_vlan.append(port_native_vlans[index][1])
        local_allowed_vlans.append(port_allowed_vlans[index][1])
    # print len(port_native_vlans),len(port_allowed_vlans)
    # print port_native_vlans
    # print port_allowed_vlans
    # str = "Po1       to-aci-leaf01&03-p notconnect   unassigned   auto   auto"
    # str1 = "Gi1/0/4   to-aci-leaf03-port notconnect   1            auto   auto 10/100/1000BaseTX SFP"
    # str2 = "Fa1/0/1                      connected    1          a-full  a-100 10/100BaseTX"
    # str3='Fa1/0/47  to-usc-mini-FI5324 connected    1          a-full  a-100 10/100BaseTX'
    # print re.findall(r"(^.*(?= ))\s{1,3}(\s+|[a-z,A-Z,0-9,&,-]+)\s+([a-z]+)\s+([a-z,0-9]+)\s+([a-z,-]+)\s+([a-z,0-9,-]+){0,1}\s*([a-z,A-Z,0-9,/,\s]+){0,1}",str1)
    # ["Fa1/0/35                     connected    1          a-full  a-100 10/100BaseTX", "Fa1/0/35", "                 ", "connected", "1", "a-full", "a-100", "10/100BaseTX"]
    return {'local_trunk_interface': local_trunk_interface, 'native_vlan': native_vlan, 'local_allowed_vlans': local_allowed_vlans}


def show_ip_route(before):
    # f = open(r'C:\Users\nantian\Desktop\command_result\show_ip_route.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    route_subnet = []
    route_metric = []
    route_next_hop = []
    route_interface = []
    masks = []
    # 利用正则表达式获取需要信息的行
    count = 0
    for i in range(len(alllines)):
        if count:
            count = count - 1
            continue
        subnets = 0
        if len(alllines[i]) > 1:
            subnets_obj = re.search(r'(?<=,).*(?=subnets)',alllines[i])
            if subnets_obj:
                subnets = subnets_obj .group().strip()
                line_mask_obj=re.search(r'(?<=)[\d+.]+(?= is)',alllines[i])
                if line_mask_obj:
                    mask=line_mask_obj.group().strip()
            if subnets:
                count = int(subnets)
                for j in range(int(subnets)):
                    contains_ip = re.findall(r'(([0-9]+(?:\.[0-9]+){3}/*\d*) is directly connected,\s(.*))|(([0-9]+(?:\.[0-9]+){3}/*\d*)\s([0-9,\[,\],/]+)\svia\s(.*))', alllines[i+1+j])
                    if contains_ip:
                        if contains_ip[0][1]:
                            # route_subnet.append(contains_ip[0][1])
                            route_metric.append('')
                            route_next_hop.append('')
                            route_interface.append(contains_ip[0][2])
                            if '/'in contains_ip[0][1]:
                                ip_mask = contains_ip[0][1].split('/')
                                route_subnet.append(ip_mask[0])
                                masks.append(ip_mask[1])
                            else:
                                route_subnet.append(contains_ip[0][1])
                                masks.append(mask)

                        else:
                            # route_subnet.append(contains_ip[0][-3])
                            route_metric.append(contains_ip[0][-2])
                            route_next_hop.append(contains_ip[0][-1])
                            route_interface.append('')
                            if '/'in contains_ip[0][-3]:
                                ip_mask = contains_ip[0][-3].split('/')
                                route_subnet.append(ip_mask[0])
                                masks.append(ip_mask[1])
                            else:
                                route_subnet.append(contains_ip[0][-3])
                                masks.append(mask)
                        # print contains_ip
            else:
                contains_ip = re.findall(r'(([0-9]+(?:\.[0-9]+){3}/*\d*) is directly connected,\s(.*))|(([0-9]+(?:\.[0-9]+){3}/*\d*)\s([0-9,\[,\],/]+)\svia\s(.*))', alllines[i])
                if contains_ip:
                        if contains_ip[0][1]:
                            # route_subnet.append(contains_ip[0][1])
                            route_metric.append('')
                            route_next_hop.append('')
                            route_interface.append(contains_ip[0][2])
                            if '/'in contains_ip[0][1]:
                                ip_mask = contains_ip[0][1].split('/')
                                route_subnet.append(ip_mask[0])
                                masks.append(ip_mask[1])
                            else:
                                route_subnet.append(contains_ip[0][1])
                                masks.append(mask)
                        else:
                            # route_subnet.append(contains_ip[0][-3])
                            route_metric.append(contains_ip[0][-2])
                            route_next_hop.append(contains_ip[0][-1])
                            route_interface.append('')
                            if '/'in contains_ip[0][-3]:
                                ip_mask = contains_ip[0][-3].split('/')
                                route_subnet.append(ip_mask[0])
                                masks.append(ip_mask[1])
                            else:
                                route_subnet.append(contains_ip[0][-3])
                                masks.append(mask)
                        # print contains_ip
    # print route_interface,route_metric ,route_next_hop
    # print route_subnet
    # print masks
    # print len(route_interface), len(route_metric), len(route_next_hop), len(route_subnet)
    return {'dst_ip': route_subnet, 'dst_netmask': masks, 'interface_id': route_interface, 'metric': route_metric, 'next_hop': route_next_hop}


def show_spanning_tree_summary(before):
    # f = open(r'C:\Users\nantian\Desktop\command_result\show_spanning_tree_summary.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    root_brige = []
    port_type_default = []
    bpdu_guard_default = []
    bridge_assurance = ['']
    bpdu_filter_default = []
    loopguard_default = ''
    pathcost_method_used = ''
    # 利用正则表达式获取需要信息的行
    stp_mode = []
    for index ,line in enumerate(alllines):
        if len(line)>1:
            m = re.search('(?<=^switch is in).*(?= mode)',line,re.IGNORECASE)
            if m:
                stp_mode.append(m.group().strip())
                continue
            if re.findall('^Root bridge for:\s([a-z,A-Z,0-9,-]+.*)', line, re.IGNORECASE):
                sub = re.compile('([a-zA-Z0-9-]+(?=,)|[a-zA-Z0-9-]+$)')
                # root_brige= re.findall('Root bridge for:\s([a-zA-Z0-9,-]+)+.*', line, re.IGNORECASE)
                root_brige = sub.findall(line)
            elif re.findall('^\s+([a-zA-Z0-9-]+)$',line,re.IGNORECASE):
                list1 = re.findall('^\s+([a-zA-Z0-9-]+)$',line,re.IGNORECASE)
                for i in list1:
                    root_brige.append(i)
                print root_brige
            elif re.findall('(?:Portfast Default|Port Type Default)\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE):
                port_type_default = re.findall('^(?:Portfast Default|Port Type Default)\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE)
                print port_type_default
            elif re.findall('BPDU Guard Default\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE):
                bpdu_guard_default = re.findall('^PortFast BPDU Guard Default\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE)
            elif re.findall('BPDU Filter Default\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE):
                bpdu_filter_default = re.findall('^Portfast BPDU Filter Default\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE)
            elif re.findall('Bridge_Assurance\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE):
                bridge_assurance = re.findall('^Bridge_Assurance\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE)
            elif re.findall('Loopguard Default\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE):
                loopguard_default = re.findall('^Loopguard Default\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE)
            elif re.findall('Pathcost method used\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE):
                pathcost_method_used = re.findall('Pathcost method used\s+is\s+([a-zA-Z]+)$', line, re.IGNORECASE)
    return {'stp_mode':stp_mode,'port_type_default':port_type_default,'root_bridge_for_vlans':root_brige,
            'bpdu_guard_default': bpdu_guard_default,'bpdu_filter_default': bpdu_filter_default,
            'bridge_assurance': bridge_assurance, 'loopguard_default': loopguard_default,
            'pathcost_method_used': pathcost_method_used}


def show_spanning_tree_summary_total(before):
    # f = open(r'C:\Users\nantian\Desktop\command_result\show_spanning_tree_summary_totals.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    start_index = len(alllines)
    native_lines = []
    allowed_lines = []
    #利用正则表达式获取需要信息的行
    total_logical_ports = []
    for index ,line in enumerate(alllines):
        if len(line)>1:
            if index<=start_index:
                m = re.search('STP Active',line,re.IGNORECASE)
                if m:
                    start_index=index+2
                    continue
            else:
               if re.split('\s\s+',line):
                   _logger = logging.getLogger(__name__)
                   _logger.info(re.split('\s\s+',line))
                   total_logical_ports.append(int(re.split('\s\s+',line)[-1]))
                   break

    return {'logical_ports_available': total_logical_ports,}


def show_mac_address_table_count(before):
    # f=open(r'C:\Users\nantian\Desktop\command_result\show_mac_address_table_count.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    start_index = len(alllines)

    dynamic_address_count=0
    counts=[]
    for index ,line in enumerate(alllines):
        if len(line)>1:
            if index<=start_index:
                m = re.search('(?<=^Dynamic Address Count)\s+:\s+[0-9]+',line,re.IGNORECASE)
                if m:
                    counts.append(m.group().split(':'))
                    continue
    for count in counts:
        dynamic_address_count += int(count[1].strip())

    return {'mac_current':dynamic_address_count}


def show_mac_address_table(before):
    # f = open(r'C:\Users\nantian\Desktop\command_result\show_mac_address_table.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    start_index = len(alllines)
    use_lines = []
    # 利用正则表达式获取需要信息的行
    for index,line in enumerate(alllines):
        if line:
            if index <= start_index and index < len(alllines)-3:
                m = re.search('Vlan',line,re.IGNORECASE)
                if m:
                    start_index = index+1
                    continue
            elif index < len(alllines)-1:
                use_lines.append(line.split(' '))
    print len(use_lines)
    # 将相关信息放在一个列表中
    lines=[]
    for line in use_lines:
        merage_line=[]
        for ele in line:
            if ele:
                merage_line.append(ele.strip())
        lines.append(merage_line)
    print merage_line
    print len(lines)
    vlan = []
    mac_address = []
    ports = []
    for line in lines:
        vlan.append(line[0])
        mac_address.append(line[1])
        ports.append(line[3])
    return {'vlan_ids':vlan,'mac':mac_address,'interface_id':ports}


def show_ip_arp(before):
    # f=open(r'C:\Users\nantian\Desktop\command_result\show_ip_arp.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    start_index = len(alllines)
    use_lines = []
    use_line = []
    # 利用正则表达式获取需要信息的行
    for index,line in enumerate(alllines):
        if line:
            if index <= start_index:
                m = re.search('Interface',line,re.IGNORECASE)
                if m:
                    start_index = index
                    continue
            else:
                use_lines.append(line.split(' '))
    # 将相关信息放在一个列表中
    lines=[]
    for line in use_lines:
        merage_line=[]
        for ele in line:
            if ele:
                merage_line.append(ele.strip())
        lines.append(merage_line)
    address=[]
    hardware_addr=[]
    interface = []
    for line in lines:
        address.append(line[1])
        hardware_addr.append(line[3])
        interface.append(line[5])
    return{'ip':address,'mac_id':hardware_addr,'interface_id':interface}


def show_interface_status(before):
    # f=open(r'C:\Users\nantian\Desktop\command_result\show_interface_status.txt','r')
    # alllines = f.readlines()
    # f.close()
    alllines = before.splitlines()
    start_index = len(alllines)
    use_lines = []
    use_line = []
    # 利用正则表达式获取需要信息的行
    for inddex ,line in enumerate(alllines):
        if line:
            if inddex < start_index:
                m = re.search('Port',line,re.IGNORECASE)
                if m:
                    start_index = inddex
                    continue
            else:
                # use_lines.append(re.findall(
                #     r"(^.*(?= ))\s{1,7}(\s+|[a-z,A-Z,0-9,&,-]+)\s+([a-z]+)\s+([a-z,0-9]+)\s+([a-z,-]+)\s+([a-z,0-9,-]+){0,1}\s*([a-z,A-Z,0-9,/,\s]+){0,1}",
                #     line))
                use_lines.append(re.findall(
                    r"(^[a-zA-Z0-9/]+)\s{1,7}(\s+|[a-z,A-Z,0-9,&,-]+)\s+([a-z]+)\s+([a-z,0-9]+)\s+([a-z,-]+)\s+([a-z,0-9,-]+){0,1}\s*([a-z,A-Z,0-9,/,\s]+){0,1}",
                    line))
    # 将相关信息放在一个列表
    show_interface_status = []
    for line in use_lines:
        if line:
            print line
            show_interface_status.append({'port':line[0][0].strip().split(' ')[0],'sfp_type':line[0][-1].strip()})
    # print sfp_type
    # print port
    # print show_interface_status
    return show_interface_status


# 接口解析非nexus(测试--6500,3750)
def show_interface(before):
    # file_object = open(r'E:\桌面\logs\B_XDA02_CAM_AS02_22.1.181.250.log', 'r')
    # file_object = open(r'C:\Users\nantian\Desktop\command_result\show_interface.txt', 'r')
    # context = file_object.read()
    # file_object.close()
    context = before
    # pattern = re.compile(r'((?:Fast|Gigabit)[\s|\S]*?swapped out)')
    pattern = re.compile(r'([A-Z][\s|\S]*?swapped out)')
    interfaces = pattern.findall(context)
    datas = []
    for interface in interfaces:
        if interface:
            # interface_name = re.search('(?:^Fast|^Gigabit)Ethernet[0-9/]+', interface, re.I)
            interface_name = re.search('^[A-Z][a-zA-Z-]+[0-9/]+', interface, re.I)
            # 1
            if interface_name:
                # print(interface_name.group().strip())
                data = {}
                # interface_admin_state = re.search(r'(?:^Fast|^Gigabit)Ethernet[0-9/]+\s+is\s+(.*),', interface, re.I)
                interface_admin_state = re.search(r'^[A-Z][a-zA-Z-]+[0-9/]+\s+is\s+(.*),', interface, re.I)
                interface_line_protocol_state = re.search(r'.*line protocol\s+is\s+(.*?)\s', interface, re.I)
                interface_ip_address = re.search(r'Internet address\s+is\s+(.*?)\s', interface, re.I)
                interface_mac_address = re.search(r'.*address\s+is\s+(.*?)\s', interface, re.I)
                interface_description_string = re.search(r'Description:\s+(.*)', interface, re.I)
                interface_mtu = re.search(r'MTU\s+(.*?)\s+bytes,', interface, re.I)
                interface_bandwidth = re.search(r'BW\s+(.*?)\s+Kbit,', interface, re.I)
                interface_delay = re.search(r'DLY\s+(.*?)\s+usec,', interface, re.I)
                interface_reliability = re.search(r'reliability\s+(.*?),', interface, re.I)
                interface_txload = re.search(r'txload\s+(.*?),', interface, re.I)
                interface_rxload = re.search(r'rxload\s+(.*?)\s', interface, re.I)
                interface_speed = re.search(r'.*duplex,\s+(.*?),', interface, re.I)
                interface_duplex = re.search(r'(.*duplex),', interface, re.I)
                interface_input_flow_control = re.search(r'input flow-control is\s+(.*),', interface, re.I)
                interface_output_flow_control = re.search(r'output flow-control is\s+(.*)\s', interface, re.I)
                interface_input_rate_5_minute = re.search(r'5 minute input rate\s+(.*),', interface, re.I)
                interface_output_rate_5_minute = re.search(r'5 minute output rate\s+(.*),', interface, re.I)

                interface_rx_input_packets = re.search(r'\s+(.*)\s+packets input,', interface, re.I)
                interface_rx_input_bytes = re.search(r'packets input,\s+(.*)\s+bytes,', interface, re.I)
                interface_rx_multicast_packets = re.search(r'\((.*)\s+multicasts\)', interface, re.I)
                interface_rx_broadcast_packets = re.search(r'Received\s+(.*)\s+broadcasts\s+', interface, re.I)
                interface_rx_runts = re.search(r'\s+(.*)runts,', interface, re.I)
                interface_rx_giants = re.search(r'runts,\s+(.*)giants,', interface, re.I)
                interface_rx_crc = re.search(r'errors,\s+(.*)\s+CRC,', interface, re.I)
                interface_rx_no_buffer = re.search(r'bytes,\s+(.*)\s+no buffer', interface, re.I)
                interface_rx_input_error = re.search(r'\s+(.*)\s+input errors,', interface, re.I)
                interface_rx_short_frame = re.search(r'CRC,\s+(.*)\s+frame,', interface, re.I)
                interface_rx_overrun = re.search(r'frame,\s+(.*)\s+overrun,', interface, re.I)
                interface_rx_underrun = re.search(r'bytes,\s+(.*)\s+underruns', interface, re.I)
                interface_rx_watchdog = re.search(r'\s+(.*)\s+watchdog,', interface, re.I)
                interface_rx_ignored = re.search(r'overrun,\s+(.*)\s+ignored', interface, re.I)
                interface_rx_input_with_dribble = re.search(r'\s+(.*)\s+input packets with dribble', interface, re.I)
                interface_rx_rx_pause = re.search(r'multicast,\s(.*)\spause input', interface, re.I)

                interface_tx_output_packets = re.search(r'\s+(.*)\s+packets output,', interface, re.I)
                interface_tx_output_bytes = re.search(r'output,\s+(.*)\s+bytes,', interface, re.I)
                interface_tx_output_error = re.search(r'\s+(.*)\s+output errors,', interface, re.I)
                interface_tx_collision = re.search(r'errors,\s+(.*)\s+collisions,', interface, re.I)
                interface_tx_deferred = re.search(r'collision,\s+(.*)\s+deferred', interface, re.I)
                interface_tx_late_collision = re.search(r'babbles,\s+(.*)\s+late collision,', interface, re.I)
                interface_tx_lost_carrier = re.search(r'\s+(.*)\s+lost carrier,', interface, re.I)
                interface_tx_no_carrier = re.search(r'carrier,\s+(.*)\s+no carrier', interface, re.I)
                interface_tx_babble = re.search(r'\s+(.*)\s+babbles,', interface, re.I)
                interface_tx_tx_pause = re.search(r'no carrier,\s+(.*)\s+PAUSE output', interface, re.I)
                # print(interface_delay.group(1))
                # 1
                data['interface_name'] = interface_name.group().strip()
                # 3
                if interface_admin_state:
                    if interface_admin_state.group(1).strip().lower() == "up".lower():
                        data['admin_state'] = interface_admin_state.group(1).strip()
                    else:
                        data['admin_state'] = 'down'
                # 4
                if interface_line_protocol_state:
                    data['line_protocol_state'] = interface_line_protocol_state.group(1).strip()
                # 5
                if interface_ip_address:
                    data['ip'] = interface_ip_address.group(1).strip()
                # 6
                if interface_mac_address:
                    data['mac'] = interface_mac_address.group(1).strip()
                # 7
                if interface_description_string:
                    data['desc'] = interface_description_string.group(1).strip()
                # 8
                if interface_mtu:
                    data['mtu'] = interface_mtu.group(1).strip()
                # 9
                if interface_bandwidth:
                    data['bandwidth'] = interface_bandwidth.group(1).strip()
                # 10
                if interface_delay:
                    data['delay'] = interface_delay.group(1).strip()
                # 11
                if interface_reliability:
                    data['reliability'] = interface_reliability.group(1).strip()
                # 12
                if interface_txload:
                    data['txload'] = interface_txload.group(1).strip()
                # 13
                if interface_rxload:
                    data['rxload'] = interface_rxload.group(1).strip()
                # 14
                if interface_speed:
                    data['speed'] = interface_speed.group(1).strip()
                # 15
                if interface_duplex:
                    data['duplex'] = interface_duplex.group(1).strip()
                # 16
                if interface_input_flow_control:
                    data['input_flow_control'] = interface_input_flow_control.group(1).strip()
                # 17
                if interface_output_flow_control:
                    data['output_flow_control'] = interface_output_flow_control.group(1).strip()
                # 18
                if interface_input_rate_5_minute:
                    data['input_rate_5_minute'] = interface_input_rate_5_minute.group(1).strip()
                # 19
                if interface_output_rate_5_minute:
                    data['output_rate_5_minute'] = interface_output_rate_5_minute.group(1).strip()
                # Interface_RX_input_packets
                if interface_rx_input_packets:
                    data['rx_input_packets'] = interface_rx_input_packets.group(1).strip()
                # Interface_RX_input_bytes
                if interface_rx_input_bytes:
                    data['rx_input_bytes'] = interface_rx_input_bytes.group(1).strip()
                # Interface_RX_multicast_packets
                if interface_rx_multicast_packets:
                    data['rx_multicast_packets'] = interface_rx_multicast_packets.group(1).strip()
                # Interface_RX_broadcast_packets
                if interface_rx_broadcast_packets:
                    data['rx_broadcast_packets'] = interface_rx_broadcast_packets.group(1).strip()
                # Interface_RX_runts
                if interface_rx_runts:
                    data['rx_runts'] = interface_rx_runts.group(1).strip()
                # Interface_RX_giants
                if interface_rx_giants:
                    data['rx_giants'] = interface_rx_giants.group(1).strip()
                # Interface_RX_CRC
                if interface_rx_crc:
                    data['rx_crc'] = interface_rx_crc.group(1).strip()
                # Interface_RX_no_buffer
                if interface_rx_no_buffer:
                    data['rx_no_buffer'] = interface_rx_no_buffer.group(1).strip()
                # Interface_RX_input_error
                if interface_rx_input_error:
                    data['rx_input_error'] = interface_rx_input_error.group(1).strip()
                # Interface_RX_short_frame
                if interface_rx_short_frame:
                    data['rx_short_frame'] = interface_rx_short_frame.group(1).strip()
                # Interface_RX_overrun
                if interface_rx_overrun:
                    data['rx_overrun'] = interface_rx_overrun.group(1).strip()
                # Interface_RX_underrun
                if interface_rx_underrun:
                    data['rx_underrun'] = interface_rx_underrun.group(1).strip()
                # Interface_RX_ignored
                if interface_rx_ignored:
                    data['rx_ignored'] = interface_rx_ignored.group(1).strip()
                # Interface_RX_watchdog
                if interface_rx_watchdog:
                    data['rx_watchdog'] = interface_rx_watchdog.group(1).strip()
                # Interface_RX_input_with_dribble
                if interface_rx_input_with_dribble:
                    data['rx_input_with_dribble'] = interface_rx_input_with_dribble.group(1).strip()
                # Interface_RX_Rx_pause
                if interface_rx_rx_pause:
                    data['rx_pause'] = interface_rx_rx_pause.group(1).strip()
                # Interface_TX_output_packets
                if interface_tx_output_packets:
                    data['tx_output_packets'] = interface_tx_output_packets.group(1).strip()
                # Interface_TX_output_bytes
                if interface_tx_output_bytes:
                    data['tx_output_bytes'] = interface_tx_output_bytes.group(1).strip()
                # Interface_TX_output_error
                if interface_tx_output_error:
                    data['tx_output_error'] = interface_tx_output_error.group(1).strip()
                # Interface_TX_collision
                if interface_tx_collision:
                    data['tx_collision'] = interface_tx_collision.group(1).strip()
                # Interface_TX_deferred
                if interface_tx_deferred:
                    data['tx_deferred'] = interface_tx_deferred.group(1).strip()
                # Interface_TX_late_collision
                if interface_tx_late_collision:
                    data['tx_late_collision'] = interface_tx_late_collision.group(1).strip()
                # Interface_TX_lost_carrier
                if interface_tx_lost_carrier:
                    data['tx_lost_carrier'] = interface_tx_lost_carrier.group(1).strip()
                # Interface_TX_no_carrier
                if interface_tx_no_carrier:
                    data['tx_no_carrier'] = interface_tx_no_carrier.group(1).strip()
                # Interface_TX_babble
                if interface_tx_babble:
                    data['tx_babble'] = interface_tx_babble.group(1).strip()
                # Interface_TX_Tx_pause
                if interface_tx_tx_pause:
                    data['tx_pause'] = interface_tx_tx_pause.group(1).strip()
            datas.append(data)
    # print(len(device.keys()))
    # print(len(interfaces))
    return datas
