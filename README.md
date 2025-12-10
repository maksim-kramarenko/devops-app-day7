# devops-app-day7

Small demo application to practice DevOps skills: Docker, GitHub Actions, AWS ECR, EC2, and basic monitoring.

## Overview

This repository contains a minimal Flask application and all the pieces needed to build and deploy it as a Docker container to AWS.

Stack:

- Python 3.10 + Flask
- Docker / Dockerfile
- GitHub Actions (CI + CD)
- Docker Hub (optional) and AWS ECR
- AWS EC2 (Ubuntu)
- CloudWatch Alarms + SNS
- Email and Telegram alerts

The goal is to simulate a real-world junior DevOps workflow end to end.

## Application

File `app.py`:

- simple Flask web server
- listens on port 8000 inside the container
- responds on `/` with a plain text message

Dependencies are defined in `requirements.txt`.

## Docker

The Dockerfile:

- uses `python:3.10-slim`
- copies `requirements.txt` and installs dependencies
- copies the application code
- starts the app with `python app.py`

To build and run locally:

```bash
docker build -t devops-app .
docker run -d -p 8000:8000 --name devops-app devops-app
curl http://localhost:8000/
CI: GitHub Actions
Workflow: .github/workflows/docker-ci.yml

Main steps:

check out repository

log in to Docker registry (Docker Hub or ECR)

build Docker image from Dockerfile

push image with tags:

latest

commit SHA

The pipeline runs on every push to main.

CD: Deploy to AWS EC2
Workflow: .github/workflows/deploy-aws.yml

Main idea:

use secrets to store:

AWS_EC2_HOST (public IP of EC2)

AWS_EC2_USER (ubuntu)

AWS_EC2_SSH_KEY (private SSH key for the instance)

prepare SSH key on the runner

connect to EC2 via SSH

on the server:

pull latest image from AWS ECR

stop and remove old container prod_app if it exists

run new container on port 80 → 8000

After a push to main, GitHub Actions automatically deploys the new version to EC2.

AWS ECR and EC2
ECR repository: devops-app

Images are tagged and pushed from CI

EC2 instance:

Ubuntu Server

Docker and AWS CLI installed

Security Group opens ports:

22 (SSH)

80 (HTTP)

On EC2 the container is started with:

bash
Копировать код
docker run -d --name prod_app -p 80:8000 <account-id>.dkr.ecr.<region>.amazonaws.com/devops-app:latest
Health check
The deploy workflow also performs a health check:

runs curl http://AWS_EC2_HOST/ from the GitHub runner

retries several times

if HTTP status is not 200, the job fails

This helps detect broken deployments early.

Monitoring and alerts
Monitoring is configured in AWS CloudWatch:

metrics:

CPUUtilization

StatusCheckFailed

StatusCheckFailed_System

alarms:

high CPU (for example, CPUUtilization >= 80 percent)

instance or system status failed

Each alarm sends notifications to an SNS topic.

SNS subscriptions:

email (for basic alerts)

Lambda function that forwards messages to a Telegram bot

Telegram bot receives alerts like:

high CPU on EC2 instance

EC2 status check failed

How to reuse this project
You can fork this repository and adapt it:

change the Flask app to your own service

update Docker image name and ECR repository

adjust GitHub Actions workflows for your AWS account and region

tune CloudWatch alarms and alert destinations

This repo is mainly for learning and showcasing an end to end DevOps flow.

yaml
Копировать код
