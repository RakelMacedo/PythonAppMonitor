####################################### CHECKPOINT 5 | DOCKER API ###############################

'''
GRUPO: AIKEL

INTEGRANTES: RAKEL DE MACEDO OLIVEIRA | RM99435
             JOÃO VICTOR SANTOS ALVES | RM99634

LINK DO YOUTUBE: 
'''

import requests
import json


# Api do docker
docker_api = 'http://localhost:2375'


def menu():
    while True:
        print("-" * 112)
        print("\nOpções:")
        print("1. Listar containers")
        print("2. Criar container")
        print("3. Listar processos em containers")
        print("4. Obter logs de container")
        print("5. Iniciar container")
        print("6. Parar container")
        print("7. Reiniciar container")
        print("8. Matar container")
        print("9. Remover container")
        print("10. Listar imagens")
        print("11. Remover imagem")
        print("12. Obter informações do sistema")
        print("13. Ping do servidor Docker")
        print("14. Obter versão do Docker")
        print("15. Obter informações de uso de dados")
        print("16. Sair do menu")
        print("-" * 112)
    
        try:

            choice = input("\nEscolha uma opção pelo número: ")

            if choice == "1":
                list_containers()
            elif choice == "2":
                create_container()
            elif choice == "3":
                list_process_in_containers()
            elif choice == "4":
                get_logs()
            elif choice == "5":
                start_container()
            elif choice == "6":
                stop_container()
            elif choice == "7":
                restart_container()
            elif choice == "8":
                kill_container()
            elif choice == "9":
                remove_container()
            elif choice == "10":
                list_images()
            elif choice == "11":
                remove_images()
            elif choice == "12":
                get_info_system()
            elif choice == "13":
                ping()
            elif choice == "14":
                get_version()
            elif choice == "15":
                get_data_usage_info()
            elif choice == "16":
                print("\nSaindo do menu.\n")
                break
            else:
                print("\nOpção inválida. Escolha um número de 1 a 16.\n")
        
        except:
            menu()


def list_containers(see=None):
    global containers_ids

    containers_ids = []

    # Endpoint que lista os containers
    endpoint = '/containers/json?all=true'

    # Faça a solicitação GET para listar os containers
    response = requests.get(f'{docker_api}{endpoint}')
    
    # Verifique o código de resposta da solicitação
    if response.status_code == 200:
        containers_info = response.json()
        
        # Loop para listar informações de cada container
        for container_info in containers_info:
            
            container_id = container_info['Id']
            containers_ids.append(container_id)

            container_name = container_info['Names'][0] if container_info['Names'] else 'N/A'
            container_status = container_info['Status']
            container_image_id = container_info['Image']

            if see == None:
                print(f"\nID do Container: {container_id}")
                print(f"Nome do Container: {container_name}")
                print(f"Status do Container: {container_status}")
                print(f"Nome da Imagem: {container_image_id}")
                print("-" * 85, "\n")
            else:
                pass
    else:
        print(f"Falha ao listar os containers. Código de resposta: {response.status_code}, Mensagem de erro: {response.text}")


def list_process_in_containers():

    list_containers(see='No')

    print('\nEscolha o número do container que deseja ver os processos')
    print('Temos esses containers: \n')

    running_containers_ids = []

    for index, container_id in enumerate(containers_ids, start=1):
        container_info_endpoint = f'/containers/{container_id}/json'
        container_info_response = requests.get(f'{docker_api}{container_info_endpoint}')

        if container_info_response.status_code == 200:
            container_info = container_info_response.json()
            if container_info["State"]["Status"] == "running":
                running_containers_ids.append(container_id)

    if not running_containers_ids:
        print("Não há contêineres em execução para listar processos.")
        return

    for index, container_id in enumerate(running_containers_ids, start=1):
        print(f"Container {index}: {container_id}")

    option = input('\nDigite o número do container que você deseja ver os processos: ')

    try:
        option = int(option)
        if 1 <= option <= len(running_containers_ids):
            container_id = running_containers_ids[option - 1]

            # Endpoint que lista os processos dos containers
            endpoint = f'/containers/{container_id}/top'

            response = requests.get(f'{docker_api}{endpoint}')

            # Verifique o código de resposta da solicitação
            if response.status_code == 200:
                print('\nAqui estão os processos:\n')

                containers_info = response.json()
                for process in containers_info['Processes']:
                    print(process)
            else:
                print(f"Falha ao listar os processos do container. Código de resposta: {response.status_code}, Mensagem de erro: {response.text}")
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")


