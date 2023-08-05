Scodb
-----

Para utilizadar o conector, você pode seguir o exemplo::

    >>> from pprint import pprint
    >>> import scodb
    >>> api = scodb.ScodbConnector(url, user, password)
    >>> data = api.member('103238')
    >>> pprint(data)

Métodos disponíveis:
- member: Busca um membro com base na CID.
- authenticate: Dado um usuário e senha, valida estes dados no SISDM.
- chapter: Busca informações de um Capítulo com base em seu número.
- convent: Busca informações de um Convento com base em seu número.
- council: Informando o tipo de entidade e seu número, retorna uma coleção com as informações dos membros do Conselho Consultivo.