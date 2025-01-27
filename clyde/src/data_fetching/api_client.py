import requests
import logging
from typing import Generator, Dict, Any
from urllib.parse import urlparse, parse_qs

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class APIClient:
    """Client for interacting with external API."""
    def __init__(self, base_url: str, api_key: str, timeout: int = 10):
        """
        Initialize the API client.
        args:
            base_url (str): Base URL of the API.
            api_key (str): API key for authentication.
            timeout (int): Request timeout in seconds.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def fetch_data(self, endpoint: str, params: Dict[ str, Any ] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch data from the API with pagination.
        Args:
            endpoint (str): API endpoint to fetch data from.
            params (Dict[str, Any]): Query parameters to include in the request.
            Yields:
                Dict[str, Any]: A single page of data.
        """
        if params is None:
            params = {}
        
        params.setdefault('limit', 100)
        params.setdefault('offset', 0)

        while True:
            url = f'{self.base_url}/{endpoint}'
            logger.info(f'Fetching data from {url} with params {params}')

            try:
                response = requests.get(
                    url, headers=self.headers, params=params, timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()

                yield data

                if not data.get('next'):
                    logger.info('No more data to fetch')
                    break
                
                """
                Strip the offset from the 'next' url parameter
                """
                parsed_url = urlparse(data['next'])
                query_params = parse_qs(parsed_url.query)
                offset = query_params.get('offset', [None])[0]

                params['offset'] = offset

            except requests.exceptions.RequestException as e:
                logger.error(f'Request failed: {e}')
                break

        def get_resource(self, endpoint: str, resource_id:str) -> Dict[ str, Any ]:
            """
            Fetch a specific resource by ID.
            Args:
                endpoint (str): API endpoint.
                resource_id (str): ID of the resource to fetch.
                Returns:
                Dict[str, Any]: The fetched resource.Dict[str, Any]: Resource data.
            """
            url = f'{self.base_url}/{endpoint}/{resource_id}'
            logger.info(f'Fetching resource from {url}')

            try:
                response = requests.get(
                    url, headers=self.headers, timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f'Request failed: {e}')
                return None
            
if __name__ == '__main__':
    BASE_URL = 'https://pokeapi.co/api/v2'
    API_KEY = None

    client = APIClient(base_url=BASE_URL, api_key=API_KEY)

    for page in client.fetch_data('/pokemon', params={'limit': 100}):
        logger.info(f'Fetched {len(page.get('results', []))} records')