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
