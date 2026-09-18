import os
import cv2
import numpy as np
import mediapipe as mp

# Inicializa a webcam e retorna o objeto de captura.
def inicializar_webcam():
    return cv2.VideoCapture(0)

# Cria um diretório para as faces das pessoas.
def criar_diretorio_faces(nome_pessoa):
    diretorio_faces = 'face-detector/faces/'
    diretorio_pessoa = os.path.join(diretorio_faces, nome_pessoa)
    
    os.makedirs(diretorio_faces, exist_ok=True)
    os.makedirs(diretorio_pessoa, exist_ok=True)
    
    return diretorio_pessoa

# Captura imagens do rosto da pessoa e salva no diretório especificado.
def capturar_faces(webcam, diretorio_pessoa):
    contador = 0
    mp_face_detection = mp.solutions.face_detection
    
    # Gerenciador de contexto para liberar recursos do MediaPipe corretamente
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        print("\nPosicione-se em frente à câmara. Capturando 100 imagens...")
        
        while contador < 100:
            ret, quadro = webcam.read()
            if not ret:
                print("Falha ao capturar imagem da webcam.")
                break
            
            imagem_rgb = cv2.cvtColor(quadro, cv2.COLOR_BGR2RGB)
            resultados = face_detection.process(imagem_rgb)
            
            if resultados.detections:
                for detection in resultados.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    h, w, _ = quadro.shape
                    bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)

                    # Verifica se a caixa delimitadora está dentro dos limites da imagem
                    if bbox[1] >= 0 and bbox[0] >= 0 and (bbox[1] + bbox[3]) <= h and (bbox[0] + bbox[2]) <= w:
                        imagem_rosto = quadro[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
                        
                        # CORREÇÃO CRÍTICA: Padroniza o tamanho para o LBPH aceitar
                        imagem_rosto_redimensionada = cv2.resize(imagem_rosto, (200, 200))
                        
                        caminho_salvamento = os.path.join(diretorio_pessoa, f"{contador}.jpg")
                        cv2.imwrite(caminho_salvamento, imagem_rosto_redimensionada)
                        contador += 1

            cv2.imshow("Captura de Rostos (Pressione 'q' para sair)", quadro)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    print(f"Captura concluída para {diretorio_pessoa}!\n")

# Treina o reconhecedor de rostos com as imagens armazenadas.
def treinar_reconhecedor(diretorio_faces):
    reconhecedor = cv2.face.LBPHFaceRecognizer_create()
    rotulos = []
    faces = []
    ids_rotulos = {}
    
    if not os.path.exists(diretorio_faces):
        os.makedirs(diretorio_faces, exist_ok=True)
        return reconhecedor, ids_rotulos
    
    id_atual = 0
    for nome_pessoa in os.listdir(diretorio_faces):
        caminho_pessoa = os.path.join(diretorio_faces, nome_pessoa)
        
        if not os.path.isdir(caminho_pessoa):
            continue
            
        imagens = os.listdir(caminho_pessoa)
        if not imagens:
            continue

        for nome_imagem in imagens:
            caminho_imagem = os.path.join(caminho_pessoa, nome_imagem)
            imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
            
            if imagem is not None:
                # Garante redimensionamento de segurança
                imagem_redimensionada = cv2.resize(imagem, (200, 200))
                faces.append(imagem_redimensionada)
                rotulos.append(id_atual)
        
        ids_rotulos[id_atual] = nome_pessoa
        id_atual += 1

    if faces and rotulos:
        reconhecedor.train(faces, np.array(rotulos))
        os.makedirs("face-detector", exist_ok=True)
        reconhecedor.save("face-detector/face_trained.yml")
        print("Modelo treinado com sucesso!")
    else:
        print("Aviso: Nenhuma face encontrada para treinamento.")

    return reconhecedor, ids_rotulos

# Reconhece rostos usando o modelo treinado e exibe os resultados na tela.
def reconhecer_faces(webcam, reconhecedor, ids_rotulos):
    mp_face_detection = mp.solutions.face_detection
    
    if not ids_rotulos:
        print("Nenhum rosto cadastrado no sistema para reconhecimento.")
        return

    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        print("\nIniciando reconhecimento facial. Pressione 'Esc' para sair.")
        
        while True:
            ret, quadro = webcam.read()
            if not ret:
                print("Falha ao capturar imagem.")
                break
            
            imagem_rgb = cv2.cvtColor(quadro, cv2.COLOR_BGR2RGB)
            resultados = face_detection.process(imagem_rgb)

            if resultados.detections:
                for detection in resultados.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    h, w, _ = quadro.shape
                    bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)

                    if bbox[1] >= 0 and bbox[0] >= 0 and (bbox[1] + bbox[3]) <= h and (bbox[0] + bbox[2]) <= w:
                        rosto_recorte = quadro[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
                        rosto_cinza = cv2.cvtColor(rosto_recorte, cv2.COLOR_BGR2GRAY)
                        
                        # Padroniza a dimensão da face capturada em tempo de execução
                        rosto_padrao = cv2.resize(rosto_cinza, (200, 200))
                        
                        rotulo, confianca = reconhecedor.predict(rosto_padrao)
                        
                        limite_confianca = 70  # Ajustado para maior tolerância operacional no LBPH
                        
                        if confianca < limite_confianca and rotulo in ids_rotulos:
                            nome = ids_rotulos.get(rotulo, "Desconhecido")
                            cor_texto = (0, 255, 0)    # Verde para reconhecido
                        else:
                            nome = "Desconhecido"
                            cor_texto = (0, 0, 255)    # Vermelho para desconhecido
                        
                        texto_exibicao = f'{nome} ({int(confianca)})'
                        cv2.putText(quadro, texto_exibicao, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_texto, 2)
                        cv2.rectangle(quadro, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), cor_texto, 2)
            
            cv2.imshow("Reconhecimento Facial", quadro)
            
            if cv2.waitKey(5) == 27:  # Pressionar 'Esc'
                break

def main():
    while True:
        adicionar_pessoa = input("Deseja adicionar uma nova pessoa? (s/n): ").strip().lower()
        
        if adicionar_pessoa == 's':
            nome_pessoa = input("Digite o nome da pessoa: ").strip()
            if not nome_pessoa:
                print("Nome inválido.")
                continue
            webcam = inicializar_webcam()
            diretorio_pessoa = criar_diretorio_faces(nome_pessoa)
            capturar_faces(webcam, diretorio_pessoa)
            webcam.release()
        elif adicionar_pessoa == 'n':
            break
        else:
            print("Opção inválida. Por favor, digite 's' ou 'n'.")

    diretorio_base = 'face-detector/faces/'
    reconhecedor, ids_rotulos = treinar_reconhecedor(diretorio_base)
    
    caminho_modelo = "face-detector/face_trained.yml"
    if os.path.exists(caminho_modelo):
        reconhecedor.read(caminho_modelo)
    
    webcam = inicializar_webcam()
    if not webcam.isOpened():
        print("Erro: Não foi possível aceder à webcam.")
        return

    reconhecer_faces(webcam, reconhecedor, ids_rotulos)
    
    webcam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
