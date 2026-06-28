# O Tabuleiro das Almas

Um roguelike deckbuilder baseado em Inscryption, mas com criaturas do folclore nordestino. Você joga contra o Matheus, um narrador que coleciona almas dos perdedores.

## O Jogo

A premissa é simples: você começa em um bar jogando cartas contra o Matheus. Se ganhar, explora um mapa procurando novas criaturas. Se perder, sua alma vira parte de um cortejo fantasmagórico. Objetivo final: derrotar os três bosses e conseguir os totens do Saci.

O jogo usa copos de shot como vida (você tem 2) e tampinhas de cerveja na balança para contar pontos. Cada criatura tem um custo em ouro e algumas têm efeitos especiais.

## Criaturas

| Nome | Ataque | Vida | Custo | Efeito |
|------|--------|------|-------|--------|
| Acauã | 2 | 3 | 2 | Dano direto |
| Anhangá | 3 | 7 | 4 | — |
| Boitatá | 2 | 1 | 2 | Morte instantânea |
| Caboclo D'água | 1 | 1 | 1 | Se esconde |
| Cacto | 0 | 3 | 0 | — |
| Capelobo | 1 | 2 | 1 | — |
| Chupa Cabra | 1 | 1 | 1 | Dano de sangue |
| Cobra Coral | 2 | 2 | 1 | Morte instantânea |
| Cuca | 2 | 2 | 2 | Shell (escudo) |
| Comadre Fulozinha | 1 | 1 | 2 | Dano em 3 direções |
| Curupira | 3 | 2 | 2 | — |
| La Ursa | 4 | 6 | 3 | — |
| Leão-do-Norte | 7 | 7 | 4 | — |
| Mula Sem-Cabeça | 3 | 4 | 3 | — |
| Perna Cabeluda | 0 | 1 | 0 | Sacrifício |
| Timbu | 2 | 2 | 1 | Dano de volta |

## Personagens

**O Matheus**: Narrador que já perdeu a conta de almas. Você o encontra em um bar e joga com ele. Se perder, você vira parte de sua lenda.

**Bosses**:
- Caboclo: Fura e elimina suas cartas
- Papa-figo: Rouba suas criaturas
- Papangu: Inverte seus ataques em dano direto (uma vez a cada 3 rodadas)

**Matinta Pereira**: Uma bruxa que oferece bênçãos pra suas criaturas—asas, dano bifurcado, ou imortalidade.

**Cangaceiros**: Aparecem em uma fogueira e oferecem +1 de ataque ou vida pra uma de suas cartas.

## Itens

- Peixeira: Corta a carta inimiga
- Cantil: +1 de vida
- Abridor de cerveja: Abre uma tampinha
- Garrafa com carta: Uma Perna Cabeluda extra

## Tecnicamente

- Resolução: 384x216
- Cartas: 36x44 pixels (144x176 em zoom 4x)
- Arte: Pixel art + xilogravura
- Controle: Point & Click

## Status do Projeto

- Bruno: Menu principal
- Maria Luiza: Arte (xilogravura) e Matinta Pereira
- Caio Cesar: Programação do combate
- Vicente: Mapa e lore
- João Lucas: Documentação
- Matheus: Design de cartas, efeitos visuais, som, creditos e bosses 
