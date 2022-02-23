# Pré-requisitos do Sistema

## Pré-requisitos

*  Instalar git

```shell
$ sudo apt install git
```
*  Instalar Make

```shell
$ sudo apt-get install make
```

* Instalar o Pip

    - Instruções neste [link](https://pip.pypa.io/en/stable/installing/)

    - Checagem:

    ```shell
    $ pip<version> --version

    #Exemplo de retorno, nota que está usando a instalação padrão do Python:
    pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)
    ```

* Instalar Docker e Docker Compose.

    - Instruções de instalação do Docker neste [link](https://docs.docker.com/engine/install/ubuntu/)


    - Para incluir seu usuário para não precisar executar como root, pode seguir esta [dica](https://docs.docker.com/engine/install/linux-postinstall/).


    - Instruções de instalação do Docker Compose, [aqui](https://docs.docker.com/compose/install).


* Instalar Poetry

    - Na raiz do projeto executar comando: 
    
    ```shell
    </bobby>$ make install-poetry
    ```

    - (opcional) Também tem instruções de instalação neste [link](https://python-poetry.org/docs/#installation).

    - Checagem:

    ```shell
    $ poetry --version

    #Exemplo de retorno:
    Poetry version 1.1.4
    ```

    - Caso não consiga executar o *poetry --version*, adicione o path do poetry na variável *$PATH* do ambiente:

    ```shell
    $ echo -e 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.bashrc
    ```