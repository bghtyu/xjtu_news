# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import smtplib
import email.utils
from email.mime.text import MIMEText
import getpass

# Prompt the user for connection info
to_email = 'ich@agsay.com'
servername = 'smtp.agsay.com'
username = 'so@agsay.com'
password = 'qazwsx'

r = requests.get('http://jwc.xjtu.edu.cn/html/tzgg/1.html')
print r.status_code
print r.headers
print r.encoding

mail = ''

soup = BeautifulSoup(r.text)
div_links = soup.find("div", class_="list_main_content")
links = div_links.find_all('a')
for link in links:
        print link.get_text()
        url = 'http://jwc.xjtu.edu.cn'+link.get('href')
        page = requests.get(url)
        print page.status_code
        page_soup = BeautifulSoup(page.text)
        title = page_soup.find("div",class_="detail_main_content")
        mail = mail + str(title.find('h3'))
        mail = mail + str(title.find_next_sibling("div").find_next_sibling("div"))
        print ;

# Create the message
msg = MIMEText(mail,'html','utf-8')
msg.set_unixfrom('agsay')
msg['To'] = email.utils.formataddr(('Hello', to_email))
msg['From'] = email.utils.formataddr(('Agsay', username))
msg['Subject'] = 'News of Xjtu'

server = smtplib.SMTP(servername)
try:
    # identify ourselves, prompting server for supported features
    server.ehlo()

    # If we can encrypt this session, do it
    if server.has_extn('STARTTLS'):
        server.starttls()
        server.ehlo() # re-identify ourselves over TLS connection

    server.login(username, password)
    server.sendmail(username, [to_email], msg.as_string())
finally:
    server.quit()

