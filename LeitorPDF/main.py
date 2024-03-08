from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime, timedelta
import holidays, random
from PyPDF2 import PdfReader, PdfWriter

pdf_original = "C:/Projetos/horasMPS/LeitorPDF/pdfteste.pdf"
pdf_modificado = "C:/Projetos/horasMPS/LeitorPDF/pdfteste_modificado.pdf"

pdf_temp = "temp.pdf"
ano = datetime.now().year
mes = datetime.now().month

print(f"Mês corrente: {mes}, Ano corrente: {ano}\n")

def perguntar_ferias():
    while True:
        esta_de_ferias = input("O colaborador teve ferias esse mês? (sim/não): ").lower()
        if esta_de_ferias in ['sim', 's']:
            inicio_ferias = input("Digite a data de início das férias (DD/MM/YYYY): ")
            duracao_ferias = int(input("Quantos dias de férias? "))
            inicio_ferias = datetime.strptime(inicio_ferias, "%d/%m/%Y").date()
            fim_ferias = inicio_ferias + timedelta(days=duracao_ferias)
            return inicio_ferias, fim_ferias
        elif esta_de_ferias in ['não', 'nao', 'n']:
            return None, None
        else:
            print("Por favor, responda com 'sim' ou 'não'.")

def get_input_int(mensagem, minimo=0, maximo=59):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"Por favor, digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Por favor, digite um número inteiro.")

hora_entrada_inicio = get_input_int("Digite a hora de início para o intervalo de entrada (ex: 8 para 08:00): ", 0, 23)
minuto_entrada_inicio = get_input_int("Digite o minuto de início para o intervalo de entrada (ex: 1 para 08:01): ", 0, 59)

hora_entrada_fim = get_input_int("Digite a hora de fim para o intervalo de entrada (ex: 9 para 09:00): ", hora_entrada_inicio, 23)
minuto_entrada_fim = get_input_int("Digite o minuto de fim para o intervalo de entrada (ex: 9 para 08:09): ", minuto_entrada_inicio if hora_entrada_fim == hora_entrada_inicio else 0, 59)

posicao_x_entrada = int(input("\nDigite a posição no eixo X para o horário de entrada (ex: 117): "))
posicao_x_saida = int(input("Digite a posição no eixo X para o horário de saída (ex: 305): "))

inicio = datetime(100, 1, 1, hora_entrada_inicio, minuto_entrada_inicio)
fim = datetime(100, 1, 1, hora_entrada_fim, minuto_entrada_fim)

diferenca_total_minutos = int((fim - inicio).total_seconds() / 60)

inicio_ferias, fim_ferias = perguntar_ferias()

pdf_temp = "temp.pdf"
ano = 2024
mes = 3

feriados_br = holidays.Brazil(years=ano)
primeiro_dia_mes = datetime(ano, mes, 1)
total_dias_mes = (primeiro_dia_mes.replace(month=primeiro_dia_mes.month % 12 + 1) - primeiro_dia_mes).days

altura_inicial = 666
altura_por_linha = 14.73
espaco_extra_sabado_domingo_feriado = 14  

c = canvas.Canvas(pdf_temp, pagesize=letter)
c.setFont("Helvetica", 10)  

altura_atual = altura_inicial
nao_uteis_contados = 0  

for dia in range(1, total_dias_mes + 1):
    data_atual = datetime(ano, mes, dia).date()
    
    if data_atual.weekday() >= 5 or data_atual in feriados_br or (inicio_ferias and inicio_ferias <= data_atual <= fim_ferias):
        nao_uteis_contados += 1
        if data_atual.weekday() == 4 and (data_atual + timedelta(days=1)) in feriados_br:
            nao_uteis_contados += 2  
        continue
    
    altura_ajustada = altura_atual - (dia - 1 - nao_uteis_contados) * altura_por_linha - nao_uteis_contados * espaco_extra_sabado_domingo_feriado
    
    minutos_aleatorios = random.randint(0, diferenca_total_minutos)

    horario_entrada_sorteado = inicio + timedelta(minutes=minutos_aleatorios)
    horario_entrada_str = horario_entrada_sorteado.strftime("%H:%M")
    c.drawString(posicao_x_entrada, altura_ajustada, horario_entrada_str)

    horario_saida = (horario_entrada_sorteado + timedelta(hours=10)).strftime("%H:%M")
    c.drawString(posicao_x_saida, altura_ajustada, horario_saida)

c.save()

reader_original = PdfReader(pdf_original)
reader_temp = PdfReader("temp.pdf")
writer = PdfWriter()

page = reader_original.pages[0]
page.merge_page(reader_temp.pages[0])
writer.add_page(page)

for i in range(1, len(reader_original.pages)):
    writer.add_page(reader_original.pages[i])

with open(pdf_modificado, "wb") as output_pdf:
    writer.write(output_pdf)

print(f"\nPDF modificado salvo em: {pdf_modificado}")
