#!/usr/bin/env python3

from project_configurations.helper import load_bootstrap

bootstrap_commands = load_bootstrap('project_configurations/bootstrap.sh')
account = "xxxxxxxx"
region = 'xx-xxxxx-x'

props = {


    # Vars
    "environment_Name": 'DevSecOpsEnvIDE',
    "description": "DevSecOps IDE Blog",
    "vpc_id": "vpc-3abcdk",
    "subnet_selection": ["subnet-adasdhd12", "subnet-1223wqwq"],
    "instance_size": "t3.small",
    "EBS_Volumesize": "20",
    "bootstrap_commands": bootstrap_commands,
    "codecommit_repos": [
            "SimpleApp"
    ],

    # Tags
    "tags": [
        {"key": 'CentralCost',
         "value": 'avxxdw'
         }
    ]
}
