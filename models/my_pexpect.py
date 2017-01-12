# -*- coding: utf-8 -*-
import pexpect

def ssh_command(account_name,manage_ip,account_password,command):
    """
       This runs a command on the remote host. This could also be done with the
       pxssh class, but this demonstrates what that class does at a simpler level.
       This returns a pexpect.spawn object. This handles the case when you try to
       connect to a new host and ssh asks you if you want to accept the public key
       fingerprint and continue connecting.
       """
    ssh_newkey = 'Are you sure you want to continue connecting'
    # 为 ssh 命令生成一个 spawn 类的子程序对象.
    child = pexpect.spawn('ssh -l %s %s %s' % (account_name,manage_ip,command),maxread=2000)
    #child.send('\n')
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
    # 如果登录超时，打印出错信息，并退出.
    if i == 0:  # Timeout
        print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        return None
    # 如果 ssh 没有 public key，接受它.
    if i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        child.expect('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0:  # Timeout
            print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        return None
    # 输入密码.
    child.sendline(account_password)
    return child

def telnet_command(account_name,manage_ip,account_password,command):
    # 即将 telnet 所要登录的远程主机的域名
    #ipAddress = '10.10.1.187 32790'
    # 登录用户名
    #loginName = 'admin'
    # 用户名密码
    #loginPassword = 'admin'
    # ipAddress = arge['manage_ip']
    # loginName = arge['admin']
    # loginPassword = arge['admin']
    # command = arge['command']


    # 提示符，可能是’ $ ’ , ‘ # ’或’ > ’
    loginprompt = '[$#>]'

    telnet_newkey = 'Are you sure you want to continue connecting ? (yes/no)'
    # 拼凑 telnet 命令
    cmd = 'telnet ' + manage_ip
    # 为 telnet 生成 spawn 类子程序
    child = pexpect.spawn(cmd)
    index = child.expect(["telnet_newkey","(?i)login:","()", pexpect.EOF, pexpect.TIMEOUT])
    child.expect('.*?')
    child.sendline(account_name)
    child.expect(account_name)
    child.expect('(?i)password:')
    child.sendline(account_password)
    child.expect('.*?')
    #print "正在输入命令"
    #child.sendline(command + ' | xml | no-more')
    #child.expect(command + ' | xml | no-more')
    child.sendline(command)
    child.expect(command)
    child.expect('(.*?)#')

    text_before = child.before
    text_after = child.after
    # print text_after#这个打印不能去掉不知道为什么
    child.close(force=True)
    return text_after


def telnet_command_old(arge):
    # 即将 telnet 所要登录的远程主机的域名
    #ipAddress = '10.10.1.187 32790'
    # 登录用户名
    #loginName = 'admin'
    # 用户名密码
    #loginPassword = 'admin'

    ipAddress = arge['manage_ip']
    loginName = arge['admin']
    loginPassword = arge['admin']
    command = arge['command']


    # 提示符，可能是’ $ ’ , ‘ # ’或’ > ’
    loginprompt = '[$#>]'

    telnet_newkey = 'Are you sure you want to continue connecting ? (yes/no)'
    # 拼凑 telnet 命令
    cmd = 'telnet ' + ipAddress
    # 为 telnet 生成 spawn 类子程序
    child = pexpect.spawn(cmd)
    index = child.expect(["telnet_newkey","(?i)login:","()", pexpect.EOF, pexpect.TIMEOUT])
    child.expect('.*?')
    child.sendline('admin')
    child.expect('admin')
    child.expect('(?i)password:')
    child.sendline('admin')
    child.expect('.*?')
    #print "正在输入命令"
    #child.sendline(command + ' | xml | no-more')
    #child.expect(command + ' | xml | no-more')
    child.sendline(command)
    child.expect(command)
    child.expect('(.*?)#')

    text_before = child.before
    text_after = child.after
    #print text_after#这个打印不能去掉不知道为什么
    child.close(force=True)
    return text_after
