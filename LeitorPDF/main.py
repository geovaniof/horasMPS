from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime, timedelta
import holidays, random
from PyPDF2 import PdfReader, PdfWriter

pdf_original = "C:/Projetos/LeitorPDF/pdfteste.pdf"
pdf_modificado = "C:/Projetos/LeitorPDF/pdfteste_modificado.pdf"

pdf_temp = "temp.pdf"
ano = 2024
mes = 3  

def perguntar_ferias():
    esta_de_ferias = input("O colaborador está de férias? (sim/não): ").lower()
    if esta_de_ferias == 'sim':
        inicio_ferias = input("Digite a data de início das férias (DD/MM/YYYY): ")
        duracao_ferias = int(input("Quantos dias de férias? "))
        inicio_ferias = datetime.strptime(inicio_ferias, "%d/%m/%Y").date()
        fim_ferias = inicio_ferias + timedelta(days=duracao_ferias)
        return inicio_ferias, fim_ferias
    else:
        return None, None

hora_entrada_inicio = int(input("Digite a hora de início para o intervalo de entrada (ex: 8 para 08:00): "))
minuto_entrada_inicio = int(input("Digite o minuto de início para o intervalo de entrada (ex: 1 para 08:01): "))
hora_entrada_fim = int(input("Digite a hora de fim para o intervalo de entrada (ex: 9 para 09:00): "))
minuto_entrada_fim = int(input("Digite o minuto de fim para o intervalo de entrada (ex: 9 para 08:09): "))

if hora_entrada_inicio == hora_entrada_fim and minuto_entrada_inicio > minuto_entrada_fim:
    minuto_entrada_fim = minuto_entrada_inicio

hora_entrada_inicio_str = f"{hora_entrada_inicio:02d}"
hora_entrada_fim_str = f"{hora_entrada_fim:02d}"

minuto_entrada = random.randint(minuto_entrada_inicio, minuto_entrada_fim)
minuto_entrada_str = f"{minuto_entrada:02d}"

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
    minuto_entrada = random.randint(1, 9)

    hora_entrada = random.randint(hora_entrada_inicio, hora_entrada_fim)
    minuto_entrada = random.randint(minuto_entrada_inicio, minuto_entrada_fim)
    horario_entrada = datetime.strptime(f"{hora_entrada:02d}:{minuto_entrada:02d}", "%H:%M")

    horario_entrada_str = horario_entrada.strftime("%H:%M")
    c.drawString(117, altura_ajustada, horario_entrada_str)

    horario_saida = (horario_entrada + timedelta(hours=10)).strftime("%H:%M")
    c.drawString(305, altura_ajustada, horario_saida)

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

print(f"PDF modificado salvo em: {pdf_modificado}")
