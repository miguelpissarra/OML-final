# Avaliação do módulo de Operacionalização de Machine Learning - Projecto Individual

## Rumos Bank going live

The Rumos Bank é um banco que tem perdido bastante dinheiro devido à quantidade de créditos que fornece e que não são pagos dentro do prazo devido. 

Depois do banco te contratar, como data scientist de topo, para ajudares a prever os clientes que não irão cumprir os prazos, os resultados exploratórios iniciais são bastante promissores!

Mas o banco está algo receoso, já que teve uma má experiência anterior com uma equipa de data scientists, em que a transição dos resultados iniciais exploratórios até de facto conseguirem ter algo em produção durou cerca de 6 meses, bem acima da estimativa inicial.

Por causa desta prévia má experiência, o banco desta vez quer ter garantias que a passagem dos resultados iniciais para produção é feita de forma mais eficiente. O objetivo é que a equipa de engenharia consegue colocar o vosso modelo em produção em dias em vez de meses!

## Avaliação

Os componentes que vão ser avaliados neste projecto são:

* `README.md` atualizado
* Todas as alterações que fazem são trackeadas num repositório do github
* Ambiente do projecto (conda.yaml) definido de forma adequada
* Runs feitas no notebook `rumos_bank_leading_prediction.ipynb` estão documentadas, reproduzíveis, guardadas e facilmente comparáveis
* Os modelos utilizados estão registados e versionados num Model Registry
* O melhor modelo está a ser servido num serviço - não precisa de UI
* O serviço tem testes
* O serviço está containerizado
* O container do serviço é built, testado e enviado para um container registry num pipeline de CICD

Garantam que tanto o repositório do github como o package no github estão ambos públicos!

### Data limite de entrega

01MAI25

Deve ser enviada, até à data limite de entrega, um link para o vosso github (tem de estar público). Podem enviar este link para o meu email `lopesg.miguel@gmail.com` ou slack.

###

