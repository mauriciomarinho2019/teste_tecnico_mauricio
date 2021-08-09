# Como Rodar 

### Criando Ambiente

```console
foo@bar:~$ sudo apt update 

foo@bar:~$ curl -fsSL https://get.docker.com -o get-docker.sh

foo@bar:~$ sh get-docker.sh

foo@bar:~$ sudo docker volume create portainer_data

foo@bar:~$ sudo docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce

```  

### Deploy Aplicação 

```console
foo@bar:~$ sudo docker build -t teste_tecnico_mauricio .

foo@bar:~$ sudo docker run  -d  -v /tmp/:/tmp/ --restart=always teste_tecnico_mauricio 

foo@bar:~$ sudo docker run  -d  -v /tmp/:/tmp/ --restart=always teste_tecnico_mauricio 

```
