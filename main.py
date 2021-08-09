import schedule
import time
import pandas as  pd 
from utils import *
from console_logging.console import Console
from datetime import datetime as dt, timedelta as delta
console = Console()

endpoint = "https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=gerarCSVFechamentoMoedaNoPeriodo&ChkMoeda=61&DATAINI={}&DATAFIM={}"
 
endpoint_euro = "https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=gerarCSVFechamentoMoedaNoPeriodo&ChkMoeda=222&DATAINI={}&DATAFIM={}"

## criar uma funcao para extrair dados em dolar
def extracao_base(moeda, dt_inicial, dt_final):
  console.log(moeda)
  console.log("ETAPA DE EXTRACAO")
  if moeda == "USD": 
      # codigo 
      url = endpoint.format(dt_inicial, dt_final)
      df = pd.read_csv (url, sep = ";", names=['Data','Cod_Moeda',"Tipo_Moeda",'Moeda','USD_compra',"USD_Venda","Aux","Aux1"]) 
      return df[['Data','USD_compra','USD_Venda']]
      
  if moeda == "EURO":
      # codigo aqui 
      url = endpoint_euro.format(dt_inicial, dt_final)
      df = pd.read_csv(url, sep = ";",names=['Data', 'Cod_Moeda',"Tipo_moeda",'Moeda','EURO_compra',"EURO_venda","Aux","Auxi1"])   
      return df[['Data','EURO_compra','EURO_venda']]

# funcao de transformação 

def transformacao_base(df):
  console.info ("ETAPA DE TRANSFORMACAO")
  df['Data'] = df["Data"].apply(checking_valid_dates)
  return df

## criar uma funcao de load carga
def carregar_csv(moeda,df): 
  console.info("ETAPA DE CARGA")
  arquivo = "base_{}.csv".format(moeda)
  df.to_csv(arquivo,index=False)    
   

def job():
   dt_inicial = str(dt.now().date() - delta(days=20))
   dt_final =  str(dt.now().date())

   dt_inicial = dt.strptime(dt_inicial, "%Y-%m-%d").strftime("%d/%m/%Y")
   dt_final = dt.strptime(dt_final, "%Y-%m-%d").strftime("%d/%m/%Y")
   
   ## buscar dados api do boletim em dolar 
   # aqui em baixo 
   base = extracao_base("USD",dt_inicial, dt_final)
   # transformação_base
   base_nova = transformacao_base(base)
   # carregando base para csv
   carregar_csv("USD",base_nova)  

   ## buscar dados api boletim em euro 
   base = extracao_base("EURO",dt_inicial, dt_final)
   base_nova = transformacao_base(base)
   carregar_csv("EURO",base_nova)

   # concatenar as bases 
   console.info("[CONCATENANDO BASES") 
   base_USD=pd.read_csv("base_USD.csv")
   base_EURO=pd.read_csv("base_EURO.csv")
   base_EURO.drop(['Data'],inplace=True, axis=1)

   final_base = pd.concat([base_USD, base_EURO],axis = 1)
   final_base.to_csv("/tmp/final.csv",index=False)
   console.success("final.csv")

def main ():
  schedule.every().day.at("21:20").do(job)
  while True:
    schedule.run_pending()
    time.sleep(1)
    console.log ("...Aguardando")

if __name__ == "__main__":
    main()  