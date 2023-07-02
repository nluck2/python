'''
目标：爬取动漫视频
(1)获取第一层m3u8地址
(2)获取第二层m3u8文件
(3)下载视频
(4)合并所有视频
'''
import requests
import aiohttp
import asyncio
import aiofiles
import os
def get_second_m3u8_file(url,name):
    resp = requests.get(url)
    with open(name,mode='w',encoding='utf-8') as f:
        f.write(resp.text)
def get_frist_m3u8(url,name):
    reap = requests.get(url)
    with open(name,mode='w',encoding='utf-8') as f:
        f.write(reap.text)
def frist_m3u8(url):
    return  "https://vip.lz-cdn14.com/20230410/21607_94652f73/index.m3u8?t=56161604"
async def down_ts(url,name,session):
    async with session.get(url) as resp:
        async with aiofiles.open(f"viode2/{name}",mode="wb") as f:
            await f.write(await resp.content.read())
    print(f"{name}下载完毕")

async def aio_downloda(url): #https://vip.lz-cdn14.com/20230410/21607_94652f73/2000k/hls
    tasks = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64,verify_ssl=False)) as session: #提前准备
        async with aiofiles.open("动漫sencond.txt",mode="r",encoding='utf-8') as f:
            async for line in f:
                if line.startswith('#'):
                    continue
                else:
                    line=line.strip()
                    #拼接真正的视频路径
                    ts_url = url+line
                    take = asyncio.create_task(down_ts(ts_url,line,session))  #创建任务
                    tasks.append(take)
            await asyncio.wait(tasks)
def ts():
    ts = []
    with open('动漫sencond.txt',mode="r",encoding='utf-8') as f:
        for line in f:
            if line.startswith("#"):
                continue
            line=line.strip()
            ts.append(line)
    #print(ts)
    dir=os.getcwd()
    os.chdir('viode2')
    temp=[]
    n=1
    # 每一百个合并
    for i in range(len(ts)):
        name=ts[i]
        temp.append(name)
        if i!=0 and i % 100==0:
            # 合并视频
            # copy /b 1.ts 2.ts 3.ts  xxx.mp4
            names="+".join(temp)
            os.system(f"copy {names} >{n}.ts")
            n += 1
            temp=[]
    #把最后没合并的进行收尾
    names = "+".join(temp)
    os.system(f"copy  {names} > {n}.ts")
    n += 1
    temp_=[]
    for i in range(1,n):
        temp_.append(f"{i}.ts")

    names="+".join(temp_)
    os.system(f"copy {names} > moive.mp4")
    print("搞定")
    os.chdir(dir)
def main():
    url = 'https://www.yhdmz.org/vp/22285-2-0.html'
    m3u8 = frist_m3u8(url)
    # (1)获得一层m3u8
    get_frist_m3u8(m3u8,'动漫')
    # #下载第一层m3u8文件
    with open('动漫',mode='r',encoding='utf-8') as f:
        for line in f:
            if line.startswith("#"):
                continue
            else:
                line = line.strip()  #去掉空白或者换行符
                #(2)准备第二层m3u8文件的下载路径
                #https://vip.lz-cdn14.com/20230410/21607_94652f73/2000k/hls/mixed.m3u8  第二层
                #2000k/hls/mixed.m3u8
                #https://vip.lz-cdn14.com/20230410/21607_94652f73/index.m3u8?t=56161604 第一层
                second_m3u8=m3u8.split("index.m3u8?t=56161604")[0] + line
                #https://vip.lz-cdn14.com/20230410/21607_94652f73/2000k/hls/mixed.m3u8
                get_second_m3u8_file(second_m3u8,'动漫sencond.txt')
    #(3)下载视频
    #https://vip.lz-cdn14.com/20230410/21607_94652f73/2000k/hls/b30d92a2d02000000.ts
    second_m3u8_up = second_m3u8.replace("mixed.m3u8","")
    #准备异步协程
    asyncio.run(aio_downloda(second_m3u8_up))
    ts()

if __name__ == '__main__':
    main()


