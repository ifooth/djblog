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

from fabric.api import *
from fabric.context_managers import cd
from fabric.contrib.files import exists
import tempfile


project={
    'name':'djblog',
    'home':'/usr/local/djblog',
    'run':'/run/djblog',
    'pid':'/run/djblog/djblog.pid',
    'log':'/var/log/uwsgi',      
}

tempdir='/tmp/%s'%project['name']

import json
cfg=json.load(open('etc/djblog.json'))
env.hosts=cfg['hosts'].split(' ')
env.password=cfg['password']
project['git']=cfg['git']

##环境变量


def check_env():
    if exists(tempdir):
        run('rm -rf %s'%tempdir)    
    run('mkdir %s'%tempdir)
    
    if exists(project['home']):#修复在linux server 12.04上不能创建目录的bug
        if exists('%s.old'%project['home']):
            run('rm -rf %s.old'%project['home'])         
        run('mv -f %s %s.old'%(project['home'],project['home'])) 
    #run('mkdir %s'%project['home']) #修复deploy时 代码复制到错误文件夹

    if not exists(project['run']):
        run('mkdir %s'%project['run'])

    if not exists(project['log']):
        run('mkdir %s'%project['log'])

##检测环境完成

def clone_code():    
    run('git archive HEAD --remote=%s | tar -x -C %s'%(project['git'],tempdir))
    
def compile_code():
    run('python -m compileall %s'%tempdir) #issue python -OO优化编译 uwsgi不能正确得到wsgi
    
def clear_source():
    with cd(tempdir):
        run('find . -name "*.py" |xargs rm -r')

####获取代码完成

def production():
    with cd(tempdir):
        run('cp etc/production.py djblog/settings.py')

def collect_static():
    with cd(tempdir):
        run('python manage.py collectstatic')

def syncdb():
    with cd(tempdir):
        run('mysql -h %s -u%s -p%s < etc/initdb.sql'%(cfg['dbhost'],cfg['dbuser'],cfg['dbpasswd']))
        run('python manage.py syncdb')


### djblog生产环境配置

def deploy_code():    
    run('mv %s %s'%(tempdir,project['home']))    
    
def deploy_conf():
    with cd(project['home']):
        run('cp etc/nginx_djblog.conf /etc/nginx/sites-available')
        run('ln -f -s /etc/nginx/sites-available/nginx_djblog.conf /etc/nginx/sites-enabled/nginx_djblog.conf')
        if exists('/etc/nginx/sites-enabled/default'):
            run('rm /etc/nginx/sites-enabled/default')
            
    if exists('/run/nginx.pid'):
        run('nginx -s stop')
    run('nginx')

## 配置文件

def restart():
    if exists(project['pid']):
        with settings(warn_only=True):
            run('kill -s kill $(cat %s) > /dev/null 2>&1'%project['pid'])
        
    with cd(project['home']):
        run('/opt/uwsgi/uwsgi -x etc/uwsgi_djblog.xml') #使用自己编译的uwsgi v 1.9.5

##重启nginx uwsgi

def test():
    pass

def prepare_deploy():
    check_env()
    clone_code()    
    production()
    collect_static()
    syncdb()
    compile_code()
    clear_source()

    test()

def deploy():
    prepare_deploy()

    deploy_code()
    deploy_conf()    
    restart()