# Biblioteca de captura de dados de máquina
import psutil as ps

# Bibliotecas para conexão com r
import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr, data

# Biblioteca de gráficos em r
import rpy2.robjects.lib.ggplot2 as ggplot2

# Data frame (pandas) de exemplo
pd_df = pd.DataFrame({'id': [1,2,3],
                      'valor': [10, 20, 30]})

# Conversor de data frame do pandas para o data frame em r
with localconverter(ro.default_converter + pandas2ri.converter):
  r_from_pd_df = ro.conversion.py2rpy(pd_df)

grdevices = importr('grDevices')
grdevices.png(file="/home/aluno/Music/teste-r-html/teste.png", width=1024, height=512)

pp = (ggplot2.ggplot(r_from_pd_df) +
    ggplot2.aes_string(x='id', y='valor') +
    ggplot2.geom_point() +
    ggplot2.geom_smooth(method = 'lm'))

pp.plot()

grdevices.dev_off()