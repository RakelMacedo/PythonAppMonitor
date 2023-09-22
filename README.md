# Título e Imagem de capa

<h1 align="center">Python App Monitor </h1>

![alt text](https://i.morioh.com/9ccb7b143f.png)

# Badges
![badge1](https://img.shields.io/badge/python-3.11-blue) ![badge2](https://img.shields.io/badge/status-aguardando%20revis%C3%A3o-yellow) ![badge3](https://img.shields.io/badge/gitstars-4-blue) ![badge4](https://img.shields.io/badge/testado%20por-44Sec-green)


# Índice 

* [Título e Imagem de capa](#título-e-imagem-de-capa)
* [Badges](#badges)
* [Índice](#índice)
* [Descrição do Projeto](#descrição-do-projeto)
* [Vídeo Explicativo](#vídeo-explicativo)
* [Status do Projeto](#status-do-projeto)
* [Funcionamento](#funcionamento)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Link de vídeo explicativo](https://youtu.be/WcaoXCMeOw4)
* [Pessoas Desenvolvedoras do Projeto](#pessoas-desenvolvedoras-do-projeto)
* [Licença](#licença)

# Descrição do Projeto

O Python App Monitor é uma aplicação desenvolvida para simplificar o monitoramento e gerenciamento de containers Docker. Utilizando a linguagem de programação Python 3 e suas bibliotecas relacionadas, este sistema oferece uma interface intuitiva para controlar e acompanhar containers Docker em um ambiente de hospedagem.

# Vídeo Explicativo

* https://www.youtube.com/watch?v=WyYauB-P-mM

# Status do Projeto

O projeto foi desenvolvido mediante a proposta de trabalho do professor Fábio Cabrini, na disciplina "Coding for Security", como quinto "checkpoint" para a turma 1TDCG da Faculdade de Administração e Informática Paulista.

# Funcionamento

O programa através de uma CLI oferece diversas opções para o gerenciamento e monitoramento de containers dockers, que é possível através de requisições HTTP ao servidor. O programa possuí 16 opções, sendo elas:

**1.** Listar containers
**2.** Criar container
**3.** Listar processos em containers
**4.** Obter logs de container
**5.** Iniciar container
**6.** Parar container
**7.** Reiniciar container
**8.** Matar container
**9.** Remover container
**10.** Listar imagens
**11.** Remover imagem
**12.** Obter informações do sistema
**13.** Ping do servidor Docker
**14.** Obter versão do Docker
**15.** Obter informações de uso de dados
**16.** Sair do menu

## Execução

* Primeiro, clone o repositório no diretório desejado, utilizando o git bash, caso esteja no Windows, ou diretamente pelo terminal Linux/MacOS, com o comando:
```
git clone https://github.com/RakelMacedo/PythonAppMonitor.git
```
* Em seguida, utilizando um terminal, vá para o diretório onde foi baixado o repositório:
```
cd /caminho/para/o/diretorio/
```

* É necessário habilitar a api do docker, com o comando:
```
sudo dockerd --host unix://var/run/docker.sock --host tcp://0.0.0.0:2375
```

* E após isso, utilizar um servidor Apache ou Nginx:
```
sudo docker run --name pplware -p 8080:80 -v /home/{usuario}/site/:/usr/local/apache2/htdocs/httpd
```

# Tecnologias utilizadas

Foi feita a utilização da api do Docker e de um servidor Apache hospedado no mesmo. Utilizamos, também, as bibliotecas json e requests do Python 3.

# Link de vídeao explicativo
[Vídeo Explicativo](https://youtu.be/pstK7a-2TmM)

# Pessoas Desenvolvedoras do Projeto

João Victor Santos Alves

Rakel de Macedo Oliveira

# Licença

GNU General Public License
