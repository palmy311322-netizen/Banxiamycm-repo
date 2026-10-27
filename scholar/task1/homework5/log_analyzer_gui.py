import tkinter as tk
from tkinter import filedialog,messagebox
import re
##以下都是直接复制的
pattern=re.compile(
    r'(?P<ip>\S+)'
    r'\s+\S+\s+\S+\s+'
    r'\[(?P<time>[^\]]+)\]'
    r'\s+["＂](?P<request>[^"＂]*)["＂]'
    r'\s+(?P<status>\d{3})'
    r'\s+(?P<bytes>\d+|-)'
)

HTTP_VERSION=re.compile(r'HTTP/\d(?:\.\d)?')

def split_request(request):
    parts=request.split(' ')
    if not parts:
        return '','',''
    if len(parts)==1:
        return parts[0],'',''
    if HTTP_VERSION.fullmatch(parts[-1]):
        return parts[0],' '.join(parts[1:-1]),parts[-1]
    return parts[0],' '.join(parts[1:]),''

def analyze_file(filepath):
    ips=[]
    times=[]
    methods=[]
    urls=[]
    statuses=[]
    bytes_list=[]
    bad_count=0
    with open(filepath,'r',encoding='utf-8',errors='replace') as f:
        for line in f:
            try:
                m=pattern.match(line)
                if not m:
                    raise ValueError('行格式不匹配')
                method,url,_=split_request(m.group('request'))
                ips.append(m.group('ip'))
                times.append(m.group('time'))
                methods.append(method)
                urls.append(url)
                statuses.append(m.group('status'))
                bytes_list.append(m.group('bytes'))
            except:
                bad_count+=1
    bytes_int=list(map(lambda s:int(s) if s!='-' else 0,bytes_list))
    status_new=list(map(lambda s:s[0]+'xx',statuses))
    ip_error={}
    for ip,status in zip(ips,status_new):
        if status=='4xx' or status=='5xx':
            if ip not in ip_error:
                ip_error[ip]=0
            ip_error[ip]+=1
    top5=sorted(ip_error.items(),key=lambda x:x[1],reverse=True)[:5]
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
    total=len(ips)
    unique_ips=len(set(ips))
    total_bytes=sum(bytes_int)
    status_count={}
    for s in status_new:
        if s not in status_count:
            status_count[s]=0
        status_count[s]+=1
    url_count={}
    for u in urls:
        if u not in url_count:
            url_count[u]=0
        url_count[u]+=1
    top10_url=sorted(url_count.items(),key=lambda x:x[1],reverse=True)[:10]
    report=[]
    report.append('     日志分析报告')
    report.append('总请求数: '+str(total))
    report.append('独立IP数: '+str(unique_ips))
    report.append('脏数据行数: '+str(bad_count))
    report.append('各状态码占比:')
    for s in sorted(status_count.keys()):
        pct=status_count[s]/total*100 if total>0 else 0
        report.append('  '+s+': '+str(status_count[s])+' ('+'{:.1f}'.format(pct)+'%)')
    report.append('流量总计: '+str(total_bytes)+' 字节')
    report.append('')
    report.append('错误请求Top5 IP:')
    for ip,count in top5:
        report.append('  '+ip+': '+str(count))
    report.append('')
    report.append('只在上午出现的IP:')
    for ip in only_morning:
        report.append('  '+ip)
    report.append('')
    report.append('只在下午出现的IP:')
    for ip in only_afternoon:
        report.append('  '+ip)
    report.append('')
    report.append('全天都在访问的IP:')
    for ip in all_day:
        report.append('  '+ip)
    report.append('')
    report.append('访问量Top10 URL:')
    for u,cnt in top10_url:
        report.append('  '+u+': '+str(cnt))
    return '\n'.join(report)
##以上都是直接复制的

def main():
    root=tk.Tk()
    root.title('日志分析器')
    root.geometry('800x600')
    file_path=tk.StringVar()
    top_frame=tk.Frame(root,padx=10,pady=10)
    top_frame.pack(fill=tk.X)
    entry=tk.Entry(top_frame,textvariable=file_path,width=50)
    entry.pack(side=tk.LEFT,padx=5,fill=tk.X,expand=True)
    def browse_file():
        path=filedialog.askopenfilename(filetypes=[('Log','*.log'),('All','*.*')])
        if path:
            file_path.set(path)
    tk.Button(top_frame,text='浏览',command=browse_file).pack(side=tk.LEFT,padx=5)
    text=tk.Text(root,font=('Courier New',10))
    text.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
    def run():
        path=file_path.get()
        if not path:
            return
        try:
            text.delete(1.0,tk.END)
            text.insert(tk.END,analyze_file(path))
        except Exception as e:
            messagebox.showerror('错误','分析失败: '+str(e))
    tk.Button(root,text='开始分析',command=run,width=15).pack(pady=10)
    root.mainloop()

if __name__=='__main__':
    main()
