def on_event(event, posture):
    if event == "Caída confirmada":
        print(f"[ALERTA] {event} detectada! Postura actual: {posture}")
    elif event == "Recuperación de caída":
        print(f"[INFO] {event}. Postura actual: {posture}")