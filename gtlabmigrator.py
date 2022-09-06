# pip install --upgrade python-gitlab

import gitlab
import os


gl = gitlab.Gitlab(private_token="<token-gitlab-com>")
glnew = gitlab.Gitlab('<URL-selfhosted-gitlab>', private_token="<token-selfhosted-gitlab>")

gl.auth()
groups = gl.groups.list()

for x in groups:
    print(x.id)
    newgrp = x.name.replace('m_','').replace('m-','').replace('mmaks_','')
    glnew.groups.create({'name': newgrp, 'path': f"{newgrp}"})
    group = glnew.namespaces.get(newgrp)

    for project in x.projects.list(iterator=True):
        try:
            print(project.name)
            newproj = glnew.projects.create({'name': f"{project.name}", 'path': f"{project.name}", 'namespace_id':f"{group.id}"})
            os.system(f"git clone {project.ssh_url_to_repo}")
            os.system(f" cd {project.name}  && git remote  set-url origin  {newproj.ssh_url_to_repo} && git push -u origin --all && cd ../")
        finally:
            print(f"что то пошло не так с {project.name}")
