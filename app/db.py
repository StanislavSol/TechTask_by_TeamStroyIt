from psycopg2.extras import NamedTupleCursor
import psycopg2
from contextlib import contextmanager


@contextmanager
def create_connection(db_url):
    '''Получаем соединение с БД'''
    try:
        connection = psycopg2.connect(db_url)
        yield connection
    except Exception:
        if connection:
            connection.rollback()
        raise
    else:
        if connection:
            connection.commit()


def close_connection(connection):
    '''Закрываем соединение с БД'''
    if connection:
        connection.close()


def get_top100(connection):
    '''Извлекаем из таблицы top100 репозитории'''
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''SELECT repo, owner,
                     position_cur, position_prev,
                     forks, watchers, stars, open_issues, language
                     FROM top100 ORDER BY position_cur DESC''')
        context = curs.fetchall()
        return context


def get_info_by_repo(connection, repo):
    '''Извлекаем данные из таблицы top100 по названию репозитория'''
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''SELECT id, repo, position_cur
                     FROM top100
                     WHERE repo=%s;''', (repo,))
        return curs.fetchone()


def create_info_rep(
    connection,
    repo,
    owner,
    position_cur,
    forks,
    watchers,
    stars,
    open_issues,
    lang
):
    '''Вводим данные в таблицу top100'''
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            '''INSERT INTO top100 (repo, owner,
            position_cur, forks,
            watchers, stars, open_issues, language)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);''',
            (
                repo,
                owner,
                position_cur,
                forks,
                watchers,
                stars,
                open_issues,
                lang,
            )
        )


def update_info_rep(
    connection,
    repo,
    position_cur,
    position_prev,
    forks,
    watchers,
    stars,
    open_issues
):
    '''Обновалеям данные в таблице top100'''
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            '''UPDATE top100 SET
            position_cur=%s,
            position_prev=%s,
            forks=%s,
            watchers=%s,
            stars=%s,
            open_issues=%s
            WHERE repo=%s;''',
            (
                position_cur,
                position_prev,
                forks,
                watchers,
                stars,
                open_issues,
                repo,
            )
        )


def get_info_by_commit(connection, date):
    '''Извлекам данные об актиности репозитория по дате'''
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''SELECT commits
                     FROM repo_info
                     WHERE date=%s;''', (date,))
        return curs.fetchone()


def create_info_commit(connection, date, autor):
    '''Вводим данные в таблицу repo_info'''
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(f'''INSERT INTO repo_info (date, commits, autors)
                     VALUES (%s, %s, '{'{'}{autor}{'}'}');''', (date, 1))


def update_info_commit(connection, date, autor):
    '''Обновляем данные в таблице repo_info'''
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
           '''UPDATE repo_info
           SET commits=commits+1, autors=array_append(autors, %s)
           WHERE date=%s''',
           (
               autor,
               date,
           )
        )


def get_commits(connection):
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        '''Извлекаем данные об активносити репозитория'''
        curs.execute('''SELECT date, commits, autors
                     FROM repo_info ORDER BY date DESC''')
        context = curs.fetchall()
        return context
