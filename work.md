1) DESCRIÇÃO RÁPIDA DO PROJETO

Nesta fase do projeto, a FarmTech Solutions avança na aplicação de sensores físicos integrados a um sistema de irrigação inteligente. O objetivo é desenvolver um sistema físico (simulado) que colete dados de sensores de umidade, nutrientes e pH e controle uma bomba de irrigação conforme os valores obtidos. Os dados também devem ser armazenados em um banco de dados SQL, com possibilidade de visualização e análises estatísticas.

2) DESCRIÇÃO DETALHADA DO PROJETO

Com base nas modelagens feitas na Fase 2, você agora irá simular o funcionamento de sensores agrícolas em um sistema montado na plataforma Wokwi.com. Como alguns sensores agrícolas reais não estão disponíveis na versão gratuita da plataforma, utilizaremos componentes que simulem o comportamento esperado de cada sensor, mantendo o objetivo pedagógico do projeto:

Sensor de Fósforo (P): será representado por um botão físico. O botão simula a leitura de presença/ausência de fósforo no solo, com valores booleanos (pressionado = presença; solto = ausência).
Sensor de Potássio (K): também será representado por um botão, funcionando com a mesma lógica binária do sensor de fósforo.
Sensor de pH: será representado por um sensor de luz LDR (Light Dependent Resistor). O LDR fornece valores analógicos que variam com a luminosidade. Essa variação será usada como analogia ao comportamento do pH, que também apresenta variações contínuas (exemplo: pH entre 0 e 14).
Sensor de umidade do solo: utilizaremos o sensor DHT22, disponível na plataforma Wokwi. Este sensor retorna valores analógicos que representam a umidade do solo em tempo real.
O controle geral do sistema será realizado por um microcontrolador ESP32, responsável por receber os dados dos sensores e controlar a bomba de irrigação, representada por um relé. O relé poderá ser ligado ou desligado automaticamente de acordo com a lógica criada pelo grupo, e seu status será indicado por um LED embutido (ligado = irrigação ativa, desligado = inativa).

O sistema deve:

Receber dados dos sensores;
Ligar ou desligar o relé (bomba d'água) de acordo com a lógica criada pelo grupo;
Armazenar manualmente os dados do monitor serial em um banco de dados SQL (simulado em Python);
Implementar as operações CRUD básicas no banco de dados;
Documentar toda a lógica de funcionamento no README.MD do GitHub.
Entrega 1: Sistema de Sensores e Controle com ESP32

Metas da entrega:

Construir o circuito de sensores no VS Code usando as extensões do Wokwi e Platformio;
Criar código em C/C++ para ler os sensores e acionar o relé conforme lógica definida;
Comentar o código explicando a lógica usada;
Documentar o circuito com imagem no README.MD.
Entregáveis:

Código C/C++ funcional no GitHub;
Imagem (.png) do circuito Wokwi;
README.MD explicativo sobre o circuito e a lógica de controle.