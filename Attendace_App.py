import requests
import re 
from bs4 import BeautifulSoup
import time
from tqdm import tqdm_notebook as tqdm

def calc(username,password):
    #Add your web browser header details, mine was Mozilla.
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
    }

    login_data = {
        'username': username,
        'password': password
    }

    with requests.Session() as s:
        url = "http://app.bmiet.net/student/login"
        r = s.get(url, headers=header)
        soup = BeautifulSoup(r.content, 'html.parser')
        login_data['_token'] = soup.find('input', {'name': '_token'})['value']
        post = s.post('http://app.bmiet.net/student/student-login',login_data, headers=header)

    def link_finder():
        dat = s.get('http://app.bmiet.net/student/attendance/view',headers=header)
        soup = BeautifulSoup(dat.content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

    def pagecal(links):
        x = True 
        i = 2
        while x:
            val = 'http://app.bmiet.net/student/attendance/view?page='+ str(i)
            if val in links: i += 1
            else: break
        return i

    Tot_absent = 0
    Tot_present = 0
    links = link_finder()
    num = pagecal(links)
    for j in tqdm(range(1,num),desc = 'Calculating'):
        info = s.get('http://app.bmiet.net/student/attendance/view?page='+str(j), headers=header)
        res = re.findall(r'\w+', str(info.content))
        Tot_present += res.count('Present')
        Tot_absent += res.count('Absent')
    print(' Total Present:',Tot_present,'| Total Absent:',Tot_absent,'\n','Total Attendance:',round((Tot_present/(Tot_present+Tot_absent))*100,2),'%')

username = input("Enter Username: ")
password = input("Enter Password: ")

