from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.client import SyncClientSession


class ApiUser:
    nickname: str
    username: str
    discord_id: str
    db_id: int | None
    created_at: str | None
    updated_at: str | None
    connection: SyncClientSession | None = None

    def __init__(
        self,
        username: str,
        nickname: str,
        discord_id: str,
        db_id: int | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        connection: SyncClientSession | None = None,
    ):
        self.connection = connection
        self.nickname = nickname
        self.username = username
        self.discord_id = discord_id
        self.db_id = db_id
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<User nickname={self.nickname} username={self.username} discord_id={self.discord_id} db_id={self.db_id} created_at={self.created_at} updated_at={self.updated_at}>"

    def create(self):
        if self.db_id is not None:
            raise TypeError("User already created")
        response = self.connection.execute(
            gql(
                """
        mutation CreateUser ($nickname: String!, $username: String!, $discord_id: String!) {
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
            ),
            variable_values={
                "nickname": self.nickname,
                "username": self.username,
                "discord_id": str(self.discord_id),
            },
        )["createUser"]
        self.created_at = response["created_at"]
        self.db_id = response["id"]
        self.nickname = response["nickname"]
        self.username = response["username"]
        self.discord_id = response["discord_id"]
        self.updated_at = response["updated_at"]
        return self


def parse_user(
    raw_user: dict[str, any], connection: SyncClientSession | None = None
) -> ApiUser:
    return ApiUser(
        username=raw_user["username"],
        nickname=raw_user["nickname"],
        discord_id=raw_user["discord_id"],
        db_id=raw_user["id"],
        created_at=raw_user["created_at"],
        updated_at=raw_user["updated_at"],
        connection=connection,
    )


class apiInterface:
    transport: RequestsHTTPTransport
    client: Client
    connection: SyncClientSession

    def __init__(self):
        """Initilize the graphql connection"""
        # Select your transport with a defined url endpoint
        self.transport = RequestsHTTPTransport(url="http://localhost:8060/graphql")

        # Create a GraphQL client using the defined transport
        self.client = Client(
            transport=self.transport,
            fetch_schema_from_transport=True,
            parse_results=True,
        )

        # Create the graphql connection using the defined client
        self.connection = self.client.connect_sync()

        self.client.introspection.update()

    def get_users(self) -> list[ApiUser]:
        raw_users = self.connection.execute(
            gql(
                """
        query GetAllUsers {
        users {
            data {
            created_at
            id
            nickname
            updated_at
            discord_id
            username
            }
        }
        }
        """
            )
        )["users"]["data"]
        users: list[ApiUser] = []
        for raw_user in raw_users:
            users.append(
                ApiUser(
                    connection=self.connection,
                    username=raw_user["username"],
                    nickname=raw_user["nickname"],
                    discord_id=raw_user["discord_id"],
                    db_id=raw_user["id"],
                    created_at=raw_user["created_at"],
                    updated_at=raw_user["updated_at"],
                )
            )
        return users

    def get_user(self, discord_id: int) -> ApiUser | bool:
        response = self.connection.execute(
            gql(
                """
        query GetUser ($discord_id: String!) {
        user (discord_id: $discord_id) {
            created_at
            id
            discord_id
            nickname
            updated_at
            username
        }
        }
        """
            ),
            variable_values={"discord_id": str(discord_id)},
        )
        if "user" in response:
            return parse_user(raw_user=response["user"], connection=self.connection)
        else:
            return False

    def delete_user(self, discord_id: int) -> ApiUser | bool:
        response = self.connection.execute(
            gql(
                """
        mutation DeleteUser($discord_id: String!) {
        deleteUser(discord_id: $discord_id) {
            id
            discord_id
            username
            nickname
            created_at
            updated_at
            }
        }
        """
            ),
            variable_values={"discord_id": str(discord_id)},
        )
        print(response)
        if "deleteUser" in response:
            return parse_user(raw_user=response["deleteUser"])
        else:
            return False
