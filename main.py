from sys import argv, exit
import json

argv=argv[1:]

data=dict()

c=int()
for i in argv:
    if i == '--token_bot':
        try:
            data['token_bot']=argv[c+1]
        except:
            print('Token empty')
            print('Examples: python main.py --token_bot 79334...:AAGM2q2...')
            exit()

    if i == '--admin_id':
        try:
            data['admin_id']=argv[c+1]
        except:
            print('Admin_id empty')
            print('Examples: python main.py --admin_id 4325...')
            exit()

    if i == '--timezone':
        try:
            data['timezone']=argv[c+1]
        except:
            print('Timezone empty')
            print('Examples: python main.py --timezone Europe/Moscow')
            exit()

    c+=1
js=open('data//temp_bot//custom_cfg.json', 'w', encoding='UTF-8')
json.dump(data, js, indent=4)
js.close()
from core.start import start
start()
