# Plano de Sprint - Kalawenda Turístico Inteligente

## Objetivo do sprint
Criar um protótipo funcional de uma solução digital para o hackathon, baseada no conceito de Kalawenda Turístico Inteligente: uma plataforma que usa IA generativa e geoespacial para ajudar turistas a descobrir destinos, conversar com um assistente cultural e conectar-se a driver-guides locais certificados.

## Premissas de base
- O projeto deve responder a um dos problem statements do hackathon.
- A solução deve incluir um protótipo demonstrável, Lean Canvas, pitch deck, documento curto do projeto e apresentação final.
- A arquitetura sugerida no pipeline inclui:
  - Frontend/Chatbot
  - Backend/API
  - Camada geoespacial (mapa e rotas)
  - Integração com IA e dados

## Fase 1 - Definição do problema e alinhamento da equipa
**Duração:** 2 a 3 horas

### Objetivo
Escolher o problem statement mais adequado e definir claramente o valor da solução.

### Tarefas
- Definir o nome da equipa e papéis principais.
- Escolher o problem statement: experiência turística inteligente ou turismo comunitário.
- Documentar o problema, público-alvo e necessidades principais.
- Definir os utilizadores-chave: turistas, driver-guides, comunidades locais.
- Criar uma versão inicial do Lean Canvas.
- Identificar datasets e fontes de informação relevantes.

### Entregável
- Problema bem definido
- Público-alvo claro
- Lean Canvas inicial

## Fase 2 - Design da solução e arquitetura do MVP
**Duração:** 3 a 4 horas

### Objetivo
Transformar a ideia em um conceito técnico viável para protótipo.

### Tarefas
- Desenhar o fluxo do utilizador: conversa -> intenção -> recomendação -> confirmação -> mapa.
- Definir a arquitetura do MVP em 3 camadas:
  - Frontend/Chatbot
  - Backend/API
  - Mapa/GIS
- Escolher as tecnologias principais:
  - Frontend: React ou next.js
  - Backend: FastAPI
  - IA: API do modelo open-source
  - Mapas: Folium/Leaflet/OpenStreetMap
  - Dados: PostgreSQL/PostGIS ou ficheiros estruturados simples
- Definir os endpoints principais da API.
- Criar wireframes básicos da interface.

### Entregável
- Arquitetura do MVP
- Fluxo de utilização
- Stack tecnológica definida

## Fase 3 - Implementação do núcleo do protótipo
**Duração:** 1 a 2 dias

### Objetivo
Construir a primeira versão funcional da solução.

### Tarefas
- Preparar o repositório e a estrutura do projeto.
- Implementar o frontend com uma interface simples para interação com o utilizador.
- Criar um chatbot ou assistente conversacional para captar intenções turísticas.
- Implementar endpoints no backend para:
  - receber mensagens do utilizador
  - processar intenções
  - devolver sugestões de locais ou services
- Integrar a lógica de recomendação de driver-guides.
- Criar uma camada básica de mapa com pontos de interesse e rotas.
- Adicionar um fluxo de confirmação da reserva/seleção do driver-guide.

### Entregável
- Protótipo funcional com interação básica
- Chatbot ou assistente conversacional
- Mapa interativo simples

## Fase 4 - Integração de dados, IA e validação
**Duração:** 1 dia

### Objetivo
Tornar a solução mais realista, útil e preparada para demo.

### Tarefas
- Integrar datasets relevantes para destinos, pontos turísticos, rotas ou dados culturais.
- Configurar a lógica de IA para responder de forma contextualizada.
- Adicionar filtros de recomendação por:
  - localização
  - interesses do turista
  - disponibilidade do guide
  - avaliações
- Validar o fluxo completo do utilizador.
- Testar cenários principais: descoberta de destino, pedido de guia, visualização do mapa.
- Aplicar boas práticas de uso responsável de IA e dados.

### Entregável
- Fluxo completo testado
- Recomendação mais contextualizada
- Dados e IA integrados

## Fase 5 - Preparação de pitch, documentação e demo final
**Duração:** 0,5 a 1 dia

### Objetivo
Preparar os materiais obrigatórios do hackathon e garantir uma apresentação convincente.

### Tarefas
- Elaborar o documento curto do projeto com:
  - problema
  - solução
  - impacto
  - dados
  - tecnologia
  - próximos passos
- Atualizar o Lean Canvas com base no protótipo.
- Criar o pitch deck com 5 a 8 slides.
- Preparar screenshots ou vídeo curto da demo.
- Rehearsar a apresentação final.
- Garantir que o protótipo está funcional para a demo.

### Entregável
- Pitch deck final
- Documento do projeto
- Lean Canvas final
- Demo preparada

## Tarefas transversais recomendadas
- Gestão de tarefas com quadro Kanban.
- Reuniões curtas diárias de alinhamento.
- Versionamento no GitHub.
- Backup e organização de ficheiros do projeto.
- Revisão constante do alinhamento com os critérios do hackathon.

## Cronograma sugerido
- Dia 1: Fases 1 e 2
- Dia 2: Fase 3
- Dia 3: Fases 4 e 5

## Resultado esperado ao fim do sprint
Um protótipo demonstrável de Kalawenda Turístico Inteligente, com:
- chatbot/assistente conversacional
- recomendação de driver-guides
- mapa com rotas e pontos de interesse
- narrativa clara para apresentação final
