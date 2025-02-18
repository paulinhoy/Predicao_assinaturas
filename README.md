# Análise de Modelo de Classificação para Assinaturas

## Visão Geral do Projeto
Este projeto visa prever clientes propensos a assinar um serviço após 15 dias (**target=1**), com base em dados históricos. O modelo utiliza **Random Forest** e foi avaliado em métricas críticas para dados desbalanceados (6.44% de assinantes na base de teste).

---

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

## 📂 Estrutura do Projeto

├── data/ # Dados brutos e processados
├── notebooks/ # Jupyter Notebooks de análise
├── models/ # Modelos treinados
└── requirements.txt # Dependências


## 💰 Impacto Financeiro
- **Falsos Negativos (FN)**: 284 assinantes não identificados  
  **Perda potencial**: `284 × R$ 22,90 = R$ 6.503,60`  
- **Falsos Positivos (FP)**: 84 ações desnecessárias  
  **Custo operacional**: Depende do custo por ação de marketing.

---

## ✅ **Pontos Fortes**
1. **Alta Especificidade (99.58%)**: Minimiza intervenções em não-assinantes.
2. **Precisão Sólida (92.88%)**: Confiabilidade nas previsões positivas.
3. **Lift Excepcional**: 13x mais eficiente nos 5% mais propensos.

---

## 🚨 **Oportunidades de Melhoria**
1. **Recall Moderado (79.42%)**: 20.58% dos assinantes são perdidos.
2. **Overfitting Detectável**: Diferença entre treino (99.71%) e teste (98.28%).

---

## 🛠️ Próximos Passos
1. **Ajustar Threshold**: Reduzir de 0.5 para 0.3 e monitorar recall.
2. **Balanceamento de Dados**: Testar técnicas como SMOTE ou `class_weight`.
3. **Análise de Custo-Benefício**: Comparar custos de FN vs. FP.

---



### Recursos Incluídos:
- **Visualização clara de métricas** em tabelas.
- **Destaque para decisões de negócio** (impacto financeiro, lift).
- **Chamadas para ação** (próximos passos).
- **Instruções de execução** para reprodução do projeto.
