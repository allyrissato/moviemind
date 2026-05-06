# 🎬 MovieMind — Sistema de Recomendação de Filmes

Projeto em Python com Streamlit para recomendar filmes parecidos com base em gêneros e título. A interface foi melhorada com um visual inspirado em plataformas de streaming, usando tons de rosa, roxo e azul.

---

## ✅ Melhorias aplicadas

- Interface mais moderna e responsiva
- Menu lateral com páginas
- Página inicial com banner estilo streaming
- Página de recomendações
- Catálogo com busca e filtro por gênero
- Dashboard com gráficos
- Integração com TMDB mais segura
- Tratamento de erro quando a API não está configurada
- `requirements.txt` corrigido
- `.gitignore` melhorado
- `.env` removido do pacote final por segurança
- `.env.example` criado
- Pasta `venv` removida do ZIP final
- Código separado em arquivos dentro da pasta `src`

---

## 🚀 Tecnologias usadas

- Python
- Streamlit
- Pandas
- Scikit-learn
- Plotly
- Requests
- Python-dotenv
- API TMDB

---

## 📂 Estrutura do projeto

```text
movie-recommendation-system-melhorado/
│
├── app.py
├── requirements.txt
├── README.MD
├── .gitignore
├── .env.example
│
├── data/
│   └── movies.csv
│
└── src/
    ├── recommendation.py
    └── tmdb_api.py
```

---

## ▶️ Como rodar o projeto

### 1. Abra a pasta no VS Code

Abra a pasta principal do projeto no VS Code.

---

### 2. Crie o ambiente virtual

No terminal:

```bash
python -m venv .venv
```

---

### 3. Ative o ambiente virtual

No Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear, use:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

---

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 5. Configure a chave TMDB

Crie uma cópia do arquivo:

```text
.env.example
```

Renomeie a cópia para:

```text
.env
```

Dentro do `.env`, coloque sua chave:

```text
TMDB_API_KEY=sua_chave_aqui
```

> O projeto também funciona sem chave, mas usará imagens reserva.

---

### 6. Rode o projeto

```bash
python -m streamlit run app.py
```

Depois abra no navegador:

```text
http://localhost:8501
```

---

## 🧠 Como funciona a recomendação

O sistema usa:

- `TfidfVectorizer`
- Similaridade do cosseno
- Dados de título e gênero dos filmes

Ele transforma texto em números e compara quais filmes são mais parecidos com o filme escolhido.

---

## 💼 Como apresentar em entrevista

Você pode dizer:

> Desenvolvi um sistema de recomendação de filmes em Python usando Streamlit. O projeto utiliza TF-IDF e similaridade do cosseno para indicar filmes parecidos com base em título e gênero. Também implementei uma interface visual inspirada em plataformas de streaming, integração com API externa, tratamento de erros e dashboard com análise da base de dados.

---

## 🔮 Próximas melhorias possíveis

- Sistema de login
- Lista de favoritos
- Avaliação dos usuários
- Histórico de filmes assistidos
- Banco de dados MySQL ou PostgreSQL
- Deploy no Streamlit Cloud
- Testes automatizados
