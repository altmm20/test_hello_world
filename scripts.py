import requests
import os
import git
import json
from urllib.parse import urljoin
from github import Github


class GitHelper:
    

    def __init__(self,access_token):
        self.access_token = access_token
        self.repo_url = None
        self.repo_name = None
        self.git_url = None
        self.repo_name = None
        self.user_name = None


    def create_github_repo(self,repo_name):
        headers = {
        'Authorization': f'token {self.access_token}',
        'Accept': 'application/vnd.github.v3+json'
        }

        data = {
        'name': repo_name,
        'private': False
        }
        
        response = requests.post(url="https://api.github.com/user/repos",json=data, headers=headers)
        #print(response.status_code)
        response_text = response.json()
        #print(response_text)
        if response.status_code == 201:
            print(f'Repository with name {response_text["name"]} created succesfully!')
            repo_url = response_text['html_url']
            remote_url = response_text['clone_url']
            #self.user_name = response_text['owner']['login']
            print(f"GitHub URL : {repo_url}")
            print(f"Remote URL : {remote_url}")
        elif response.status_code == 422:
            print(response_text["message"])
            print(response_text["errors"][0]['message'])


    def delete_github_repo(self,user_name,repo_name=""):
        headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        url = f"https://api.github.com/repos/{user_name}/{repo_name}"
        response = requests.delete(url=url,headers=headers)
        if response.status_code == 204:
            print("Repository deleted successfully.")
        else:
            print("Error occurred while deleting the repository.")
            print(f"Response: {response.text}")    
    

    def clone_github_repo(self,username,repo_name):
        url = f"https://github.com/{username}/{repo_name}"
        print(url)
        current_dir= os.getcwd()  
        os.makedirs(repo_name, exist_ok=True)
        path_to_clone = os.path.join(current_dir,repo_name)
        
        try:
            git.Repo.clone_from(url=url,to_path=path_to_clone)
            print("Repo cloned successfully !!")
        except git.GitCommandError as e:
            if ("exists" in str(e)):
                print("Repo exists and already cloned")

    def add_commit_push_to_repo(self,repo_name,commit_msg):
        current_dir= os.getcwd()  
        repo_path = os.path.join(current_dir,repo_name)
        repo = git.Repo(repo_path)
        current_username = repo.config_reader().get_value('user', 'name')
        current_email = repo.config_reader().get_value('user', 'email')
        print(current_username)
        print(current_email)
        repo.config_writer().set_value("user", "name", "testgitstlc").release()
        repo.config_writer().set_value("user", "email", "testgitstlc@gmail.com").release()
        #print(repo)
        repo.index.add("*")
        repo.index.commit(commit_msg)
        origin = repo.remote(name='origin')
        origin.push()
        print(f"Pushed the content to {repo_name}")
        

            


#g1.delete_github_repo(repo_name=repo_name,user_name=username)
#g1.delete_github_repo(user_name=username,repo_name=repo_name)
#g1.clone_github_repo(repo_name=repo_name,username=username)
# g1.add_commit_push_to_repo(repo_name=repo_name,commit_msg="My 1st commit")
