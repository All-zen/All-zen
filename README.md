<p align="center">
  <img src="assets/vault-vivo.svg" width="100%" alt="Allan Zeni · AZ Sistemas · Infraestrutura de TI, Python e IA aplicada. Uma constelação com as 699 notas do meu vault e o vault-vector em ação, em quatro cenas: busca híbrida (o reranker aparece em semântico #1 e literal #1), sinalização de incerteza (uma pergunta de culinária volta com confiança baixa), escrita com histórico pelo MCP e descrição automática das 8 seções, 699 notas e 6.080 trechos.">
</p>

**Analista de infraestrutura de TI e desenvolvedor Python.** Sou o único profissional de TI de um grupo da Serra Gaúcha com indústria de laticínios, parque turístico e loja, e pela AZ Sistemas, minha empresa, faço sistemas e automações para pequenas e médias empresas.\
Bento Gonçalves, RS · [sistemasaz.com.br](https://sistemasaz.com.br) · [LinkedIn](https://www.linkedin.com/in/allan-zeni) · [English below](#english)

### vault-vector

O [vault-vector](https://github.com/All-zen/vault-vector) é a memória que a IA usa comigo. Ele indexa as minhas notas markdown no meu computador e expõe busca e escrita como servidor MCP, para o Claude Code e o Claude Desktop. Hoje são 699 notas e 6.080 trechos num índice de 71 MB, e nada sai da máquina.

<p align="center">
  <img src="assets/como-busca.svg" width="100%" alt="Como o vault-vector responde: a pergunta vai para a busca semântica (bge-m3 no Ollama) e para a literal (SQLite FTS5); os dois rankings são fundidos por Reciprocal Rank Fusion, o resultado ganha uma faixa de confiança e um juiz local relê os casos da faixa média. 699 notas, 6.080 trechos, índice local de 71 MB.">
</p>

- **Busca híbrida.** Similaridade vetorial com bge-m3 e busca literal com FTS5, fundidas por Reciprocal Rank Fusion. Acha tanto a pergunta conceitual quanto o hostname, o IP ou o código de erro exato.
- **Faixas de confiança medidas.** O score do RRF mede concordância entre os dois lados e não serve como certeza, então cada resultado sai classificado em alta, média ou baixa. Em 8 perguntas legítimas contra 8 fora do assunto, nenhuma legítima caiu em baixa e nenhum ruído caiu em alta.
- **Juiz local na faixa média.** Um modelo pequeno, só em CPU, dá nota de 0 a 10 para cada trecho duvidoso. Com ele, 5 das 8 perguntas legítimas passaram para confiança alta, a um custo de 0,3 a 1,7 s por trecho.
- **Escrita com histórico.** Sete ferramentas MCP para editar, acrescentar, criar, mover, apagar, listar e reindexar. Toda gravação guarda a versão anterior em `_historico/`, e mover uma nota reescreve os wikilinks que apontavam para ela.
- **Descrição automática do vault.** O servidor lê o próprio índice e descreve seções, subpastas e convenções para o modelo, que navega um vault que nunca viu sem instrução escrita à mão.
- **Leve de propósito.** SQLite e numpy no lugar de banco vetorial, recorte por título sem partir tabela nem bloco de código, devolução da seção inteira em volta do trecho e reindexação só do que mudou. `vault-vector init` instala do zero, e `calibrar` refaz a medição das faixas no vault de cada um.

### Infraestrutura

Cuido de servidores, rede, Wi-Fi entre unidades, backup e monitoramento: 102 hosts no Zabbix e 125 painéis no Grafana, sobre Proxmox, Windows Server com Active Directory, Sophos e UniFi. Três diagnósticos que estão no vault:

- **Wi-Fi de visitantes caindo.** O pool DHCP tinha 241 endereços para cerca de 245 aparelhos por dia, com concessão de 24 h. Ampliei a faixa para 252 e reduzi a concessão para 4 h.
- **Gateway verde, internet parada.** A checagem só confirmava que o equipamento respondia ao ping. Agora ela testa TCP 443 e DNS.
- **261 alertas enviados, nenhum recebido.** O provedor recusava com HTTP 203, um código 2xx, e a recusa vinha no corpo. Hoje só conta como entregue com confirmação positiva.

### Sistemas

Pela AZ, desenvolvi e mantenho o sistema de gestão da indústria: mais de 20 módulos em Python, Flask e PostgreSQL, com 9.570 testes que rodam antes de cada push e no GitHub Actions. Ele é privado. O [NotaFlow](https://github.com/All-zen/NotaFlow) é público, um projeto-demo de contas a pagar com dados fictícios que lê a fatura com OCR, confere com regras e IA local e lança no ERP.

A arquitetura e as decisões são minhas, o código é gerado por IA a partir da minha especificação, e eu reviso e respondo por ele em produção. Ainda não trabalhei com nuvem pública em produção nem com Kubernetes.

**Stack:** Proxmox VE · Proxmox Backup Server · Windows Server · Linux · Active Directory · Sophos · VLANs · VPN · UniFi · Zabbix e a API dele em Python · Grafana · Python · Flask · PostgreSQL · pytest · GitHub Actions · Docker · Ollama · MCP

### AZ Sistemas

Sistemas sob medida e automações para pequenas e médias empresas da Serra Gaúcha. Resposta no mesmo dia, falando direto com quem desenvolve. → [sistemasaz.com.br](https://sistemasaz.com.br)

---

<a id="english"></a>

### English

**IT infrastructure analyst and Python developer.** I am the only IT professional for a group in southern Brazil with a dairy plant, a tourist park and a retail store. Through AZ Sistemas, my own company, I built and maintain the dairy plant's management system.

[vault-vector](https://github.com/All-zen/vault-vector) is the memory the AI works with: a local hybrid search over my markdown notes, exposed as an MCP server. Today it holds 699 notes and 6,080 passages in a 71 MB index, and nothing leaves the machine.

- **Hybrid search.** bge-m3 vector similarity and FTS5 keyword search, merged with Reciprocal Rank Fusion.
- **Measured confidence bands.** The RRF score measures agreement between rankers, so every result is labeled high, medium or low. On 8 legitimate questions against 8 off-topic ones, no legitimate question landed in low and no noise landed in high.
- **Local judge for the medium band.** A small CPU-only model scores each doubtful passage from 0 to 10, which moved 5 of the 8 legitimate questions to high confidence at 0.3 to 1.7 s per passage.
- **Writes with history.** Seven MCP tools; every write keeps the previous version in `_historico/`, and moving a note rewrites the wikilinks that pointed to it.
- **Self-describing vault.** The server reads its own index and describes the structure, so the model can navigate a vault it has never seen.

On the infrastructure side: 102 monitored hosts in Zabbix and 125 Grafana panels. I fixed a guest DHCP pool that had 241 addresses for about 245 devices a day, a gateway check that stayed green with the internet down, and an alert channel that logged 261 sends while the provider refused every one with HTTP 203. The management system runs 9,570 automated tests (Python, Flask, PostgreSQL). The architecture and decisions are mine, the code is AI-generated under my specification, and I review it and am accountable for it in production. Not yet in my experience: public cloud in production and Kubernetes.

Bento Gonçalves, Brazil (UTC−3) · [LinkedIn](https://www.linkedin.com/in/allan-zeni) · [sistemasaz.com.br](https://sistemasaz.com.br)
