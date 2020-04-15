# PneumoScan: An AI Tool For PPE Check & COVID19 Testing

### INTRODUCTION

PneumoScan.ai is developed to be a secured AI tool with the purpose to assist radiologists with COVID-19 dectection on chest X-ray, and medical staff's PPE safety check amid this COVID-19 pandemics.


### INSTALL
Now Let's Install Virtualenv with pip. There are other ways also to install virtualenv but I prefer this.*

```sh
$ easy_install pip
```
Next step is to install the virtualenv package: 

```sh
$ pip install virtualenv
```

Great you have installed ```virtualenv```on your machine.

Cloning the project. Type this command in terminal to clone the repo.
```sh
$ git clone https://github.com/sagban/pneumonia-ppe.git
```

Create an Environment with virtualenv
```sh
$ cd pneumoscan-ppe
```
To create the environment with virtualenv:
```sh
$ virtualenv python venv  #see alternative if you are using other than LINUX/UNIX.
```
 After creating virtual environment, it's time to activate it. Type this command
```sh
$ source venv/bin/activate
```

To check wether the cloning process done corectly type ``` ls```,and it'll look like this.
```sh
ls
app  covid-19-model  db.sqlite3     manage.py   pneomonia               ppe-check   requirements.txt    venv
``` 

```sh
$ pip install -r requirements.txt
```
Now, start the deployment server
```sh
$ python manage.py runserver
```
If everything worked fine >>
Congratulations, you setup the pneumoscan project in your pc.

### Description
Here, is the description of the folders containing files used for the deployemnt of the pre-trained model (covid-19 model), VitechLab’s PPE Detector for Laboratory Safety (curated model) and Quantipil’s Barcode/QR-code Scanner (curated model) from AWS Marketplace.
1. **covid-19-model/**
This folder containes the files related to the pre-trained tensorflow model deployed on the aws sagemaker. We used the tesnsorflow model checkpoints o deploy a TensorFlow model using Amazon SageMaker, taking advantage of Amazon SageMaker deployment capabilities, such as selecting the type and number of instances, performing A/B testing, and Auto Scaling.
There are two main files here, 
```covid19-lambda-function.py covid-endpoint.ipynb```
**covid-endpoint.ipynb**: It is used for the creating the endpoints from the Tensorflow saved checkpoints and them converting to the Tensorflow Protobuff. After that model is move to the S3 bucket for further deployment of endpoints using the sagemaker.
**covid19-lambda-function**: This file containes the code used for the setting up the aws lambda function to invoke the created endpoints.

2. **ppe-check**
This folder containes the files related to the VitechLab’s PPE Detector for Laboratory Safety (curated model) from the marketplace.

3. **badge-scan**
This folder containes the files related to the Quantipil’s Barcode/QR-code Scanner (curated model) from the marketplace.



Happy Coding!
