# Sistema de Reconhecimento Facial para Controle de Presença Escolar

Este projeto implementa um sistema de reconhecimento facial nas escolas para substituir o método tradicional de chamada, permitindo um controle automatizado e preciso da presença de alunos. O sistema também otimiza o fluxo de entrada e saída, garantindo maior segurança e eficiência no monitoramento do ambiente escolar. Com a tecnologia, o processo se torna mais rápido, reduzindo falhas humanas e fornecendo registros digitais em tempo real.

## Abordagens Implementadas

### 1. Reconhecimento com `face_recognition`

- **Biblioteca**: `face_recognition`
- **Funcionalidades**:
  - Detecta e reconhece rostos a partir de imagens ou vídeos.
  - Permite adicionar novos rostos à base de dados em tempo real, capturando-os pela webcam.
  - Salva as codificações dos rostos em uma pasta específica para futuras comparações.
  - Exibe o nome do rosto identificado ou "Desconhecido" se o rosto não for reconhecido.

### 2. Reconhecimento com OpenCV, Mediapipe e LBPH

- **Bibliotecas**: `OpenCV`, `Mediapipe`, `LBPH`
- **Funcionalidades**:
  - Detecta rostos em imagens capturadas pela webcam utilizando o Mediapipe.
  - Captura e armazena múltiplas imagens do rosto de cada pessoa para treinamento.
  - Treina um modelo de reconhecimento facial utilizando o algoritmo LBPH (Local Binary Patterns Histograms).
  - Permite o reconhecimento em tempo real, exibindo o nome da pessoa ou "Desconhecido".

## Bibliotecas Usadas

- `face_recognition`: Para codificação e comparação de rostos.
- `opencv-python`: Para captura de vídeo e exibição dos resultados.
- `numpy`: Para cálculos e manipulação de arrays.
- `mediapipe`: Para detecção de rostos.

## Como Usar

### Script com `face_recognition`

1. **Instale as dependências**:
   ```
   pip install face_recognition opencv-python numpy
   ```
    Execute o script para iniciar o reconhecimento facial:

   ```
    python reconhecimento_face_recognition.py
   ```
    Instruções:
        Ao iniciar, você pode optar por adicionar um novo rosto, capturando a imagem pela webcam.
        Pressione 's' para salvar a imagem e insira o nome da pessoa.
        O sistema irá reconhecer rostos em tempo real, exibindo o nome das pessoas conhecidas ou "Desconhecido" para rostos não reconhecidos.

Script com OpenCV, Mediapipe e LBPH

   ```
pip install opencv-python mediapipe numpy
   ```
Execute o script para adicionar novas pessoas e treinar o modelo:

   ```
python reconhecimento_opencv_lbph.py
   ```
Instruções:
    O sistema irá solicitar se você deseja adicionar uma nova pessoa.
    Caso sim, o script capturará 100 imagens do rosto para treinar o modelo LBPH.
    Após o treinamento, o sistema estará pronto para reconhecer rostos em tempo real, exibindo o nome da pessoa ou "Desconhecido".

Após testes, recomendo o uso do código que contenha a biblioteca "Face Recognition", pois acho mais otimizado que a biblioteca "LBPH", já que enquanto a LBPH precisa de muitas fotos para fazer o reconhecimento, a Face Recognition utiliza apenas uma.

O código que contem a biblioteca LBPH pode cometer erros, já que ele vai comparar o rosto que aparece no vídeo em tempo real e as imagens que estão na pasta criada pela aplicação, enquanto o Face Recognition tende a ser mais exato, e quando não existe um rosto parecido com o do vídeo em tempo real, ele pode sim colocar o nome de alguém cadastrado nas imagens da pasta "rostos_conhecidos", mas o código está apenas fazendo uma comparação, para ver se realmente se parece. Faça bom uso! :)
