import subprocess

def call_std(args, cwd=None, env=None):
    p = subprocess.Popen(args, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, cwd=cwd, env=env)
    return_code = p.wait()
    stdout = str(p.stdout.read(), 'utf-8')
    stderr = str(p.stderr.read(), 'utf-8')
    return (return_code, stdout, stderr)

def try_call_std(args, cwd=None, env=None):
    code, stdout, stderr = call_std(args, cwd, env)
    if code != 0:
        print("STDOUT: ")
        print(stdout)
        print("STDERR: ")
        print(stderr)
    else:
        return stdout