import sys
import getopt
import json
import requests
import re


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


def main(argv):
    arg_filter(argv)


def arg_filter(argv):
    if re.match('-', argv[0]):
        normal_argv(argv)
    else:
        tool_argv(argv)


# 工具类命令
def tool_argv(argv):
    if not argv[0]:
        _help()
        sys.exit()
    # 工具-make：
    if re.match('make:', argv[0]):
        arg = argv[0][5:]
        if arg == 'config':
            p = argv[1]
            if not p:
                print('visit make:config file_name')
                exit()
            else:
                with open(p + '.json', 'w') as cf:
                    cf.write(json.dumps(
                        {
                            "method": "GET",
                            "header": {
                                "token": "XnUVBkjHBJKL"
                            },
                            "params": {
                                "user_id": 888888888,
                                "name": "didi"
                            }
                        }
                        , indent=1))
                    cf.close()

    # 未匹配工具命令
    else:
        print(argv[0] + ' is not a visit command. See \'visit -h\' .')
        sys.exit()


# -h命令
def _help():
    print('---normal command:')
    print('     visit -u <url_str> -c <config_file_name>')
    print('-----tool command:')
    print('     visit make:')
    print('           make:config file_name')


# 普通参数命令
def normal_argv(argv):
    config_file_name = ''
    url_str = ''
    try:
        opts, args = getopt.getopt(argv, "hu:c:", ["url_str=", "config_file_name="])
    except getopt.GetoptError:
        print('option requires an argument : ' + argv[0] + ' arg')
        _help()
        sys.exit()

    command = 0  # 标明执行的命令是哪个，默认为0
    # print(opts)
    # print(args)
    # 获取命令参数并识别想要执行的函数
    for opt, arg in opts:
        # print(opt, arg)
        if opt == '-h':
            command = 1
            break
        elif opt in ("-u", "--url_str"):
            url_str = arg
            if command == 2:
                break
            else:
                command = 2
        elif opt in ("-c", "--config_file_name"):
            config_file_name = arg
            if command == 2:
                break
            else:
                command = 2
        else:
            print('Unknown method to use: ' + opt + ' ' + arg)
            print('use visit -h to get help')
            sys.exit()
    # 命令执行
    if command == 1:
        _help()
    elif command == 2:
        if url_str and config_file_name:
            getresponse(url_str, config_file_name)
        else:
            print('-c and -u need to exist simultaneously')
    else:
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
