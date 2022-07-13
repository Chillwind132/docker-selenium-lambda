import subprocess
import os

os.chdir("/home/mike/Desktop/Projects/docker-selenium-lambda")
command = "sls invoke --function demo --raw --data"
site_url = " https://www.example.com/"

sls_invoke = subprocess.Popen(command + site_url, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
stdout, stderr = sls_invoke.communicate()

print(stdout)
print("Done")