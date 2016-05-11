import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

#Define sender and receiver

sender = 'wimmaweppa@topkek.fi'
receiver = 'mikael.paloranta@metropolia.fi'

#Define graph for msg
graph = 'test.png'
img_data = open(graph, 'rb').read()

#Define text and attach to msg
msg = MIMEMultipart()
text = MIMEText("testi")
msg.attach(text)

#Define attach img to msg
image = MIMEImage(img_data)
msg.attach(image) 

#Basic message build
msg['Subject'] = 'RRD Graafeja'
msg['From'] = sender
msg['To'] = receiver
msg.preamble = 'RRD Graafeja'

#Define SMTP and send message
s = smtplib.SMTP('smtp.metropolia.fi')
s.send_message(msg)
s.quit()