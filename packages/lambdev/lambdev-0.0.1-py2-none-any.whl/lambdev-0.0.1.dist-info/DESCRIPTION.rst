# lambdev
A wrapper around a boto3 lambda client, lambdev helps automate the process of deploying, testing, and versioning AWS lambda
functions.

## Installation
```pip install lambdev```

## Configuration

##### AWS credectials
Please refer to the [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)
documentation on configuring your aws credentials. Best option when working with lambdev is to store your credentials
(`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) and region (`AWS_DEFAULT_REGION`) as environment variables.

##### create .lambdevignore.txt
create a file called `.lambdevignore.txt` where you can list the *names* of files and directories that are in your project folder
that you would like to exclude from your lambda function deployment package. 

for example:
```text
env
test.py
build.sh
function_name.txt
```
All hidden files (names that start with `.`) are
ignored by default (ie `.gitignore`) and do not need to be added to the ignore file.

#### Usage
simply run the lambdev functions from the root directory of your AWS lambda function project folder.

##### Available functions:
1. `lambdev.create()`
    - creates a new lambda function by uploading a deployment package from the non-ignored files in the working directory.
   Saves new function ARN in `$WORKINGDIR/function_name.txt`.
1. `lambdev.test()`
    - uploads non-ignored code in working dir to lambda function `$latest` channel, invokes it, and returns log.
1. `lambdev.publish()`
    - publishes code in `$latest` and updates input alias to point to new version.

#### Examples
Example files can be found [here](./examples)

