from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.client import SyncClientSession
from HomeworkBot.core.bot import HomeworkBot

class User:
    nickname: str
    username: str
    discord_id: str
    db_id: int | None
    created_at: str | None
    updated_at: str | None

    def __init__(self, username: str, nickname: str, discord_id: str, db_id: int | None = None, created_at: str | None = None, updated_at: str | None = None):
        self.nickname = nickname
        self.username = username
        self.discord_id = discord_id
        self.db_id = db_id
        self.created_at = created_at
        self.updated_at = updated_at

    def create(self):
        if self.db_id is not None:
            raise TypeError('User already created')
        response = HomeworkBot.api.connection.execute(gql(
        """
        mutation CreateUser ($nickname: String!, $username: String!) {
        createUser(input: {username: $username, nickname: $nickname, discord_id: $discord_id}) {
            id
            discord_id
            username
            nickname
            created_at
            updated_at
        }
        }
        """
        ), variable_values={"nickname": self.nickname, "username": self.username, "discord_id": self.discord_id})['createUser']
        self.created_at = response['created_at']
        self.db_id = response['id']
        self.nickname = response['nickname']
        self.username = response['username']
        self.discord_id = response['discord_id']
        self.updated_at = response['updated_at']
        return self


class apiInterface:
    transport: RequestsHTTPTransport
    client: Client
    connection: SyncClientSession

    def __init__(self):
        """Initilize the graphql connection"""
        # Select your transport with a defined url endpoint
        self.transport = RequestsHTTPTransport(url="http://localhost:8060/graphql")

        # Create a GraphQL client using the defined transport
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True, parse_results=True)

        # Create the graphql connection using the defined client
        self.connection = self.client.connect_sync()

    def get_users(self) -> list[User]:
        raw_users = self.connection.execute(gql(
        """
        query GetAllUsers {
        users {
            data {
            created_at
            id
            nickname
            updated_at
            username
            }
        }
        }
        """))['users']['data']
        users: list[User] = []
        for raw_user in raw_users:
            users.append(User(username=raw_user['username'], nickname=raw_user['nickname'], discord_id=raw_user['discord_id'], db_id=raw_user['db_id'], created_at=raw_user['crated_at'], updated_at=raw_user['updated_at']))
        return users
    
    def get_user(self, id: int) -> User:
        raw_user = self.connection.execute(gql(
        """
        query GetUser {
        user (id: $id) {
            data {
            created_at
            id
            nickname
            updated_at
            username
            }
        }
        }
        """), variable_values={'id': id})['user']
        return User(username=raw_user['username'], nickname=raw_user['nickname'], discord_id=raw_user['discord_id'], db_id=raw_user['db_id'], created_at=raw_user['crated_at'], updated_at=raw_user['updated_at'])