Este repositório (https://github.com/miguelpissarra/OML-final) descreve o processo de treino, implementação e operacionalização de modelos de Machine Learning para prever a probabilidade de crédito entrar em default. Contém instruções detalhadas sobre como configurar e utilizar o MLFlow e a FastAPI para servir os modelos assim como o fluxo de CICD definido.  


# Índice
- [Prever Default](#prever-default)
    - [Configuração](#configuracao)
    - [Modelos](#modelos)
    - [Mlflow](#mlflow)
    - [Webservice](#webservice)
    - [Tests](#tests)
    - [CICD](#cicd)
- [Comandos Úteis](#comandos-úteis)

# Prever Default

## Configuração

Localmente foi criada a pasta OML-final onde estão todas as pastas e ficheiros do projeto. Para garantir a distribuição e a partilha, foi criado também um repositório no github.
Tudo foi versionado com o git e feito push para o github sempre que localmente algo era criado ou atualizado. Por opção, não foram criados outros branches, tudo foi feito no main.
Para isolar o projeto em termos de ambiente, foi criado um ambiente conda dedicado, denominado: OML-final

Criar ambiente: 
```
conda create -n OML-final python=3.12
```
Instalar os packages necessários para o projeto:
```
conda install mlflow pandas scikit-learn ipykernel pytest
```
Criar o ficheiro conda.yaml com o export o ambiente
```
conda env export --no-builds -f conda.yaml
```
No entanto devido a problemas com o conda.yaml criado, foi utilizado o ficheiro gerado em aula.

Ficheiros docker-compose.yaml e Dockerfile.Service:
```
O ficheiro docker-compose.yaml contém a gestão dos dois serviços criados, o do mlflow e da fastapi.
O ficheiro Dockerfile.Service contém a configuração do fastapi que irá permitir a utilização dos modelos para efetuar as previsões.


## Modelos
Os modelos foram treinados através do notebook `rumos_bank_lending_prediction.ipynb` que está na pasta `notebooks`.
O notebook foi adaptado para criar várias runs (com pipelines), uma por modelo, além da baseline inicial. Em termos de uns, temos:
- logistec_reg
- KNN
- SVM
- Decision Tree
- Random Forest
- Neural Network

No final, o modelo com melhores resultados foi o random forest e através do frontend do mlflow, coloquei a tag de `champiom`, ajustando também o ficheiro `app.json` da pasta `config` que é onde são guardados e depois lidas as configurações de acesso aos dois serviços.

Fica a resalva que devido ao tamanho do modelo gerado, reduzi os estimadores para manter o tamanho abaixo dos 60MB. Quando o modelo foi treinado com os estimadores que o notebook tinha inicialmente, o tamanho do modelo não permitia fazer o push para o repositório. A diferença de estimadores não prejudicou muito o desempenho e permitiu avançar com o projeto.
Ainda criei um novo ambiente para testar a utilização do package lfs para gerir ficheiros de elevado volume. Embora localmente tenha funcionado e fosse possível faser push para o repositório (um criado para este efeito), na execução dos testes por exemplo, dava sempre erro (http connection failed ou timeout), provavelmente porque no ambiente remoto faltava a instalação do lfs. Provavelmente é possível resolver este problema de volume de dados mas não investiguei mais pois não é o propósito do projeto.
O importante é que com a redução dos estimadores, no final tudo funcionou sem problemas :).

## Mlflow
Para instanciar (através do terminal no VSC por exemplo):
- mlflow ui --backend-store-uri ./mlruns

Para testar o funcionamento do Mlflow (UI):
- http://localhost:5000

Nota: caso não seja possível aceder à UI do Mlflow, deve ser feito o seguinte:
pip uninstall mlflow
pip install mlflow
Desta forma será resolvida qualquer incompatibilidade e o UI irá funcionar sem problemas.


## Webservice

No python script `src\app\main.py` foi desenvolvida uma aplicação simples com a fastapi.

Esta app expõe o endpoint `/default` na qual espera receber as features de input do modelo (em formato json, no body do pedido) e retorna a previsão dada pelo modelo.

Para correr a app: com o ambiente deste projeto ativo, na raiz do projeto, executar o comando abaixo:

```
python ./src/app/main.py
```

Para testar se o modelo ficou corretamente exposto na app:
- http://localhost:5002/docs
- Utilizar a página html presente na diretoria `frontend` deste projeto e realizar um pedido (e ver a resposta) através desse frontend.

## Tests

Para testar o modelo registado utilizei a framework de Python `pytest`.

Os testes estão na pasta `tests`, a saber:

* `test_model.py`: testa o output do modelo e verifica se coincide com o output esperado bem como a shape
* `test_service.py`: testa o output do modelo e verifica se coincide com o output esperado utilizando o serviço

Para correr os testes (com o ambiente deste projeto ativo), executar o comando abaixo:

```
python -m pytest tests

```

## CICD

Para criar as actions no github que garantem o CICD, é necessário criar localmente a seguinte pasta `github\workflows` e dentro dela, colocar o ficheiro yaml responsável pela execução do fluxo (action) que irá ser disparado sempre que for efetuado um push.
Caso o fluxo corra sem erros, será criada uma nova versão da imagem docker no repositório.
As actions poderão ser consultadas no repositório, aqui: https://github.com/miguelpissarra/OML-final/actions


# Comandos Úteis

## Anaconda

Instalar: https://docs.anaconda.com/miniconda/miniconda-install/

Nota: Em Windows, para o comando `conda` funcionar corretamente em qualquer janela, devem abrir o Anaconda Prompt e correr `conda init`. A partir desse momento, podem fechar o Anaconda Prompt, reiniciar todos os terminais e usar o terminal normal do Windows para correr comandos do `conda`.

Nota 2: Em Windows, poderá ser necessário executar o comando `Set-ExecutionPolicy -ExecutionPolicy Unrestricted` na PowerShell caso não estejam autorizados a correr comandos na consola.

`conda create -n <env-name> python=<python-version>`: comando utilizado para criar um novo ambinete de anaconda com a versão `<python-version>` (que deverá ser substituido pela versão do Python que queremos usar) do Python e com o nome `<env-name>`(que deverá ser substituido pelo nome que queremos dar ao ambiente). [Link para a documentação do conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)

`conda activate <env-name>`: activa o ambiente `<env-name>` do Anaconda

`conda deactivate`: desactiva o ambiente atualmente activo do Anaconda

`conda env list`: comando utilizar para listar os ambientes que temos do Anaconda. Útil também para verificarmos onde estão instalados os ambientes do Anaconda

`conda env export --file conda.yaml`: comando utilizado para exportar o ambiente atual do anaconda para um ficheiro yaml. [Link para a documentação do conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#exporting-the-environment-yml-file)

`conda env export --from-history --file conda.yml`: comando utilizado para exportar o ambiente atual do anaconda para um ficheiro yaml, **incluindo apenas pacotes explicitamente pedidos** graças à flag `--from-history`. Esta flag é normalmente utilizada para tentar não incluir dependências que não funcionam cross platform, como é referido [na documentação do conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#exporting-an-environment-file-across-platforms) 

`conda env create -f conda.yaml`: comando utilizado para criar um ambiente do Anaconda a partir de um ficheiro que contenha a especificação de um ambiente do Anaconda. Este novo ambiente ficará com o nome que está especificado no ficheiro. Para usar um outro nome basta adicionar ao comando `-n <env-name>` (substituindo `<env-name>` pelo nome qu querem que fique). [Link para a documentação do conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)


Por padrão, o Windows bloqueia a execução de scripts não assinados no PowerShell. Pode-se alterar essa configuração com:

```
Set-ExecutionPolicy Unrestricted -Scope LocalMachine -Force
```

