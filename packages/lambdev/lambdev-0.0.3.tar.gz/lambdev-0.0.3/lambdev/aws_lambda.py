import base64
import json

import core

l = core.l


# Publish function from $Latest. If desired alias already exists, update its version. If not, create it.
# Assumes that the latest version of code is already in $latest via the test.py script
def publish(alias, description=''):
    fn = core.getFunctionName()

    pubresponse = l.publish_version(FunctionName=fn)

    if core.alias_exists(l.list_aliases(FunctionName=fn), alias):
        print('alias exists...updating version')
        aliasresponse = l.update_alias(FunctionName=core.getFunctionName(),
                                       Name=alias,
                                       FunctionVersion=pubresponse['Version'])
        print('alias %s updated to version %s' % (aliasresponse['Name'],
                                                  aliasresponse['FunctionVersion']))
    else:
        print('creating new alias: {}'.format(alias))
        l.create_alias(FunctionName=fn,
                       Name=alias,
                       FunctionVersion=pubresponse['Version'],
                       Description=description)


def test(test_object):
    core.upload_dir()

    response = l.invoke(FunctionName=core.getFunctionName(), InvocationType='RequestResponse',
                                   LogType='Tail', Payload=json.dumps(test_object))

    print('VERSION %s' % (response['ExecutedVersion']))
    print(
        '''log:
            %s''' % base64.b64decode(response['LogResult']))

    if 'functionError' in response:
        raise(Exception('~~FUNCTION ERROR~~'))
    else:
        print('SUCCESS:')


def create_function(function_name=None, role=None, handler=None, description=None, runtime='python3.7'):
    response = l.create_function(FunctionName=function_name,
                                 Runtime=runtime,
                                 Role=role,
                                 Handler=handler,
                                 Code={'ZipFile': core.build_zip()},
                                 Description=description,
                                 Publish=False
                                 )

    with open(core.workingDir + '/function_name.txt', 'w') as f:
        f.write(response['FunctionArn'])

    print('CREATE_FUNCTION SUCCESS')
