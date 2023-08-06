# Naegin
Naegin é uma API Wrapper para o site [naeg.in](https://naeg.in/  "Clique para acessar").

A API tem o objetivo de fornecer Imagens para desenvolvedores de bots fazerem uso das mesmas em seus respectivos projetos.

Você precisa de um token para fazer uso desse serviço. Entre no [Discord](https://discord.gg/kdb4Hvd3 "Servidor no Discord") do site para requisitar um.

# Instalação
Através do pip, você pode facilmente instalar a Wrapper, basta digitar **`pip install naegin`** no terminal.

Certifique-se de estar usando o **Python 3**.

# Uso
```python
import naegin

#Cria uma instância para ser usada
naegin = naegin.Client('token')

#Pegar todas as tags disponíveis em uma list
async def tags():
    tags = await naegin.get_all_tags()
    print(tags)

#Pegar a URL de uma Imagem aleatória, com uma Tag especifica
async def random(tag):
    url = await naegin.get_random(tag)
    print(url)
```