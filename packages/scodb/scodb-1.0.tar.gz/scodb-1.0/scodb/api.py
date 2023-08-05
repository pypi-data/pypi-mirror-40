from hashlib import md5
from typing import Dict
from functools import reduce
from json import loads, dumps
from urllib.parse import urljoin, urlencode

import requests
from xmltodict import parse
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from xml.parsers.expat import ExpatError

from scodb.exceptions import ApiException


class ScodbConnector:
    """SCODB API

    Classe utilizada para abstrair a conexão com
    a API do SCODB e consumir informações do SISDM.

    Atributos:
        url: URL de conexão com o SCODB.
        username: Usuário de autenticação.
        password: Senha para autenticação.
    """

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self._auth = HTTPBasicAuth(self.username, self.password)

    def member(self, cid: str) -> Dict:
        """Busca um usuário no SISDM com base na sua CID."""
        try:
            url = reduce(urljoin, (self.url, 'member/', cid))
            request = requests.get(url, auth=self._auth)
            ordered_dict = parse(request.text)

            return loads(dumps(ordered_dict))

        except ExpatError:
            raise ApiException('Erro interno.')

        except TypeError:
            raise ApiException('CID informada mal formada.')

        except RequestException:
            raise ApiException('Erro ao conectar com o SCODB.')

    def authenticate(self, username: str, password: str) -> Dict:
        """Valida as credênciais fornecidas junto ao SCODB."""
        try:
            url = reduce(urljoin, (self.url, 'authenticate/'))
            encripted_password = md5(password.encode('utf-8')).hexdigest()
            info = dict(cid=username, password=encripted_password)
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            config = {'data': urlencode(info),
                      'headers': headers,
                      'auth': self._auth}

            request = requests.post(url, **config)

            if request.status_code != 200:
                response = {
                    'error': {
                        'description': 'Usuário e/ou senha incorretos.'
                    }
                }

            else:
                response = loads(dumps(parse(request.text)))

            return response

        except ExpatError:
            raise ApiException('Erro interno.')

        except TypeError:
            raise ApiException('Dados informados mal formatados.')

        except RequestException:
            raise ApiException('Erro ao conectar com o SCODB.')

    def chapter(self, number: str) -> Dict:
        """Busca um Capítulo no SISDM com base na sua Numeração."""
        try:
            url = reduce(urljoin, (self.url, 'chapters/', number))
            request = requests.get(url, auth=self._auth)
            ordered_dict = parse(request.text)

            return loads(dumps(ordered_dict))

        except ExpatError:
            raise ApiException('Erro interno.')

        except TypeError:
            raise ApiException('Dados informados mal formatados.')

        except RequestException:
            raise ApiException('Erro ao conectar com o SCODB.')

    def convent(self, number: str) -> Dict:
        """Busca um Convento no SISDM com base na sua Numeração."""
        try:
            url = reduce(urljoin, (self.url, 'convents/', number))
            request = requests.get(url, auth=self._auth)
            ordered_dict = parse(request.text)

            return loads(dumps(ordered_dict))

        except ExpatError:
            raise ApiException('Erro interno.')

        except TypeError:
            raise ApiException('Dados informados mal formatados.')

        except RequestException:
            raise ApiException('Erro ao conectar com o SCODB.')

    def council(self, entity: str, number: str) -> Dict:
        """Dada uma entidade, informa os membros do conselho."""
        try:
            entity += '/'
            number += '/'
            url = reduce(urljoin, (self.url, entity, number, 'council/'))
            request = requests.get(url, auth=self._auth)
            ordered_dict = parse(request.text)

            return loads(dumps(ordered_dict))

        except ExpatError:
            raise ApiException('Erro interno.')

        except TypeError:
            raise ApiException('Dados informados mal formatados.')

        except RequestException:
            raise ApiException('Erro ao conectar com o SCODB.')

    def __repr__(self):
        return f'Scodb(username="{self.username}")'
