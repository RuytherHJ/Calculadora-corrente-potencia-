import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Funções utilitárias para cálculos
def potencia_para_corrente(potencia, tensao, fator_potencia=1.0):
    corrente = potencia / (tensao * fator_potencia)
    return corrente

def capacidade_de_conducao_corrente(corrente, metodo_instalacao):
    tabela_capacidade = {
        'A1': [(1.5, 14), (2.5, 19), (4, 26), (6, 34), (10, 46)],
        'B1': [(1.5, 13), (2.5, 18), (4, 24), (6, 31), (10, 42)]
    }
    
    for secao, capacidade in tabela_capacidade.get(metodo_instalacao, []):
        if corrente <= capacidade:
            return secao
    return None

def verificacao_disjuntor(corrente, secao):
    tabela_disjuntor = {
        1.5: 16,
        2.5: 20,
        4: 25,
        6: 32,
        10: 40
    }
    
    return tabela_disjuntor.get(secao, None)

# Função para processar a entrada e calcular a seção do condutor
def calcular_secao():
    try:
        entrada_tipo = tipo_var.get()
        metodo_instalacao = metodo_combobox.get().strip().upper()
        tensao = 220  # Supondo uma tensão padrão de 220V para o exemplo

        if entrada_tipo == 'A':
            corrente = float(corrente_entry.get().strip())
        elif entrada_tipo == 'W':
            potencia = float(potencia_entry.get().strip())
            fator_potencia = float(fp_entry.get().strip())
            corrente = potencia_para_corrente(potencia, tensao, fator_potencia)
        else:
            raise ValueError("Tipo de entrada inválido!")

        secao = capacidade_de_conducao_corrente(corrente, metodo_instalacao)
        if secao is None:
            result_label.config(text="Não foi possível determinar a seção do condutor.")
        else:
            result_text = f"A seção recomendada do condutor é {secao} mm²."
            corrente_disjuntor = verificacao_disjuntor(corrente, secao)
            if corrente_disjuntor:
                result_text += f"\nA corrente do disjuntor recomendada é {corrente_disjuntor} A."
            else:
                result_text += "\nNão foi possível determinar a corrente do disjuntor."
            result_label.config(text=result_text)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para limpar a entrada
def limpar_entradas():
    tipo_var.set('A')
    corrente_entry.delete(0, tk.END)
    potencia_entry.delete(0, tk.END)
    fp_entry.delete(0, tk.END)
    metodo_combobox.set('')
    result_label.config(text="")
    update_fields()

# Função para atualizar os campos de entrada com base no tipo selecionado
def update_fields(*args):
    entrada_tipo = tipo_var.get()
    if entrada_tipo == 'A':
        corrente_label.grid(row=1, column=0, sticky=tk.W)
        corrente_entry.grid(row=1, column=1)
        potencia_label.grid_forget()
        potencia_entry.grid_forget()
        fp_label.grid_forget()
        fp_entry.grid_forget()
    elif entrada_tipo == 'W':
        corrente_label.grid_forget()
        corrente_entry.grid_forget()
        potencia_label.grid(row=2, column=0, sticky=tk.W)
        potencia_entry.grid(row=2, column=1)
        fp_label.grid(row=3, column=0, sticky=tk.W)
        fp_entry.grid(row=3, column=1)

# Criação da janela principal
janela = tk.Tk()
janela.title("Calculadora de Seção do Condutor")

# Widgets para entrada de dados
tipo_var = tk.StringVar(value='A')
tipo_var.trace_add('write', update_fields)

tk.Label(janela, text="Tipo de Entrada:").grid(row=0, column=0, sticky=tk.W)
tk.Radiobutton(janela, text="Corrente (A)", variable=tipo_var, value='A').grid(row=0, column=1, sticky=tk.W)
tk.Radiobutton(janela, text="Potência (W)", variable=tipo_var, value='W').grid(row=0, column=2, sticky=tk.W)

corrente_label = tk.Label(janela, text="Corrente (A):")
corrente_entry = tk.Entry(janela)

potencia_label = tk.Label(janela, text="Potência (W):")
potencia_entry = tk.Entry(janela)

fp_label = tk.Label(janela, text="Fator de Potência:")
fp_entry = tk.Entry(janela)

tk.Label(janela, text="Método de Instalação:").grid(row=4, column=0, sticky=tk.W)
metodo_combobox = ttk.Combobox(janela, values=["A1", "B1"])
metodo_combobox.grid(row=4, column=1)

# Botões
tk.Button(janela, text="Calcular", command=calcular_secao).grid(row=5, column=0)
tk.Button(janela, text="Limpar", command=limpar_entradas).grid(row=5, column=1)

# Label para exibir resultados
result_label = tk.Label(janela, text="")
result_label.grid(row=6, columnspan=2)

# Atualiza os campos inicialmente
update_fields()

# Inicia a interface gráfica
janela.mainloop()
