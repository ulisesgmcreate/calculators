def disegna_vista_3d(self, larghezza, lunghezza, altezza, num_pali_x, num_pali_y, num_pannelli, num_posti_auto=0):
        # Pulisci il canvas
        self.canvas_3d.delete("all")
        
        # Ottieni dimensioni del canvas
        canvas_width = self.canvas_3d.winfo_width()
        canvas_height = self.canvas_3d.winfo_height()
        
        # Se il canvas non è ancora disegnato, usa dimensioni predefinite
        if canvas_width < 10:
            canvas_width = 600
        if canvas_height < 10:
            canvas_height = 400
        
        # Parametri di proiezione isometrica
        # L'angolo di visualizzazione influisce sulla prospettiva
        angolo = 30  # gradi
        sin_a = math.sin(math.radians(angolo))
        cos_a = math.cos(math.radians(angolo))
        
        # Fattore di scala per adattare al canvas
        max_dim = max(larghezza, lunghezza, altezza)
        scala = min(canvas_width, canvas_height) * 0.45 / max_dim
        
        # Offset per centrare il disegno
        offset_x = canvas_width * 0.5
        offset_y = canvas_height * 0.3
        
        # Funzione per convertire coordinate 3D in 2D con proiezione isometrica
        def iso(x, y, z):
            # Proiezione isometrica semplificata
            ix = offset_x + (x - y) * cos_a * scala
            iy = offset_y + (x + y) * sin_a * scala - z * scala
            return ix, iy
        
        # Disegna il terreno (griglia)
        step = 50  # cm
        for i in range(0, int(larghezza) + 1, step):
            for j in range(0, int(lunghezza) + 1, step):
                if (i + j) % (2 * step) == 0:
                    x1, y1 = iso(i, j, 0)
                    x2, y2 = iso(i + step, j, 0)
                    x3, y3 = iso(i + step, j + step, 0)
                    x4, y4 = iso(i, j + step, 0)
                    self.canvas_3d.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                                 fill="#EAEAEA", outline="#CCCCCC")
        
        # Disegna i pali verticali
        distanza_pali_x = larghezza / (num_pali_x - 1) if num_pali_x > 1 else larghezza
        distanza_pali_y = lunghezza / (num_pali_y - 1) if num_pali_y > 1 else lunghezza
        
        for i in range(num_pali_x):
            x = i * distanza_pali_x
            for j in range(num_pali_y):
                y = j * distanza_pali_y
                if (i == 0 or i == num_pali_x - 1 or j == 0 or j == num_pali_y - 1):  # Solo i pali perimetrali
                    # Base del palo
                    x1, y1 = iso(x - 5, y - 5, 0)
                    x2, y2 = iso(x + 5, y - 5, 0)
                    x3, y3 = iso(x + 5, y + 5, 0)
                    x4, y4 = iso(x - 5, y + 5, 0)
                    self.canvas_3d.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                                 fill="#888888", outline="#666666")
                    
                    # Palo verticale
                    x1, y1 = iso(x - 5, y - 5, 0)
                    x2, y2 = iso(x + 5, y - 5, 0)
                    x3, y3 = iso(x + 5, y + 5, 0)
                    x4, y4 = iso(x - 5, y + 5, 0)
                    x5, y5 = iso(x - 5, y - 5, altezza)
                    x6, y6 = iso(x + 5, y - 5, altezza)
                    x7, y7 = iso(x + 5, y + 5, altezza)
                    x8, y8 = iso(x - 5, y + 5, altezza)
                    
                    # Lati del palo
                    self.canvas_3d.create_polygon(x1, y1, x2, y2, x6, y6, x5, y5, 
                                                 fill="#999999", outline="#666666")
                    self.canvas_3d.create_polygon(x2, y2, x3, y3, x7, y7, x6, y6, 
                                                 fill="#888888", outline="#666666")
                    
                    # Non disegnare i lati posteriori se non necessario
                    if x < larghezza / 2 or y < lunghezza / 2:
                        self.canvas_3d.create_polygon(x3, y3, x4, y4, x8, y8, x7, y7, 
                                                     fill="#777777", outline="#666666")
                        self.canvas_3d.create_polygon(x4, y4, x1, y1, x5, y5, x8, y8, 
                                                     fill="#AAAAAA", outline="#666666")
        
        # Disegna la struttura del tetto
        # Base del tetto
        x1, y1 = iso(0, 0, altezza)
        x2, y2 = iso(larghezza, 0, altezza)
        x3, y3 = iso(larghezza, lunghezza, altezza)
        x4, y4 = iso(0, lunghezza, altezza)
        self.canvas_3d.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                     fill="#BBBBBB", outline="#999999")
        
        # Disegna i pannelli fotovoltaici
        pannelli_larghezza = math.floor(larghezza / self.pannello_larghezza)
        pannelli_lunghezza = math.floor(lunghezza / self.pannello_altezza)
        
        for i in range(pannelli_larghezza):
            for j in range(pannelli_lunghezza):
                x_start = i * self.pannello_larghezza
                y_start = j * self.pannello_altezza
                x_end = x_start + self.pannello_larghezza
                y_end = y_start + self.pannello_altezza
                
                x1, y1 = iso(x_start, y_start, altezza + 5)
                x2, y2 = iso(x_end, y_start, altezza + 5)
                x3, y3 = iso(x_end, y_end, altezza + 5)
                x4, y4 = iso(x_start, y_end, altezza + 5)
                
                # Pannello con gradiente di blu (effetto fotovoltaico)
                self.canvas_3d.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                             fill="#1E90FF", outline="#0000CD")
                
                # Crea linee di divisione nei pannelli
                mid_x = (x_start + x_end) / 2
                mid_x1, mid_y1 = iso(mid_x, y_start, altezza + 5)
                mid_x2, mid_y2 = iso(mid_x, y_end, altezza + 5)
                self.canvas_3d.create_line(mid_x1, mid_y1, mid_x2, mid_y2, fill="#0000CD")
                
                mid_y = (y_start + y_end) / 2
                mid_x1, mid_y1 = iso(x_start, mid_y, altezza + 5)
                mid_x2, mid_y2 = iso(x_end, mid_y, altezza + 5)
                self.canvas_3d.create_line(mid_x1, mid_y1, mid_x2, mid_y2, fill="#0000CD")
        
        # Disegna posti auto
        if num_posti_auto > 0:
            disposizione = self.disposizione_var.get()
            
            if disposizione == "lineare":
                # Posti auto in fila singola
                for i in range(num_posti_auto):
                    x_start = i * self.posto_auto_larghezza
                    y_start = (lunghezza - self.posto_auto_lunghezza) / 2
                    x_end = x_start + self.posto_auto_larghezza
                    y_end = y_start + self.posto_auto_lunghezza
                    
                    # Posto auto (pavimento)
                    x1, y1 = iso(x_start, y_start, 1)  # Leggermente sopra il terreno
                    x2, y2 = iso(x_end, y_start, 1)
                    x3, y3 = iso(x_end, y_end, 1)
                    x4, y4 = iso(x_start, y_end, 1)
                    self.canvas_3d.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                                 fill="#DDDDDD", outline="#999999")
                    
                    # Silhouette auto semplificata (se c'è spazio sufficiente)
                    if self.posto_auto_larghezza > 150 and self.posto_auto_lunghezza > 300:
                        car_x_start = x_start + 25
                        car_y_start = y_start + 50
                        car_width = self.posto_auto_larghezza - 50
                        car_length = self.posto_auto_lunghezza - 100
                        car_height = 120  # Altezza dell'auto
                        
                        # Corpo dell'auto
                        cx1, cy1 = iso(car_x_start, car_y_start, 1)
                        cx2, cy2 = iso(car_x_start + car_width, car_y_start, 1)
                        cx3, cy3 = iso(car_x_start + car_width, car_y_start + car_length, 1)
                        cx4, cy4 = iso(car_x_start, car_y_start + car_length, 1)
                        cx5, cy5 = iso(car_x_start, car_y_start, car_height)
                        cx6, cy6 = iso(car_x_start + car_width, car_y_start, car_height)
                        cx7, cy7 = iso(car_x_start + car_width, car_y_start + car_length, car_height)
                        cx8, cy8 = iso(car_x_start, car_y_start + car_length, car_height)
                        
                        # Carrozzeria auto (lati visibili)
                        self.canvas_3d.create_polygon(cx1, cy1, cx5, cy5, cx6, cy6, cx2, cy2, 
                                                     fill="#3366CC", outline="#000000")
                        self.canvas_3d.create_polygon(cx2, cy2, cx6, cy6, cx7, cy7, cx3, cy3, 
                                                     fill="#3366CC", outline="#000000")
                        
                        # Tetto auto
                        tetto_perc = 0.6  # Percentuale del tetto rispetto alla base
                        tetto_x_start = car_x_start + (car_width * (1 - tetto_perc) / 2)
                        tetto_y_start = car_y_start + (car_length * (1 - tetto_perc) / 2)
                        tetto_width = car_width * tetto_perc
                        tetto_length = car_length * tetto_perc
                        
                        tx1, ty1 = iso(tetto_x_start, tetto_y_start, car_height)
                        tx2, ty2 = iso(tetto_x_start + tetto_width, tetto_y_start, car_height)
                        tx3, ty3 = iso(tetto_x_start + tetto_width, tetto_y_start + tetto_length, car_height)
                        tx4, ty4 = iso(tetto_x_start, tetto_y_start + tetto_length, car_height)
                        
                        self.canvas_3d.create_polygon(tx1, ty1, tx2, ty2, tx3, ty3, tx4, ty4, 
                                                     fill="#000033", outline="#000000")
            else:  # doppia fila
                # Calcola quante auto per fila
                file = math.ceil(num_posti_auto / 2)
                fila1 = min(file, num_posti_auto)
                fila2 = max(0, num_posti_auto - fila1)
                
                # Prima fila
                for i in range(fila1):
                    x_start = i * self.posto_auto_larghezza
                    y_start = 0
                    x_end = x_start + self.posto_auto_larghezza
                    y_end = y_start + self.posto_auto_lunghezza
                    
                    # Posto auto
                    x1, y1 = iso(x_start, y_start, 1)
                    x2, y2 = iso(x_end, y_start, 1)
                    x3, y3 = iso(x_end, y_end, 1)
                    x4, y4 = iso(x_start, y_end, 1)
                    self.canvas_3d.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                                 fill="#DDDDDD", outline="#999999")
                    
                    # Silhouette auto semplificata
                    if self.posto_auto_larghezza > 150 and self.posto_auto_lunghezza > 300:
                        car_x_start = x_start + 25
                        car_y_start = y_start + 50
                        car_width = self.posto_auto_larghezza - 50
                        car_length = self.posto_auto_lunghezza - 100
                        car_height = 120
                        
                        # Corpo auto
                        cx1, cy1 = iso(car_x_start, car_y_start, 1)
                        cx2, cy2 = iso(car_x_start + car_width, car_y_start, 1)
                        cx3, cy3 = iso(car_x_start + car_width, car_y_start + car_length, 1)
                        cx4, cy4 = iso(car_x_start, car_y_start + car_length, 1)
                        cx5, cy5 = iso(car_x_start, car_y_start, car_height)
                        cx6, cy6 = iso(car_x_start + car_width, car_y_start, car_height)
                        cx7, cy7 = iso(car_x_start + car_width, car_y_start + car_length, car_height)
                        cx8, cy8 = iso(car_x_start, car_y_start + car_length, car_height)
                        
                        # Carrozzeria auto (lati visibili)
                        self.canvas_3d.create_polygon(cx1, cy1, cx5, cy5, cx6, cy6, cx2, cy2, 
                                                     fill="#CC3366", outline="#000000")
                        self.canvas_3d.create_polygon(cx2, cy2, cx6, cy6, cx7, cy7, cx3, cy3, 
                                                     fill="#CC3366", outline="#000000")
                
                # Seconda fila
                for i in range(fila2):
                    x_start = i * self.posto_auto_larghezza
                    y_start = self.posto_auto_lunghezza
                    x_end = x_start + self.posto_auto_larghezza
                    y_end = y_start + self.posto_auto_lunghezza
                    
                    # Posto auto
                    x1, y1 = iso(x_start, y_start, 1)
                    x2, y2 = iso(x_end, y_start, 1)
                    x3, y3 = iso(x_end, y_end, 1)
                    x4, y4 = iso(x_start, y_end, 1)
                    self.canvas_3d.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                                 fill="#DDDDDD", outline="#999999")
                    
                    # Silhouette auto semplificata
                    if self.posto_auto_larghezza > 150 and self.posto_auto_lunghezza > 300:
                        car_x_start = x_start + 25
                        car_y_start = y_start + 50
                        car_width = self.posto_auto_larghezza - 50
                        car_length = self.posto_auto_lunghezza - 100
                        car_height = 120
                        
                        # Corpo auto
                        cx1, cy1 = iso(car_x_start, car_y_start, 1)
                        cx2, cy2 = iso(car_x_start + car_width, car_y_start, 1)
                        cx3, cy3 = iso(car_x_start + car_width, car_y_start + car_length, 1)
                        cx4, cy4 = iso(car_x_start, car_y_start + car_length, 1)
                        cx5, cy5 = iso(car_x_start, car_y_start, car_height)
                        cx6, cy6 = iso(car_x_start + car_width, car_y_start, car_height)
                        cx7, cy7 = iso(car_x_start + car_width, car_y_start + car_length, car_height)
                        cx8, cy8 = iso(car_x_start, car_y_start + car_length, car_height)
                        
                        # Carrozzeria auto (lati visibili)
                        self.canvas_3d.create_polygon(cx1, cy1, cx5, cy5, cx6, cy6, cx2, cy2, 
                                                     fill="#66CC33", outline="#000000")
                        self.canvas_3d.create_polygon(cx2, cy2, cx6, cy6, cx7, cy7, cx3, cy3, 
                                                     fill="#66CC33", outline="#000000")
        
        # Aggiungi una legenda o etichette
        legend_x = 20
        legend_y = canvas_height - 100
        self.canvas_3d.create_text(legend_x, legend_y, 
                                  text=f"Altezza: {altezza} cm", 
                                  anchor=tk.W, font=("Arial", 10), fill="#000000")
        self.canvas_3d.create_text(legend_x, legend_y + 20, 
                                  text=f"Pannelli fotovoltaici: {num_pannelli}", 
                                  anchor=tk.W, font=("Arial", 10), fill="#000000")
        self.canvas_3d.create_text(legend_x, legend_y + 40, 
                                  text=f"Posti auto: {num_posti_auto}", 
                                  anchor=tk.W, font=("Arial", 10), fill="#000000")import tkinter as tk
