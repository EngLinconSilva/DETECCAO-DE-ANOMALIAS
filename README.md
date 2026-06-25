# Detecção de Anomalias em Imagens NDVI

## Descrição

Este projeto implementa um algoritmo para detecção automática de anomalias em imagens do Índice de Vegetação por Diferença Normalizada (NDVI) utilizando Python. A metodologia baseia-se na comparação entre o valor de cada pixel e a média de seus pixels vizinhos, permitindo identificar regiões com comportamento espectral distinto em relação ao padrão local.

A abordagem foi desenvolvida com foco em aplicações de Agricultura de Precisão, monitoramento de culturas agrícolas e identificação preliminar de áreas com potencial ocorrência de estresse vegetal, falhas de plantio, pragas, doenças ou outras alterações que possam impactar o vigor da vegetação.

---

## Metodologia

O algoritmo executa as seguintes etapas:

1. Leitura da imagem raster NDVI.
2. Tratamento de valores NoData.
3. Cálculo da média local utilizando uma janela móvel (5 × 5 pixels).
4. Cálculo do erro quadrático entre o valor do pixel e a média dos vizinhos.
5. Normalização dos valores de erro para uma escala de 0 a 100.
6. Identificação de anomalias utilizando o método estatístico do Intervalo Interquartil (IQR).
7. Remoção de regiões pequenas (< 25 pixels conectados).
8. Geração de produtos raster e relatório estatístico.

---

## Requisitos

### Bibliotecas Python

```bash
pip install numpy rasterio scipy
```

### Dependências

* Python 3.9+
* NumPy
* Rasterio
* SciPy

---

## Estrutura do Projeto

```text
projeto/
│
├── ndvi.tif
├── detectar_anomalias.py
│
└── result/
    ├── erro_normalizado.tif
    ├── anomalias.tif
    └── estatisticas.txt
```

---

## Configuração

Edite as seguintes variáveis no início do script:

```python
raster_path = r"D:\Mestrado\DeteccaoObj\Anomalias\ndvi.tif"
output_dir = r"D:\Mestrado\DeteccaoObj\Anomalias\result"

window_size = 5
iqr_factor = 1.5
```

### Parâmetros

| Parâmetro   | Descrição                                                 |
| ----------- | --------------------------------------------------------- |
| raster_path | Caminho da imagem NDVI                                    |
| output_dir  | Pasta onde serão salvos os resultados                     |
| window_size | Tamanho da janela móvel                                   |
| iqr_factor  | Fator multiplicador do IQR                                |
| min_pixels  | Número mínimo de pixels conectados para manter uma região |

---

## Execução

Execute o script utilizando:

```bash
python detectar_anomalias.py
```

---

## Arquivos Gerados

### erro_normalizado.tif

Raster contendo o erro normalizado entre o valor do pixel e a média dos seus vizinhos.

### anomalias.tif

Raster binário contendo:

| Valor | Classe   |
| ----- | -------- |
| 0     | Normal   |
| 1     | Anomalia |
| 255   | NoData   |

### estatisticas.txt

Relatório contendo:

* Quartil inferior (Q1)
* Quartil superior (Q3)
* Intervalo Interquartil (IQR)
* Limite utilizado para detecção
* Número total de pixels
* Número de pixels anômalos
* Percentual de anomalias
* Desvio padrão do NDVI

---

## Fundamentação Estatística

A detecção de anomalias utiliza o método do Intervalo Interquartil (IQR), amplamente empregado para identificação de outliers.

O limite superior é calculado por:

```text
Limite = Q3 + 1.5 × IQR
```

onde:

```text
IQR = Q3 − Q1
```

Pixels com valores acima desse limite são classificados como anomalias.

---

## Aplicações

* Agricultura de Precisão
* Monitoramento de lavouras
* Identificação de áreas sob estresse vegetal
* Direcionamento de inspeções de campo
* Detecção preliminar de problemas fitossanitários
* Monitoramento temporal da vegetação

---

## Limitações

O algoritmo identifica apenas regiões que apresentam comportamento espectral diferente da vizinhança local. Portanto, ele não determina a causa da anomalia detectada.

As áreas classificadas como anômalas devem ser verificadas em campo para confirmar sua origem.

Além disso, podem ocorrer detecções nas bordas dos talhões devido ao efeito de borda, especialmente em áreas com forte contraste espectral entre a cultura e o entorno.

---

## Autor

Engenheiro Cartógrafo Lincon Silva


Área de pesquisa: Sensoriamento Remoto, Agricultura de Precisão e Processamento Digital de Imagens.

---

## Licença

Este projeto está disponibilizado sob a licença MIT.
