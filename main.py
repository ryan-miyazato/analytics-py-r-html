# pip install psutil
# pip install rpy2
# pip install pandas
# pip install mysql-connector-python


# Biblioteca de captura de dados de máquina
import psutil as ps
from collections import deque
from time import sleep

# Bibliotecas para conexão com r
import pandas as pd
import rpy2
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr, data

# Biblioteca de gráficos em r
import rpy2.robjects.lib.ggplot2 as ggplot2

# Biblioteca para conexão com mysql
import mysql.connector as sql

base = importr('base')

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

  print(ids)
  print(cpuPercent)
  print(ramPercent)
  print(diskPercent)

  if cont >= 20:
    # Data frame (pandas) de exemplo
    pd_df = pd.DataFrame({'id': ids,
                          'cpu': cpuPercent,
                          'ram': ramPercent,
                          'disk': diskPercent})

    # Conversor de data frame do pandas para o data frame em r
    with localconverter(ro.default_converter + pandas2ri.converter):
      dadosMaquina = ro.conversion.py2rpy(pd_df)

    metricas = ["cpu","ram","disk"]

    for metrica in metricas:

      # Gera um .png vazio
      grdevices = importr('grDevices')
      grdevices.png(file=f"~/Music/analytics-py-r-html/graficos/{metrica}.png", width=1024, height=512)

      # Plota o gráfico
      pp = (ggplot2.ggplot(dadosMaquina) +
          ggplot2.aes_string(x='id', y=metrica) +
          ggplot2.geom_point() +
          ggplot2.geom_smooth(method = 'lm'))

      pp.plot()

      # Salva o gráfico no .png
      grdevices.dev_off()

    ids.popleft()
    cpuPercent.popleft()
    ramPercent.popleft()
    diskPercent.popleft()

  sleep(3)
  cont += 1