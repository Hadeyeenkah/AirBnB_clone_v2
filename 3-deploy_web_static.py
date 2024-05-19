#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive
from the contents of the web_static folder of
AirBnB Clone repo, using the function do_pack

"""
from fabric.api import local
from time import strftime
from fabric.api import env, put, run, runs_once
import os.path


@runs_once
def do_pack():
    """generate a .tgz archive"""
    time = strftime("%Y%M%d%H%M%S")
    try:
        local("mkdir -p versions")
        name = "versions/web_static_{}.tgz".format(time)
        local("tar -cvzf {} web_static/".format(name))
        return name
    except Exception:
        return None


"""
a Fabric script that deploys a file
using the 1-pack_web_static.py file
to pack the file

"""
env.hosts = ['54.237.13.197', '3.83.245.109']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """ deploy file"""
    if os.path.isfile(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp/")
        f_name = archive_path.split("/")[-1]
        f_n_w_xt = f_name.split(".")[0]
        f_path = '/data/web_static/releases/{}'.format(f_n_w_xt)
        s_link = '/data/web_static/current'  # older symlink
        run("mkdir -p {}".format(f_path))
        run("tar -xzf /tmp/{} -C {}".format(f_name, f_path))
        run("rm /tmp/{}".format(f_name))
        run("mv {}/web_static/* {}".format(f_path, f_path))
        run("rm -rf {}/web_static".format(f_path))
        run("rm -rf {}".format(s_link))
        run("ln -s {} {}".format(f_path, s_link))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """ deploy file after achiving"""
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
