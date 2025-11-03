# Arquivo: app.py
from flask import Flask, render_template, request, Response
from classes import Apartamento, Casa, Estudio # Importa suas classes

app = Flask(__name__)

def _processar_dados_formulario(form_data):
    """Função auxiliar para processar os dados do formulário."""
    tipo_imovel = form_data.get('tipo_imovel')
    num_quartos = int(form_data.get('num_quartos', 1))
    tem_garagem = 'tem_garagem' in form_data
    tem_criancas = 'tem_criancas' in form_data # Checkbox marcado = tem crianças
    num_vagas_estudio = int(form_data.get('num_vagas_estudio', 0))
    parcelas_contrato = int(form_data.get('parcelas_contrato', 5))

    imovel = None
    if tipo_imovel == 'apartamento':
        imovel = Apartamento(num_quartos, tem_garagem, tem_criancas)
    elif tipo_imovel == 'casa':
        imovel = Casa(num_quartos, tem_garagem)
    elif tipo_imovel == 'estudio':
        imovel = Estudio(num_vagas_estudio)
        
    return imovel, parcelas_contrato

@app.route('/')
def index():
    """Renderiza a página inicial com o formulário."""
    return render_template('index.html')

@app.route('/orcamento', methods=['POST'])
def orcamento():
    """Recebe os dados do formulário, calcula e mostra o resultado."""
    try:
        imovel, parcelas_contrato = _processar_dados_formulario(request.form)
        
        if imovel:
            aluguel_mensal = imovel.calcular_aluguel_mensal()
            valor_parcela_contrato = imovel.VALOR_CONTRATO / parcelas_contrato

            # Dados para enviar para a página de resultado
            contexto = {
                'tipo_imovel': imovel.tipo_imovel,
                'aluguel_mensal': f'{aluguel_mensal:.2f}',
                'valor_contrato': f'{imovel.VALOR_CONTRATO:.2f}',
                'parcelas_contrato': parcelas_contrato,
                'valor_parcela_contrato': f'{valor_parcela_contrato:.2f}'
            }
            return render_template('resultado.html', **contexto)
        
    except Exception as e:
        return f"Ocorreu um erro ao processar seu pedido: {e}"

    return "Tipo de imóvel inválido", 400

@app.route('/download_csv', methods=['POST'])
def download_csv():
    """Gera e faz o download do arquivo CSV."""
    try:
        imovel, parcelas_contrato = _processar_dados_formulario(request.form)
        
        if imovel:
            aluguel_mensal = imovel.calcular_aluguel_mensal()
            valor_parcela_contrato = imovel.VALOR_CONTRATO / parcelas_contrato
            
            # Chama a nova função para gerar os dados do CSV
            csv_data = imovel.gerar_csv_data(aluguel_mensal, valor_parcela_contrato, parcelas_contrato)
            
            # Retorna o CSV como um download para o usuário
            return Response(
                csv_data,
                mimetype="text/csv",
                headers={"Content-disposition":
                         "attachment; filename=orcamento_12_parcelas.csv"}
            )
            
    except Exception as e:
        return f"Ocorreu um erro ao gerar o CSV: {e}"

    return "Tipo de imóvel inválido", 400


if __name__ == '__main__':
    app.run(debug=True)