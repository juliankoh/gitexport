import requests
import os


class Github:
    def __init__(self, token):
        self.token = token
        self.username = self.get_username()
        print(self.username)

    def make_req(self, url, payload):
        final_url = "https://api.github.com" + url
        print(f"sending request to {final_url}")
        headers = {'Authorization': 'token %s' % self.token}
        return (requests.get(final_url, headers=headers, params=payload))

    def get_username(self):
        result = self.make_req("/user", {}).json()
        return (result['login'])

    def list_all_repo(self):
        result = (self.make_req("/user/repos", {})).json()
        for repo in result:
            print(repo['name'])

    def list_all_repo_name(self):
        result = (self.make_req("/user/repos", {})).json()
        list = []
        for repo in result:
            list.append(repo['full_name'])
        return list

    def normalize_repo_name(self, repo_name):
        user, repo = repo_name.split('/')
        normalized = user+'__'+repo
        return normalized

    def download_repo(self, url, directory):
        filename = self.normalize_repo_name(url)+'.tar'
        filepath = os.path.join(directory, filename)
        with open(filepath, "wb") as file:
            response = self.make_req("/repos/"+url+"/tarball/master", {})
            file.write(response.content)


if __name__ == '__main__':
    token = input("Enter your Github token: ")
    g = Github(token)
    list_of_repo_urls = g.list_all_repo_name()
    g.download_repo(list_of_repo_urls[0])
