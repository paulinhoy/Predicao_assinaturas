# Projeto de Previsão de Assinaturas

## Visão Geral do Projeto
Este projeto tem como objetivo prever quais clientes têm maior probabilidade de assinar um serviço após 15 dias (**target=1**), utilizando técnicas de Machine Learning. O modelo foi desenvolvido com base em dados históricos de jogadores e assinaturas, e é avaliado em métricas críticas para dados desbalanceados (6.44% de assinantes na base de teste).

O projeto está organizado em **4 pastas principais**:
1. **Modelo**: Contém o Jupyter Notebook com a análise e construção do modelo de Machine Learning.
2. **Original_csv**: Armazena os dados brutos utilizados no projeto.
3. **New_csv**: Contém os dados processados e transformados para uso no modelo.
4. **ConstrucaoABT**: Inclui scripts para a construção da ABT (Analytical Base Table), com estatísticas de jogadores e assinaturas.

---

## 🎯 Objetivos
1. **Previsão de Assinaturas**: Identificar clientes propensos a assinar o serviço após 15 dias.
2. **Análise de Desempenho**: Avaliar o modelo com métricas robustas, como AUC-ROC, KS Statistic, Precision-Recall e Lift Curve.
3. **Impacto Financeiro**: Quantificar o custo de falsos negativos e falsos positivos para otimizar campanhas de marketing.

---

## 🛠️ Estrutura do Projeto

### 1. **Modelo**
- **Notebook Principal**: Pré-processamento, teste de modelos, otimização do modelo que apresentou melhor performance (Random Forest) e avaliação de métricas.
- **Métricas Avaliadas**:
  - Acurácia, AUC-ROC, KS Statistic, Precision-Recall, Lift Curve.
  - Matriz de Confusão para análise de falsos positivos e negativos.

### 2. **Original_csv**
- **Dados Brutos**:
  - `tb_lobby_stats_player.csv`: Estatísticas de jogadores em partidas.
  - `tb_players_medalha.csv`: Informações sobre medalhas e assinaturas dos jogadores.
  - 'tb_medalhas.csv' Descrição das medalhas
  - 'tb_players.csv' Descrição das redes sociais dos players

### 3. **New_csv**
- **Dados Processados**:
     Os dados processados carregam todas as informações dos players em dado uma data de referência até 30 dias no passado 
  - `df_info_statsplayers.csv`: Estatísticas agregadas de jogadores (ex: K/D, win rate, mapas preferidos).
  - `df_info_medalhas.csv`: Informações sobre assinaturas e medalhas adquiridas pelos jogadores.

### 4. **ConstrucaoABT**
- **Scripts de Construção da ABT**:
  Dadas estatisticas temporal dos players, foi construida a variável resposta (target= 1 se o player fez uma assinatura em até 15 dias após a data de referência). 
  - **Estatísticas de Jogadores**:
    - Calcula métricas como número de partidas, dias jogados, recência, win rate, K/D, KDA, preferência por mapas e dias da semana.


## Resumo dos resultados

## 🎯 Métricas de Desempenho

### **Desempenho Geral**
| Métrica               | Treino   | Teste    | Baseline (Ingênuo) |
|-----------------------|----------|----------|--------------------|
| **Acurácia**          | 99.71%   | 98.28%   | 93.56%            |
| **AUC-ROC**           | 0.9785   | 0.8950   | 0.5000            |
| **KS Statistic**      | -        | 0.933    | -                 |

### **Classe de Interesse (Assinantes - target=1)**
| Métrica               | Valor    |
|-----------------------|----------|
| **Precisão**          | 92.88%   |
| **Recall**            | 79.42%   |
| **F1-Score**          | 85.6%    |
| **AUC-PR**            | 0.919    |

---

## 📊 Eficiência em Campanhas (Lift Curve)
| % da População | Lift  | Interpretação                             |
|----------------|-------|-------------------------------------------|
| 5%             | 13x   | 13x mais assinantes que a média           |
| 10%            | 9.8x  | ~10x mais eficiente que um modelo aleatório|
| 20%            | 5x    | Ideal para cobertura moderada             |
| 60%            | 1.8x  | Ainda superior ao baseline                |

---


## 💰 Impacto Financeiro
- **Falsos Negativos (FN)**: 284 assinantes não identificados  
  **Perda potencial**: `284 × R$ 22,90 = R$ 6.503,60` Perda devido a não identificação de assinantes 

---

## ✅ **Pontos Fortes**
1. **Alta Especificidade (99.58%)**: Minimiza intervenções em não-assinantes.
2. **Precisão Sólida (92.88%)**: Confiabilidade nas previsões positivas.
3. **Lift Excepcional**: 13x mais eficiente nos 5% mais propensos.

---

## 🚨 **Oportunidades de Melhoria**
1. **Recall Moderado (79.42%)**: 20.58% dos assinantes são perdidos.
2. **Data Off Time** Separação de uma parte do Dataset que está fora dos dados preocessados.

---

## 🛠️ Próximos Passos
1. **Ajustar Threshold**: Ajustar o thereshold e avaliar a performance.
2. **Balanceamento de Dados**: Testar técnicas como SMOTE ou `class_weight`.
3. **Análise de Custo-Benefício**: Comparar custos de FN vs. FP.

---
