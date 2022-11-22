# pip install psutil
# pip install rpy2
# pip install pandas
# pip install mysql-connector-python


# Biblioteca de captura de dados de máquina
import psutil as ps
from collections import deque
from time import sleep
from datetime import datetime 

# Bibliotecas para conexão com r
import pandas as pd
import rpy2
import rpy2.robjects as ro
import rpy2.robjects.packages as rpackages
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr, data
from rpy2.robjects.vectors import StrVector



# Importando pacote base do R
base = importr('base')

# Instalando packages do R 
utils = importr('utils')
utils.chooseCRANmirror(ind=1) # CRAN é um network de arquivos onde são mantidos pacotes em R
packnames = ["ggplot2", "lazyeval", "grDevices"] # Pacotes que serão utilizados

# Verificando quais pacotes já estão instalados e instalando os não instalados
packages_a_instalar = [packname for packname in packnames if not rpackages.isinstalled(packname)]
if len(packages_a_instalar) > 0:
  utils.install_packages(StrVector(packages_a_instalar))


# Biblioteca de gráficos em r
import rpy2.robjects.lib.ggplot2 as ggplot2

# Biblioteca para conexão com mysql
import mysql.connector as sql



def main():
  capturarDados()



def capturarDados():

  cont = 0

  ids = deque([])
  cpuPercent = deque([])
  ramPercent = deque([])
  diskPercent = deque([])


  while cont < 100:

    # Captura de dados de máquina

    ids.append(cont)
    cpuPercent.append(ps.cpu_percent())
    ramPercent.append(ps.virtual_memory().percent)
    diskPercent.append(ps.disk_usage("/").percent)

    print(f"Captura {cont}\n\n")
    print(ids)
    print(cpuPercent)
    print(ramPercent)
    print(diskPercent)

    sleep(1)
    cont += 1

  
  # Data frame (pandas) de exemplo
  pd_df = pd.DataFrame({'id': ids,
                        'cpu': cpuPercent,
                        'ram': ramPercent,
                        'disk': diskPercent})

  # Conversor de data frame do pandas para o data frame em r
  with localconverter(ro.default_converter + pandas2ri.converter):
    dadosMaquina = ro.conversion.py2rpy(pd_df)

  
  plotarGrafico(dadosMaquina)



def plotarGrafico(dadosMaquina):

  metricas = ["cpu","ram","disk"]

  for metrica in metricas:

    # Gera um .png vazio
    grdevices = importr('grDevices')
    grdevices.png(file=f"./graficos/{metrica}.png", width=1024, height=512)

    # Plota o gráfico
    pp = (ggplot2.ggplot(dadosMaquina) +
        ggplot2.aes_string(x='id', y=metrica) +
        ggplot2.geom_point() +
        ggplot2.geom_line() +
        ggplot2.geom_smooth(method = 'lm'))

    sleep(1)
    pp.plot()

    # Salva o gráfico no .png
    grdevices.dev_off()

    # if cont >= 20:
    #   ids.popleft()
    #   cpuPercent.popleft()
    #   ramPercent.popleft()
    #   diskPercent.popleft()


# Iniciando programa
main()