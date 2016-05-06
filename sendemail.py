import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


sender = 'wimmaweppa@topkek.fi'
receiver = 'mikael.paloranta@metropolia.fi'

graph = 'test.png'
img_data = open(graph, 'rb').read()

msg = MIMEMultipart()
text = MIMEText("testi")
msg.attach(text)

image = MIMEImage(img_data)
msg.attach(image) 

msg['Subject'] = 'RRD Graafeja'
msg['From'] = sender
msg['To'] = receiver
msg.preamble = 'RRD Graafeja'


s = smtplib.SMTP('smtp.metropolia.fi')
s.send_message(msg)
s.quit()