from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime, timedelta
import holidays, random
from PyPDF2 import PdfReader, PdfWriter
import params
from PIL import Image, ImageEnhance

assinatura_imagem_path = params.caminho_imagem_assinatura

img = Image.open(assinatura_imagem_path)
img = img.convert("RGBA")
datas = img.getdata()
nova_imagem_data = [(255, 255, 255, 0) if item[:3] == (255, 255, 255) else item for item in datas]
img.putdata(nova_imagem_data)

enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)  

enhancer = ImageEnhance.Color(img)
img = enhancer.enhance(2)  

assinatura_imagem_transparente = "assinatura_transparente.png"
img.save(assinatura_imagem_transparente)

assinatura_imagem = assinatura_imagem_transparente

while True:
    pdf_original = params.caminho_pdf_original
    if pdf_original.endswith('.pdf'):
        break
    else:
        print("Por favor, forneça um caminho de arquivo válido com a extensão .pdf.")

pdf_modificado = params.caminho_pdf_modificado
pdf_temp = "temp.pdf"

feriados_br = holidays.Brazil(years=params.ano)
primeiro_dia_mes = datetime(params.ano, params.mes, 1)
total_dias_mes = (primeiro_dia_mes.replace(month=primeiro_dia_mes.month % 12 + 1) - primeiro_dia_mes).days

inicio_ferias = None
fim_ferias = None
if params.esta_de_ferias.lower() == 's':
    inicio_ferias = datetime.strptime(params.ferias_inicio, "%d/%m/%Y").date()
    fim_ferias = inicio_ferias + timedelta(days=params.ferias_duracao)

dias_atestado = []
if params.teve_atestado.lower() == 's':
    dias_atestado = params.dias_atestado  

altura_inicial = 666
altura_por_linha = 14.73
espaco_extra_sabado_domingo_feriado = 14  

c = canvas.Canvas(pdf_temp, pagesize=letter)
c.setFont("Helvetica", 10)  

altura_atual = altura_inicial
nao_uteis_contados = 0 

for dia in range(1, total_dias_mes + 1):
    data_atual = datetime(params.ano, params.mes, dia).date()
    
    if data_atual.weekday() >= 5 or data_atual in feriados_br:
        nao_uteis_contados += 1
        continue
    
    altura_ajustada = altura_atual - (dia - 1 - nao_uteis_contados) * altura_por_linha - nao_uteis_contados * espaco_extra_sabado_domingo_feriado
    
    if (inicio_ferias and inicio_ferias <= data_atual <= fim_ferias) or data_atual in dias_atestado:
        altura_ajustada -= espaco_extra_sabado_domingo_feriado * 0.5
        continue

    inicio = datetime(100, 1, 1, params.hora_entrada_inicio, params.minuto_entrada_inicio)
    fim = datetime(100, 1, 1, params.hora_entrada_fim, params.minuto_entrada_fim)
    diferenca_total_minutos = int((fim - inicio).total_seconds() / 60)
    minutos_aleatorios = random.randint(0, diferenca_total_minutos)

    horario_entrada_sorteado = inicio + timedelta(minutes=minutos_aleatorios)
    horario_entrada_str = horario_entrada_sorteado.strftime("%H:%M")
    c.drawString(params.eixo_x_entrada, altura_ajustada, horario_entrada_str)

    horario_saida = (horario_entrada_sorteado + timedelta(hours=10)).strftime("%H:%M")
    c.drawString(params.eixo_x_saida, altura_ajustada, horario_saida)

    posicao_x_assinatura = params.posicao_x_assinatura  
    largura_assinatura = params.largura_assinatura  
    altura_assinatura = params.altura_assinatura

    c.drawImage(assinatura_imagem, posicao_x_assinatura, altura_ajustada, width=largura_assinatura, height=altura_assinatura)

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
