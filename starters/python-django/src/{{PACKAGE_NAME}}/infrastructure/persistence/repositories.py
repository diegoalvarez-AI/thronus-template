"""
Adapters Django ORM para os Ports definidos em application/ports/.

Padrão: cada classe implementa um Protocol da camada de aplicação usando o ORM.
Os imports de modelos Django ficam aqui — não nos services — mantendo a camada de
aplicação livre de dependências Django e testável sem banco.

Ver: src/{{PACKAGE_NAME}}/application/ports/ para as interfaces correspondentes.
"""
from __future__ import annotations
