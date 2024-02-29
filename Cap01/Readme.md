# Flask Excel Upload API

Esta API foi projetada para facilitar o upload de arquivos Excel e processá-los no servidor.

## Endpoint de Upload

O endpoint `/upload` aceita um arquivo Excel (`.xlsx`) enviado como `multipart/form-data`. Depois de fazer o upload, o arquivo é processado e as primeiras 5 linhas do arquivo Excel são retornadas como um objeto JSON.

### HTTP Request

`POST /upload`

### Parâmetros

| Nome       | Tipo          | Descrição                          |
|------------|---------------|------------------------------------|
| `excel`    | file          | Arquivo Excel a ser carregado.     |

### Response

Se bem-sucedido, o endpoint retorna um JSON com as primeiras 5 linhas do arquivo Excel. Em caso de erro, retorna um código de status HTTP apropriado com uma mensagem de erro.

## Exemplo de Consumo com `curl`

Para consumir o serviço via `curl`, você pode usar o seguinte comando:

```bash
curl -X POST -F "excel=@caminho_para_seu_arquivo.xlsx" http://localhost:5000/upload
