import pandas as pd ## BIBLIOTECA PANDAS PARA LER DADOS NA VARIAVEL PD
import plotly.express as px # BIBLIOTECA PLOTLY PARA FAZER GRAFICOS NA VARIAVEL PX
import plotly.io as pio # PIO NAO CRIA, MAS EXIBE O GRAFICO 
import matplotlib.pyplot as plt #PLOTLIB PARA CONSTRUIR O GRAFÍCO USANDO PANDAS E PLOTLIB
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf #API PARA DADOS DO YAHOO FINANCEIROS
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#BUSCANDO OS DADOS DA PLANILHA 

df_principal = pd.read_excel("Imersáo Py.xlsx", sheet_name="Principal") #VARIAVEL lPLANILHA = PANDAS.LER_EXCEL("LOCAL DO ARQUIVO", NOME DA PLANILHA="NOME DA PAGINA DO EXCEL")
# print(df_principal)

df_total_acoes = pd.read_excel("Imersáo Py.xlsx", sheet_name="Total_de_acoes")
# print(df_total_acoes) 

df_ticker = pd.read_excel("Imersáo Py.xlsx", sheet_name="Ticker")
# print(df_ticker) 

df_chatgpt = pd.read_excel("Imersáo Py.xlsx", sheet_name="Chat gpt")
# print(df_chatgpt) 

pd.options.display.float_format = '{:.2f}'.format

df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy() #EXIBINDO APENAS AS COLUNAS INFORMADAS 
df_principal = df_principal.rename(columns={'Último (R$)':'Valor Final', 'Var. Dia (%)':'Var_Dias_Pct'}).copy() #RENOMEANDO AS COLUNAS A FIM DE EVITAR ERRO NO CÓDIGO DEVIDO A CARACTERES ESPECIAIS
df_principal['Var_pct'] = df_principal['Var_Dias_Pct'] / 100 #CRIANDO UMA COLUNA NOVA E FAZENDO A FORMULA DE VARIAÇÃO DE DIAS EM %
df_principal['Var_inicial'] = df_principal['Valor Final'] / (df_principal['Var_pct'] + 1) #CRIANDO A COLUNA DE VARIAÇÃO INICIAL (VALOR FINAL / VARIAÇÃO PERCENTUAL +1)
df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left') # .MERGE PARA FAZER O PROCV | LADO ESQUERDO É A ABA PRINCIAPL E A DIREITA É A ABA ONDE BUSCA OS VALORES e depois HOW indica que a aba da esquerda é a principal
df_principal = df_principal.drop(columns=['Código']) #REMOVENDO A COLUNA A COLUNO CÓDIGO
df_principal['Variacao_RS'] = (df_principal['Valor Final'] - df_principal['Var_inicial']) * df_principal['Qtde. Teórica'] # CRIANDO VARIAÇÃO EM REAIS (VALOR FINAL - INICIAL * QTDE TEORICA QUE FOI PUXADA DE OUTRA ABA .MERGE)
df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int) #FORMANDO A COLUNA QUANTIDADE TEORIA QUE É INT 
df_principal = df_principal.rename(columns={'Qtde. Teórica':'Qtd_teorica'}).copy() # RENOMEANDO
df_principal['Resultado'] = df_principal['Variacao_RS'].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável')) #CRIANDO A COLUNA RESULTADO APLICANDO O LAMBDA QUE APLICA A FUNÇÃO DE LINHA A LINHA 
df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left') #PROCV DA ABA TICKER 
df_principal = df_principal.drop(columns=['Ticker']) #REMOVENDO A COLUNA A COLUNOA TICKERCÓDIGO
df_principal = df_principal.merge(df_chatgpt, left_on='Nome', right_on='Empresa', how='left') #PROCV DA ABA TICKER 
df_principal = df_principal.drop(columns=['Empresa']) #REMOVENDO A COLUNA A COLUNOA TICKERCÓDIGO
df_principal = df_principal.rename(columns={'Idade (anos)':'Idade'}).copy() # RENOMEANDO
df_principal['Cat_Idade'] = df_principal['Idade'].apply(lambda x: 'Mais ded 100' if x >100 else ('Menos de 50' if x > 50 else 'Entre 50 e 100')) #FAZENDO DE CONFORME A IDADE