def get_logs():
    list_containers(see='No')

    print('\nEscolha o número do container que deseja ver os logs')
    print('Temos esses containers: \n')

    for index, container_id in enumerate(containers_ids, start=1):
        print(f"Container {index}: {container_id}")

    option = input('\nDigite o número do container que você deseja ver os logs: ')
    print('\nAqui está os logs do container:\n')
    print("-" * 112)

    option = int(option)
    if 1 <= option <= len(containers_ids):
        container_id = containers_ids[option - 1]

        # Endpoint que lista os processos dos containers
        endpoint = f'/containers/{container_id}/logs?stdout=true&stderr=true'

        response = requests.get(f'{docker_api}{endpoint}', stream=True)
        
        if response.status_code == 200:
            # Itere sobre os logs linha por linha e imprima-os
            for line in response.iter_lines():
                if line:
                    # Decodifique a linha para texto UTF-8
                    print(line.decode('latin-1'))
                    print('\n')
        else:
            print(f"Erro ao obter os logs (Código de Status: {response.status_code})")


def start_container():

    list_containers(see='No')

    print('\nEscolha o número do container que deseja iniciar')
    print('Temos esses containers: \n')

    for index, container_id in enumerate(containers_ids, start=1):
        print(f"Container {index}: {container_id}")

    option = input('\nDigite o número do container que você deseja iniciar: ')

    option = int(option)
    if 1 <= option <= len(containers_ids):
        container_id = containers_ids[option - 1]

        try:
            # Verifique se o contêiner está em execução
            container_info_endpoint = f'/containers/{container_id}/json'
            container_info_response = requests.get(f'{docker_api}{container_info_endpoint}')

            if container_info_response.status_code == 200:
                container_info = container_info_response.json()
                if container_info["State"]["Status"] == "running":
                    print(f"O contêiner {container_id} já está em execução.")
                else:
                    # Endpoint que inicia o contêiner
                    start_endpoint = f'/containers/{container_id}/start'
                    response = requests.post(f'{docker_api}{start_endpoint}')

                    # Verifique se a solicitação foi bem-sucedida (código de status 204)
                    if response.status_code == 204:
                        print(f"Contêiner {container_id} iniciado com sucesso.")
                    else:
                        print(f"Erro ao iniciar o contêiner {container_id} (Código de Status: {response.status_code}).")
            else:
                print(f"Erro ao obter informações do contêiner {container_id} (Código de Status: {container_info_response.status_code}).")

        except Exception as e:
            print(f"Erro ao iniciar o contêiner {container_id}: {str(e)}")


def stop_container():

    list_containers(see='No')

    print('\nEscolha o número do container que deseja parar')
    print('Temos esses containers: \n')

    running_containers_ids = []

    for index, container_id in enumerate(containers_ids, start=1):
        container_info_endpoint = f'/containers/{container_id}/json'
        container_info_response = requests.get(f'{docker_api}{container_info_endpoint}')

        if container_info_response.status_code == 200:
            container_info = container_info_response.json()
            if container_info["State"]["Status"] == "running":
                running_containers_ids.append(container_id)

    if not running_containers_ids:
        print("Não há contêineres em execução para parar.")
        return

    for index, container_id in enumerate(running_containers_ids, start=1):
        print(f"Container {index}: {container_id}")

    option = input('\nDigite o número do container que você deseja parar: ')

    option = int(option)
    if 1 <= option <= len(running_containers_ids):
        container_id = running_containers_ids[option - 1]

        try:
            # Endpoint que para o contêiner
            stop_endpoint = f'/containers/{container_id}/stop'
            response = requests.post(f'{docker_api}{stop_endpoint}')

            # Verifique se a solicitação foi bem-sucedida (código de status 204)
            if response.status_code == 204:
                print(f"Contêiner {container_id} parado com sucesso.")
            else:
                print(f"Erro ao parar o contêiner {container_id} (Código de Status: {response.status_code}).")

        except Exception as e:
            print(f"Erro ao parar o contêiner {container_id}: {str(e)}")


def restart_container():
    
    list_containers(see='No')

    print('\nEscolha o número do container que deseja reiniciar')
    print('Temos esses containers: \n')

    for index, container_id in enumerate(containers_ids, start=1):
        print(f"Container {index}: {container_id}")

    option = input('\nDigite o número do container que você deseja iniciar: ')

    option = int(option)
    if 1 <= option <= len(containers_ids):
        container_id = containers_ids[option - 1]

        try:
            # Endpoint que reinicia o contêiner
            endpoint = f'/containers/{container_id}/restart'
            response = requests.post(f'{docker_api}{endpoint}')

            # Verifique se a solicitação foi bem-sucedida (código de status 204)
            if response.status_code == 204:
                print(f"Contêiner {container_id} reiniciado com sucesso.")
            else:
                print(f"Erro ao reiniciar o contêiner {container_id} (Código de Status: {response.status_code}).")

        except Exception as e:
            print(f"Erro ao reiniciar o contêiner {container_id}: {str(e)}")


