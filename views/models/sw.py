# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models

# 设备管理地址与设备名称对照表
class network_management_ip(models.Model):
    _name = 'cmdb.network_management_ip'

    type = fields.Selection([('ilo','ilo'),('hardware','hardware'),('software','software')])
    device_id = fields.Many2one('cmdb.device',string='设备')
    os_instance_id = fields.Many2one('cmdb.os_instance',string='关联的操作系统实例')
    manage_ip = fields.Char(string='管理地址')
    manage_interface = fields.Char(string='管理接口')

# class network_ip_address(models.Model):
#     _name = 'cmdb.network_ip_address'
#
#     name = fields.Char(string=u"设备名称")
#
#
# 设备交换矩阵信息表
class xbar(models.Model):
    _name = 'cmdb.xbar'
    os_instance_id = fields.Many2one('cmdb.os_instance',string='关联软件实例')
    number = fields.Integer(string='xbar号')
    module_type = fields.Char(string='类型')
    model = fields.Char(string='板卡')
    status = fields.Char(string='状态')

#接口状态及接口信息统计表
class interface_info(models.Model):
    _name = 'cmdb.interface_info'

    os_id = fields.Many2one('cmdb.os_instance', string='关联的设备')
    interface_name = fields.Char()
    module_model= fields.Char()
    module_type =fields.Char()
    sfp_type = fields.Char()
    rate_mode = fields.Char()
    admin_state = fields.Char()
    line_protocol_state = fields.Char()
    ip = fields.Char()
    mac = fields.Char()
    desc = fields.Char()
    mtu = fields.Char()
    bandwidth = fields.Char()
    delay= fields.Char()
    txload = fields.Char()
    rxload = fields.Char()
    speed = fields.Char()
    duplex = fields.Char()
    input_flow_control = fields.Char()
    output_flow_control = fields.Char()
    input_rate_5_minute= fields.Char()
    output_rate_5_minute = fields.Char()
    input_rate_30_second = fields.Char()
    output_rate_5_second = fields.Char()
    rx_unicast_packets = fields.Char()
    rx_multicast_packets = fields.Char()
    rx_broadcast_packets = fields.Char()
    rx_input_packets = fields.Char()
    rx_input_bytes= fields.Char()
    rx_jumbo_packets= fields.Char()
    rx_storm_suppression_packets= fields.Char()
    rx_runts= fields.Char()
    rx_giants= fields.Char()
    rx_CRC= fields.Char()
    rx_no_buffer = fields.Char()
    rx_input_error = fields.Char()
    rx_short_frame = fields.Char()
    rx_overrun = fields.Char()
    rx_underrun= fields.Char()
    rx_ignored= fields.Char()
    rx_watchdog = fields.Char()
    rx_bad_ethertype_drop= fields.Char()
    rx_bad_protocol_drop= fields.Char()
    rx_if_down_drop = fields.Char()
    rx_input_with_dribble= fields.Char()
    rx_input_discard= fields.Char()
    rx_pause= fields.Char()
    tx_unicast_packets = fields.Char()
    tx_multicast_packets = fields.Char()
    tx_broadcast_packets= fields.Char()
    tx_output_packets= fields.Char()
    tx_output_bytes= fields.Char()
    tx_jumbo_packets= fields.Char()
    tx_output_error= fields.Char()
    tx_collision= fields.Char()
    tx_deferred= fields.Char()
    tx_late_collision= fields.Char()
    tx_lost_carrier= fields.Char()
    tx_no_carrier= fields.Char()
    tx_babble= fields.Char()
    tx_output_discard = fields.Char()
    tx_Tx_pause = fields.Char()
# class inventory(models.Model):
#     _name = 'cmdb.inventory'
#     device_id = fields.Many2one('cmdb.ne', string='设备')
#     Product_id = fields.Char()
#     Product_serial_number = fields.Char()
#     Product_decription = fields.Char()
# class network_software_table(models.Model):
#     _name = 'cmdb.network_software_table'
#     device_id = device_id = fields.Many2one('cmdb.ne', string='设备')
#     system_image = fields.Char()
#     config_register = fields.Char()
#     uptime_days = fields.Char()
#     uptime_hours = fields.Char()
#     uptime_minutes = fields.Char()
#     kickstart_image =fields.Char()
#     memory_size = fields.Char()
#     bootflash_size = fields.Char()

