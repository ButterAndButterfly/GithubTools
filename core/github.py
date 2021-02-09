# coding=utf-8
import requests
import time,datetime
import os
import re


def query_stargazers_name(user, repo, token):
    query_star = """
    query {{
      repository(owner:"{0}", name:"{1}") {{
        stargazers(first:100 {2}) {{
          pageInfo {{
            endCursor
            hasNextPage
          }}
          edges {{
            starredAt
            node {{
              login
            }}
          }}
        }}
      }}
    }}
    """
    headers = {"Authorization": "token "+ token}
    endCursor = ""
    hasNextPage = True
    stargazers = []
    while hasNextPage:
        this_url = query_star.format(user, repo, endCursor)
        response = requests.post('https://api.github.com/graphql', json={'query': this_url}, headers=headers)
        result = response.json()
        endCursor = result['data']['repository']['stargazers']['pageInfo']['endCursor']
        endCursor = ', after: "' + endCursor + '"'
        data = result['data']['repository']['stargazers']['edges']
        for i_user in data:
            stargazers.append([ i_user['node']['login'], i_user['starredAt'][:10] ])
        hasNextPage = result['data']['repository']['stargazers']['pageInfo']['hasNextPage']
    return (stargazers)

def query_top(user, token, top:int = 3):
    '''
    使用graphQL 查询star最高的top个repo
    '''
    query_repos_url = """
    query {{
      user(login: "{0}") {{
        repositories(first: {1}, ownerAffiliations: OWNER, orderBy: {{field: STARGAZERS, direction: DESC}}) {{
          nodes {{
            name
            stargazerCount
            forkCount
            description
          }}
        }}
      }}
      organization(login: "{0}") {{
        repositories(first: {1}, orderBy: {{field: STARGAZERS, direction: DESC}}) {{
          nodes {{
            name
            stargazerCount
            forkCount
            description
          }}
        }}
      }}
    }}
    """
    headers = {"Authorization": "token "+ token}
    this_url = query_repos_url.format(user, top)
    response = requests.post('https://api.github.com/graphql', json={'query': this_url}, headers=headers)
    result = response.json()
    obj = result['data']['user']
    if obj  == None:
        obj = result['data']['organization']
    assert obj  != None
    return obj["repositories"]["nodes"]

def query_total(user, token):
    '''
    使用graphQL 查询star，forks
    '''
    query_repos_url = """
    query {{
      user(login:"{0}") {{
        repositories(first:100 {1}) {{
          pageInfo {{
            endCursor
            hasNextPage
          }}
          nodes {{
            stargazerCount
            forkCount
          }}
        }}
      }}
      organization(login:"{0}") {{
        repositories(first:100 {1}) {{
          pageInfo {{
            endCursor
            hasNextPage
          }}
          nodes {{
            stargazerCount
            forkCount
          }}
        }}
      }}
    }}
    """
    info = {"stars": 0, "forks": 0}
    headers = {"Authorization": "token "+ token}
    endCursor = ""
    hasNextPage = True
    while hasNextPage:
        this_url = query_repos_url.format(user, endCursor)
        response = requests.post('https://api.github.com/graphql', json={'query': this_url}, headers=headers)
        result = response.json()
        obj = result['data']['user']
        if obj  == None:
            obj = result['data']['organization']
        if obj  == None:
            print("查询出错")
            break
        endCursor = obj['repositories']['pageInfo']['endCursor']
        endCursor = ', after: "' + endCursor + '"'
        data = obj['repositories']['nodes']
        for i_repo in data:
            info["stars"] += i_repo["stargazerCount"]
            info["forks"] += i_repo["forkCount"]
        hasNextPage = obj['repositories']['pageInfo']['hasNextPage']
    return (info)

'''    
def query_total(user):
    """
    使用v3 api
    """
    query_repos_url = 'https://api.github.com/users/{0}/repos?per_page=100&page={1}'
    info = {"stars": 0, "forks": 0}
    page = 1
    while True:
        this_url = query_repos_url.format(user, page)
        headers = {'User-Agent': 'ButterAndButterfly'}
        response = requests.get(this_url, headers=headers)
        result = response.json()
        for reposity in result:
            info["stars"] += reposity["stargazers_count"]
            info["forks"] += reposity["forks"]
        #print(response.headers)
        page += 1
        if not "link" in response.headers:
            break
        if not 'rel="last"' in response.headers:
            break
    return info
'''

def query_star_history(user, repo, token, div = 7):
    '''
    返回(日期,star数)
    '''
    history = {}
    lastStarCnt = [0]
    def dealResponseData(data):
        tmp_history = {}
        for star in response.json():
            date = star["starred_at"][:10]
            tmp_history[date] = lastStarCnt[0] + 1
            lastStarCnt[0] = tmp_history[date]
        keys = list(tmp_history.keys())
        tlen = len(keys)
        history[keys[0]] = tmp_history[keys[0]]
        history[keys[tlen//3]] = tmp_history[keys[tlen//3]]
        history[keys[tlen*2//3]] = tmp_history[keys[tlen*2//3]]
        
    url = 'https://api.github.com/repos/{0}/{1}/stargazers'.format(user, repo)
    headers = {'User-Agent': 'ButterAndButterfly', 'Accept': 'application/vnd.github.v3.star+json', "Authorization": "token "+ token}
    response = requests.get(url, headers=headers)
    dealResponseData(response.json())    
    
    if not "link" in response.headers:
        pass
    else:
        sResult = re.search(r'page=([0-9]+)>; rel="last"', response.headers["link"])
        totalPageNum = int(sResult.group(1))
        if(div >= totalPageNum):
            div = totalPageNum -1
        deta = totalPageNum//div
        #print( "totalPageNum: %s, deta: %s"%(totalPageNum, deta))
        for p in range(1+deta, totalPageNum, deta):
            last_p = p
            lastStarCnt[0] = (p-1)*30
            this_url = url + "?page=" + str(p);
            response = requests.get(this_url, headers=headers)
            print(this_url)
            dealResponseData(response.json())
        if last_p < totalPageNum:
            lastStarCnt[0] = (totalPageNum-1)*30
            print("lastStarCnt[0]:", lastStarCnt[0])
            this_url = url + "?page=" + str(totalPageNum);
            response = requests.get(this_url, headers=headers)
            dealResponseData(response.json())
            now = datetime.datetime.utcnow()
            strTime = now.strftime("%Y-%m-%d")
            history[strTime] = (totalPageNum-1)*30 + len(response.json())
    print (history)
    return (history)
    
    
if __name__ == '__main__':
    #query_total("nICEnnnnnnnLee", token)
    query_star_history("ButterAndButterfly", "GithubHost", token)