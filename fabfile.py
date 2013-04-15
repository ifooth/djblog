#encoding=utf-8

'''
Created on 2013/4/14 
@author: Joe Lei
'''

#重要数据
#1. 代码用git管理 分布式储存
#2. 数据库用mysql 没有备份
#3  用户上传文件位置待定

#运行数据
#1. 代码编译成最优化字节码文件
#2. 静态文件放在/usr/share/djblog/static

from fabric.api import run,env,run
from fabric.context_managers import cd
from fabric.contrib.files import exists
import tempfile
env.hosts=['root@ifooth.com']
#env.password='leijiaomin'

project={
    'name':'djblog',
    'home':'/usr/local/djblog',
    'sock':'/run/apollo/djblog.sock',
    'pid':'/run/apollo/djblog.pid',
    'log':'/var/log/uwsgi/djblog.log',
    'git':'git@ifooth.com:djblog.git',    
}

tempdir='/tmp/%s'%project['name']

def fresh_code():    
    run('git archive HEAD --remote=%s | tar -x -C %s'%(project['git'],tempdir))
    
def compile_code():
    run('python -OO -m compileall %s'%tempdir)
    
def rm_source():
    with cd(tempdir):
        run('find . -name "*.py" |xargs rm -r')
    
def mv_code():    
    run('mv %s %s'%(tempdir,project['home']))
    
    
def flesh_conf():
    with cd(project['home']):
        run('cp etc/nginx_djblog.conf /etc/nginx/sites-available')
        run('ln -f -s /etc/nginx/sites-available/nginx_djblog.conf /etc/nginx/sites-enabled/nginx_djblog.conf')
        if exists('/etc/nginx/sites-enabled/default'):
            run('rm /etc/nginx/sites-enabled/default')
            
    if exists('/run/nginx.pid'):
        run('nginx -s stop')
    run('nginx')
def restart():
    if exists(project['pid']):
        run('kill -s kill $(cat %s)'%project['pid'])
        
    with cd(project['home']):
        run('uwsgi -x %s/etc/uwsgi_djblog.xml'%project['home'])

def check_env():
    if exists(tempdir):
        run('rm -rf %s'%tempdir) 
    else:
        run('mkdir %s'%tempdir)
    
    if exists(project['home']):#修复在linux server 12.04上不能创建目录的bug
        if exists('%s.old'%project['home']):
            run('rm -rf %s.old'%project['home'])         
        run('mv -f %s %s.old'%(project['home'],project['home'])) 
    else:
        run('mkdir %s'%project['home'])
def collect_static():
    run('python manage.py collectstatic')
def syncdb():
    run('python manage.py syncdb')
    
def deploy():
    check_env()
    fresh_code()
    compile_code()
    rm_source()
    mv_code()
    flesh_conf()
    restart()