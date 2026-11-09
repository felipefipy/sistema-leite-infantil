import json
import os
import time
import random

ARQUIVO_DADOS = "registros_leite.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_dados(registros):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=4)

def cadastrar_registro(registros, pilha_desfazer):
    print("\n--- NOVO LANÇAMENTO DE CONSUMO ---")
    try:
        codigo = int(input("Código numérico único (ex: 101): "))
        if any(r["codigo"] == codigo for r in registros):
            print("Erro: Já existe um registo com esse código!")
            return

        data = input("Data (DD/MM/AAAA): ")
        horario = input("Horário (HH:MM): ")
        volume_ml = float(input("Volume ingerido (ml): "))
        tipo_leite = input("Tipo de leite (ex: Fórmula, Materno): ")

        novo = {
            "codigo": codigo,
            "data": data,
            "horario": horario,
            "volume_ml": volume_ml,
            "tipo_leite": tipo_leite
        }

        registros.append(novo)
        pilha_desfazer.append(novo)
        salvar_dados(registros)
        print("Registo cadastrado e guardado com sucesso!")
    except ValueError:
        print("Erro: Digite valores numéricos válidos para o código e o volume.")

def listar_registros(registros):
    print("\n--- LISTA DE CONSUMO DE LEITE ---")
    if not registros:
        print("Nenhum registo cadastrado.")
        return
    
    for r in registros:
        print(f"Código: {r['codigo']} | Data: {r['data']} {r['horario']} | Volume: {r['volume_ml']}ml | Tipo: {r['tipo_leite']}")

def desfazer_ultimo(registros, pilha_desfazer):
    print("\n--- DESFAZER ÚLTIMO LANÇAMENTO (PILHA) ---")
    if not pilha_desfazer:
        print("Não há ações recentes para desfazer na sessão atual.")
        return
    
    ultimo = pilha_desfazer.pop()
    if ultimo in registros:
        registros.remove(ultimo)
        salvar_dados(registros)
        print(f"Registo de código {ultimo['codigo']} desfeito e removido com sucesso!")
    else:
        print("O último registo já não se encontra na lista principal.")

def ordenar_por_volume(registros):
    print("\n--- ORDENAÇÃO MANUAL POR VOLUME (BUBBLE SORT) ---")
    if not registros:
        print("Não há registos para ordenar.")
        return
    
    regs = list(registros)
    n = len(regs)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if regs[j]["volume_ml"] > regs[j + 1]["volume_ml"]:
                regs[j], regs[j + 1] = regs[j + 1], regs[j]
    
    print("Registos ordenados do menor para o maior volume:")
    for r in regs:
        print(f"Volume: {r['volume_ml']}ml | Código: {r['codigo']} | Data: {r['data']} {r['horario']}")

def busca_sequencial(registros):
    print("\n--- BUSCA SEQUENCIAL POR CÓDIGO ---")
    if not registros:
        print("Não há registos para procurar.")
        return
    
    try:
        codigo_procurado = int(input("Digite o código que deseja procurar: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

    comparacoes = 0
    inicio = time.time()
    
    encontrado = None
    for r in registros:
        comparacoes += 1
        if r["codigo"] == codigo_procurado:
            encontrado = r
            break
            
    fim = time.time()
    tempo_execucao = (fim - inicio) * 1000

    if encontrado:
        print(f"Registo encontrado com sucesso!")
        print(f"Código: {encontrado['codigo']} | Volume: {encontrado['volume_ml']}ml | Data: {encontrado['data']} {encontrado['horario']} | Tipo: {encontrado['tipo_leite']}")
    else:
        print("Registo com o código especificado não foi encontrado.")
        
    print(f"[Métricas] Comparações feitas: {comparacoes} | Tempo de execução: {tempo_execucao:.6f} ms")

def busca_binaria(registros):
    print("\n--- BUSCA BINÁRIA POR CÓDIGO (EXIGE ORDENAÇÃO PRÉVIA) ---")
    if not registros:
        print("Não há registos para procurar.")
        return

    try:
        codigo_procurado = int(input("Digite o código que deseja procurar: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro.")
        return

    regs = sorted(registros, key=lambda x: x["codigo"])
    
    comparacoes = 0
    inicio = time.time()
    
    esquerda = 0
    direita = len(regs) - 1
    encontrado = None

    while esquerda <= direita:
        comparacoes += 1
        meio = (esquerda + direita) // 2
        
        if regs[meio]["codigo"] == codigo_procurado:
            encontrado = regs[meio]
            break
        elif regs[meio]["codigo"] < codigo_procurado:
            esquerda = meio + 1
        else:
            direita = meio - 1

    fim = time.time()
    tempo_execucao = (fim - inicio) * 1000

    if encontrado:
        print(f"Registo encontrado com sucesso!")
        print(f"Código: {encontrado['codigo']} | Volume: {encontrado['volume_ml']}ml | Data: {encontrado['data']} {encontrado['horario']} | Tipo: {encontrado['tipo_leite']}")
    else:
        print("Registo com o código especificado não foi encontrado.")

    print(f"[Métricas] Comparações feitas: {comparacoes} | Tempo de execução: {tempo_execucao:.6f} ms")

def gerar_dados_em_massa(registros):
    print("\n--- GERAR DADOS EM MASSA (TESTE DE DESEMPENHO) ---")
    try:
        quantidade = int(input("Quantos registos deseja gerar automaticamente? (ex: 50): "))
    except ValueError:
        print("Erro: Digite um número inteiro válido.")
        return

    tipos = ["Fórmula", "Materno", "Cabra", "Soja"]
    
    # Encontra o próximo código disponível para evitar duplicados com os existentes
    base_codigo = max([r["codigo"] for r in registros], default=100) + 1

    for i in range(quantidade):
        novo = {
            "codigo": base_codigo + i,
            "data": "24/10/2026",
            "horario": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
            "volume_ml": float(random.randint(50, 300)),
            "tipo_leite": random.choice(tipos)
        }
        registros.append(novo)

    salvar_dados(registros)
    print(f"{quantidade} registos gerados e guardados com sucesso no ficheiro!")

def main():
    registros = carregar_dados()
    pilha_desfazer = []

    while True:
        print("\n=== SISTEMA DE CONTROLE DE LEITE INFANTIL ===")
        print("1. Cadastrar novo consumo")
        print("2. Listar todos os registos")
        print("3. Desfazer último cadastro (Pilha)")
        print("4. Ordenar por volume (Bubble Sort manual)")
        print("5. Buscar registo (Busca Sequencial + Métricas)")
        print("6. Buscar registo (Busca Binária + Métricas)")
        print("7. Gerar dados em massa (Teste de Desempenho)")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_registro(registros, pilha_desfazer)
        elif opcao == "2":
            listar_registros(registros)
        elif opcao == "3":
            desfazer_ultimo(registros, pilha_desfazer)
        elif opcao == "4":
            ordenar_por_volume(registros)
        elif opcao == "5":
            busca_sequencial(registros)
        elif opcao == "6":
            busca_binaria(registros)
        elif opcao == "7":
            gerar_dados_em_massa(registros)
        elif opcao == "0":
            print("A sair do sistema...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
