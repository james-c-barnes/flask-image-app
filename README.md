## 3DV Infrastructure -- code test

### Notes:

Django app exists for an image service -- looks like a great fit. Seemed like cheating so I skipped it.

https://github.com/matthewwithanm/django-imagekit

Decided to use Flask due to service simplicity. Additionally, I haven't used Flask before. Thought it would be fun to explore it.

Forked AWS Flask app from this tutorial to start.

https://github.com/inkjet/flask-aws-tutorial

Created Amazon AMI instance running this service. Browser to:

http://54.90.102.31:5000/

### Open Three Windows
+ running the service
+ curling the service
+ editing source files

### Running the Service
Putty to instance (note: need gemotions.pem file). Currently: ec2-user@54.90.102.31
```bash
sudo su -
cd /opt/flask-image-app
source flask-aws/bin/activate
python application.py
```
#### Curling the Service (API Testing)
##### List-all-images api call
```bash
curl http://54.90.102.31:5000/v1/image
```
##### List-one-images api call
```bash
curl http://54.90.102.31:5000/v1/image/key1
```
#### Editing Source Files
