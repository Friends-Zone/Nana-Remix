
import json
import os
import urllib.request
from git import Repo
from nana import HEROKU_API, setbot
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nana.assistant.__main__ import dynamic_data_filter

repo_name = ""
repo_docker = ""


async def change_repo(url):
    # Remove Default Dockerfile then download New Dockerfile
    os.remove("Dockerfile")
    urllib.request.urlretrieve(url, "Dockerfile")

    # Commit Changes
    repo = Repo()
    index = repo.index
    index.add(["Dockerfile"])  # add a new file to the index
    from git import Actor
    author = Actor("Nana", "nana@harumi.tech")
    committer = Actor("Nana", "nana@harumi.tech")
    # commit by commit message and author and committer
    index.commit("Change Repo", author=author, committer=committer)
    if HEROKU_API is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_API)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            heroku_app = heroku_applications[0]
            heroku_git_url = heroku_app.git_url.replace(
                "https://", f"https://api:{HEROKU_API}@"
            )

            if "heroku" in repo.remotes:
                remote = repo.remote("heroku")
                remote.set_url(heroku_git_url)
            else:
                remote = repo.create_remote("heroku", heroku_git_url)
            remote.push(refspec="HEAD:refs/heads/master", force=True)


async def configrepo():
    cache_path = "nana/cache/repo.json"
    if not os.path.exists(cache_path):
        # It was originally https://gitlab.com/EagleUnion/Nana-Userbot-Repository-Database/-/raw/master/config/repo.json
        # But it doesn't work in Heroku because of Cloudflare.
        # So I place it in an GitHub Gist instead. Please comment there if any changes happens.
        config_url = "https://gist.githubusercontent.com/AndreiJirohHaliliDev2006/b2e7f3c93aa44bf4810cfd6dba7d8541/raw/d985279c9416b4d3ec02bef663d4a91b2b25cbdb/repo.json"
        urllib.request.urlretrieve(config_url, cache_path)
    with open("nana/cache/repo.json") as f:
        data_repo = json.load(f)
    return data_repo


@setbot.on_callback_query(dynamic_data_filter("change_repo"))
async def chgrepo(_client, query):
    text = "**⚙️ Repository Configuration **\n" \
           "`Change Your Repo Source Here! `\n"

    data_repo = await configrepo()

    list_button = [
        [InlineKeyboardButton(r[0], callback_data=r[0])]
        for r in data_repo.items()
    ]

    list_button.append([InlineKeyboardButton("⬅ back️", callback_data="back")])
    button = InlineKeyboardMarkup(list_button)
    await query.message.edit_text(text, reply_markup=button)


@setbot.on_callback_query(filters.regex("^Nana"))
async def chgrepoo(_client, query):
    rp = await configrepo()
    global repo_name
    repo_name = query.data
    list_button = [
        [InlineKeyboardButton(version, callback_data=f"vs{version}")]
        for version in rp[query.data]["version"]
    ]

    list_button.append([InlineKeyboardButton("⬅ back️", callback_data="change_repo")])
    text = "**⚙️ Repository Configuration **\n" \
           "`Change Your Repo Source Here! `\n"
    text += f"""**Author** : {rp[query.data]["Author"]}
**Repository** : {rp[query.data]["repo-link"]}
    """
    button = InlineKeyboardMarkup(list_button)
    await query.message.edit_text(text, reply_markup=button)


@setbot.on_callback_query(filters.regex("^vs"))
async def selectversion(_client, query):
    ver = query.data[2:]
    rp = await configrepo()
    global repo_name, repo_docker
    desc = rp[repo_name]["version"][ver]["description"]
    print(rp[repo_name]["version"][ver])
    repo_docker = rp[repo_name]["version"][ver]["dockerfile"]
    text = "**⚙️ Repository Configuration **\n" \
           "`description : {} `\n".format(desc)
    text += "** Warning! **" \
            "This feature is still experimental! \n " \
            "Your bot might broken after change repo \n" \
            "Use at your own risk! "
    list_button = [
        [InlineKeyboardButton("Agree and Continue", callback_data="chg_repo")],
        [
            InlineKeyboardButton(
                "⬅ Return to the list", callback_data="change_repo"
            )
        ],
    ]

    button = InlineKeyboardMarkup(list_button)
    await query.message.edit_text(text, reply_markup=button)

@setbot.on_callback_query(filters.regex("chg_repo"))
async def select_version(_client, query):
    global repo_docker
    text = "Repo Changed! Please wait for up to 5 minutes to finish the post-repo change setup.."
    await query.message.edit_text(text)
    await change_repo(repo_docker)