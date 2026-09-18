# Sistema de Reconhecimento Facial - Face Capture

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Google-orange?style=for-the-badge&logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Otimizado_%26_Pronto-success?style=for-the-badge)]()

*Um ecossistema completo de visão computacional contendo duas abordagens técnicas (Deep Learning vs. Classificador Clássico) voltado para automação de chamadas, controle de presença e segurança.*

</div>

---

## Sobre o Projeto

Este projeto foi idealizado originalmente para aplicação no **ambiente escolar**, com o propósito de substituir o método tradicional de chamada manual. A tecnologia permite o controle automatizado e preciso de presença de alunos, otimizando o fluxo de entrada e saída, reduzindo falhas humanas e fornecendo registros digitais em tempo real para maior segurança institucional.

O repositório disponibiliza duas soluções técnicas distintas e otimizadas, blindadas contra erros comuns de execução (como falhas de dimensionamento, ausência de rostos nas fotos ou crashes de diretórios vazios).

---

## Abordagens Implementadas

### 1. Abordagem Moderna: `face_recognition` (Recomendada)
Baseada em aprendizado profundo (*deep learning*), esta abordagem mapeia os traços faciais gerando vetores de características (*embeddings*) altamente precisos.
* **Funcionalidades**:
  * Detecção e reconhecimento robusto de rostos em tempo real.
  * Cadastro interativo de novos usuários via webcam utilizando caixas de diálogo intuitivas (`Tkinter`).
  * Validação prévia de quadros para evitar o salvamento de imagens corrompidas ou sem rostos.
  * Alta tolerância a variações de iluminação e ângulos de rotação.

### 2. Abordagem Clássica: OpenCV + MediaPipe + LBPH
Abordagem tradicional baseada em histogramas de texturas locais.
* **Funcionalidades**:
  * Detecção de faces de alta performance através do **MediaPipe** (Google).
  * Rotina automatizada para captura sequencial de 100 imagens de treino por usuário.
  * Treinamento e salvamento de modelo descritivo utilizando o algoritmo **LBPH** (*Local Binary Patterns Histograms*).
  * Classificação e identificação em tempo real via matrizes de cinza redimensionadas.

---

## Dependências (`requirements.txt`)

Para facilitar a instalação de todas as bibliotecas necessárias de uma só vez, utilize o arquivo `requirements.txt` com o seguinte conteúdo:

```text
face-recognition>=1.3.0
opencv-python>=4.8.0
numpy>=1.24.0
mediapipe>=0.10.0
```
---

## Como Usar

### 1. Instalação das Dependências

Clone o repositório e instale as dependências executando o comando abaixo:

```bash
pip install -r requirements.txt
```

> **Nota:** O pacote `face-recognition` depende da biblioteca `dlib`. No sistema operacional Windows, pode ser necessário instalar previamente o **Visual Studio Build Tools**.

---

### 2. Execução do Projeto

Escolha uma das abordagens disponíveis para rodar o sistema:

#### **Opção A: Abordagem Moderna (`face_recognition.py`)**

```bash
python codigo-face_recognition.py
```
* **Como utilizar:** Responda ao diálogo gráfico exibido na tela, pressione a tecla `s` para capturar a imagem do rosto e insira o nome correspondente. O sistema realizará o reconhecimento em tempo real.
* **Sair:** Pressione a tecla `q`.

#### **Opção B: Abordagem Clássica (`LBPH + MediaPipe`)**

```bash
python codigo-LBPH.py
```
* **Como utilizar:** Siga os passos indicados no terminal para cadastrar novas pessoas e efetuar o treinamento do modelo.
* **Sair:** Pressione a tecla `Esc`.

---

## Comparativo: LBPH vs. Face Recognition

| Critério | LBPH (Clássica) | Face Recognition (Moderna) |
| :--- | :--- | :--- |
| **Precisão** | Baixa/Média *(sensível a sombras e ruídos no ambiente)*. | Alta *(baseada em redes neurais profundas)*. |
| **Ambiente** | Exige iluminação e ambiente controlados. | Tolera variações de iluminação e ângulos. |
| **Erros** | Maior risco de falso positivo *(pode classificar sombras como rostos)*. | Menor taxa de erro *(utiliza cálculo de distância métrica)*. |

---

## Notas Finais

* **Recomendação:** Dê preferência ao uso do script `face_recognition.py` devido à maior estabilidade e precisão em cenários reais do dia a dia.
* **Código Educacional:** Sinta-se totalmente livre para modificar, evoluir e adaptar este projeto. Todos os scripts estão comentados linha a linha para facilitar o seu aprendizado e estudo.
