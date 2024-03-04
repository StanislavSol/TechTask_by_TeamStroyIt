from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app import db
import requests
from dotenv import load_dotenv
import os


load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
DATABASE_URL = os.getenv('DATABASE_URL')
TOP_POSITION = 1
DATE_INDEX_PARS = 10


@app.get("/api/repos/top100")
def get_repos(request: Request):
    '''Запрашиваем и получаем Топ100 репозиториев'''
    repos = requests.get('https://api.github.com/search/repositories?q=stars:>100&per_page=100').json()  # E501
    for position, repo in enumerate(repos['items']):
        with db.create_connection(DATABASE_URL) as conn:
            info_repos = db.get_info_by_repo(conn, repo['full_name'])
        db.close_connection(conn)
        if info_repos:
            with db.create_connection(DATABASE_URL) as conn:
                db.update_info_rep(
                    connection=conn,
                    repo=repo['full_name'],
                    position_cur=position+TOP_POSITION,
                    position_prev=info_repos.position_cur,
                    forks=repo['forks_count'],
                    watchers=repo['watchers_count'],
                    stars=repo['stargazers_count'],
                    open_issues=repo['open_issues'],
                )
            db.close_connection(conn)
        else:
            with db.create_connection(DATABASE_URL) as conn:
                db.create_info_rep(
                    connection=conn,
                    repo=repo['full_name'],
                    owner=repo['owner']['login'],
                    position_cur=position+TOP_POSITION,
                    forks=repo['forks_count'],
                    watchers=repo['watchers_count'],
                    stars=repo['stargazers_count'],
                    open_issues=repo['open_issues'],
                    lang=repo['language'],
                )
            db.close_connection(conn)

    with db.create_connection(DATABASE_URL) as conn:
        context = {'repos': db.get_top100(conn)}
    db.close_connection(conn)
    return templates.TemplateResponse(
        request=request,
        name='repos.html',
        context=context,
    )


@app.get("/api/repos/{owner}/{repo}/activity")
def get_repository_activity(owner: str, repo: str, request: Request):
    '''Запрашиваем и получаем активность репозитория за 2023 год'''
    commits = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits?since=2023-01-01&untill=2024-01-01").json()  # E501
    for commit in commits:
        date = commit['commit']['author']['date'][:DATE_INDEX_PARS]
        with db.create_connection(DATABASE_URL) as conn:
            info_commit = db.get_info_by_commit(conn, date)
        db.close_connection(conn)
        autor = commit['commit']['author']['name']
        if info_commit:
            with db.create_connection(DATABASE_URL) as conn:
                db.update_info_commit(conn, date, autor)
            db.close_connection(conn)
        else:
            with db.create_connection(DATABASE_URL) as conn:
                db.create_info_commit(conn, date, autor)
            db.close_connection(conn)

    with db.create_connection(DATABASE_URL) as conn:
        context = {
            'commits': db.get_commits(conn),
            'repo_name': repo,
        }
    db.close_connection(conn)
    return templates.TemplateResponse(
        request=request,
        name='active_repo.html',
        context=context,
    )
