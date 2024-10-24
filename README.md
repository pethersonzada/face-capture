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

## LBPH vs Face Recognition, qual eu deveria escolher pra usar no meu projeto?

O código que utiliza a biblioteca LBPH pode apresentar algumas falhas durante o processo de captura de imagens. Por exemplo, ao tirar múltiplas fotos, o algoritmo pode interpretar incorretamente uma sombra ou outro artefato visual como um rosto, especialmente em condições de iluminação inadequadas. Isso pode resultar em fotos erradas, registrando elementos que não são, de fato, rostos. Esse tipo de erro é uma limitação do LBPH, principalmente em situações onde o ambiente não é controlado ou onde há interferências visuais.

Por outro lado, a biblioteca Face Recognition se destaca por sua precisão superior em relação ao LBPH. Mesmo quando ela atribui um nome incorretamente, o que acontece é que o sistema está apenas realizando uma varredura entre todos os rostos armazenados no banco de dados e encontrando a correspondência mais próxima. O Face Recognition nunca faz uma afirmação definitiva de que o rosto detectado é de uma pessoa diferente da realidade. Ele sempre busca a melhor correspondência possível, garantindo uma taxa de erro menor e oferecendo maior confiabilidade nos resultados comparativos, especialmente em comparação com o LBPH.

Para modificar o código, você pode ajustar os parâmetros de detecção de rostos no LBPH ou Face Recognition, melhorar a qualidade das imagens de treinamento, ou adicionar filtros para ignorar sombras e elementos não faciais.

Recomendo o uso do código que contenha o face-recognition, mas fica ao seu critério! Disponibilizo os códigos para você, desenvolvedor, ou apenas alguém que quer entender os códigos e como funciona, aprender o por que o face-recognition pode ser melhor em alguns casos, sinta-se livre para utilizar o código para aprendizado! Caso queira fazer alguma alteração, pode fazer!! Faça bom uso :)
