import my_pexpect
#print my_pexpect.telnet_command_sw('admin','10.12.248.250','123456','show interfaces')
#print my_pexpect.telnet_command_sw('admin','10.12.248.250','123456','show ip interface brief')
print my_pexpect.ssh_command('cisco','10.10.1.243','JCFWnantian2014','show ip interface brief')
