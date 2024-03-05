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
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
TOP_POSITION = 1
DATE_INDEX_PARS = 10


@app.get("/api/repos/top100")
def get_repos(request: Request):
    '''Запрашиваем и получаем Топ100 репозиториев'''
    url = 'https://api.github.com/search/repositories?q=stars:>100&per_page=100'
    headers = {
              'Authorization': f'Token {GITHUB_TOKEN}'
              }
    repos = requests.request("GET", url, headers=headers).json()
    for position, repo in enumerate(repos['items']):
        with db.create_connection(DATABASE_URL) as conn:
            info_repos = db.get_info_by_repo(conn, repo['full_name'])
        db.close_connection(conn)
        if info_repos:
            with db.create_connection(DATABASE_URL) as conn:
                if position+TOP_POSITION == info_repos.position_cur:
                    pos_cur = None
                else:
                    pos_cur = info_repos.position_cur
                db.update_info_rep(
                    connection=conn,
                    repo=repo['full_name'],
                    position_cur=position+TOP_POSITION,
                    position_prev=pos_cur,
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
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?since=2023-01-01&untill=2023-12-01"
    headers = {
              'Authorization': f'Token {GITHUB_TOKEN}'
              }
    commits = requests.request("GET", url, headers=headers).json()
    with db.create_connection(DATABASE_URL) as conn:
        id_commits = db.get_info_by_repo(conn, f'{owner}/{repo}').id
        commits_info = db.get_commits(conn, id_commits)
    db.close_connection(conn)
    if commits_info:
        context = {
            'commits': commits_info,
            'repo_name': repo,
        }
        return templates.TemplateResponse(
            request=request,
            name='active_repo.html',
            context=context,
        )

    for commit in commits:
        date = commit['commit']['author']['date'][:DATE_INDEX_PARS]
        with db.create_connection(DATABASE_URL) as conn:
            info_commit = db.get_info_by_commit(conn, id_commits, date)
        db.close_connection(conn)
        autor = commit['commit']['author']['name']
        if info_commit:
            with db.create_connection(DATABASE_URL) as conn:
                db.update_info_commit(conn, date, autor, id_commits)
            db.close_connection(conn)
        else:
            with db.create_connection(DATABASE_URL) as conn:
                db.create_info_commit(conn, date, autor, id_commits)
            db.close_connection(conn)

    with db.create_connection(DATABASE_URL) as conn:
        context = {
            'commits': db.get_commits(conn, id_commits),
            'repo_name': repo,
        }
    db.close_connection(conn)
    return templates.TemplateResponse(
        request=request,
        name='active_repo.html',
        context=context,
    )
