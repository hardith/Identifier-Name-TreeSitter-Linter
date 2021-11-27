from github import Github

def get_file_contents(github_url,file_extension):
    # using an access token
    # token = "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"
    token = "EnterToken"
    g = Github(token)
    # https://github.com/darkprinx/break-the-ice-with-python
    # github_URL = "https://github.com/adaptives/python-examples"
    file_content_list = []

    try:
        url = github_url.split("https://github.com/")[1]
        repo = g.get_repo(url)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.lower().endswith(file_extension):
                    # print(file_content.decoded_content)
                    file_content_list.append(file_content)

    except: 
        print("Error: GitHub URL is not proper, please provide the root url of the repo")

    # print(len(file_content_list))
    return file_content_list



