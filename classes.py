# Arquivo: classes.py
import csv
from datetime import date, timedelta
import io 

# Classe Base: Imovel 
class Imovel:
    VALOR_CONTRATO = 2000.00 # Fixo em R$2.000
    
    def __init__(self, tipo_imovel):
        self.tipo_imovel = tipo_imovel
        self.valor_base = 0.0
        
    def calcular_adicionais_padrao(self, tem_garagem=False):
        adicional = 0.0
        # Vagas custam R$ 300,00 para casas e aps.
        if self.tipo_imovel in ['Apartamento', 'Casa'] and tem_garagem:
            adicional += 300.00
        return adicional
    
    def calcular_aluguel_mensal(self):
        raise NotImplementedError ("Método 'calcular_aluguel_mensal' Deve ser implementado nas subs!")
    
    def gerar_orcamento_terminal(self, parcelas_contrato):
        """Este método gera o orçamento para o terminal (como no seu script original)"""
        aluguel_mensal = self.calcular_aluguel_mensal()
        
        if not 1 <= parcelas_contrato <=5:
            raise ValueError("O número de parcelas do contrato deve ser entre 1 e 5")
        
        valor_parcela_contrato = self.VALOR_CONTRATO / parcelas_contrato
        
        print("\n  - - - Orçamento Mensal Imobiliária R. M. - - - ")
        print(f"Tipo de Imóvel: {self.tipo_imovel}")
        print(f"O valor do aluguel mensal orçado: R${aluguel_mensal:.2f}")
        print(f"O valor do contrato imobiliário: R${self.VALOR_CONTRATO:.2f}")
        print(f"Parcelamento do contrato: {parcelas_contrato} x de R${valor_parcela_contrato:.2f}")
        print("-" * 40)
        
        return aluguel_mensal, valor_parcela_contrato

    def gerar_csv_data(self, aluguel_mensal, parcela_contrato, num_parcelas_contrato):
        """Gera o conteúdo do CSV como uma string para download via web."""
        output = io.StringIO() 
        escritor = csv.writer(output)
        
        data_inicio = date.today() + timedelta(days=30)
        
        # Cabeçalho
        escritor.writerow (['Parcela', 'Data de Vencimento', 'Valor do Aluguel (R$)', 'Valor do Contrato (R$)', 'Valor Total da Parcela (R$)'])
        
        for i in range (1, 13): # Loop das 12 parcelas
            data_vencimento = data_inicio + timedelta(days=30 * (i - 1))
            
            # Logica para colocar o valor das parcelas do contratoss nas X primeiras parcelas
            valor_contrato_na_parcela = parcela_contrato if i <= num_parcelas_contrato else 0.0
            
            valor_total = aluguel_mensal + valor_contrato_na_parcela
            
            # Writer
            escritor.writerow([
                i,
                data_vencimento.strftime('%d/%m/%Y'),
                f"{aluguel_mensal:.2f}",
                f"{valor_contrato_na_parcela:.2f}",
                f"{valor_total:.2f}"
            ])
            
        return output.getvalue() 


# 2. Classes filhas (Herança)
class Apartamento(Imovel):
    VALOR_BASE_1Q = 700.00 # Apartamentos com 1 Quarto
    
    def __init__(self, num_quartos, tem_garagem, tem_criancas):
        super().__init__("Apartamento")
        self.num_quartos = num_quartos
        self.tem_garagem = tem_garagem
        self.tem_criancas = tem_criancas
            
    def calcular_aluguel_mensal(self):
        aluguel = self.VALOR_BASE_1Q

        if self.num_quartos == 2:
            aluguel += 200.00 # Acréscimo para 2 quartos

        aluguel += self.calcular_adicionais_padrao(self.tem_garagem)

        if not self.tem_criancas:
            aluguel -= aluguel * 0.05 # Desconto de 5% se não tem crianças

        return aluguel

class Casa(Imovel):
    VALOR_BASE_1Q = 900.00 # Casas com 1 Quarto

    def __init__(self, num_quartos, tem_garagem):
        super().__init__("Casa")
        self.num_quartos = num_quartos
        self.tem_garagem = tem_garagem
            
    def calcular_aluguel_mensal(self):
        aluguel = self.VALOR_BASE_1Q

        if self.num_quartos == 2:
            aluguel += 250.00 # Acréscimo para 2 quartos

        aluguel += self.calcular_adicionais_padrao(self.tem_garagem)

        return aluguel
    
class Estudio(Imovel):
    VALOR_BASE = 1200.00  # Estudio R$ 1200,00
    VALOR_2_VAGAS = 250.00 # Valor de 2 vagas de estacionamento
    VALOR_VAGA_EXTRA = 60.00 # Valor de vaga extra
    
    def __init__(self, num_vagas_estacionamento):
        super().__init__("Estudio")
        self.num_vagas_estacionamento = num_vagas_estacionamento
    
    def calcular_aluguel_mensal(self):
        aluguel = self.VALOR_BASE
        adicional_estacionamento = 0.0

        if self.num_vagas_estacionamento > 0:
            # Valor fixo para até 2 vagas
            adicional_estacionamento += self.VALOR_2_VAGAS
            
            # Vagas extras
            vagas_extras = max(0, self.num_vagas_estacionamento - 2)
            adicional_estacionamento += vagas_extras * self.VALOR_VAGA_EXTRA

        aluguel += adicional_estacionamento
        return aluguel
