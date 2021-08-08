## Como Rodar 

### Construir a Imagem 
sudo docker build -t  TEST_TEC_BOLETIM .

sudo docker run  -d  -v /tmp/:/tmp/ --restart=always TEST_TEC_BOLETIM 
 
 