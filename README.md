# inicio

Este repositório contém um exemplo simples de aplicação web usando [FastAPI](https://fastapi.tiangolo.com/).
O aplicativo permite consultar um banco de dados de clientes e filtrar por "sheet".

## Executando o servidor

1. Certifique-se de que as dependências (FastAPI e Uvicorn) já estão instaladas no ambiente.
2. Execute o servidor com o comando:
   ```bash
   uvicorn app:app --reload
   ```
3. Acesse `http://localhost:8000/` no navegador (Chrome recomendado) para visualizar a lista de clientes.
4. É possível filtrar por sheet informando o valor no campo e clicando em **Filtrar**.

O banco de dados `clients.db` será criado automaticamente na primeira execução com alguns dados de exemplo.
