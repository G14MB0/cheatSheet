import cv2
import numpy as np


def match_template(image, templates, method=cv2.TM_CCOEFF_NORMED, threshold=0.8, masks=None):
    """
    Esegue il template matching sull'immagine data utilizzando una lista di template forniti.
    Opzionalmente, utilizza una lista di maschere corrispondenti ai template.
    
    :param image: L'immagine in cui cercare.
    :param templates: Lista di template da cercare nell'immagine.
    :param method: Metodo di template matching di OpenCV da utilizzare.
    :param threshold: Soglia per determinare una corrispondenza valida.
    :param masks: Lista di maschere corrispondenti ai template (opzionale).
    :return: Lista di dizionari, ogni dizionario contiene 'location' (tuple x, y) e 'score' di ogni match trovato.
    """
    match_results = []

    for idx, template in enumerate(templates):
        mask = masks[idx] if masks is not None and idx < len(masks) else None
        # Esegue il template matching
        res = cv2.matchTemplate(image, template, method, mask=mask)
        
        # Trova i punti in cui le corrispondenze superano la soglia
        loc = np.where(res >= threshold)
        
        for pt in zip(*loc[::-1]):  # Scambia le coordinate per corrispondere all'ordine (x, y)
            match_score = res[pt[1], pt[0]]
            match_results.append({"match_locations": pt, "match_scores": match_score})
    
    # Opzionalmente, puoi ordinare i risultati basandosi sullo score di corrispondenza, dal più alto al più basso
    match_results.sort(key=lambda x: x["match_scores"], reverse=True)
    

    if len(match_results) > 0:
        return  [match_results[0]["match_locations"]], [match_results[0]["match_scores"]]
    else:
        return [], []



def generate_bounding_boxes(match_locations, match_scores, template_size):
    """
    Genera i bounding boxes a partire dalle posizioni di corrispondenza trovate con il template matching.
    
    :param match_locations: Lista di tuple (x, y) delle coordinate dei punti in alto a sinistra dove il template corrisponde all'immagine.
    :param template_size: Dimensioni del template (larghezza, altezza).
    :return: Lista di bounding boxes, dove ogni bounding box è rappresentato da una tupla (x, y, w, h), con (x, y) le coordinate del punto in alto a sinistra e (w, h) la larghezza e l'altezza del box.
    """
    bounding_boxes = [(x, y, template_size[0], template_size[1]) for x, y in match_locations]
    scores = match_scores
    
    # Applica NMS ai bounding boxes
    selected_indices = apply_nms(bounding_boxes, scores)
    selected_boxes = [bounding_boxes[i] for i in selected_indices]
    
    return selected_boxes


def apply_nms(bounding_boxes, scores, score_threshold=0.8, iou_threshold=0.4):
    """
    Applica Non-Maximum Suppression (NMS) per eliminare i bounding boxes sovrapposti.
    
    :param bounding_boxes: Lista di bounding boxes, dove ogni box è [x, y, w, h].
    :param confidence_scores: Lista degli score di confidenza per ciascun box.
    :param score_threshold: Soglia per filtrare i box con score basso.
    :param iou_threshold: Soglia di IoU per l'NMS.
    :return: Lista degli indici dei bounding boxes mantenuti dopo l'NMS.
    """
    # Converti i bounding boxes in un formato atteso da cv2.dnn.NMSBoxes
    boxes = [(box[0], box[1], box[0] + box[2], box[1] + box[3]) for box in bounding_boxes]  # Da [x, y, w, h] a [x1, y1, x2, y2]
    scores = [float(score) for score in scores]
    indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold, iou_threshold)

    # Gestisci il caso in cui indices è una tupla vuota
    if len(indices) == 0:
        return np.array([])

    # Converti in array NumPy se necessario e poi usa flatten()
    if isinstance(indices, tuple):
        indices = np.array(indices[0])
    return indices.flatten()
    