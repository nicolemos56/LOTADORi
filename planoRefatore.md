# REFACTOR.md

# Refatoração da LOTADORi

## Objetivo

A aplicação atual **não comunica a proposta de valor principal da LOTADORi**.

Hoje, o layout transmite a ideia de um **planeador de viagens**, quando o verdadeiro conceito é outro.

A LOTADORi é um **Agente Autónomo de Turismo**.

Ela **não organiza planos**.

Ela **executa intenções**.

O utilizador apenas diz o que pretende e o agente realiza as ações necessárias utilizando os serviços e plataformas existentes.

O foco da refatoração deve ser alterar completamente a experiência da aplicação para transmitir essa ideia.

---

# Nova proposta de valor

A LOTADORi deve parecer um **ChatGPT + Operator + Concierge de Turismo**.

O utilizador não navega por dezenas de menus.

Ele conversa.

O agente trabalha.

Exemplos:

> Reserve alojamento no Hotel Patriota.

> Quero conhecer lugares naturais em Luanda.

> Marca um jantar romântico hoje às 20h.

> Encontra um guia turístico que fale inglês.

> Compra dois bilhetes para o Museu da Escravatura.

> Chama um táxi para me levar ao aeroporto.

A responsabilidade da aplicação é executar.

Não apenas sugerir.

---

# Novo princípio de UX

## Errado

o atual

---

## Correto

O utilizador apenas comunica a intenção.

Exemplo:

> Quero um hotel perto da Marginal.

A aplicação interpreta.

Pesquisa.

Compara.

Reserva.

Confirma.

Tudo automaticamente.

---

# Nova Home

A Home deve parecer um assistente inteligente.

Não um dashboard.

Eliminar elementos desnecessários.

Manter apenas o essencial.

Estrutura sugerida:

```
Olá, João 👋

O que pretende fazer hoje?

________________________________

[ campo grande de conversa ]

Digite ou fale naturalmente...

🎤

```

Logo abaixo:

### Sugestões rápidas

* Reservar Hotel
* Encontrar Guia
* Descobrir Turismo
* Restaurantes
* Eventos
* Transportes
* Museus

Não utilizar muitos cartões.

Não transformar isto numa loja.

---

# Fluxo 1

## Reserva de hotel

Utilizador:

> Reserve alojamento no Hotel Patriota para amanhã.

O agente responde:

✔ Estou a verificar disponibilidade.

↓

✔ Encontrei quartos disponíveis.

↓

✔ Estou a efetuar a reserva.

↓

✔ Reserva confirmada.

Depois mostra apenas um cartão simples.

```
Hotel Patriota

✔ Confirmado

Check-in

Check-out

Código

Ver detalhes
```

Não mostrar dezenas de formulários.

---

# Fluxo 2

## Descobrir turismo

Utilizador:

Estou em Luanda.

O que recomenda?

App:

Qual o tipo de turismo?

•

Natureza

•

Gastronomia

•

Praias

•

História

•

Noite

•

Compras

Depois apresenta apenas uma recomendação forte.

Exemplo:

## Ilha do Mussulo

Imagem

Breve descrição.

Botões:

Ver detalhes

Ir para este lugar

---

# Fluxo 3

## Ir para este lugar

Quando o utilizador clicar em

"Ir para este lugar"

ou responder

"Sim"

o agente deve assumir controlo.

Fluxo:

Estou a procurar transporte...

↓

Encontrei estas opções.

↓

Guia + Driver

ou

Táxi

↓

Após seleção

↓

Reserva

↓

Mapa

↓

Motorista a caminho

Mostrar acompanhamento em tempo real.

---

# Fluxo 4

## Guia Turístico

O agente pode sugerir:

Guias certificados

Idiomas

Avaliações

Preço

Botão

Contratar

Depois acompanha todo o processo.

---

# Fluxo 5

## Restaurante

Utilizador

Reserve uma mesa para duas pessoas hoje às 20h.

Agente

Pesquisa disponibilidade.

↓

Efetua reserva.

↓

Envia confirmação.

---

# Fluxo 6

## Transportes

O utilizador nunca procura aplicações.

A LOTADORi integra:

Yango

InDrive

Táxis

Motoristas privados

Transfers

A app apenas pergunta:

Como prefere viajar?

•

Mais económico

•

Mais rápido

•

Mais confortável

Depois trata do resto.

---

# Fluxo 7

## Recomendações

A aplicação nunca despeja listas enormes.

Em vez disso:

1 recomendação

↓

Caso o utilizador não goste

↓

Mostrar outra

O agente deve conversar.

Não listar.

---

# Interface

Visual minimalista.

Muito espaço em branco.

Poucos cartões.

Grandes áreas de conversa.

Elementos arredondados.

Visual premium.

Inspirado em:

* ChatGPT
* Apple Human Interface
* Google Material 3
* Perplexity
* Operator UI

Não copiar.

Inspirar.

---

# Paleta

Branco

Roxo principal

Cinza claro

Poucos destaques.

Evitar excesso de cores.

---

# Ícones

Poucos.

Grandes.

Minimalistas.

Sem poluição visual.

---

# Conversação

A conversa é o centro da aplicação.

A UI inteira deve reforçar que existe um agente inteligente.

Evitar ecrãs tradicionais de filtros.

---

# Animações

Durante execução mostrar estados como:

🔍 A pesquisar...

📞 A contactar parceiro...

🏨 A reservar...

🚗 A chamar motorista...

✅ Concluído.

Estas animações fazem o utilizador perceber que existe trabalho a acontecer.

---

# Filosofia

A LOTADORi não vende turismo.

Ela executa tarefas de turismo.

Essa diferença deve ser evidente em toda a aplicação.

Sempre que existir dúvida entre:

"mostrar opções"

ou

"executar"

a resposta deve ser:

**executar.**

---

# Objetivo Final

Depois da refatoração, o utilizador deve sentir que está a falar com um assistente pessoal que resolve tudo por ele.

Não deve parecer um Booking.

Não deve parecer um TripAdvisor.

Não deve parecer um marketplace.

Deve parecer um **Agente Autónomo de Turismo** que recebe uma intenção, toma decisões inteligentes quando apropriado, executa tarefas de ponta a ponta, acompanha o progresso em tempo real e entrega apenas o resultado final, com o mínimo de esforço do utilizador.
