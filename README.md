# G38_Greedy_PA-26.1

Aplicacao em Python puro com interface grafica simples para cadastrar clientes e calcular a melhor agenda de visitas usando o algoritmo guloso de **Interval Scheduling**.

## Como executar

```bash
python app.py
```

## Interface

A janela da aplicacao permite:

1. Cadastrar cliente com nome, horario de inicio, horario de fim e endereco/observacao.
2. Gerar automaticamente 50 clientes com horarios aleatorios.
3. Ver todos os clientes cadastrados em uma tabela.
4. Calcular a melhor agenda de visitas.
5. Ver a quantidade maxima de visitas possiveis.
6. Ver os clientes que ficaram de fora da agenda.

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
