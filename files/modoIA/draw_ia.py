import pygame

class DrawIa():
    def __init__(self, surface):
        self.game_surface = surface
    def write_log(self,rect,log):
        font_large = pygame.font.Font("five-nights-at-freddys.ttf", 36)
        main_text_surface = font_large.render(log, True, (0, 0, 0))
        main_text_x = (rect.get_width() - main_text_surface.get_width()) // 2
        main_text_y = (rect.get_height() - main_text_surface.get_height()) // 2
        rect.fill((255, 255, 255, 220))
        rect.blit(main_text_surface, (main_text_x, main_text_y))
        self.game_surface.blit(rect, ((self.game_surface.get_width() - rect.get_width()) // 2, self.game_surface.get_height() - 80))
    def draw_rects(self,ia):
        if  ia.detection.results is not None:
            for r in  ia.detection.results: 
                for i in range(len(r.boxes)):
                    class_id = int(r.boxes.cls[i].numpy())
                    confidence = r.boxes.conf[i].numpy()
                    class_name = ia.detection.model.names[class_id]

                    # Obtener las coordenadas ajustadas a las dimensiones actuales
                    x_min, y_min, x_max, y_max = map(int, r.boxes.xyxy[i, :4].numpy())
                    pygame.draw.rect(self.game_surface, (255, 0, 0), (x_min, y_min, x_max - x_min, y_max - y_min), 5)

                    font = pygame.font.Font("five-nights-at-freddys.ttf", 36)
                    label_text = font.render(f"{class_name} {confidence:.2f}", True, (255, 255, 255))
                    self.game_surface.blit(label_text, (x_min, y_max + 5))
