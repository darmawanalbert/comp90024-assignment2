# comp90024-assignment2

This is a monorepo for COMP90024 - Assignment 2.
## COMP90024 - Team 1

1. Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
2. Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
3. I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
4. Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
5. Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

## how to deploy
- pre-requisite
  - sudo apt install ansible
  - sudo apt install python3-pip
  - pip3 install openstacksdk
```
$ ./run_deploy.sh # deploying source and instances
$ ./run_deploy_source.sh # deploying source, push to docker hub, then deploy in remote machine
$ ./run_deploy_instances.sh # deploying instances and existing source in docker hub
```

## Directory Structure

```js
|-- architectures // architecture design system .png
|-- database // CouchDB
|-- frontend // Web Application for Data Visualisation
|-- harvester // Backend Services to gather Twitter data
|-- nginx // default.cfg
|-- services // Backend Services for frontend app
|-- templates // config templates
```
