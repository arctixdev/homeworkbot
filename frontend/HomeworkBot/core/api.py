from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.client import SyncClientSession

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

    def get_users(self) -> list[dict]:
        return self.connection.execute(gql(
        """
        query MyQuery {
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