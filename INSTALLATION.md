## Install
1. Clone the project repository to your local device:
```
git clone git@github.com:StanislavSol/Technical_task_by_TeamStroyIt.git

```
2. Go to the project directory and install dependencies using Poetry:
```
cd Technical_task_by_TeamStroyIt && make build

```
3. Create a .env file that will contain your sensitive settings:
```
DATABASE_URL = postgresql://{user}:{password}@{host}:{port}/{db}

```

***
## Usege
1. To start the server in a production environment using Uvicorn, run the command:
```
make start

```
2. Run the server locally in development mode with the debugger active:
```
make dev

```
3. Add to dimain push:
```
/api/repos/top100

```