def kill_container():
    
    list_containers(see='No')

    print('\nEscolha o número do container que deseja matar (kill)')
    print('Temos esses containers: \n')

    running_containers_ids = []

    for index, container_id in enumerate(containers_ids, start=1):
        container_info_endpoint = f'/containers/{container_id}/json'
        container_info_response = requests.get(f'{docker_api}{container_info_endpoint}')

        if container_info_response.status_code == 200:
            container_info = container_info_response.json()
            if container_info["State"]["Status"] == "running":
                running_containers_ids.append(container_id)

    if not running_containers_ids:
        print("Não há contêineres em execução para matar.")
        return
    
    for index, container_id in enumerate(running_containers_ids, start=1):
        print(f"Container {index}: {container_id}")

    option = input('\nDigite o número do container que deseja matar: ')

    option = int(option)
    if 1 <= option <= len(running_containers_ids):
        container_id = running_containers_ids[option - 1]

        try:
            # Endpoint que mata (kill) o contêiner
            kill_endpoint = f'/containers/{container_id}/kill'
            response = requests.post(f'{docker_api}{kill_endpoint}')

            # Verifique se a solicitação foi bem-sucedida (código de status 204)
            if response.status_code == 204:
                print(f"Contêiner {container_id} foi morto (killed) com sucesso.")
            else:
                print(f"Erro ao matar o contêiner {container_id} (Código de Status: {response.status_code}).")

        except Exception as e:
            print(f"Erro ao matar o contêiner {container_id}: {str(e)}")


def remove_container():
    
    list_containers(see='No')

    print('\nEscolha o número do container que deseja remover (excluir): \n')

    for index, container_id in enumerate(containers_ids, start=1):
        print(f"Container {index}: {container_id}")

    option = input('\nDigite o número do container que deseja remover: ')

    option = int(option)
    if 1 <= option <= len(containers_ids):
        container_id = containers_ids[option - 1]

        try:
            # Endpoint que remove (exclui) o contêiner
            remove_endpoint = f'/containers/{container_id}'
            response = requests.delete(f'{docker_api}{remove_endpoint}')

            # Verifique se a solicitação foi bem-sucedida (código de status 204)
            if response.status_code == 204:
                print(f"Contêiner {container_id} foi removido (excluído) com sucesso.")
            else:
                print(f"Erro ao remover o contêiner {container_id} (Código de Status: {response.status_code}).")

        except Exception as e:
            print(f"Erro ao remover o contêiner {container_id}: {str(e)}")


def list_images(see=None):
    global images_id, images_name

    images_id = []
    images_name = []

    try:
        endpoint = '/images/json?all=true'

        # Faça uma solicitação GET para listar imagens
        response = requests.get(f'{docker_api}{endpoint}')

        # Verifique se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            images = response.json()

            if see == None:
                print("\nLista de imagens Docker:\n")
                for image in images:
                    print(f"ID: {image['Id']}, Nome: {image['RepoTags'][0].split(':')[0]}")
                    print("-" * 112, "\n")
            else:
                for image in images:
                    image_id = image['Id'].split(':')[1]
                    images_id.append(image_id)

                    image_name = image['RepoTags'][0].split(':')[0]
                    images_name.append(image_name)
        else:
            print(f"Erro ao listar imagens (Código de Status: {response.status_code})")

    except Exception as e:
        print(f"Erro ao listar imagens: {str(e)}")


def create_container():

    list_images(see='No')

    print('\nEscolha o número da imagem que deseja criar o container')
    print('Temos essas imagens: \n')

    for index, image_name in enumerate(images_name, start=1):
        print(f"Imagem {index}: {image_name}")

    option = input('\nDigite o número da imagem que você deseja criar o container: ')

    option = int(option)
    if 1 <= option <= len(images_name):
        image_name = images_name[option - 1]

        try:
            # Endpoint que cria container
            endpoint = f'/containers/create?fromImage={image_name}'

            # URL completa para a API do Docker
            docker_api_url = f'{docker_api}{endpoint}'

            # Defina os parâmetros de criação do container
            container_config = {
                "Image": image_name,
            }

            # Converte o dicionário em formato JSON
            data = json.dumps(container_config)

            # Cabeçalho da solicitação HTTP
            headers = {"Content-Type": "application/json"}

            # Faça a solicitação POST para criar o container
            response = requests.post(docker_api_url, data=data, headers=headers)

            # Verifique o código de resposta da solicitação
            if response.status_code == 201:
                container_info = response.json()
                container_id = container_info["Id"]
                print(f"Container criado com sucesso. ID do container: {container_id}")
            else:
                print(f"Falha ao criar o container. Código de resposta: {response.status_code}, Mensagem de erro: {response.text}")

        except Exception as e:
            print(f"Erro ao criar o container: {str(e)}")


