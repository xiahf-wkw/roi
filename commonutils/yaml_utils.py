import yaml
import os
def get_envconfig():
    folder=os.path.abspath(os.path.dirname(__file__))
    #print (folder)
    f = open(folder+'/envconfig.yaml', encoding='utf-8')
    res = yaml.load(f, Loader=yaml.FullLoader)
    #print(res['ach_envconfig'])
    f.close()
    return  res


if __name__=='__main__':
    get_envconfig()