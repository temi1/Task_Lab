 **Steps to create docker file and deploy to AWS**

Create a `Dockerfile` in the project directory and copy command below:

```Dockerfile
FROM python:3.7

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

COPY ./log /app

COPY ./words /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```



### Build the docker image
```
$ docker build -t image 
```
### Now let's add the Docker compose
```
version: '3'

services:
  app:
    container_name: 'FastAPI'
    build: ./app
    volumes:
      - ./app:/app
    ports:
      - "80:80"
    command: uvicorn main:app --reload --host 0.0.0.0 --port 80
```



### Operation Check

Start up and build container with docker-compose
```
$ docker-compose up --build
```
### Push the Docker Image on AWS ECR

Firstly you need to install and configure AWS CLI to push the docker images to AWS ECR

i) Install the AWS CLI:

Run the following two commands to install AWS CLI
```
$ curl “https://awscli.amazonaws.com/AWSCLIV2.pkg" -o “AWSCLIV2.pkg”
$ sudo installer -pkg AWSCLIV2.pkg -target /
```
ii) Verify the installation by running the following command
```
$ aws --version
```
To configure the AWS CLI , get access key ID and Secret Access Key from Identity and Access Management (IAM) in AWS

iii) Configure the AWS CLI:
```
aws configure
AWS Access Key ID [None]: ############
AWS Secret Access Key [None]:######/######/########
Default region name [None]: us-west-2
Default output format [None]:json
```
iv) After configuring AWS CLI, login into AWS ECR using the following command, provide region and account id details.
```
aws ecr get-login-password  --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
```
v) Create Repository in the AWS:
```
aws ecr create-repository --repository-name fast_api_app
```
vi)Tag your image so you can push the image to this repository
```
docker tag api 
aws_account_id.dkr.ecr.region.amazonaws.com/fast_api_app
```
vii) Run the following command to push the docker image to AWS repository
```
docker push aws_account_id.dkr.ecr.region.amazonaws.com/fast_api_app
```
viii) Deploy FastAPI application in EC2
After pushing docker image to AWS ECR , create an Amazon EC2 instance which can serve the API using the chosen Linux instance

ix) Log into ec2 instance by using following command
```
ssh -i fastapi.pem ec2-user@ec2-18-221-11-226.us-east-2.compute.amazonaws.com
```
x) Install the docker in Linux Machine.
```
sudo yum install -y docker
```
xi) Configure AWS as done earlier
```
aws configure
AWS Access Key ID [None]: #############
AWS Secret Access Key [None]:##########/########/##########
Default region name [None]: us-west-2
Default output format [None]:json
```
xii) Run the following commands to add ec2 user to perform docker commands in Linux machine.
```
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart
```
xiii) Exit the instance, ssh in to EC2 instance again and log into the Amazon ECR registry .
```
ssh -i fastapi.pem ec2-user@ec2-18-221-11-226.us-east-2.compute.amazonaws.com

aws ecr get-login --region region --no-include-email
```
xiv) Pull the docker image from AWS ECR on successful login
```
docker pull aws_account_id.dkr.ecr.region.amazonaws.com/fast_api_app
```
xv) Pull the docker image from AWS ECR on successful login
```
docker run -p 5000:5000 aws_account_id.dkr.ecr.region.amazonaws.com/fast_api_app
```
