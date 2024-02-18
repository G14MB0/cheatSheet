from preprocessing import process_video_for_training

MATCHING_THRESHOLD = 0.75
LIVE_RESULTS = True
RESIZE_VALUE = 0.5
SPLIT_RATIO = 0.8

def main():
    video_path = "./video.mp4"
    template_paths = ["./template.jpg", "./template2.jpg"]
    mask_paths = ["", ""]
    
    # Processa il video e prepara i dati di training e valutazione
    train_data, train_labels, eval_data, eval_labels = process_video_for_training(video_path,
                                                                                   template_paths, 
                                                                                   mask_paths,
                                                                                   split_ratio=SPLIT_RATIO,
                                                                                   threshold=MATCHING_THRESHOLD, 
                                                                                   live_results=LIVE_RESULTS, 
                                                                                   resizeValue=RESIZE_VALUE)
    

if __name__ == "__main__":
    main()