print(df_principal)

maior_valor = df_principal['Variacao_RS'].max() #VARIÁVEL QUE ATRIBUI A FUNÇÃO ACHAR O MAIOR VALOR NA COLUNA VARIÇAO_RS
menor_valor = df_principal['Variacao_RS'].min() #VARIÁVEL QUE ATRIBUI A FUNÇÃO ACHAR O MENOR VALOR NA COLUNA VARIÇAO_RS
media = df_principal['Variacao_RS'].mean()      #VARIÁVEL QUE ATRIBUI A FUNÇÃO ACHAR A MÉDIA VALOR NA COLUNA VARIÇAO_RS

media_subiu = df_principal[df_principal['Resultado'] == 'Subiu']['Variacao_RS'].mean() #VARIÁVEL QUE ATRIBUI A FUNÇÃO ACHAR A MÉIDA DE QUEM SUBIU NA COLUNA VARIÇAO_RS
media_desceu = df_principal[df_principal['Resultado'] == 'Desceu']['Variacao_RS'].mean() #VARIÁVEL QUE ATRIBUI A FUNÇÃO ACHAR A MÉIDA DE QUEM DESCEU NA COLUNA VARIÇAO_RS
df_principal_subiu = df_principal[df_principal['Resultado'] == 'Subiu'] #DF NOVO SÓ COM OS VALORES QUE SUBIRAM 

# Exibir os resultados COM FORMATAÇÃO DE NÚMERO FLOAT 
print("Maior R$ {:.2f}".format(maior_valor))
print("Menor R$ {:.2f}".format(menor_valor))
print("Média R$ {:.2f}".format(media))
print("Média de quem subiu R$ {:.2f}".format(media_subiu))
print("Média de quem desceu R$ {:.2f}".format(media_desceu))

print(df_principal_subiu)

df_analise_segmento = df_principal_subiu.groupby('Segmento')['Variacao_RS'].sum().reset_index() #AGRUPAR POR SEGMENTO DA COLUNA DE VARIAÇÃO #.SUM É SOMASE E RESET INDEX MANTEM O GROUPBY COMO DATAFRAME
print(df_analise_segmento)

df_analise_saldo = df_principal.groupby('Resultado')['Variacao_RS'].sum().reset_index() #AGRUPANDO VALOR POR RESUTALDO DA VARIAÇÃO 
print(df_analise_saldo)

fig = px.bar(df_analise_saldo, x= 'Resultado', y='Variacao_RS', text='Variacao_RS', title='Varição em Reais por Resultado') #X É A BASE, Y É A COLUNA 
fig.write_html('plot.html') # OPTEI PELA FIG.WRITE_HTML QUE ABRE UM ARQUIVO HTML PARA EXIBIR, O FIG.SHOW EXIBE NO TERMINAL 
#fig.show()

dados = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-31') ##SA é A NOMECLATURA BRASILEIRA  #DATA SEMPRE PADRAO AMERICANO
dados.columns = ['Abertura', 'Maximo', 'Minimo', 'Fechamento', 'Fech_Ajust', 'Volume'] #RENOMENADO AS COLUNAS DOS DADOS TRAZIDOS DA API
dados = dados.rename_axis('Data') #RENOMEANDO A DATA
dados['Fechamento'].plot(figsize=(10,6)) #CRIANDO O GRAFICO

plt.title('Preço de Fechamento da PETR4 em 2023', fontsize=16) #TITULO COM FORMATAÇÃO DA LETRA
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento')
plt.grid(True)
plt.legend('fechamento') #LEGENDA
plt.show() #EXIBINDO O GRAFICO 

#print(dados)

df = dados.head(60).copy() #TRAZENDO APENAS 60 LINHAS 
df['Data'] = df.index 
df['Data'] = df['Data'].apply(mdates.date2num) #CONVERTENDO AS DATAS PARA O NUMEROS NUMERICOS DE MATPLOTLIB

print(df)

fig, ax = plt.subplots(figsize=(15, 8))

# Vamos definir a largura dos candles no gráfico
width = 0.7

