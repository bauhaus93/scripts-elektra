
def generate_git_clone(user_name, repository):
    cmd = f"git clone https://github.com/{user_name}/{repository}.git"
    return cmd
