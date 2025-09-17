# -*- coding: utf-8 -*-

class No:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    # ===============================================================
    # MÉTODOS AUXILIARES E ROTAÇÕES
    # ===============================================================
    def obter_altura(self, no):
        return no.altura if no else 0

    def obter_fator_balanceamento(self, no):
        if not no:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)

    def _atualizar_altura(self, no):
        no.altura = 1 + max(self.obter_altura(no.esquerda),
                            self.obter_altura(no.direita))

    def obter_no_valor_minimo(self, no):
        atual = no
        while atual.esquerda:
            atual = atual.esquerda
        return atual

    def _rotacao_direita(self, y):
        x = y.esquerda
        T2 = x.direita

        # Rotação
        x.direita = y
        y.esquerda = T2

        # Atualizar alturas
        self._atualizar_altura(y)
        self._atualizar_altura(x)

        return x

    def _rotacao_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda

        # Rotação
        y.esquerda = x
        x.direita = T2

        # Atualizar alturas
        self._atualizar_altura(x)
        self._atualizar_altura(y)

        return y

    # ===============================================================
    # INSERÇÃO COM BALANCEAMENTO
    # ===============================================================
    def inserir(self, chave):
        self.raiz = self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no, chave):
        if not no:
            return No(chave)
        elif chave < no.chave:
            no.esquerda = self._inserir_recursivo(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._inserir_recursivo(no.direita, chave)
        else:
            raise ValueError("Chaves duplicadas não são permitidas.")

        self._atualizar_altura(no)
        balance = self.obter_fator_balanceamento(no)

        # Casos de rotação
        if balance > 1 and chave < no.esquerda.chave:  # Esquerda-Esquerda
            return self._rotacao_direita(no)
        if balance < -1 and chave > no.direita.chave:  # Direita-Direita
            return self._rotacao_esquerda(no)
        if balance > 1 and chave > no.esquerda.chave:  # Esquerda-Direita
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)
        if balance < -1 and chave < no.direita.chave:  # Direita-Esquerda
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    # ===============================================================
    # DELEÇÃO COM BALANCEAMENTO
    # ===============================================================
    def deletar(self, chave):
        self.raiz = self._deletar_recursivo(self.raiz, chave)

    def _deletar_recursivo(self, no, chave):
        if not no:
            return no

        if chave < no.chave:
            no.esquerda = self._deletar_recursivo(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._deletar_recursivo(no.direita, chave)
        else:
            if not no.esquerda:
                return no.direita
            elif not no.direita:
                return no.esquerda
            temp = self.obter_no_valor_minimo(no.direita)
            no.chave = temp.chave
            no.direita = self._deletar_recursivo(no.direita, temp.chave)

        self._atualizar_altura(no)
        balance = self.obter_fator_balanceamento(no)

        # Casos de rotação após deleção
        if balance > 1 and self.obter_fator_balanceamento(no.esquerda) >= 0:
            return self._rotacao_direita(no)
        if balance > 1 and self.obter_fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)
        if balance < -1 and self.obter_fator_balanceamento(no.direita) <= 0:
            return self._rotacao_esquerda(no)
        if balance < -1 and self.obter_fator_balanceamento(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    # ===============================================================
    # BUSCAS
    # ===============================================================
    def encontrar_nos_intervalo(self, chave1, chave2):
        resultado = []
        self._buscar_intervalo(self.raiz, chave1, chave2, resultado)
        return resultado

    def _buscar_intervalo(self, no, chave1, chave2, resultado):
        if not no:
            return
        if chave1 < no.chave:
            self._buscar_intervalo(no.esquerda, chave1, chave2, resultado)
        if chave1 <= no.chave <= chave2:
            resultado.append(no.chave)
        if chave2 > no.chave:
            self._buscar_intervalo(no.direita, chave1, chave2, resultado)

    def obter_profundidade_no(self, chave):
        return self._profundidade(self.raiz, chave, 0)

    def _profundidade(self, no, chave, nivel):
        if not no:
            return -1
        if no.chave == chave:
            return nivel
        elif chave < no.chave:
            return self._profundidade(no.esquerda, chave, nivel + 1)
        else:
            return self._profundidade(no.direita, chave, nivel + 1)


# --- Bloco de Teste ---
if __name__ == "__main__":
    arvore_avl = ArvoreAVL()

    print(\"\\n--- ATIVIDADE PRÁTICA: ÁRVORE AVL ---\")

    print(\"\\n--- 1. Inserindo nós ---\")
    chaves_para_inserir = [9, 5, 10, 0, 6, 11, -1, 1, 2]
    try:
        for chave in chaves_para_inserir:
            arvore_avl.inserir(chave)
        print(\"Inserção concluída.\")
    except Exception as e:
        print(f\"ERRO DURANTE A INSERÇÃO: {e}\")

    print(\"\\n--- 2. Deletando nós ---\")
    try:
        chaves_para_deletar = [10, 11]
        for chave in chaves_para_deletar:
            arvore_avl.deletar(chave)
        print(\"Deleção concluída.\")
    except Exception as e:
        print(f\"ERRO DURANTE A DELEÇÃO: {e}\")

    print(\"\\n--- 3. Buscando nós no intervalo [1, 9] ---\")
    try:
        nos_no_intervalo = arvore_avl.encontrar_nos_intervalo(1, 9)
        print(f\"Nós encontrados: {sorted(nos_no_intervalo)}\")
    except Exception as e:
        print(f\"ERRO: {e}\")

    print(\"\\n--- 4. Calculando profundidade do nó 6 ---\")
    try:
        profundidade = arvore_avl.obter_profundidade_no(6)
        print(f\"Profundidade do nó 6: {profundidade}\")
    except Exception as e:
        print(f\"ERRO: {e}\")
