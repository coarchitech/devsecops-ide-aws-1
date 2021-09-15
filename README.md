
# Welcome to Cloud9 CDK Python project!

This is a blank project for Python development with CDK. You can deploy a custom environment with ec2 instance role, custom size of disk and bootstraping options.
Before Run edit `app.py` file:
* Firts setup your environment with the `accountId` and `region`
* Edit your props in file [project_Configurations](project_configurations/project_props_example.py) and create project_props in the same folder, for example:

```bash
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

```

Now you can deploy your environment with the nexts steps.


The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
