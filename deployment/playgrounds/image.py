import openstack
import subprocess as sp

conn = openstack.connect(cloud='comp90024')

# example_image = conn.image.find_image('NeCTAR Ubuntu 20.04 LTS (Focal) amd64')
for image in conn.image.images():
    if(image.name == 'NeCTAR Ubuntu 20.04 LTS (Focal) amd64'):
        print(image.id)