for i in range(len(df)):
    # Determinando a cor do candle
    # Se o preço de fechamento for maior que o de abertura, o candle é verde (a ação valorizou nesse dia).
    # Se for menor, o candle é vermelho (a ação desvalorizou).
    if df['Fechamento'].iloc[i] > df['Abertura'].iloc[i]: #se o fechamento for maior que a abertura é green 
        color = 'green'
    else:
        color = 'red'

    # Desenhando a linha vertical do candle (mecha)
    # Essa linha mostra os preços máximo (topo da linha) e mínimo (base da linha) do dia.
    # Usamos `ax.plot` para desenhar uma linha vertical.
    # [df['Data'].iloc[i], df['Data'].iloc[i]] define o ponto x da linha (a data), e [df['Mínimo'].iloc[i], df['Máximo'].iloc[i]] define a altura da linha.
    ax.plot([df['Data'].iloc[i], df['Data'].iloc[i]],
            [df['Minimo'].iloc[i], df['Maximo'].iloc[i]],
            color=color,
            linewidth=1)

    ax.add_patch(plt.Rectangle((df['Data'].iloc[i] - width/2, min(df['Abertura'].iloc[i], df['Fechamento'].iloc[i])),
                               width,
                               abs(df['Fechamento'].iloc[i] - df['Abertura'].iloc[i]),
                               facecolor=color))

df['MA7'] = df['Fechamento'].rolling(window=7).mean() #MÉDIA DE 7 DIAS ROLANDO DE 7 EM 7 
df['MA14'] = df['Fechamento'].rolling(window=14).mean()

# Plotando as médias móveis
ax.plot(df['Data'], df['MA7'], color='orange', label='Média Móvel 7 Dias')  # Média de 7 dias
ax.plot(df['Data'], df['MA14'], color='yellow', label='Média Móvel 14 Dias')  # Média de 14 dias
# Adicionando legendas para as médias móveis
ax.legend()

# Formatando o eixo x para mostrar as datas
# Configuramos o formato da data e a rotação para melhor legibilidade
ax.xaxis_date() #O método xaxis_date() é usado para dizer ao Matplotlib que as datas estão sendo usadas no eixo x
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Adicionando título e rótulos para os eixos x e y
plt.title("Gráfico de Candlestick - PETR4.SA com matplotlib")
plt.xlabel("Data")
plt.ylabel("Preço")

# Adicionando uma grade para facilitar a visualização dos valores
plt.grid(True)

# Exibindo o gráfico
plt.show()

# Criando subplots
'''
"Primeiro, criamos uma figura que conterá nossos gráficos usando make_subplots.
Isso nos permite ter múltiplos gráficos em uma única visualização.
Aqui, teremos dois subplots: um para o gráfico de candlestick e outro para o volume de transações."

'''
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=('Candlesticks', 'Volume Transacionado'),
                    row_width=[0.2, 0.7])

'''
"No gráfico de candlestick, cada candle representa um dia de negociação,
mostrando o preço de abertura, fechamento, máximo e mínimo. Vamos adicionar este gráfico à nossa figura."
'''
# Adicionando o gráfico de candlestick
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Abertura'],
                             high=df['Maximo'],
                             low=df['Minimo'],
                             close=df['Fechamento'],
                             name='Candlestick'),
                             row=1, col=1)

# Adicionando as médias móveis
# Adicionamos também médias móveis ao mesmo subplot para análise de tendências
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA7'],
                         mode='lines',
                         name='MA7 - Média Móvel 7 Dias'),
                         row=1, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA14'],
                         mode='lines',
                         name='MA14 - Média Móvel 14 Dias'),
                         row=1, col=1)

# Adicionando o gráfico de barras para o volume
# Em seguida, criamos um gráfico de barras para o volume de transações, que nos dá uma ideia da atividade de negociação naquele dia
fig.add_trace(go.Bar(x=df.index,
                     y=df['Volume'],
                     name='Volume'),
                     row=2, col=1)

# Atualizando layout
#Finalmente, configuramos o layout da figura, ajustando títulos, formatos de eixo e outras configurações para tornar o gráfico claro e legível.
fig.update_layout(yaxis_title='Preço',
                  xaxis_rangeslider_visible=False,  # Desativa o range slider
                  width=1100, height=600)

# Mostrando o gráfico
fig.show()

dados = yf.download('AAPL', start='2023-01-01', end='2023-12-31')
mpf.plot(dados.head(30), type='candle', figsize = (16,8), volume=True, mav=(7,14))