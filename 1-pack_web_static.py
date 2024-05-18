#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive
from the contents of the web_static folder of
AirBnB Clone repo, using the function do_pack

"""
from fabric.api import local
from time import strftime


def do_pack():
    """generate a .tgz archive"""
    time = strftime("%Y%M%d%H%M%S")
    try:
        local("mkdir -p versions")
        name = "versions/web_static_{}.tgz".format(time)
        local("tar -cvzf {} web_static/".format(name))
        return name
    except:
        return None
