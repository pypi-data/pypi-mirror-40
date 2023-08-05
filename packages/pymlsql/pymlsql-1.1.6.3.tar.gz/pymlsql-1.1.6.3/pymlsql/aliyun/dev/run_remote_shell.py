# -*- coding: utf-8 -*-

import argparse
import logging
import os
from pymlsql.aliyun.dev.instance_context import ECSInstanceContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("build_mysql_server")

parser = argparse.ArgumentParser(description='run shell in new ECS instance.')
parser.add_argument('--script_path', help='the path of script will be executed', required=True)
parser.add_argument('--instance_id', help='If you already have a instance, please set thi parameter', required=True)
parser.add_argument('--execute_user', help='the user will execute the command', required=True)
parser.add_argument('--keyPairName', help='', required=True)

args = parser.parse_args()

if not args.script_path.endswith(".sh"):
    raise ValueError("script_path is not a script")
print("-----%s %s" % (args.keyPairName, args.instance_id))
# cwd = os.getcwd()
instance_context = ECSInstanceContext(keyPairName=args.keyPairName, instance_id=args.instance_id,
                                      need_public_ip=True)

instance_context.start_server()
try:
    if instance_context.is_ssh_server_ready():
        with open(os.path.abspath(args.script_path), "r") as script_file:
            content = "\n".join(script_file.readlines())
            res = instance_context.execute_shell(content, args.execute_user)
            # show the result
            if res != -1:
                print(res.decode("utf-8"))
except Exception as e:
    logger.exception("Something wrong is happened", exc_info=True)