# 设备邻接表
class neighbor(models.Model):
    _name = 'cmdb.neighbor'

    os_id = fields.Many2one('cmdb.os_instance', string='关联的设备')
    local_interface = fields.Char(string='本地接口')
    local_interface_model = fields.Char(string='本地接口所在板卡')
    peer_os_id =fields.Many2one('cmdb.os_instance', string='关联对端设备')
    peer_interface = fields.Char(string='对端接口')
    peer_interface_model = fields.Char(string='对端接口所在板卡')

# class network_arptable(models.Model):
#     _name = 'cmdb.network_arptable'
#
#     device_id = fields.Many2one('cmdb.ne', string='设备')
#     interface = fields.Char(string='接口')
#     ip_address = fields.Char(string="IP地址")
#     mac_address = fields.Char(string="MAC地址")
# class network_macaddresstable(models.Model):
#     _name = 'cmdb.network_macaddresstable'
#
#     device_id = fields.Many2one('cmdb.ne', string='设备')
#     interface_type = fields.Char(string='接口类型')
#     interface = fields.Char(string='接口')
#     vlan = fields.Char()
#     mac_address = fields.Char(string='MAC地址')
#     interface_model = fields.Char(string='接口模式')
# class network_mac_arp_table(models.Model):
#     _name = 'cmdb.network_mac_arp_table'
#
#     pass
#  Allowed_vlan表
class trunk_allowed_vlan(models.Model):
    _name = 'cmdb.trunk_allowed_vlan'

    os_id = fields.Many2one('cmdb.os_instance', string='关联的设备')
    local_trunk_interface = fields.Char()
    native_vlan = fields.Char()
    local_allowed_vlans = fields.Char()
    peer_os_id = fields.Many2one('cmdb.os_instance', string='关联的设备')
    peer_trunk_interface = fields.Char()
    peer_allowed_vlans = fields.Char()
    consistency = fields.Boolean()
    is_cisco = fields.Boolean()
# VPC设备主备关系表
class vpc_peergroup(models.Model):
    _name = 'cmdb.vpc_peergroup'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    local_vpc_role_priority= fields.Char(string='本端VPC role priority')
    local_vpc_role = fields.Char(string='本端VPC role')
    local_vpc_domain_id = fields.Char(string='本端VPC domain id')
    local_peer_status = fields.Char(string='本端peer status')
    local_vpc_sum = fields.Char()
    local_keep_alive_status = fields.Char(string='本端keep-alive status')
    local__peer_link_ = fields.Char(string='本端vpc peer_link接口')
    peer_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    peer_vpc_role_priority = fields.Char(string='对端VPC role priority')
    peer_vpc_role = fields.Char(string='对端VPC role')
    peer_vpc_domain_id = fields.Char(string='对端VPC domain id')
    peer_status = fields.Char(string='对端peer status')
    peer_keep_alive_status = fields.Char(string='对端keep-alive status')
    peer_vpc_sum = fields.Char(string='对端Number of vPCs configured')
    peer_vpc_peer_link = fields.Char(string='对端vpc peer_link接口')
#HSRP信息表
class hsrp(models.Model):
    _name = 'cmdb.hsrp'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    vlan = fields.Char()
    group_number = fields.Char()
    version = fields.Char()
    active_ip_address = fields.Char()
    standby_ip_address = fields.Char()
    vip_address = fields.Char()
    active_priority = fields.Char()
    standby_priority = fields.Char()
    hello_timer = fields.Char()
    hold_timer = fields.Char()
    active_preempt = fields.Char()
    active_delaytime = fields.Char()
    standby_preempt = fields.Char()
    standby_delaytime = fields.Char()
    peer_os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')