def remove_images():

    list_images(see='No')

    print('\nEscolha o número da imagem que deseja remover')
    print('Temos essas imagens: \n')

    for index, image_id in enumerate(images_id, start=1):
        print(f"Imagem {index}: {image_id}")

    option = input('\nDigite o número da imagem que você deseja remover: ')

    option = int(option)
    if 1 <= option <= len(images_id):
        image_id = images_id[option - 1]

    try:
        endpoint = f'/images/{image_id}'
        response = requests.delete(f'{docker_api}{endpoint}')

        # Verifique se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            print(f"Imagem com ID {image_id} removida com sucesso.")
        else:
            print(f"Erro ao remover a imagem com ID {image_id} (Código de Status: {response.status_code})")

    except Exception as e:
        print(f"Erro ao remover a imagem com ID {image_id}: {str(e)}")


def get_info_system():
    
    try:

        endpoint = "/info"
        response = requests.get(f'{docker_api}{endpoint}')
        
        # Verifique se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            system_info = json.loads(response.text)
            print("\nInformações do Sistema Docker:")
            print("-" * 112)
            print(f"Nome do Sistema: {system_info['Name']}")
            print(f"Versão do Docker: {system_info['ServerVersion']}")
            print(f"Sistema Operacional: {system_info['OperatingSystem']}")
            print(f"Arquitetura: {system_info['Architecture']}")
            print(f"Kernel: {system_info['KernelVersion']}")
            print(f"Total de Contêineres: {system_info['Containers']}")
            print(f"Total de Imagens: {system_info['Images']}")
            print(f"Sistema de Armazenamento: {system_info['Driver']}")
            print(f"Tempo de Uptime: {system_info['SystemTime']}\n")

            # Você pode adicionar mais informações conforme necessário
        else:
            print(f"Erro ao obter informações do sistema Docker (Código de Status: {response.status_code})")

    except Exception as e:
        print(f"Erro ao obter informações do sistema Docker: {str(e)}")


def ping():
    try:
        # URL para a API do Docker para executar um "ping"
        endpoint = "/_ping"

        # Faça uma solicitação GET para executar o "ping"
        response = requests.get(f'{docker_api}{endpoint}')

        # Verifique se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            print("\nServidor Docker está disponível e responde ao ping.\n")
        else:
            print(f"\nErro ao executar o ping no servidor Docker (Código de Status: {response.status_code})\n")

    except Exception as e:
        print(f"\nErro ao executar o ping no servidor Docker: {str(e)}\n")


def get_version():
    
    try:
        # URL para a API do Docker para obter informações sobre a versão
        docker_api_url = "http://localhost:2375/version"

        # Faça uma solicitação GET para obter informações sobre a versão
        response = requests.get(docker_api_url)

        # Verifique se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            version_info = json.loads(response.text)
            print("\nInformações da Versão do Docker:")
            print("-" * 112, "\n")
            print(f"Versão do Docker: {version_info['Version']}")
            print(f"API Version: {version_info['ApiVersion']}")
            print(f"Versão de Go: {version_info['GoVersion']}")
            print(f"Sistema Operacional: {version_info['Os']}")
            print(f"Arquitetura: {version_info['Arch']}")
            print(f"Kernel: {version_info['KernelVersion']}\n")
        else:
            print(f"Erro ao obter informações da versão do Docker (Código de Status: {response.status_code})")

    except Exception as e:
        print(f"Erro ao obter informações da versão do Docker: {str(e)}")


def get_data_usage_info():
    try:
        # URL para a API do Docker para obter informações de uso de dados do sistema
        endpoint = "/system/df"

        # Faça uma solicitação GET para obter informações de uso de dados do sistema
        response = requests.get(f'{docker_api}{endpoint}')

        # Verifique se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            system_data_info = json.loads(response.text)
            print("\nInformações de Uso de Dados do Sistema Docker:")
            print("-" * 112)
            print(f"Uso de disco total: {system_data_info['LayersSize']} bytes")
            
            # Calcular o uso de disco total para imagens
            total_image_usage = sum(image['Size'] for image in system_data_info['Images'])
            print(f"Uso de disco para imagens: {total_image_usage} bytes")

            # Calcular o uso de disco total para contêineres
            total_container_usage = sum(container['SizeRootFs'] for container in system_data_info['Containers'])
            print(f"Uso de disco para contêineres: {total_container_usage} bytes\n")

            # Você pode adicionar mais informações conforme necessário
        else:
            print(f"Erro ao obter informações de uso de dados do sistema Docker (Código de Status: {response.status_code})")

    except Exception as e:
        print(f"Erro ao obter informações de uso de dados do sistema Docker: {str(e)}")

menu()