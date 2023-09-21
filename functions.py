import requests
import json


# Api do docker
docker_api = 'http://localhost:2375'


def menu():
    pass


def list_containers(see=None):
    global containers_ids

    containers_ids = []

    # Endpoint que lista os containers
    endpoint = '/containers/json'

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
            container_image_name = container_info['Image']

            if see == None:
                print(f"\nID do Container: {container_id}")
                print(f"Nome do Container: {container_name}")
                print(f"Status do Container: {container_status}")
                print(f"Nome da Imagem: {container_image_name}")
                print("-" * 85, "\n")
            else:
                pass
    else:
        print(f"Falha ao listar os containers. Código de resposta: {response.status_code}, Mensagem de erro: {response.text}")


def create_container():

    # Endpoint que cria container
    endpoint = '/containers/create'
    
    image = input('Digite aqui o nome da imagem que você deseja criar: ')
    
    # Defina os parâmetros de criação do container
    container_config = {
        "Image": image,
        "HostConfig": {},
    }

    # Converte o dicionário em formato JSON
    data = json.dumps(container_config)

    # Cabeçalho da solicitação HTTP
    headers = {"Content-Type": "application/json"}

    # Faça a solicitação POST para criar o container
    response = requests.post(f"{docker_api}{endpoint}", data=data, headers=headers)

    # Verifique o código de resposta da solicitação
    if response.status_code == 201:
        container_info = response.json()
        container_id = container_info["Id"]
        print(f"Container criado com sucesso. ID do container: {container_id}")
    else:
        print(f"Falha ao criar o container. Código de resposta: {response.status_code}, Mensagem de erro: {response.text}")


def list_process_in_containers():

    list_containers(see='No')

    print('\nEscolha o número do container que deseja ver os processos')
    print('Temos esses containers com esses ids de pé: \n')

    for index, container_id in enumerate(containers_ids, start=1):
        print(f"Container {index}: {container_id}")

    option = input('\nDigite o número do container que você deseja ver os processos: ')

    try:
        option = int(option)
        if 1 <= option <= len(containers_ids):
            container_id = containers_ids[option - 1]

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
        list_process_in_containers()


def get_logs():
    list_containers(see='No')

    print('\nEscolha o número do container que deseja ver os logs')
    print('Temos esses containers com esses ids de pé: \n')

    for index, container_id in enumerate(containers_ids, start=1):
        print(f"Container {index}: {container_id}")

    option = input('\nDigite o número do container que você deseja ver os logs: ')

    try:
        option = int(option)
        if 1 <= option <= len(containers_ids):
            container_id = containers_ids[option - 1]

            # Endpoint que lista os processos dos containers
            endpoint = f'/containers/{container_id}/logs'

            response = requests.get(f'{docker_api}/containers/dc5412bfd614ad40c2a4228aa3d805063588be20bc1cb8c6c925ef5ac5862d43/logs')
            print(response.text)
            return

            # Verifique o código de resposta da solicitação
            if response.status_code == 200:
                print('\nAqui estão os logs:\n')

                containers_info = response.json()
                for process in containers_info['Processes']:
                    print(process)
            else:
                print(f"Falha ao listar os processos do container. Código de resposta: {response.status_code}, Mensagem de erro: {response.text}")
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")
        #list_process_in_containers()


get_logs()


def start_container():
    pass

def stop_container():
    pass

def restart_container():
    pass

def kill_container():
    pass

def remove_container():
    pass

def list_images():
    pass

def remove_images():
    pass

def get_info_system():
    pass

def ping():
    pass

def get_version():
    pass

def get_data_usage_infor():
    pass


#response = requests.get('http://localhost:2375/containers/json')
#print(response.status_code)



