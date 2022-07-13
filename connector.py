import subprocess

cd = subprocess.run(["cd", "C:\\Users\\Mike\\Desktop\\Python_projects\\mike-docker-selenium-lambda"])
sls_invoke = subprocess.run(["sls invoke --function demo --raw --data", "'https://www.google.com/'"])

print("Done")