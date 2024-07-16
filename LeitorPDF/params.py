import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ano = config.getint('configuracoes', 'ano')
mes = config.getint('configuracoes', 'mes')
esta_de_ferias = config.get('configuracoes', 'esta_de_ferias')
ferias_inicio = None
ferias_duracao = None

if esta_de_ferias.lower() == 's':
    ferias_inicio = config.get('configuracoes', 'ferias_inicio')
    ferias_duracao = config.getint('configuracoes', 'ferias_duracao')

eixo_x_entrada = config.getint('configuracoes', 'eixo_x_entrada')
eixo_x_saida = config.getint('configuracoes', 'eixo_x_saida')
hora_entrada_inicio = config.getint('configuracoes', 'hora_entrada_inicio')
minuto_entrada_inicio = config.getint('configuracoes', 'minuto_entrada_inicio')
hora_entrada_fim = config.getint('configuracoes', 'hora_entrada_fim')
minuto_entrada_fim = config.getint('configuracoes', 'minuto_entrada_fim')
caminho_pdf_original = config.get('configuracoes', 'caminho_pdf_original')
caminho_pdf_modificado = config.get('configuracoes', 'caminho_pdf_modificado')
caminho_imagem_assinatura = config.get('configuracoes', 'caminho_imagem_assinatura')
posicao_x_assinatura = config.getint('configuracoes', 'posicao_x_assinatura')
largura_assinatura = config.getint('configuracoes', 'largura_assinatura')
altura_assinatura = config.getint('configuracoes', 'altura_assinatura')
