# Sistema de Controle de Protocolos (ARIS)

Solução analítica desenvolvida para monitorar o fluxo de protocolos no setor de saneamento. O sistema transforma fluxos operacionais repetitivos em uma interface reativa e modular, mitigando erros de triagem e otimizando a governança dos dados.

## 📌 Contexto e Impacto no Negócio
Na regulação do saneamento, o processamento manual de comunicados e protocolos gera gargalos operacionais e riscos de inconsistência. Esta aplicação foi projetada para atuar na camada de inteligência do setor, padronizando a triagem de documentos e fornecendo uma estrutura centralizada para a tomada de decisões administrativas baseadas em regras de negócio consolidadas.

## 🏗️ Arquitetura e Engenharia da Solução
O projeto foi estruturado utilizando padrões de desenvolvimento modulares para garantir escalabilidade, legibilidade e separação de conceitos:

* **`app.py` (Core da Aplicação):** Ponto de entrada que gerencia o estado da aplicação e a orquestração do fluxo de navegação principal.
* **`pages/` (Arquitetura Multipáginas):** Módulos de interface independentes que segmentam o controle e a visualização dos diferentes estágios e categorias dos protocolos de forma reativa.
* **`config.py` (Centralização de Parâmetros):** Concentra as variáveis globais, mapeamentos de fluxos e definições de ambiente, garantindo fácil manutenção.
* **`utils.py` (Camada Auxiliar de Lógica):** Funções utilitárias dedicadas ao processamento, validação e manipulação das estruturas de dados.
* **`.streamlit/` & `assets/` (Customização de Interface):** Camada de estilo e configurações globais de exibição para aprimorar a experiência do usuário.

## 🛠️ Stack Técnica
* **Linguagem:** Python 3
* **Interface Dinâmica:** Streamlit (Arquitetura Multipáginas)
* **Manipulação de Dados:** Estruturas de dados nativas e bibliotecas de processamento declaradas em `requirements.txt`.

## 🔒 Segurança, Governança e Implantação
Devido à natureza sensível dos dados processados, a aplicação foi projetada e homologada para ser executada estritamente em **ambiente e servidor interno da agência**. 

* **Privacidade por Design:** Garante o isolamento completo das bases de dados, impedindo o tráfego de informações sigilosas em redes externas ou nuvens públicas.
* **Segurança da Informação:** Alinhamento com as políticas de governança locais e conformidade com diretrizes de proteção de dados.

---
*Desenvolvido por [Vitória Borges Bulhões](https://linkedin.com)*



<img width="1700" height="2200" alt="Protocolos_1" src="https://github.com/user-attachments/assets/9ab24afe-ea9b-44a3-bcb4-00acb31240e7" />

<img width="1700" height="2200" alt="Protocolos_2" src="https://github.com/user-attachments/assets/ba6ae19a-696c-43bf-ac4c-d5a70bc4f39b" />

<img width="1700" height="2200" alt="Protocolos_3" src="https://github.com/user-attachments/assets/8d880f24-b695-4863-a828-1e0d3f62578e" /> 
