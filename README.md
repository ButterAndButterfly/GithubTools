<p align="center">
      <strong>
        <a href="https://github.com/ButterAndButterfly/GithubTools" target="_blank">Github 工具箱</a>&nbsp;
      </strong>
  <br>
      源自<strong>
        <a href="https://github.com/ButterAndButterfly" target="_blank">ButterAndButterfly</a><br>
      </strong>  
        Butter, 寓意宅男; Butterfly, 寓意美好的事物。 
        <br/> 美好的世界由我们创造!  
</p>

## 功能  
+ 统计个人/组织的star总数和fork总数(基于Github graphQL)
+ 统计个人/组织的star数最多的项目信息(基于Github graphQL)
+ 统计项目的star历史数据并绘图(基于Github API v3)
+ 【**开箱即用**】提供完整的静态的图片生成方法，只需要fork后简单修改配置即可转为自己使用(基于Github Actions)
+ 【**开箱即用**】提供现成的动态的图片。(因为Github API的访问频率限制，有可能获取失败。您也可以clone/fork后自己部署在vercel上。)
+ 【**开箱即用**】提供会自动刷新的ReadMe首页。[Demo](https://github.com/ButterAndButterfly/GithubTools/tree/master/data)

## 展示
### 动态star/fork总数
![](https://img.shields.io/badge/dynamic/json?label=Total%20Stars&cacheSeconds=3600&query=stars&url=https://github.nicelee.vercel.app/s/nICEnnnnnnnLee)  
### 静态star/fork总数(刷新周期为1天)
![](https://img.shields.io/badge/dynamic/json?label=Total%20Stars&cacheSeconds=3600&query=stars&url=https://raw.githubusercontent.com/ButterAndButterfly/GithubTools/master/data/total.json)  

### 动态star历史数
![](https://github.nicelee.vercel.app/h/nICEnnnnnnnLee/bilibilidown?div=4)  

### 静态star历史数(刷新周期为1天)
![](https://raw.githubusercontent.com/ButterAndButterfly/GithubTools/master/data/stars_history.jpg) 

## 使用  
<details>
<summary>最快捷的方法</summary>


+ 某人或组织的star/fork 总数: 
    + json信息：
        + 链接：`https://github.nicelee.vercel.app/s/{user}` 
        + 举例：<https://github.nicelee.vercel.app/s/nICEnnnnnnnLee>  
    + 有了这个，我们可以根据`shields.io`的接口提供图片：
        + 链接：`https://img.shields.io/badge/dynamic/json?label=Total%20Stars&cacheSeconds=3600&query=stars&url={查询接口}`
        + 举例：<https://img.shields.io/badge/dynamic/json?label=Total%20Stars&cacheSeconds=3600&query=stars&url=https://github.nicelee.vercel.app/s/nICEnnnnnnnLee> 
+ 某项目的star历史图：
    + 链接：`https://github.nicelee.vercel.app/h/{owner}/{repo}`
    + 举例：<https://github.nicelee.vercel.app/h/nICEnnnnnnnLee/bilibilidown?div=4>  
    + 可以通过适当增大`div`参数来增加取样点  

+ 因为**Github API的访问频率限制**，有可能获取失败。
</details>


<details>
<summary>最实用的方法 - Github静态部署</summary>


+ 原理： 使用Github Actions周期(默认每天)查询并保存生成的相关数据，访问静态数据即可。  
+ 步骤：
    1. fork本项目，并**激活Actions**
    2. 修改`config.json`
    ```
    {
        "token":"token", //因为安全需要，最好在项目里面设置，此处可不填
        "tasks":[ // tasks 是一个任务数组，可根据需要删除或增加任务
            {
                "type": "get_total_stars_and_forks", //获取某用户/组织的stars和forks总数
                "name":"nICEnnnnnnnLee",             // 可以是user 或者 organization 或者任意相加，比如nICEnnnnnnnLee+ButterAndButterfly
                "output":"data/total.json"           // 保存的路径
            },{
                "type": "get_stars_history",         //获取某项目的star历史图
                "name":"nICEnnnnnnnLee",             // 可以是user 或者 organization
                "repo":"BilibiliDown",               // repo的名字
                "div":7,                             // 可以增大`div`参数来增加取样点
                "output":"data/stars_history.jpg"    // 保存的路径
            },{
                "type": "get_top_star_repos",
                "name":"ButterAndButterfly",         // 可以是user 或者 organization
                "top":3,                             // 获取star数最多的TOP个
                "output":"data/top/ButterAndButterfly/top4.json"
            },{
                "type": "get_top_star_repos",
                "name":"nICEnnnnnnnLee",
                "top":4,
                "output":"data/top/nICEnnnnnnnLee/top4.json"
            },{
                "type": "render_template",  // 根据前面任务获取的数据来渲染模板，请确认模板里面的变量在前文已经生成，否则会报错
                "template_path":"README_template.md",
                "output":"README.md"  // 可以fork后将配置改为README.md，并将项目名改为你的用户名
            }
        ]
    }
    ```
    4. 图片和数据会周期性地刷新，接下来是怎样访问的问题了。  
        + Github raw：  
        ```
        https://raw.githubusercontent.com/{owner}/{repo}/master/{path}
        举例： https://raw.githubusercontent.com/ButterAndButterfly/GithubTools/master/data/total.json
        然后由img.shields.io生成图片，样式什么的可以自定义
        ```
        + jsdelivr CDN：
        ```
        https://cdn.jsdelivr.net/gh/{owner}/{repo}@master/{path}
        举例： https://cdn.jsdelivr.net/gh/ButterAndButterfly/Q-Gif-ImgBed@master/2020/8/1/nICEnnnnnnnLee-1596288015648.gif
        ```
</details>


<details>
<summary>好吧，部署到vercel的方法</summary>


+ 简介： 提供现成的Serverless实现和配置
+ 步骤：
    1. [可选0-1]fork本项目，vercel上直接根据现有的项目新建
    1. [可选0-2]克隆项目到本地，命令行cd 到目录后直接`vercel`(需要本地存在vercel环境)
    2. 生成自己的`token`，权限不必给多（[参考](https://docs.github.com/en/graphql/guides/forming-calls-with-graphql#authenticating-with-graphql)）。点击[传送门](https://github.com/settings/tokens)  
    3. 在vercel网页端的项目管理里面，设置环境变量   
        + 链接:`https://vercel.com/{vercel用户名}/{vercel项目名}/settings/environment-variables`
        + `name`为`MY_GITHUB_TOKEN`
        + `value`为刚刚生成的token
    4. 相关接口：
    ```
    json信息：{domain}/s/{user}
    某项目的star历史图：{domain}/h/{owner}/{repo}`
    ```        
 
</details>


<details>
<summary>给开发者</summary>


+ 有关数据查询的内容主要在`core/github.py`里面
+ Star历史折线图绘制在`core/github_star_history.py`里面
```
伪代码
from core import github, github_star_history

total_dic = github.query_total(user, token)
total_dic: {"stars":123,"forks":456}

top_repos_list = github.query_top(user, token, 3)
top_repos_list: [{
	"name": "BilibiliDown",
	"stargazerCount": 334,
	"forkCount": 51,
	"description": "xxx"
}, {
	"name": "BilibiliLiveRecorder",
	"stargazerCount": 184,
	"forkCount": 34,
	"description": "xxx"
}, {
	"name": "LiveRecorder",
	"stargazerCount": 56,
	"forkCount": 8,
	"description": "xxx"
}]

history_dic = github.query_star_history(user, repo, token, div = 7)
history_dic: {"2020-01-01":1, "2020-01-02":4, "2020-01-03":6, "2020-01-04":9 }
# key - 日期, value - 当天的star数量

jpg_bytes = github_star_history.draw(history_dic)
jpg_bytes: jpg图片的字节数组
```
</details>

## LICENSE
MIT 


