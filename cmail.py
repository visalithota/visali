import smtplib
from smtplib import SMTP
from email.message import EmailMessage
def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('206156@siddharthamahila.ac.in','phdjyhbrmsiaydpf')
    msg=EmailMessage()
    msg['From']='206156@siddharthamahila.ac.in'
    msg['Subject']=subject
    msg['To']=to
    msg.set_content(body)
    server.send_message(msg)
    server.quit()

    







        
    






        
    
