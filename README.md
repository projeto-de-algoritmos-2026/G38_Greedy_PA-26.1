# G38_Greedy_PA-26.1

Aplicacao em Python puro com interface grafica simples com duas funcionalidades:

1. Cadastrar clientes e calcular a melhor agenda de visitas usando o algoritmo ganancioso de **Interval Scheduling**.
2. Cadastrar produtos e calcular a melhor combinacao de itens para a mochila do vendedor usando **Knapsack**.

## Como executar

```bash
python3 app.py (Mac) ou python app.py
```

## Video da entrega

[Acessar video da entrega](https://drive.google.com/file/d/1XBiNg-ipWnzcgI0N0B68DxT8fu6CT_xz/view?usp=sharing)

## Interface

A janela da aplicacao permite:

1. Cadastrar cliente com nome, horario de inicio, horario de fim e endereco/observacao.
2. Gerar automaticamente 50 clientes com horarios aleatorios.
3. Ver todos os clientes cadastrados em uma tabela.
4. Calcular a melhor agenda de visitas.
5. Ver a quantidade maxima de visitas possiveis.
6. Ver os clientes que ficaram de fora da agenda.
7. Cadastrar produtos com peso (kg) e valor (R$).
8. Gerar automaticamente uma lista de produtos cosmeticos aleatorios.
9. Informar a capacidade maxima (kg) e calcular o maior valor possivel dentro do limite de massa usando um algoritmo ganancioso baseado na razao valor/peso.

## Exemplo de uso

Clientes cadastrados:

| Cliente | Inicio | Fim | Observacao |
| --- | --- | --- | --- |
| Ana | 08:00 | 09:00 | Centro |
| Bruno | 08:30 | 10:00 | Bairro Norte |
| Carla | 09:00 | 10:30 | Avenida Principal |
| Diego | 10:30 | 11:30 | Proximo ao mercado |
| Eduarda | 10:00 | 12:00 | Condominio Azul |
| Fabio | 11:30 | 12:30 | Sala comercial |

Agenda calculada pelo algoritmo:

| Ordem | Cliente | Inicio | Fim |
| --- | --- | --- | --- |
| 1 | Ana | 08:00 | 09:00 |
| 2 | Carla | 09:00 | 10:30 |
| 3 | Diego | 10:30 | 11:30 |
| 4 | Fabio | 11:30 | 12:30 |

Quantidade maxima de visitas possiveis: **4**

Clientes que ficaram de fora:

- Bruno, porque sua disponibilidade termina as 10:00, mas comeca as 08:30 e entra em conflito com Ana.
- Eduarda, porque comeca as 10:00 e entra em conflito com Carla, que vai ate 10:30.

## Por que o algoritmo escolheu essa agenda?

O algoritmo de Interval Scheduling ordena todos os clientes pelo menor horario de termino. Em seguida, escolhe o primeiro cliente que termina mais cedo e continua escolhendo apenas clientes cujo horario de inicio seja maior ou igual ao horario de fim do ultimo cliente escolhido.

Essa estrategia gulosa funciona para o problema classico de maximizar a quantidade de intervalos nao sobrepostos porque deixar a agenda livre o mais cedo possivel aumenta as chances de encaixar mais visitas depois.

## Knapsack

A segunda funcionalidade da aplicacao resolve o problema da mochila do vendedor utilizando o algoritmo ganancioso de **Knapsack**.

Cada produto possui:

- nome
- peso
- valor

O algoritmo calcula a razao entre valor e peso:

```text
valor / peso
```

Os produtos sao inseridos em um **heap de prioridade maxima** e o algoritmo sempre escolhe primeiro o produto com maior retorno por unidade de peso.

No escopo deste proejto os itens sao divisiveis. Isso significa que o algoritmo pode selecionar apenas uma fracao do ultimo produto para preencher completamente a mochila.

Exemplo:

| Produto | Peso | Valor | Valor/Peso |
| --- | --- | --- | --- |
| Perfume Premium | 1 kg | R$ 200 | 200 |
| Creme Facial | 2 kg | R$ 240 | 120 |
| Shampoo | 1 kg | R$ 80 | 80 |

Se a mochila possuir capacidade de apenas 1.5 kg:

1. O algoritmo escolhe primeiro o Perfume Premium.
2. Ainda restam 0.5 kg livres.
3. O algoritmo pega apenas 25% do Creme Facial.

Essa estrategia gananciosa produz a solucao otima para o problema Knapsack.
