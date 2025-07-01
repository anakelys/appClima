# App de Previsão do Tempo

Este é um aplicativo web de previsão do tempo que permite ao usuário buscar o clima atual e a previsão de 5 dias para qualquer cidade do mundo. Utiliza a API Open-Meteo para obter dados como temperatura, umidade, vento, precipitação e exibe ícones visuais do clima. O frontend é responsivo, moderno e fácil de usar.

## Visão Geral
- Busca clima atual e previsão de 5 dias para qualquer cidade do mundo.
- Exibe temperatura, umidade, vento, precipitação e descrição visual do clima (com ícones).
- Autocomplete internacional de cidades.
- Interface responsiva e visualmente atraente (Tailwind CSS + Weather Icons).
- Tratamento de erros para cidades inválidas ou falha de API.
- Resultados podem ser registrados em arquivo (no backend Python).

## Instalação
1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd appClima
   ```
2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Instale as dependências Python:**
   ```bash
   pip install -r requirements.txt
   ```
4. **(Opcional) Execute o backend Python:**
   - O backend pode ser usado para registrar buscas, cache e testes automatizados.
   - Exemplo:
     ```bash
     python src/api/open_meteo.py
     ```
5. **Abra o arquivo `templates/index.html` em seu navegador** para usar a interface web.

## Guia de Uso
- Digite o nome de uma cidade no campo de busca. O autocomplete irá sugerir cidades conforme você digita.
- Clique em "Buscar" para ver o clima atual e a previsão de 5 dias.
- Os dados exibidos incluem:
  - Temperatura (°C)
  - Umidade (%)
  - Vento (km/h)
  - Precipitação (mm)
  - Descrição visual com ícone
- Em caso de erro (cidade inválida ou API fora do ar), uma mensagem será exibida.

## Exemplo de Resultado
```
Cidade: São Paulo, Brasil
Temperatura: 22°C
Umidade: 70%
Vento: 12 km/h
Precipitação: 0 mm
Descrição: Parcialmente nublado ☁️

Previsão para 5 dias:
01/07/2025: Máx 25°C / Mín 16°C, Parcialmente nublado ☁️
02/07/2025: Máx 24°C / Mín 15°C, Chuvoso 🌧️
...
```

## Funcionalidades
- Busca de clima atual por cidade
- Previsão de 5 dias
- Autocomplete internacional de cidades
- Exibição visual com ícones de clima
- Interface responsiva e moderna
- Tratamento de erros e mensagens amigáveis
- Cache de resultados (backend)
- Registro de buscas e respostas em arquivo (backend)
- Testes automatizados (pytest)

## Melhorias Futuras
- Permitir busca por localização atual (geolocalização)
- Histórico de buscas recentes
- Suporte a múltiplas línguas
- Exportar resultados (PDF/CSV)
- Notificações de alerta de tempo severo
- Melhorar acessibilidade (A11y)
- Deploy como Progressive Web App (PWA)

---

## Uso responsável e créditos
- Este projeto utiliza dados das APIs públicas Open-Meteo (https://open-meteo.com/) e Nominatim (https://nominatim.org/).
- Os ícones de clima são fornecidos pela biblioteca Weather Icons (https://erikflowers.github.io/weather-icons/).
- O uso deste software deve respeitar os termos de uso das APIs e bibliotecas envolvidas.
- Não utilize este app para fins abusivos, automação massiva ou coleta de dados sensíveis.
- Código parcialmente gerado com auxílio de IA (GitHub Copilot) e revisado manualmente.

Desenvolvido por Ana Souza com o apoio da ferramenta Copilot.
