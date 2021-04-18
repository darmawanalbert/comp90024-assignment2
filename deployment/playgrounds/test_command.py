import subprocess as sp

# sp.call(["ansible-playbook","instance1.yml","-u","ubuntu","-i","45.113.233.153,45.113.235.236,45.113.232.233,45.113.232.231","--private-key","../keypairs/group1-keypair.pem"])
command_bash = "ls -lart"
result = sp.Popen(command_bash.split(), stdout=sp.PIPE)
output, error = result.communicate()
print("total" in output.decode("utf-8"))