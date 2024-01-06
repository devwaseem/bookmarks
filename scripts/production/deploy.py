import argparse

from fabric import Connection

parser = argparse.ArgumentParser(prog="Deploy to Production")
parser.add_argument(
    "-k",
    "--key",
    help="Specify AWS EC2 SSH Key",
    nargs=1,
    required=True,
    dest="ssh_key_path",
)
parser.add_argument(
    "-t",
    "--token",
    help="Github Repo Token (Personal Access token for repository)",
    nargs=1,
    default=[
        # TODO: Add Github Personal access token
        ""
    ],
    dest="github_token",
)
parser.add_argument(
    "-b",
    "--branch",
    help="which git branch should be used to deploy the code",
    nargs=1,
    default=[
        "main",
    ],
    dest="git_branch",
)
parser.add_argument(
    "-o",
    "--host",
    help="host of the ec2 server (eg: domain name, ip address, etc)",
    nargs=1,
    required=True,
    dest="host",
)
parser.add_argument(
    "-u",
    "--user",
    help="user of the ec2 server",
    nargs=1,
    required=True,
    dest="user",
)
args = parser.parse_args()


HOST = args.host[0]
USER = args.user[0]
PRIVATE_KEY_PATH = args.ssh_key_path[0]
GITHUB_REPO_SUFFIX = "bookmarks/bookmarks"
GITHUB_REPO_TOKEN = args.github_token[0]
PROJECT_NAME = "bookmarks"

c = Connection(
    host=HOST,
    user=USER,
    connect_kwargs={"key_filename": str(PRIVATE_KEY_PATH)},
)
print("Starting Deploy script...")
if c.run(f"test -d {PROJECT_NAME}", warn=True).failed:
    c.run(
        f"git clone https://oauth:{GITHUB_REPO_TOKEN}@github.com/{GITHUB_REPO_SUFFIX} {PROJECT_NAME}"
    )

with c.cd(PROJECT_NAME):
    c.run(f"git checkout {args.git_branch[0]}")
    c.run("git pull")
    c.run("sudo docker-compose -f production.yml stop")
    c.run("sudo docker-compose -f production.yml build --progress=plain")
    c.run("sudo docker-compose -f production.yml up -d")
