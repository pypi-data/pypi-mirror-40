import boto3
import cStringIO
import zipfile
from os import listdir, getcwd, sep
from os.path import isfile, join, basename

l = boto3.client('lambda')
files = []
dirs = []
ignore = []
workingDir = getcwd() + sep


def getFunctionName():
    with open(workingDir + 'function_name.txt') as f:
        return [line.rstrip('\n').rstrip('\r') for line in f][0]


def import_ignore():
    global ignore
    with open(workingDir + '.lambdevignore.txt') as f:
        ignore = [line.rstrip('\n').rstrip('\r') for line in f]
        print('IGNORING: %s' % ignore)


# Sort out files and dirs in a root directory
def sort():
    global workingDir, files, dirs
    names = listdir(workingDir)
    print(names)
    for name in names:
        if name[0] == '.' or name in ignore or name[-3:] == 'pyc':
            pass
        else:
            if isfile(workingDir+name):
                files.append(join(sep, workingDir, name))
                print(workingDir+name)
            else:
                dirs.append(workingDir+name+sep)
    print(dirs)
    print(files)


# loop until all recursive files are added to files list
def get_recursive():
    global workingDir, files, dirs
    while len(dirs) > 0:
        workingDir = dirs.pop()
        # print('workingDir = %s' % workingDir)
        sort()


def zipit():
    buf = cStringIO.StringIO()
    with zipfile.ZipFile(buf, 'w') as ziph:
        for f in files:
            ziph.write(f, basename(f))
    buf.seek(0)
    return buf.read()


def upload_file(z):
    l.update_function_code(
        FunctionName=getFunctionName(),
        ZipFile=z
    )


def build_zip():
    import_ignore()
    sort()
    get_recursive()
    return zipit()


# perform directory upload
def upload_dir():
    upload_file(build_zip())


def alias_exists(alias_response, desired):
    for alias in alias_response['Aliases']:
        if alias['Name'] is desired:
            return True
    return False
