# Triagem focada por título e resumo

Avalie somente as informações fornecidas. Não use ferramentas nem presuma que
uma propriedade existe quando não for afirmada no título ou no resumo.

São necessários: estudo primário, modelos de linguagem ou agentes baseados
neles e memória/estado textual. Ignore escala do modelo de embeddings ou
avaliador quando o critério diz respeito ao modelo que escreve a memória.

Classifique como **CORE** apenas quando houver evidência das três condições:

1. Escrita, atualização, revisão ou preservação de memória ou estado ao longo
   de entradas, eventos, turnos ou sessões. Geração estática de JSON não basta.
2. Memória ou estado explicitamente estruturado: JSON, esquema, entidades e
   atributos, registros tipados, tabela ou grafo de fatos.
3. Pelo menos uma aproximação adicional: escritor/gestor compacto de até cerca
   de 4B parâmetros; avaliação da fidelidade ou correção do estado atualizado,
   e não apenas da resposta final; ou comparação explícita de paradigmas
   gerativos na escrita/edição do estado.

Use **CONTEXT** quando houver aproximação parcial ou evidência insuficiente
para todas as condições: por exemplo, memória em texto livre; saída JSON
estática; ou difusão e chamadas de ferramentas sem memória estruturada
incremental. Não transforme suposições em CORE.

Use **EXCLUDE** para estudo secundário (E3), memória de hardware (E2),
modalidade não textual principal (E4), segurança/privacidade como objeto
principal (E5), aplicação de domínio sem contribuição ao problema (E6),
informação insuficiente mesmo para classificá-lo (E8) ou fora do tema (E9).

Para CORE, use os códigos de maneira consistente com o protocolo anterior:
IC1 para atualização, IC3 para estado estruturado, IC2 apenas quando houver
escritor compacto explícito e IC4 para comparação gerativa pertinente. Atribua
relevância 3 quando a fidelidade por atualização ou o escritor compacto em
estado estruturado estiver explícito; caso contrário, relevância 2. Para
CONTEXT ou EXCLUDE, a relevância é 0.

Para cada registro, devolva exatamente um item em `decisoes` com `key`
inalterada, `decision` (`CORE`, `CONTEXT` ou `EXCLUDE`), `codes` (lista de
códigos; vazia para CONTEXT), `relevance` e `note` em português com até 160
caracteres, justificando a decisão e distinguindo o que é informado do que não
é informado. Não invente escala, método ou avaliação.
