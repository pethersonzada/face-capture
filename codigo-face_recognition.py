import os
import cv2
import numpy as np
import face_recognition
import tkinter as tk
from tkinter import simpledialog, messagebox

# Função para garantir que uma pasta exista
def criar_pasta(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# Criar pastas necessárias
PASTA_ROSTOS = "Projeto/rostos_conhecidos"
criar_pasta(PASTA_ROSTOS)

def obter_nome_usuario():
    """Abre uma caixa de diálogo segura do Tkinter para recolher o nome."""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True) # Garante que a janela abre em primeiro plano
    nome = simpledialog.askstring("Cadastro", "Digite o nome do novo rosto:")
    root.destroy()
    return nome

def salvar_novo_rosto():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível aceder à webcam para captura.")
        return

    print("\nPressione 's' para capturar o rosto ou 'q' para cancelar.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o vídeo.")
            break

        cv2.imshow("Cadastro - Pressione 's' para salvar", frame)
        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord('s'):
            # Validação prévia: Verifica se existe pelo menos um rosto no frame antes de salvar
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locais = face_recognition.face_locations(rgb_frame)
            
            if not locais:
                print("Nenhum rosto detetado! Posicione-se melhor em frente à câmara.")
                continue

            nome_rosto = obter_nome_usuario()
            
            if nome_rosto and nome_rosto.strip():
                nome_limpo = nome_rosto.strip()
                caminho_rosto = os.path.join(PASTA_ROSTOS, f"{nome_limpo}.jpg")
                cv2.imwrite(caminho_rosto, frame)
                print(f"Sucesso: Rosto guardado como '{nome_limpo}.jpg'.")
                break
            else:
                print("Operação cancelada: Nome inválido.")

        elif tecla == ord('q'):
            print("Captura cancelada pelo utilizador.")
            break

    cap.release()
    cv2.destroyAllWindows()

def carregar_rostos_conhecidos(pasta):
    """Carrega as codificações validando a presença de rostos para evitar crashes."""
    codificacoes = []
    nomes = []

    if not os.path.exists(pasta):
        return codificacoes, nomes

    for nome_arquivo in os.listdir(pasta):
        if not nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
            
        caminho_imagem = os.path.join(pasta, nome_arquivo)
        
        try:
            imagem = face_recognition.load_image_file(caminho_imagem)
            encodings = face_recognition.face_encodings(imagem)
            
            if encodings:
                codificacoes.append(encodings[0])
                nomes.append(os.path.splitext(nome_arquivo)[0])
            else:
                print(f"Aviso: A imagem '{nome_arquivo}' foi ignorada por não conter rostos detetáveis.")
        except Exception as e:
            print(f"Erro ao processar o ficheiro {nome_arquivo}: {e}")

    return codificacoes, nomes

def main():
    # Pergunta inicial ao utilizador
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    resposta = messagebox.askquestion("Sistema", "Deseja cadastrar um novo rosto?")
    root.destroy()

    if resposta == 'yes':
        salvar_novo_rosto()

    # Carrega base de dados facial
    print("A carregar rostos conhecidos...")
    codificacoes_rostos_conhecidos, nomes_rostos_conhecidos = carregar_rostos_conhecidos(PASTA_ROSTOS)
    print(f"{len(nomes_rostos_conhecidos)} identidade(s) carregada(s) com sucesso.")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a webcam.")
        return

    print("\nIniciando reconhecimento em tempo real. Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame da câmara.")
            break

        # Redimensiona para acelerar o processamento da rede neural (escala 0.25)
        pequeno_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        frame_rgb_pequeno = cv2.cvtColor(pequeno_frame, cv2.COLOR_BGR2RGB)

        locais_rostos = face_recognition.face_locations(frame_rgb_pequeno)
        
        # Só calcula encodings se houver rostos detetados no frame
        if locais_rostos:
            codificacoes_rostos = face_recognition.face_encodings(frame_rgb_pequeno, locais_rostos)

            for codificacao_rosto, local_rosto in zip(codificacoes_rostos, locais_rostos):
                nome = "Desconhecido"
                cor = (0, 0, 255) # Vermelho para desconhecido por defeito

                if codificacoes_rostos_conhecidos:
                    distancias_rostos = face_recognition.face_distance(codificacoes_rostos_conhecidos, codificacao_rosto)
                    indice_melhor_correspondencia = np.argmin(distancias_rostos)
                    
                    # Limiar de tolerância padrão (0.6). Quanto menor, mais restrito e seguro.
                    if distancias_rostos[indice_melhor_correspondencia] < 0.55:
                        nome = nomes_rostos_conhecidos[indice_melhor_correspondencia]
                        cor = (0, 255, 0) # Verde para reconhecido

                # Ajusta as coordenadas para o tamanho original da imagem (multiplica por 4)
                topo, direita, baixo, esquerda = [v * 4 for v in local_rosto]

                # Desenha o retângulo e o nome no frame original
                cv2.rectangle(frame, (esquerda, topo), (direita, baixo), cor, 2)
                cv2.putText(frame, nome, (esquerda, topo - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, cor, 2)

        cv2.imshow('Reconhecimento Facial', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
