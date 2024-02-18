import cv2
from template_matching import match_template, generate_bounding_boxes
from tqdm import tqdm

def read_image(filePath):
    """
    Carica un'immagine template dal disco e la converte in scala di grigi.

    :param template_path: Percorso del file del template da caricare.
    :return: Template in scala di grigi.
    """
    # Carica l'immagine utilizzando OpenCV
    template = cv2.imread(filePath)
    # Verifica se l'immagine è stata caricata correttamente
    if template is None:
        raise FileNotFoundError(f"Impossibile trovare o aprire il template all'indirizzo '{filePath}'")
    # Converte l'immagine in scala di grigi
    template_gray = convert_to_grayscale(template)
    return template_gray



def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_filters(image):
    return image


def resize_image(image, scale_factor):
    """
    Ridimensiona un'immagine per un fattore di scala dato.

    :param image: Immagine da ridimensionare, come array NumPy.
    :param scale_factor: Fattore di scala per il ridimensionamento. 
                         Un valore di 1.0 mantiene la dimensione originale, 
                         < 1.0 riduce l'immagine, > 1.0 ingrandisce l'immagine.
    :return: Immagine ridimensionata.
    """
    # Calcola le nuove dimensioni
    new_width = int(image.shape[1] * scale_factor)
    new_height = int(image.shape[0] * scale_factor)
    
    # Ridimensiona l'immagine
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA if scale_factor < 1.0 else cv2.INTER_LINEAR)
    
    return resized_image




def process_video_for_training(video_path, template_paths, mask_paths=[], split_ratio=0.8, threshold=0.8, live_results=False, resizeValue=0.5):
    """
    Elabora il video per il training, eseguendo il template matching su ogni frame
    e generando le labels. Divide i dati per training e valutazione.
    
    :param video_path: Percorso del file video.
    :param template_path: Percorso del file template.
    :param split_ratio: Rapporto di divisione tra dati di training e di valutazione.
    """
    # Carica il template
    templates = []
    for template_path in template_paths:
        templates.append(resize_image(read_image(template_path), resizeValue))
    # Carica la maschera creata con Photoshop
        
    # Carica il template
    masks = []
    for mask_path in mask_paths:
        if mask_path != "" and mask_path:
            masks.append(resize_image(cv2.imread(mask_path, 0), resizeValue))
        else:
            pass


    template_size = templates[0].shape
    if len(masks) > 0:
        mask_size = masks[0].shape
    else:
        mask_size = template_size
    if mask_size != template_size:
        raise ValueError("Mask and Template have not the same dimensions!")


    if live_results: template_w, template_h = template_size[::-1]
    
    # Inizializza la lista per contenere i dati di training (immagini) e le labels (bounding boxes)
    training_data = []
    labels = []
    
    # Apri il video
    cap = cv2.VideoCapture(video_path)
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    train_eval_split = int(frame_count * split_ratio)
    
    current_frame = 0
    
    # Utilizziamo tqdm qui per visualizzare la barra di progresso
    for _ in tqdm(range(frame_count), total=frame_count, desc="Processing video"):
        ret, frame = cap.read()
        if not ret:
            break
        
        # Pre-elaborazione del frame
        frame_processed = apply_filters(convert_to_grayscale(resize_image(frame, resizeValue)))
        # frame_processed = apply_filters(convert_to_grayscale(frame))
        
        # Template Matching
        match_locations, match_scores = match_template(frame_processed, templates, threshold=threshold, masks=masks)

        if live_results: 
            # Generazione delle Labels e disegno dei bounding boxes
            for loc in match_locations:
                top_left = loc
                bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
                cv2.rectangle(frame_processed, top_left, bottom_right, (0, 255, 0), 2)  # Disegna un rettangolo verde
                
            # Mostra il frame con i bounding boxes
            cv2.imshow('Template Matching in Action', frame_processed)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Premi 'q' per uscire
                break
        
        # Generazione delle Labels
        bounding_boxes = generate_bounding_boxes(match_locations, match_scores, template_size[::-1])
        
        # Aggiungi i dati elaborati alle liste
        training_data.append(frame_processed)
        labels.append(bounding_boxes)
        
        current_frame += 1
        if current_frame >= frame_count:
            break
    
    cap.release()
    
    # Qui dovresti dividere `training_data` e `labels` in set di training e valutazione
    # basato su `split_ratio`, per ora li lasciamo come esempio di struttura
    
    train_data = training_data[:train_eval_split]
    train_labels = labels[:train_eval_split]
    eval_data = training_data[train_eval_split:]
    eval_labels = labels[train_eval_split:]

    return train_data, train_labels, eval_data, eval_labels