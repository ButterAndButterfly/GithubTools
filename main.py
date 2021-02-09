import sys
from core.github import *
from core import github_star_history
import json, os
from functools import wraps
from jinja2 import FileSystemLoader,Environment

'''
注解,用于优雅地扩展任务类型
'''
taskSolver = {}
def task(type: str, description = "暂无描述"):
    assert task != None
    def decoratedFunc(func):
        @wraps(func)      
        def run(*args, **kwargs):
            return func(*args, **kwargs)
        taskSolver[type] = run
        return run
    return decoratedFunc

def checkDir(file: str):
    '''
    输出文件前,确保其父路径存在
    '''
    folder = os.path.dirname(file)
    if not os.path.exists(folder) and not folder == '':
        os.makedirs(folder)

@task(type = "get_total_stars_and_forks", description =\
    "将指定用户/组织的总star和fork数目输出到指定目录")
def get_total_stars_and_forks(name:str, output:str, **kwargs):
    def starsAndForks(name, token):
        names = name.split("+");
        result = {"stars": 0, "forks": 0}
        for name in names:
            if name == "":
                break
            data = query_total(name, token)
            result["stars"] += data["stars"]
            result["forks"] += data["forks"]
        return result   
    result = starsAndForks(name, token)
    data = json.dumps(result, ensure_ascii=False)
    checkDir(output)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(data)    
    global template_inputs
    if "total_stars_and_forks" not in template_inputs:
        template_inputs["total_stars_and_forks"] = {}
    template_inputs["total_stars_and_forks"][name] = {"name": name, "result": result, "output": output}
    
@task(type = "get_stars_history", description =\
    "将指定项目的star历史记录曲线图，输出到指定目录")
def get_stars_history(name:str, repo:str, output:str, div:int = 7, **kwargs):
    data = github_star_history.draw(name, repo, token, div)
    checkDir(output)
    with open(output, 'wb') as f:
        f.write(data)
    global template_inputs
    if "stars_history" not in template_inputs:
        template_inputs["stars_history"] = {}
    fullName = name+"/"+repo
    template_inputs["stars_history"][fullName] = {"name": name, "repo": repo, "fullName":fullName, "output": output}

    
@task(type = "get_top_star_repos", description =\
    "获取指定用户/组织的若干个star数最高的项目信息，并输出到指定项目")
def get_top_star_repos(name:str, output:str, top:int = 3, **kwargs):
    result = query_top(name,token,top)
    data = json.dumps(result, ensure_ascii=False)
    checkDir(output)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(data)
    global template_inputs
    if "top_star_repos" not in template_inputs:
        template_inputs["top_star_repos"] = {}
    template_inputs["top_star_repos"][name] = {"name": name, "result": result, "topCount": top, "output": output}



@task(type = "render_template", description =\
    "根据模板输出内容到指定文件")    
def render(template_path: str, output: str, **kwargs):
    template_folder = os.path.dirname(template_path)
    env = Environment(loader=FileSystemLoader(template_folder))
    template_file = os.path.basename(template_path)
    template = env.get_template(template_file)
    
    #print("template_inputs: ", template_inputs)
    rendered_content = template.render(template_inputs = template_inputs)
    checkDir(output)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(rendered_content)
    
template_inputs = {}  
if __name__ == "__main__":
    #os.environ['MY_GITHUB_TOKEN'] = token
    print('sys.argv: ', sys.argv)
    if len(sys.argv) >= 2 and os.path.exists(sys.argv[1]):
        config_path = sys.argv[1]
    else:
        config_path = 'config.json'
    '''
    config = {
        "token":"",
        "tasks":[{
            "type": "get_total_stars_and_forks",
            "name":"nICEnnnnnnnLee",
            "output":"total.json"
            },{
            "type": "get_stars_history",
            "name":"nICEnnnnnnnLee",
            "repo":"BilibiliDown",
            "div":7,
            "output":"stars_history.jpg"
        }]
    }
    '''
    with open(config_path, 'r') as f:
        str = f.read()
        config = json.loads(str)
    
    token = os.getenv('MY_GITHUB_TOKEN')
    if not token:
        token = config["token"]
        
    for task in config["tasks"]:
        if task["type"] in taskSolver:
            taskSolver[task["type"]](**task)
        else:
            print("未找到任务: %s"%task["type"])