from tkinter import ttk, messagebox
import math
import colorsys

class TettoiaCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Colori
        self.color_bg = "#FFFFF0"  # Bianco avorio
        self.color_accent = "#FFA500"  # Arancione
        self.color_text = "#000000"  # Nero
        self.color_input_bg = "#FFFFFF"  # Bianco per gli input
        
        # Dimensioni standard dei pannelli fotovoltaici (in cm)
        self.pannello_larghezza = 120
        self.pannello_altezza = 60
        
        # Parametri costruttivi
        self.distanza_max_pali = 400  # Distanza massima tra pali (in cm)
        self.distanza_max_traverse = 200  # Distanza massima tra traverse (in cm)
        self.altezza_min_tettoia = 220  # Altezza minima della tettoia (in cm)
        
        # Dimensioni standard posto auto
        self.posto_auto_larghezza = 250  # Larghezza di un posto auto (in cm)
        self.posto_auto_lunghezza = 500  # Lunghezza di un posto auto (in cm)
        
        self.setup_ui()
        
    def setup_ui(self):
        self.title("Calcolatrice Tettoie Fotovoltaiche")
        self.geometry("800x600")
        self.configure(bg=self.color_bg)
        
        # Stile
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background=self.color_bg)
        style.configure('TLabel', background=self.color_bg, foreground=self.color_text, font=('Arial', 12))
        style.configure('TButton', background=self.color_accent, foreground=self.color_text, font=('Arial', 12, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 18, 'bold'))
        style.configure('Result.TLabel', font=('Arial', 14), background=self.color_bg)
        style.configure('Orange.TFrame', background=self.color_accent)
        
        # Container principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titolo
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Dimensionamento Tettoie Fotovoltaiche", style='Header.TLabel').pack()
        
        # Frame per input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Frame arancione decorativo
        orange_frame = ttk.Frame(input_frame, style='Orange.TFrame')
        orange_frame.pack(fill=tk.X, padx=10, pady=5, ipady=10)
        
        # Frame interno bianco per gli input
        inner_frame = ttk.Frame(orange_frame)
        inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Larghezza
        larghezza_frame = ttk.Frame(inner_frame)
        larghezza_frame.pack(fill=tk.X, pady=5)
        ttk.Label(larghezza_frame, text="Larghezza totale (cm):", width=20).pack(side=tk.LEFT)
        self.larghezza_var = tk.StringVar()
        larghezza_entry = ttk.Entry(larghezza_frame, textvariable=self.larghezza_var, width=15, background=self.color_input_bg)
        larghezza_entry.pack(side=tk.LEFT, padx=5)
        
        # Lunghezza
        lunghezza_frame = ttk.Frame(inner_frame)
        lunghezza_frame.pack(fill=tk.X, pady=5)
        ttk.Label(lunghezza_frame, text="Lunghezza totale (cm):", width=20).pack(side=tk.LEFT)
        self.lunghezza_var = tk.StringVar()
        lunghezza_entry = ttk.Entry(lunghezza_frame, textvariable=self.lunghezza_var, width=15, background=self.color_input_bg)
        lunghezza_entry.pack(side=tk.LEFT, padx=5)
        
        # Altezza
        altezza_frame = ttk.Frame(inner_frame)
        altezza_frame.pack(fill=tk.X, pady=5)
        ttk.Label(altezza_frame, text="Altezza desiderata (cm):", width=20).pack(side=tk.LEFT)
        self.altezza_var = tk.StringVar()
        altezza_entry = ttk.Entry(altezza_frame, textvariable=self.altezza_var, width=15, background=self.color_input_bg)
        altezza_entry.pack(side=tk.LEFT, padx=5)
        
        # Posti auto
        posti_auto_frame = ttk.Frame(inner_frame)
        posti_auto_frame.pack(fill=tk.X, pady=5)
        ttk.Label(posti_auto_frame, text="Numero di posti auto:", width=20).pack(side=tk.LEFT)
        self.posti_auto_var = tk.StringVar()
        self.posti_auto_var.set("1")  # Valore predefinito
        posti_auto_entry = ttk.Entry(posti_auto_frame, textvariable=self.posti_auto_var, width=15, background=self.color_input_bg)
        posti_auto_entry.pack(side=tk.LEFT, padx=5)
        
        # Disposizione posti auto
        disposizione_frame = ttk.Frame(inner_frame)
        disposizione_frame.pack(fill=tk.X, pady=5)
        ttk.Label(disposizione_frame, text="Disposizione:", width=20).pack(side=tk.LEFT)
        self.disposizione_var = tk.StringVar()
        self.disposizione_var.set("lineare")
        disposizione_combobox = ttk.Combobox(disposizione_frame, textvariable=self.disposizione_var, width=15, values=["lineare", "doppia fila"])
        disposizione_combobox.pack(side=tk.LEFT, padx=5)
        
        # Pulsante calcola
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        calcola_btn = ttk.Button(button_frame, text="Calcola", command=self.calcola)
        calcola_btn.pack(padx=10, pady=10)
        
        # Frame per risultati
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame arancione decorativo per risultati
        self.result_orange_frame = ttk.Frame(self.result_frame, style='Orange.TFrame')
        self.result_orange_frame.pack(fill=tk.X, padx=10, pady=5, ipady=10)
        
        # Frame interno per i risultati
        self.inner_result_frame = ttk.Frame(self.result_orange_frame)
        self.inner_result_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Labels per risultati
        self.num_pali_label = ttk.Label(self.inner_result_frame, text="Numero di pali verticali: ", style='Result.TLabel')
        self.num_pali_label.pack(anchor='w', pady=2)
        
        self.num_traverse_label = ttk.Label(self.inner_result_frame, text="Numero di traverse: ", style='Result.TLabel')
        self.num_traverse_label.pack(anchor='w', pady=2)
        
        self.num_supporti_label = ttk.Label(self.inner_result_frame, text="Numero di supporti per pannelli: ", style='Result.TLabel')
        self.num_supporti_label.pack(anchor='w', pady=2)
        
        self.num_pannelli_label = ttk.Label(self.inner_result_frame, text="Numero di pannelli fotovoltaici: ", style='Result.TLabel')
        self.num_pannelli_label.pack(anchor='w', pady=2)
        
        self.copertura_label = ttk.Label(self.inner_result_frame, text="Area coperta: ", style='Result.TLabel')
        self.copertura_label.pack(anchor='w', pady=2)
        
        self.posti_auto_label = ttk.Label(self.inner_result_frame, text="Dimensione consigliata per posti auto: ", style='Result.TLabel')
        self.posti_auto_label.pack(anchor='w', pady=2)
        
        self.efficienza_label = ttk.Label(self.inner_result_frame, text="Efficienza utilizzo spazio: ", style='Result.TLabel')
        self.efficienza_label.pack(anchor='w', pady=2)
        
        # Frame per visualizzazione layout
        self.layout_frame = ttk.Frame(main_frame)
        self.layout_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Crea notebook per differenti visualizzazioni
        self.tabs = ttk.Notebook(self.layout_frame)
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Tab per vista dall'alto
        self.tab_top = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_top, text="Vista dall'alto")
        self.canvas = tk.Canvas(self.tab_top, bg=self.color_input_bg, height=200)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Tab per vista 3D
        self.tab_3d = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_3d, text="Vista 3D")
        self.canvas_3d = tk.Canvas(self.tab_3d, bg=self.color_input_bg, height=300)
        self.canvas_3d.pack(fill=tk.BOTH, expand=True)
    
    def calcola(self):
        try:
            # Modalità di calcolo
            modalita = "dimensioni"  # Default: l'utente fornisce le dimensioni
            
            # Ottieni input
            try:
                larghezza = float(self.larghezza_var.get())
                lunghezza = float(self.lunghezza_var.get())
            except ValueError:
                # Se le dimensioni non sono specificate, prova a calcolare in base ai posti auto
                if self.posti_auto_var.get():
                    modalita = "posti_auto"
                else:
                    raise ValueError("Devi specificare le dimensioni o il numero di posti auto")
                    
            altezza = float(self.altezza_var.get())
            
            # Verifica l'altezza minima
            if altezza < self.altezza_min_tettoia:
                messagebox.showwarning("Attenzione", f"L'altezza minima consigliata è di {self.altezza_min_tettoia} cm.")
            
            # Se la modalità è basata sui posti auto, calcola dimensioni consigliate
            if modalita == "posti_auto":
                num_posti = int(self.posti_auto_var.get())
                disposizione = self.disposizione_var.get()
                
                if disposizione == "lineare":
                    # Posti auto in fila singola
                    larghezza = num_posti * self.posto_auto_larghezza
                    lunghezza = self.posto_auto_lunghezza
                    self.larghezza_var.set(str(larghezza))
                    self.lunghezza_var.set(str(lunghezza))
                else:  # doppia fila
                    # Posti auto in doppia fila
                    file = math.ceil(num_posti / 2)
                    larghezza = file * self.posto_auto_larghezza
                    lunghezza = 2 * self.posto_auto_lunghezza
                    self.larghezza_var.set(str(larghezza))
                    self.lunghezza_var.set(str(lunghezza))
            
            # Calcolo del numero di pali verticali
            num_pali_larghezza = math.ceil(larghezza / self.distanza_max_pali) + 1
            num_pali_lunghezza = math.ceil(lunghezza / self.distanza_max_pali) + 1
            num_pali = (num_pali_larghezza * 2) + ((num_pali_lunghezza - 2) * 2)
            
            # Calcolo del numero di traverse
            num_traverse_larghezza = math.ceil(larghezza / self.distanza_max_traverse)
            num_traverse = num_traverse_larghezza * (num_pali_lunghezza - 1)
            
            # Calcolo del numero di pannelli
            pannelli_larghezza = math.floor(larghezza / self.pannello_larghezza)
            pannelli_lunghezza = math.floor(lunghezza / self.pannello_altezza)
            num_pannelli = pannelli_larghezza * pannelli_lunghezza
            
            # Calcolo dei supporti per pannelli (2 supporti per pannello)
            num_supporti = num_pannelli * 2
            
            # Calcolo dell'area coperta
            area_coperta = num_pannelli * self.pannello_larghezza * self.pannello_altezza / 10000  # in metri quadri
            area_totale = larghezza * lunghezza / 10000  # in metri quadri
            
            # Calcolo dei posti auto che si possono ricavare
            if modalita == "dimensioni":
                disposizione = self.disposizione_var.get()
                if disposizione == "lineare":
                    posti_auto_possibili = math.floor(larghezza / self.posto_auto_larghezza)
                else:  # doppia fila
                    file = math.floor(larghezza / self.posto_auto_larghezza)
                    posti_auto_possibili = file * 2
                
                self.posti_auto_var.set(str(posti_auto_possibili))
            
            # Calcolo dell'efficienza di utilizzo dello spazio
            efficienza = (area_coperta / area_totale) * 100
            
            # Aggiorna le etichette dei risultati
            self.num_pali_label.config(text=f"Numero di pali verticali: {num_pali}")
            self.num_traverse_label.config(text=f"Numero di traverse: {num_traverse}")
            self.num_supporti_label.config(text=f"Numero di supporti per pannelli: {num_supporti}")
            self.num_pannelli_label.config(text=f"Numero di pannelli fotovoltaici: {num_pannelli}")
            self.copertura_label.config(text=f"Area coperta: {area_coperta:.2f} m² su {area_totale:.2f} m² totali")
            
            # Aggiorna informazioni sui posti auto
            self.posti_auto_label.config(text=f"Posti auto: {self.posti_auto_var.get()} ({self.disposizione_var.get()})")
            self.efficienza_label.config(text=f"Efficienza utilizzo spazio: {efficienza:.1f}%")
            
            # Disegna i layout
            self.disegna_layout(larghezza, lunghezza, num_pali_larghezza, num_pali_lunghezza, int(self.posti_auto_var.get()))
            self.disegna_vista_3d(larghezza, lunghezza, altezza, num_pali_larghezza, num_pali_lunghezza, num_pannelli, int(self.posti_auto_var.get()))
            
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi per tutte le dimensioni.")
    
    def disegna_layout(self, larghezza, lunghezza, num_pali_x, num_pali_y, num_posti_auto=0):
        # Pulisci il canvas
        self.canvas.delete("all")
        
        # Fattore di scala per adattare il disegno al canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        scala_x = (canvas_width - 40) / larghezza
        scala_y = (canvas_height - 40) / lunghezza
        scala = min(scala_x, scala_y)
        
        # Offset per centrare il disegno
        offset_x = (canvas_width - (larghezza * scala)) / 2
        offset_y = (canvas_height - (lunghezza * scala)) / 2
        
        # Disegna il perimetro
        self.canvas.create_rectangle(
            offset_x, offset_y,
            offset_x + larghezza * scala,
            offset_y + lunghezza * scala,
            outline=self.color_accent, width=2
        )
        
        # Disegna i pali verticali
        distanza_pali_x = larghezza / (num_pali_x - 1)
        distanza_pali_y = lunghezza / (num_pali_y - 1)
        
        raggio_palo = 5  # raggio del palo in pixel
        
        for i in range(num_pali_x):
            x = offset_x + (i * distanza_pali_x * scala)
            # Pali sul lato superiore
            y_top = offset_y
            self.canvas.create_oval(
                x - raggio_palo, y_top - raggio_palo,
                x + raggio_palo, y_top + raggio_palo,
                fill=self.color_accent, outline=self.color_accent
            )
            # Pali sul lato inferiore
            y_bottom = offset_y + (lunghezza * scala)
            self.canvas.create_oval(
                x - raggio_palo, y_bottom - raggio_palo,
                x + raggio_palo, y_bottom + raggio_palo,
                fill=self.color_accent, outline=self.color_accent
            )
        
        # Pali sui lati (esclusi gli angoli già disegnati)
        for j in range(1, num_pali_y - 1):
            y = offset_y + (j * distanza_pali_y * scala)
            # Pali sul lato sinistro
            x_left = offset_x
            self.canvas.create_oval(
                x_left - raggio_palo, y - raggio_palo,
                x_left + raggio_palo, y + raggio_palo,
                fill=self.color_accent, outline=self.color_accent
            )
            # Pali sul lato destro
            x_right = offset_x + (larghezza * scala)
            self.canvas.create_oval(
                x_right - raggio_palo, y - raggio_palo,
                x_right + raggio_palo, y + raggio_palo,
                fill=self.color_accent, outline=self.color_accent
            )
        
        # Disegna grigliato per pannelli
        pannelli_x = math.floor(larghezza / self.pannello_larghezza)
        pannelli_y = math.floor(lunghezza / self.pannello_altezza)
        
        for i in range(pannelli_x):
            for j in range(pannelli_y):
                x1 = offset_x + (i * self.pannello_larghezza * scala)
                y1 = offset_y + (j * self.pannello_altezza * scala)
                x2 = x1 + (self.pannello_larghezza * scala)
                y2 = y1 + (self.pannello_altezza * scala)
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="#AAAAAA", dash=(4, 4)
                )
        
        # Disegna i posti auto
        if num_posti_auto > 0:
            disposizione = self.disposizione_var.get()
            
            if disposizione == "lineare":
                # Posti auto in fila singola
                for i in range(num_posti_auto):
                    x1 = offset_x + (i * self.posto_auto_larghezza * scala)
                    y1 = offset_y + ((lunghezza - self.posto_auto_lunghezza) / 2) * scala
                    x2 = x1 + (self.posto_auto_larghezza * scala)
                    y2 = y1 + (self.posto_auto_lunghezza * scala)
                    
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="#0066CC", width=2
                    )
                    
                    # Aggiungi "A" per indicare l'auto
                    auto_x = (x1 + x2) / 2
                    auto_y = (y1 + y2) / 2
                    self.canvas.create_text(
                        auto_x, auto_y,
                        text="A",
                        fill="#0066CC",
                        font=("Arial", 12, "bold")
                    )
            else:  # doppia fila
                # Calcola quante auto per fila
                file = math.ceil(num_posti_auto / 2)
                fila1 = min(file, num_posti_auto)
                fila2 = max(0, num_posti_auto - fila1)
                
                # Prima fila
                for i in range(fila1):
                    x1 = offset_x + (i * self.posto_auto_larghezza * scala)
                    y1 = offset_y
                    x2 = x1 + (self.posto_auto_larghezza * scala)
                    y2 = y1 + (self.posto_auto_lunghezza * scala)
                    
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="#0066CC", width=2
                    )
                    
                    auto_x = (x1 + x2) / 2
                    auto_y = (y1 + y2) / 2
                    self.canvas.create_text(
                        auto_x, auto_y,
                        text="A",
                        fill="#0066CC",
                        font=("Arial", 12, "bold")
                    )
                
                # Seconda fila
                for i in range(fila2):
                    x1 = offset_x + (i * self.posto_auto_larghezza * scala)
                    y1 = offset_y + self.posto_auto_lunghezza * scala
                    x2 = x1 + (self.posto_auto_larghezza * scala)
                    y2 = y1 + (self.posto_auto_lunghezza * scala)
                    
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="#0066CC", width=2
                    )
                    
                    auto_x = (x1 + x2) / 2
                    auto_y = (y1 + y2) / 2
                    self.canvas.create_text(
                        auto_x, auto_y,
                        text="A",
                        fill="#0066CC",
                        font=("Arial", 12, "bold")
                    )

if __name__ == "__main__":
    app = TettoiaCalculator()
    app.mainloop()