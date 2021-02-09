# coding=utf-8
from . import github
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

def format_func(value, tick_number):
    strTime = time.strftime("%Y-%m-%d", time.localtime(value))
    return strTime
    
def draw(name, repo, token, div = 7):
    data = github.query_star_history(name, repo, token, div = div)
    items = data.items()    
    x_data, y_data, xlabel = [], [] , []  
    for key, value in items:        
        timeArray = time.strptime(key, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray))
        x_data.append(timeStamp)
        xlabel.append(key)
        y_data.append(value)
    '''
    x_data = [1553702400, 1558627200, 1563292800, 1567958400, 1570896000, 1572710400, 1574352000, 1576857600, 1580313600, 1581955200, 1582992000, 1584979200, 1585584000, 1586534400, 1587916800, 1589731200, 1591200000, 1593792000, 1595952000, 1596729600, 1597766400, 1599753600, 1600790400, 1602345600, 1603209600, 1604246400, 1605196800, 1605888000, 1607443200, 1608480000, 1609603200, 1610208000, 1611849600, 1612454400]
    y_data = [1, 10, 19, 31, 40, 51, 61, 70, 79, 92, 101, 112, 122, 133, 141, 151, 160, 171, 181, 190, 200, 211, 219, 230, 241, 252, 261, 272, 282, 293, 301, 311, 320, 330]
    '''
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    plt.plot(x_data,y_data)
    plt.title("Github Star History")
    plt.xlabel("time")
    plt.ylabel("Stars")
    plt.gcf().autofmt_xdate()

    buf = io.BytesIO()
    plt.savefig(buf, format='jpg')
    buf.seek(0)
    bytes = buf.read()
    buf.close()
    plt.close()
    return bytes
if __name__ == '__main__':
    x_data = [1553702400, 1558627200, 1563292800, 1567958400, 1570896000, 1572710400, 1574352000, 1576857600, 1580313600, 1581955200, 1582992000, 1584979200, 1585584000, 1586534400, 1587916800, 1589731200, 1591200000, 1593792000, 1595952000, 1596729600, 1597766400, 1599753600, 1600790400, 1602345600, 1603209600, 1604246400, 1605196800, 1605888000, 1607443200, 1608480000, 1609603200, 1610208000, 1611849600, 1612454400]
    y_data = [1, 10, 19, 31, 40, 51, 61, 70, 79, 92, 101, 112, 122, 133, 141, 151, 160, 171, 181, 190, 200, 211, 219, 230, 241, 252, 261, 272, 282, 293, 301, 311, 320, 330]

    #ax = plt.axes()
    #ax.plot(np.random.rand(50))
    #ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    #ax.plot(x_data,y_data)
    
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    plt.plot(x_data,y_data)
    
    plt.title("Github Star History")
    plt.xlabel("time") #, fontsize=22
    plt.ylabel("Stars")
    plt.gcf().autofmt_xdate()
    #plt.savefig("foo.png")
    
    plt.show()