#port_channel表
class port_channel(models.Model):
    _name = 'cmdb.network_port_channel'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    channel_number = fields.Char(string='隧道号')
    peer_os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    tag = fields.Char(string='标记')
    state = fields.Char(string='状态')
    protocol= fields.Char(string='协议类型')
    type = fields.Char(string='类别')
    mode = fields.Char(string='类型')
    child_sum = fields.Integer(string='成员接口数')
    child01 = fields.Char(string='成员接口1')
    child02 = fields.Char(string='成员接口2')
    child03 = fields.Char(string='成员接口3')
    child04 = fields.Char(string='成员接口4')
    child05 = fields.Char(string='成员接口5')
    child06 = fields.Char(string='成员接口6')
    child07 = fields.Char(string='成员接口7')
    child08 = fields.Char(string='成员接口8')
# class network_route_table(models.Model):
#     _name = 'cmdb.network_route_table'
#
#     device_id = fields.Many2one('cmdb.ne', string='设备')
#     route_type = fields.Char()
#     Route_subnet = fields.Char()
#     Route_metric = fields.Char()
#     Route_next_hop = fields.Char()
#     Route_interface = fields.Char()
#     Route_next_device = fields.Char()
# class network_bgp_neighbor_table(models.Model):
#     _name = 'cmdb.network_bgp_neighbor_table'
#
#     pass
# OSPF邻接表
class ospf_neighbor(models.Model):
    _name = 'cmdbospf_neighbor'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    neighbor_router_ip = fields.Char()
    priority = fields.Integer()
    neighbor_state = fields.Char()
    neighbor_ip_address = fields.Char()
    local_interface_name = fields.Char()
    neighbor_os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
#EIGRP邻接表
class eigrp_neighbor(models.Model):
    _name = 'cmdb.eigrp_neighbor'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    neighbor_ip_address = fields.Char()
    neighbor_local_interface = fields.Char()
    neighbor_os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
#生成树信息表
class stp_summary(models.Model):
    _name = 'cmdb.stp_summary'
    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    stp_mode = fields.Char(string='模式')
    port_type_default = fields.Char(string='端口类型')
    root_bridge_for_vlans = fields.Char()
    bpdu_guard_default = fields.Selection([('enable','enable'),('disable','disable')])
    bpdu_filter_default = fields.Selection([('enable','enable'),('disable','disable')])
    bridge_Assurance  = fields.Selection([('enable','enable'),('disable','disable')])
    loopguard_default  = fields.Selection([('enable','enable'),('disable','disable')])
    pathcost_method_used = fields.Char()

#FEX连接信息表
class fex(models.Model):
    _name = 'cmdb.fex'

    os_instance_id =  fields.Many2one('cmdb.os_instance', string='设备')
    fex_number = fields.Integer(string='fex编号')
    description = fields.Char(string='描述')
    state = fields.Char(string='状态')
    model = fields.Char(string='板卡')
    sn = fields.Char(string='串号')
# VPC状态信息表
class vpc_state(models.Model):
    _name = 'cmdb.vpc_state'

    os_instance_id =  fields.Many2one('cmdb.os_instance', string='设备')
    vpc_id = fields.Integer(string='VPC ID')
    port = fields.Char(string='端口')
    state = fields.Char(string='状态')
    consistency_check = fields.Char(string='一致性检查')
    reason = fields.Char(string='原因')
    active_vlans = fields.Char(string='活动的VLAN')
#VDC状态表
class vdc_state(models.Model):
    _name = 'cmdb.vdc_state'

    os_instance_id =  fields.Many2one('cmdb.os_instance', string='设备')
    name = fields.Char(string='vdc名称')
    vdc_id = fields.Char(string='vdc id')
    state = fields.Char(string='状态')
    supported_linecard = fields.Char(string='支持的行卡')
