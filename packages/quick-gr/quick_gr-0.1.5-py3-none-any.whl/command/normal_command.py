import getopt
import sys
import json
import requests


class Worker:
    def __init__(self, argv):
        self.argv = argv
        self.help_message = ''
        self.command_no = 0
        self.config_file_name = ''
        self.url_str = ''

    def do(self):
        try:
            opts, args = getopt.getopt(self.argv, "hu:c:", ["url_str=", "config_file_name="])
        except getopt.GetoptError:
            print('option requires an argument : ' + self.argv[0] + ' arg')
            # _help()
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
                self.url_str = arg
                if command == 2:
                    break
                else:
                    command = 2
            elif opt in ("-c", "--config_file_name"):
                self.config_file_name = arg
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
            print(self.help_message)
        elif command == 2:
            if self.url_str and self.config_file_name:
                self.ask(self.url_str, self.config_file_name)
            else:
                print('-c and -u need to exist simultaneously')
        else:
            sys.exit()

    @staticmethod
    def ask(url, file_name):
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

    @staticmethod
    def help():
        print('---normal command:')
        print('     visit -u <url_str> -c <config_file_name>')
        print('-----tool command:')
        print('     visit make:')
        print('           make:config file_name')
