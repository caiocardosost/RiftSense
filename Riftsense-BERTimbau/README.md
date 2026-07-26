# RiftSense

RiftSense é um detector de conflitos em pares de tweets em português, desenvolvido a partir do modelo **BERTimbau Base** ajustado para a tarefa de classificação binária de conflitos.

O modelo treinado está hospedado no Hugging Face e é baixado automaticamente durante a primeira execução da aplicação.

---

# Estrutura do projeto

```
.
├── app/                 # Código da aplicação
├── scripts/             # Scripts de execução
├── input/               # Arquivos de entrada
├── output/              # Resultados gerados
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Requisitos

* Python 3.12+ (execução local)
* Docker e Docker Compose (execução em contêiner)

---

# Instalação (execução local)

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

---

# Execução local

## Classificar um par de tweets

```bash
python scripts/predict_pair.py
```

Informe os dois textos quando solicitado.

---

## Classificar um dataset

Coloque o arquivo CSV em:

```
input/dataset.csv
```

Execute:

```bash
python scripts/predict_dataset.py
```

O resultado será salvo em:

```
output/dataset_classificado.csv
```

---

# Execução com Docker Compose

## Construir a imagem

Execute apenas na primeira utilização ou após alterações no Dockerfile:

```bash
docker compose build
```

---

## Classificar um par de tweets

```bash
docker compose run --rm riftsense
```

O programa solicitará a entrada dos dois tweets pelo terminal.

---

## Classificar um dataset

Coloque o arquivo CSV em:

```
input/dataset.csv
```

Em seguida execute:

```bash
docker compose run --rm riftsense python scripts/predict_dataset.py
```

O arquivo classificado será salvo em:

```
output/dataset_classificado.csv
```

---

# Modelo treinado

O modelo utilizado neste projeto encontra-se disponível no Hugging Face e é baixado automaticamente durante a primeira execução.

Após o primeiro download, o Docker armazena o modelo em um volume persistente (`huggingface_cache`), evitando novos downloads nas execuções seguintes.

---

# Observações

* O arquivo de entrada deve possuir as colunas:

```
tweet_1
tweet_2
```

* O arquivo de saída contém as colunas originais acrescidas de:

```
P(NoConflict)
P(Conflict)
Conflict
```

onde:

* **P(NoConflict):** probabilidade da classe "não conflito";
* **P(Conflict):** probabilidade da classe "conflito";
* **Conflict:** classificação final do modelo (0 = Não Conflito, 1 = Conflito).