#VDC资源利用表
class vdc_resource_usage(models.Model):
    _name = 'cmdb.vdc_resource_usage'
    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    resource_type = fields.Char(string='资源类型')
    name  = fields.Char(string='vdc名称')
    resource_allocated_minimum_value = fields.Integer(string='资源分配最小值')
    resource_allocated_max_value= fields.Integer(string='资源分配最大值')
    used_value = fields.Integer(string='已使用')
    available_value = fields.Integer(string='可用')

# 引擎冗余信息表
class redundancy_state(models.Model):
    _name = 'cmdb.redundancy_state'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    administrative_redundancy = fields.Char()
    operational_redundancy = fields.Char()
    this_supervisor = fields.Char()
    this_supervisor_redundancy_state = fields.Char()
    this_supervisor_state = fields.Char()
    other_supervisor = fields.Char()
    other_supervisor_redundancy_state = fields.Char()
    other_supervisor_state = fields.Char()
# license信息表
class license_status(models.Model):
    _name = 'cmdb.license_status'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    license_feature = fields.Char(string='功能')
    License_installed = fields.Boolean(string='是否安装')
    License_status = fields.Char(string='状态')
    License_expiry_date = fields.Date(string='过期日期')

#生成树logical ports数量信息表
class stp_logical_port(models.Model):
    _name = 'stp_logical_port'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    logical_ports_available = fields.Integer(string='支持的逻辑端口总数')
    logical_ports_current = fields.Integer(string='当前活动的逻辑端口数量')
    logical_ports_current_percentage  =fields.Float(string='当前活动的逻辑端口数量百分比')
#MAC地址数量信息表
class mac_address_count(models.Model):
    _name = 'cmdb.mac_address_count'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    mac_available = fields.Integer(string='支持的MAC总数量')
    mac_current = fields.Integer(string='当前活动MAC数量')
    mac_current_percentage = fields.Float(string='当前活动的MAC数量百分比')
#环境电源使用情况表
class environment_power_summary(models.Model):
    _name = 'cmdb.environment_power_summary'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    configured_redundancy = fields.Char(string='配置的冗余模式')
    operational_redundancy  = fields.Char(string='实际的冗余模式')
    is_normal = fields.Boolean(string='冗余模式是否正常')
    power_total = fields.Integer(string='总支持电源瓦特数量')
    Power_available  = fields.Integer(string='已使用电源瓦特数')
    Power_available_percentage= fields.Float(string='已使用百分比')

#环境电源模块状态表
class environment_module_power_supply(models.Model):
    _name = 'cmdb.environment_module_power_supply'

    os_instance_id = fields.Many2one('cmdb.os_instance', string='设备')
    module_number = fields.Integer(string='板卡编号')
    module_model = fields.Char(string='板卡')
    module_power_allocated = fields.Integer(string='板卡分配的瓦特数')
    module_power_status = fields.Char(string='状态')

#环境电源输入表
class environmet_power_supply(models.Model):
    _name = 'cmdb.environmet_power_supply'

    os_instance_id =  fields.Many2one('cmdb.os_instance', string='设备')
    power_supply_number = fields.Integer(string='电源编号')
    Power_supply_model = fields.Char(string='板卡')
    power_supply_total_capacity = fields.Char(string= '支持的总瓦数')
    power_supply_status = fields.Char(string='状态')

#环境风扇表
class environment_fan(models.Model):
    _name = 'cmdb.environment_fan'

    os_instance_id =  fields.Many2one('cmdb.os_instance', string='设备')
    fan = fields.Char(string='风扇编号')
    Fan_model = fields.Char(string='板卡')
    Fan_status = fields.Char(string='状态')
    Fan_air_filter = fields.Char(string='空气过滤状态')

#环境温度表
class environment_temperature(models.Model):
    _name = 'cmdb.environment_temperature'

    os_instance_id =  fields.Many2one('cmdb.os_instance', string='设备')
    module_number = fields.Integer(string='模块编号')
    sensor  = fields.Char(string='传感器')
    major_threshold = fields.Integer(string='最高值')
    minor_threshold = fields.Integer(string='最低值')
    current_temperature = fields.Integer(string='当前温度')
    status = fields.Char(string='状态')
