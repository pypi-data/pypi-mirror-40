import argparse
from subprocess import *

parser = argparse.ArgumentParser(description="Create a virtual host for any local website or for a magento 2 (Default "
                                             "is a normal website")

# Optionals args
parser.add_argument("-m2", "--magento2",  action="store_true", help="Virtual Host para magento 2")
parser.add_argument("-a", "--server_alias",  help="Add a server alias")
parser.add_argument("-d", "--directory_root", help="Full path of your apache document root taht will be set in the "
                                                   "virtual host (default is /var/www/html)")
parser.add_argument("-p", "--port", help="change the listening port, default is 80")
parser.add_argument("-c", "--conf_name", help="add a diferent name to your conf file, without the .conf, this will be "
                                              "added automatically, default is the name of your folder_name")

parser.add_argument("server_name", help="Your server name")
parser.add_argument("folder_name", help="The folder name with your document root, the default is inside /var/www/html "
                                        "if you which to have in different place set with -dr")

args = parser.parse_args()

folder_name = args.folder_name
server_name = args.server_name
server_alias = args.server_alias
directory_root = args.directory_root
port = args.port
magento2 = args.magento2
conf_name = args.conf_name

if conf_name:
    file_name = conf_name
else:
    file_name = folder_name
if directory_root:
    dr = directory_root
else:
    dr = "/var/www/html"
if port:
    pr = port
else:
    pr = "80"
if server_alias:
    sa = "ServerAlias {}".format(server_alias)
else:
    sa = ""
if args.magento2:
    m2 = """
        <Directory {0}/{1}>
           Options Indexes FollowSymLinks MultiViews
           AllowOverride All
        </Directory>
    """.format(dr, folder_name)
else:
    m2 = ""
conf_path = "/etc/apache2/sites-available/" + file_name + ".conf"


def create_vh():
    call(["sudo touch " + conf_path], shell=True)
    virtual_host = """
            <VirtualHost *:{0}>
                DocumentRoot {1}/{2}
                ServerName {3}
                {4}
                {5}
            </VirtualHost>
    """.format(pr, dr, folder_name, server_name, sa, m2)

    conf_file = open(conf_path, 'w')
    conf_file.write(virtual_host)
    conf_file.close()
    print("here is your file at {}".format(conf_path))
    call(["cat " + conf_path], shell=True)
    Popen("sudo a2ensite {}.conf".format(file_name), cwd="/etc/apache2/sites-available", shell=True)
    with open("/etc/hosts", "a") as hosts:
        hosts.write("\n127.0.0.1\t{}".format(server_name))
    call(["sudo apache2ctl restart"], shell=True)


