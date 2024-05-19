#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive
from the contents of the web_static folder of
AirBnB Clone repo, using the function do_pack

"""
from time import strftime
from fabric.api import local, env, put, run, cd
import os.path


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


def do_clean(number=0):
    """
    Deletes out-of-date archives
    Args:
    number: is the number of the archives, including the most recent
    """
    n = 1 if int(number) == 0 else int(number)
    files = [f for f in os.listdir('./versions')]
    files.sort(reverse=True)
    for f in files[n:]:
        local("rm -f versions/{}".format(f))
    remote = "/data/web_static/releases/"
    with cd(remote):
        tgz = run("ls -tr | grep -E '^web_static_([0-9]{6,}){1}$'").split()
        tgz.sort(reverse=True)
        for d in tgz[n:]:
            run("rm -rf {}{}".format(remote, d))
