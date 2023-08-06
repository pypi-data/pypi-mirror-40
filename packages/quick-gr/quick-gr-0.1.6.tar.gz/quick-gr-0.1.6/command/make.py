import json
import sys
import getopt


# make工具，用于快速生成其他指令所需配置文件
class Make:
    def __init__(self, argv):
        self.argv = argv
        self.help_message = 'visit make:\n' \
                            '      make:config file_name [-D (key1:value1,key2:value2....)]\n' \
                            '                            [-M GET|POST...]\n' \
                            '                            [-H (key1:value1,key2:value2....)]'

    def do(self):
        ll = len(self.argv)
        print('ll', ll)
        if self.argv[0] == 'make' or self.argv[0] == 'make:' or ll == 1:
            print(self.help_message)
            sys.exit()
        else:
            print(self.argv)
            command = self.argv[0][5:]
            if command == 'config':
                p = self.argv[1]
                if ll == 2:
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
                elif ll > 2:
                    data = {
                        "user_id": 888888888,
                        "name": "didi"
                    }
                    method = 'GET'
                    headers = {
                        "token": "XnUVBkjHBJKL"
                    }
                    try:
                        opts, args = getopt.getopt(self.argv[2:], "D:M:H:", ["data=", "method=", 'headers='])
                    except getopt.GetoptError:
                        print('option requires an argument : ' + self.argv[0] + ' arg')
                        # _help()
                        print(self.help_message)
                        sys.exit()
                    print(opts)
                    for opt, arg in opts:
                        print(opt, arg)
                        if opt == '-D':
                            data = {}
                            temp = arg.split(',')
                            for i in temp:
                                tr = i.split(':')
                                data[tr[0]] = tr[1]
                        elif opt == '-M':
                            method = arg
                        elif opt == '-H':
                            headers = {}
                            temp = arg.split(',')
                            for i in temp:
                                tr = i.split(':')
                                headers[tr[0]] = tr[1]
                    with open(p + '.json', 'w') as cf:
                        cf.write(json.dumps(
                            {
                                "method": method,
                                "header": headers,
                                "params": data
                            }
                            , indent=1))
                        cf.close()
