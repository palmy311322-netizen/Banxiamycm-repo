import re

pattern = re.compile(
    r'(?P<ip>\S+)'
    r'\s+\S+\s+\S+\s+'
    r'\[(?P<time>[^\]]+)\]'
    r'\s+["＂](?P<request>[^"＂]*)["＂]'
    r'\s+(?P<status>\d{3})'
    r'\s+(?P<bytes>\d+|-)'
)

HTTP_VERSION=re.compile(r'HTTP/\d(?:\.\d)?')

def split_request(request):
    parts=request.split()
    if not parts:
        return '','',''
    if len(parts)==1:
        return parts[0],'',''
    if HTTP_VERSION.fullmatch(parts[-1]):
        return parts[0],' '.join(parts[1:-1]),parts[-1]
    return parts[0],' '.join(parts[1:]),''

ips=[]
times=[]
methods=[]
urls=[]
statuses=[]
bytes_list=[]
bad_count=0

with open('access.log','r',encoding='utf-8',errors='replace') as f:
    for line in f:
        try:
            m=pattern.match(line)
            if not m:
                raise ValueError('行格式不匹配')
            method,url,protocol=split_request(m.group('request'))
            ips.append(m.group('ip'))
            times.append(m.group('time'))
            methods.append(method)

            urls.append(url)
            
            statuses.append(m.group('status'))
            bytes_list.append(m.group('bytes'))
        except:
            bad_count += 1
print('脏数据行数:',bad_count)

bytes_int=list(map(lambda s:int(s) if s!='-' else 0,bytes_list))
status_new=list(map(lambda s:s[0]+'xx',statuses))

ip_error={}
for ip,status in zip(ips,status_new):
    if status=='4xx' or status=='5xx':
        if ip not in ip_error:
            ip_error[ip]=0
        ip_error[ip]+=1

top5=sorted(ip_error.items(),key=lambda x:x[1],reverse=True)[:5]
print('错误请求Top5 IP:')
for ip,count in top5:
    print(ip,count)

morning_ips=set()
afternoon_ips=set()
for ip,t in zip(ips,times):
    hour=int(t.split(':')[1])
    if hour<12:
        morning_ips.add(ip)
    else:
        afternoon_ips.add(ip)

only_morning=morning_ips-afternoon_ips
only_afternoon=afternoon_ips-morning_ips
all_day=morning_ips&afternoon_ips

print('只在上午出现的IP:')
for ip in only_morning:
    print(ip,'\n')
print('只在下午出现的IP:')
for ip in only_afternoon:
    print(ip,'\n')
print('全天都在访问的IP:')
for ip in all_day:
    print(ip,'\n')

mask_pattern=re.compile(r'(\d+\.\d+\.\d+)\.\d+')
with open('access.log','r',encoding='utf-8',errors='replace') as f:
    lines=f.readlines()
with open('access_masked.log','w',encoding='utf-8') as f:
    for line in lines:
        masked=mask_pattern.sub(r'\1.***',line)
        f.write(masked)
print('已生成access_masked.log')

total=len(ips)
unique_ips=len(set(ips))

status_count={}
for s in status_new:
    if s not in status_count:
        status_count[s]=0
    status_count[s]+=1

total_bytes=sum(bytes_int)

url_count={}
for u in urls:
    if u not in url_count:
        url_count[u]=0
    url_count[u]+=1

top10_url=sorted(url_count.items(),key=lambda x:x[1],reverse=True)[:10]

with open('report.txt','w',encoding='utf-8') as f:
    f.write('     日志分析报告\n')
    f.write('总请求数: '+str(total)+'\n')
    f.write('独立IP数: '+str(unique_ips)+'\n')
    f.write('脏数据行数: '+str(bad_count)+'\n')
    f.write('各状态码占比:\n')
    for s in sorted(status_count.keys()):
        pct=status_count[s]/total*100
        f.write('  '+s+': '+str(status_count[s])+' ('+'{:.1f}'.format(pct)+'%)\n')
    f.write('流量总计: '+str(total_bytes)+' 字节\n')
    f.write('访问量Top10 URL:\n')
    for u,cnt in top10_url:
        f.write('  '+u+': '+str(cnt)+'\n')

print('已生成report.txt')