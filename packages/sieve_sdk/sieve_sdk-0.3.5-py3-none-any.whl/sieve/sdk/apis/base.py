import abc
import asyncio
from http import HTTPStatus
from typing import Optional, Dict, List, Union, Iterable, Tuple

import aiologger
from aiohttp import ClientSession, ClientResponse

from sieve.sdk.config import VERIFY_SSL
from sieve.sdk.exceptions import UnexpectedStatusCode


ResourceId = Union[str, int]


class ABCApiResource(metaclass=abc.ABCMeta):
    resource_url: str

    headers: Optional[Dict] = None

    def __init__(self,
                 session: ClientSession,
                 verify_ssl: bool=None,
                 loop: asyncio.AbstractEventLoop=None,
                 logger: aiologger.Logger=None):
        self.session = session

        if verify_ssl is None:
            verify_ssl = VERIFY_SSL
        self.verify_ssl = verify_ssl

        self.loop = loop or asyncio.get_event_loop()
        self.logger = logger

    def url_for_id(self, id_) -> str:
        return f"{self.resource_url}/{id_}"

    async def search(self, params: Union[Dict, List[Tuple]]) -> Optional[Union[Dict, List[Dict]]]:
        async with self.session.get(url=self.resource_url,
                                    params=params,
                                    headers=self.headers,
                                    verify_ssl=self.verify_ssl) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()
            elif response.status == HTTPStatus.NOT_FOUND:
                return None

            response_body = await response.text()
            if self.logger:
                self.logger.error({
                    'info': 'Unable to search resource',
                    'response_body': response_body,
                    'response_status': response.status,
                    'request_url': response.url.human_repr()
                })
            raise UnexpectedStatusCode({
                "status": response.status,
                "body": response_body
            })

    async def search_many(self, params: Iterable[Dict], return_exceptions=False):
        """
        Accessory method for concurrently doing multiple searchs with gather
        """
        tasks = (self.search(p) for p in params)
        return await asyncio.gather(*tasks,
                                    return_exceptions=return_exceptions)

    async def get(self, id_: ResourceId, **request_kwargs) -> Optional[Dict]:
        async with self.session.get(url=f'{self.resource_url}/{id_}',
                                    headers=self.headers,
                                    verify_ssl=self.verify_ssl,
                                    **request_kwargs) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()
            elif response.status == HTTPStatus.NOT_FOUND:
                return None

            response_body = await response.text()
            if self.logger:
                self.logger.error({
                    'info': 'Unable to get resource',
                    'response_body': response_body,
                    'response_status': response.status,
                    'request_url': response.url.human_repr()
                })
            raise UnexpectedStatusCode({
                "status": response.status,
                "body": response_body
            })

    async def get_many(self,
                       ids: List[ResourceId],
                       return_exceptions=False) -> List[Dict]:
        """
        Accessory method for concurrently doing multiple ABCApiResource.get
        using gather
        """
        tasks = (self.get(id_) for id_ in ids)
        results = await asyncio.gather(*tasks,
                                       return_exceptions=return_exceptions)
        return results

    def _create_response_is_valid(self, response: ClientResponse) -> bool:
        return response.status == HTTPStatus.CREATED

    async def create(self, data: Union[Dict, List], **request_kwargs) -> Dict:
        """
        Performs a POST request on the remote resource

        :param data: The content of the resource to be created
        """
        async with self.session.post(url=self.resource_url,
                                     headers=self.headers,
                                     json=data,
                                     verify_ssl=self.verify_ssl,
                                     **request_kwargs) as response:
            if self._create_response_is_valid(response):
                return await response.json()

            response_body = await response.text()
            if self.logger:
                self.logger.error({
                    "body": data,
                    "url": response.url.human_repr(),
                    "response_status": response.status,
                    "response": response_body,
                    "info": "Unable to create resource"
                })
            raise UnexpectedStatusCode({
                "status": response.status,
                "body": response_body
            })

    async def create_many(self,
                          objs: Iterable[Dict],
                          return_exceptions=False) -> List[Dict]:
        """
        Accessory method to perform multiple create calls
        """
        tasks = (self.create(data) for data in objs)
        return await asyncio.gather(*tasks, return_exceptions=return_exceptions)

    def _update_response_is_valid(self, response: ClientResponse) -> bool:
        return response.status == HTTPStatus.OK

    async def update(self, id_: ResourceId, params: Dict) -> bool:
        async with self.session.put(url=f"{self.resource_url}/{id_}",
                                    headers=self.headers,
                                    json=params,
                                    verify_ssl=self.verify_ssl) as response:
            if self._update_response_is_valid(response):
                return True

            response_body = await response.text()
            if self.logger:
                self.logger.error({
                    "params": params,
                    "url": response.url.human_repr(),
                    "response_status": response.status,
                    "response": response_body,
                    "info": "Unable to update resource data"
                })
            raise UnexpectedStatusCode({
                "status": response.status,
                "body": response_body
            })

    def _delete_response_is_valid(self, response: ClientResponse) -> bool:
        return response.status == HTTPStatus.OK

    async def delete(self, id_: ResourceId) -> bool:
        async with self.session.delete(url=f"{self.resource_url}/{id_}",
                                       headers=self.headers,
                                       verify_ssl=self.verify_ssl) as response:
            if self._delete_response_is_valid(response):
                return True

            response_body = await response.text()
            if self.logger:
                self.logger.error({
                    "url": response.url.human_repr(),
                    "response_status": response.status,
                    "response": response_body,
                    "info": "Unable delete resource"
                })
            raise UnexpectedStatusCode({
                "status": response.status,
                "body": response_body
            })

    def _exists_response_is_true(self, response: ClientResponse) -> bool:
        return response.status == HTTPStatus.OK

    def _exists_response_is_false(self, response: ClientResponse) -> bool:
        return response.status == HTTPStatus.NOT_FOUND

    async def exists(self, params: Dict) -> bool:
        async with self.session.get(url=self.resource_url,
                                    params=params,
                                    headers=self.headers,
                                    verify_ssl=self.verify_ssl) as response:
            if self._exists_response_is_false(response):
                return False
            elif self._exists_response_is_true(response):
                return True

            response_body = await response.text()
            if self.logger:
                self.logger.error({
                    "params": params,
                    "url": response.url.human_repr(),
                    "response": response_body,
                    "status_code": response.status
                })
            raise UnexpectedStatusCode({
                "status": response.status,
                "body": response_body
            })
