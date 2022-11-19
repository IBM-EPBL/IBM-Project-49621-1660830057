from flask import Flask
from flask_mail import Message,Mail

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

@app.route("/")
def index():

    msg = Message("Hello",
                  sender="psuswin00@gmail.com",
                  recipients=["suswinpalaniswamy@gmail.com"])

    mail.send(msg)
    return 'sent'

if __name__ =='__main__':
    app.run(debug=True)