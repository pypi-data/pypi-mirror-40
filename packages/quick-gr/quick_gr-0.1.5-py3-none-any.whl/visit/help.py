import sys
import getopt
import json
import requests
import re

sys.path.append('..')
import command.make as c_make
import command.normal_command as n_command


def getresponse(url, file_name):
    with open(file_name, 'r') as f:
        conf_json = f.read()
        conf = json.loads(conf_json)
        print(conf)
        headers = conf['header']
        data = conf['params']
        method = conf['method']
        if method == 'GET':
            r = requests.get(url, params=data, headers=headers)
            r_json = json.dumps({
                "status_code": r.status_code,
                "headers": dict(r.headers),
                "cookies": dict(r.cookies),
                "content": r.json()
            })
            print(r_json)
            with open('r.json', 'w') as rf:
                rf.write(r_json)
                rf.close()
        elif method == 'POST':
            r = requests.get(url, params=data, headers=headers)
            r_json = json.dumps({
                "status_code": r.status_code,
                "headers": dict(r.headers),
                "cookies": dict(r.cookies),
                "content": r.json()
            })
            with open('response.json', 'w') as rf:
                rf.write(r_json)
                rf.close()


def main():
    print(sys.argv)
    if len(sys.argv) == 1:
        # ex: root:didi$ visit
        n_command.Worker.help()
        sys.exit()

    # ex : root didi$ visit make:config config
    argv = sys.argv[1:]  # argv = ['make:config','config']
    arg_filter(argv)


def arg_filter(argv):
    if re.match('-', argv[0]):
        normal_argv(argv)
    else:
        tool_argv(argv)


# 工具类命令
def tool_argv(argv):
    # 工具-make：
    if re.match('make', argv[0]):
        make = c_make.Make(argv)
        make.do()

    # 未匹配工具命令
    else:
        print(argv[0] + ' is not a visit command. See \'visit -h\' .')
        sys.exit()


# 普通参数命令
def normal_argv(argv):
    worker = n_command.Worker(argv)
    worker.do()


if __name__ == "__main__":
    main()
