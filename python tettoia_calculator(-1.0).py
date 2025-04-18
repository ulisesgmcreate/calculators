import tkinter as tk
from tkinter import ttk, messagebox
import math

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
        
        # Fattori di zoom
        self.zoom_factor_top = 1.0
        self.zoom_factor_iso = 1.0
        
        # Dati dell'ultimo calcolo
        self.last_calc_data = None
        
        self.setup_ui()
        
    def setup_ui(self):
        self.title("Calcolatrice Tettoie Fotovoltaiche")
        self.geometry("800x700")  # Aumentata l'altezza per dare più spazio al canvas
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
        
        # Crea un notebook con due tabs
        self.tabs = ttk.Notebook(self.layout_frame)
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Tab per la vista dall'alto
        self.tab_top = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_top, text="Vista dall'alto")
        
        # Controlli di zoom per vista dall'alto
        zoom_frame_top = ttk.Frame(self.tab_top)
        zoom_frame_top.pack(fill=tk.X, pady=5)
        
        ttk.Label(zoom_frame_top, text="Zoom:").pack(side=tk.LEFT, padx=5)
        zoom_out_btn_top = ttk.Button(zoom_frame_top, text="-", width=3, command=lambda: self.adjust_zoom("top", -0.1))
        zoom_out_btn_top.pack(side=tk.LEFT, padx=2)
        
        self.zoom_factor_top_var = tk.StringVar()
        self.zoom_factor_top_var.set("1.0x")
        zoom_label_top = ttk.Label(zoom_frame_top, textvariable=self.zoom_factor_top_var, width=5)
        zoom_label_top.pack(side=tk.LEFT, padx=5)
        
        zoom_in_btn_top = ttk.Button(zoom_frame_top, text="+", width=3, command=lambda: self.adjust_zoom("top", 0.1))
        zoom_in_btn_top.pack(side=tk.LEFT, padx=2)
        
        reset_zoom_btn_top = ttk.Button(zoom_frame_top, text="Reset", width=6, command=lambda: self.reset_zoom("top"))
        reset_zoom_btn_top.pack(side=tk.LEFT, padx=10)
        
        # Canvas per vista dall'alto
        self.canvas = tk.Canvas(self.tab_top, bg=self.color_input_bg, height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Tab per la vista isometrica
        self.tab_iso = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_iso, text="Vista 3D")
        
        # Controlli di zoom per vista 3D
        zoom_frame_iso = ttk.Frame(self.tab_iso)
        zoom_frame_iso.pack(fill=tk.X, pady=5)
        
        ttk.Label(zoom_frame_iso, text="Zoom:").pack(side=tk.LEFT, padx=5)
        zoom_out_btn_iso = ttk.Button(zoom_frame_iso, text="-", width=3, command=lambda: self.adjust_zoom("iso", -0.1))
        zoom_out_btn_iso.pack(side=tk.LEFT, padx=2)
        
        self.zoom_factor_iso_var = tk.StringVar()
        self.zoom_factor_iso_var.set("1.0x")
        zoom_label_iso = ttk.Label(zoom_frame_iso, textvariable=self.zoom_factor_iso_var, width=5)
        zoom_label_iso.pack(side=tk.LEFT, padx=5)
        
        zoom_in_btn_iso = ttk.Button(zoom_frame_iso, text="+", width=3, command=lambda: self.adjust_zoom("iso", 0.1))
        zoom_in_btn_iso.pack(side=tk.LEFT, padx=2)
        
        reset_zoom_btn_iso = ttk.Button(zoom_frame_iso, text="Reset", width=6, command=lambda: self.reset_zoom("iso"))
        reset_zoom_btn_iso.pack(side=tk.LEFT, padx=10)
        
        # Canvas per vista 3D
        self.canvas_iso = tk.Canvas(self.tab_iso, bg=self.color_input_bg, height=350)
        self.canvas_iso.pack(fill=tk.BOTH, expand=True)
        
        # Inizializza un layout vuoto
        self.after(500, lambda: self.disegna_layout(500, 500, 2, 2, 1, 220, 0))
    
    def adjust_zoom(self, view_type, delta):
        """Regola il fattore di zoom per la vista specificata."""
        if view_type == "top":
            self.zoom_factor_top = max(0.5, min(5.0, self.zoom_factor_top + delta))
            self.zoom_factor_top_var.set(f"{self.zoom_factor_top:.1f}x")
            if self.last_calc_data:
                self.disegna_layout(
                    self.last_calc_data['larghezza'],
                    self.last_calc_data['lunghezza'],
                    self.last_calc_data['num_pali_x'],
                    self.last_calc_data['num_pali_y'],
                    self.last_calc_data['num_posti_auto'],
                    self.last_calc_data['altezza'],
                    self.last_calc_data['num_pannelli']
                )
        elif view_type == "iso":
            self.zoom_factor_iso = max(0.5, min(5.0, self.zoom_factor_iso + delta))
            self.zoom_factor_iso_var.set(f"{self.zoom_factor_iso:.1f}x")
            if self.last_calc_data:
                self.disegna_vista_isometrica(
                    self.last_calc_data['larghezza'],
                    self.last_calc_data['lunghezza'],
                    self.last_calc_data['altezza'],
                    self.last_calc_data['num_pali_x'],
                    self.last_calc_data['num_pali_y'],
                    self.last_calc_data['num_posti_auto'],
                    self.last_calc_data['num_pannelli']
                )
    
    def reset_zoom(self, view_type):
        """Reimposta il fattore di zoom al valore predefinito."""
        if view_type == "top":
            self.zoom_factor_top = 1.0
            self.zoom_factor_top_var.set("1.0x")
            if self.last_calc_data:
                self.disegna_layout(
                    self.last_calc_data['larghezza'],
                    self.last_calc_data['lunghezza'],
                    self.last_calc_data['num_pali_x'],
                    self.last_calc_data['num_pali_y'],
                    self.last_calc_data['num_posti_auto'],
                    self.last_calc_data['altezza'],
                    self.last_calc_data['num_pannelli']
                )
        elif view_type == "iso":
            self.zoom_factor_iso = 1.0
            self.zoom_factor_iso_var.set("1.0x")
            if self.last_calc_data:
                self.disegna_vista_isometrica(
                    self.last_calc_data['larghezza'],
                    self.last_calc_data['lunghezza'],
                    self.last_calc_data['altezza'],
                    self.last_calc_data['num_pali_x'],
                    self.last_calc_data['num_pali_y'],
                    self.last_calc_data['num_posti_auto'],
                    self.last_calc_data['num_pannelli']
                )
    
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
            
            # Salva i dati del calcolo per lo zoom
            self.last_calc_data = {
                'larghezza': larghezza,
                'lunghezza': lunghezza,
                'altezza': altezza,
                'num_pali_x': num_pali_larghezza,
                'num_pali_y': num_pali_lunghezza,
                'num_posti_auto': int(self.posti_auto_var.get()),
                'num_pannelli': num_pannelli
            }
            
            # Disegna il layout migliorato
            self.disegna_layout(larghezza, lunghezza, num_pali_larghezza, num_pali_lunghezza, 
                               int(self.posti_auto_var.get()), altezza, num_pannelli)
            
            # Disegna la vista isometrica
            self.disegna_vista_isometrica(larghezza, lunghezza, altezza, num_pali_larghezza, num_pali_lunghezza, 
                                         int(self.posti_auto_var.get()), num_pannelli)
            
            # Log dei calcoli (aiuta a verificare che funzioni)
            print(f"Calcolo completato: {larghezza}x{lunghezza} cm, {num_pannelli} pannelli")
            
        except ValueError as e:
            messagebox.showerror("Errore", str(e) if str(e) else "Inserisci valori numerici validi per tutte le dimensioni.")
    
    def disegna_layout(self, larghezza, lunghezza, num_pali_x, num_pali_y, num_posti_auto=0, altezza=220, num_pannelli=0):
        # Pulisci il canvas
        self.canvas.delete("all")
        
        # Fattore di scala per adattare il disegno al canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Se il canvas non è ancora disegnato, usa dimensioni predefinite
        if canvas_width < 10:
            canvas_width = 600
        if canvas_height < 10:
            canvas_height = 350
            
        scala_x = (canvas_width - 60) / larghezza
        scala_y = (canvas_height - 60) / lunghezza
        scala_base = min(scala_x, scala_y)
        
        # Applica il fattore di zoom
        scala = scala_base * self.zoom_factor_top
        
        # Offset per centrare il disegno
        offset_x = (canvas_width - (larghezza * scala)) / 2
        offset_y = (canvas_height - (lunghezza * scala)) / 2
        
        # Aggiungi un titolo al disegno
        self.canvas.create_text(
            canvas_width / 2, 15,
            text=f"Vista dall'alto - {larghezza/100:.1f}m x {lunghezza/100:.1f}m",
            font=("Arial", 12, "bold"),
            fill=self.color_accent
        )
        
        # Applica un leggero effetto prospettico (pseudo-3D)
        # Fattore di distorsione prospettica (più alto = più prospettiva)
        prospettiva = 0.2
        
        # Disegna prima l'ombra della tettoia (effetto 3D semplificato)
        shadow_offset = int(altezza * prospettiva / 5)  # Offset dell'ombra basato sull'altezza
        self.canvas.create_rectangle(
            offset_x + shadow_offset, offset_y + shadow_offset,
            offset_x + larghezza * scala + shadow_offset, offset_y + lunghezza * scala + shadow_offset,
            fill="#DDDDDD", outline=""
        )
        
        # Disegna il perimetro della tettoia
        self.canvas.create_rectangle(
            offset_x, offset_y,
            offset_x + larghezza * scala, offset_y + lunghezza * scala,
            fill="#F5F5F5", outline=self.color_accent, width=2
        )
        
        # Disegna i pali verticali
        distanza_pali_x = larghezza / (num_pali_x - 1) if num_pali_x > 1 else larghezza
        distanza_pali_y = lunghezza / (num_pali_y - 1) if num_pali_y > 1 else lunghezza
        
        raggio_palo = 5  # raggio del palo in pixel
        
        for i in range(num_pali_x):
            x = offset_x + (i * distanza_pali_x * scala)
            # Pali sul lato superiore
            y_top = offset_y
            # Ombra del palo
            self.canvas.create_oval(
                x - raggio_palo + 2, y_top - raggio_palo + 2,
                x + raggio_palo + 2, y_top + raggio_palo + 2,
                fill="#AAAAAA", outline=""
            )
            # Palo
            self.canvas.create_oval(
                x - raggio_palo, y_top - raggio_palo,
                x + raggio_palo, y_top + raggio_palo,
                fill=self.color_accent, outline=""
            )
            
            # Pali sul lato inferiore
            y_bottom = offset_y + (lunghezza * scala)
            # Ombra del palo
            self.canvas.create_oval(
                x - raggio_palo + 2, y_bottom - raggio_palo + 2,
                x + raggio_palo + 2, y_bottom + raggio_palo + 2,
                fill="#AAAAAA", outline=""
            )
            # Palo
            self.canvas.create_oval(
                x - raggio_palo, y_bottom - raggio_palo,
                x + raggio_palo, y_bottom + raggio_palo,
                fill=self.color_accent, outline=""
            )
        
        # Pali sui lati (esclusi gli angoli già disegnati)
        for j in range(1, num_pali_y - 1):
            y = offset_y + (j * distanza_pali_y * scala)
            # Pali sul lato sinistro
            x_left = offset_x
            # Ombra del palo
            self.canvas.create_oval(
                x_left - raggio_palo + 2, y - raggio_palo + 2,
                x_left + raggio_palo + 2, y + raggio_palo + 2,
                fill="#AAAAAA", outline=""
            )
            # Palo
            self.canvas.create_oval(
                x_left - raggio_palo, y - raggio_palo,
                x_left + raggio_palo, y + raggio_palo,
                fill=self.color_accent, outline=""
            )
            
            # Pali sul lato destro
            x_right = offset_x + (larghezza * scala)
            # Ombra del palo
            self.canvas.create_oval(
                x_right - raggio_palo + 2, y - raggio_palo + 2,
                x_right + raggio_palo + 2, y + raggio_palo + 2,
                fill="#AAAAAA", outline=""
            )
            # Palo
            self.canvas.create_oval(
                x_right - raggio_palo, y - raggio_palo,
                x_right + raggio_palo, y + raggio_palo,
                fill=self.color_accent, outline=""
            )
        
        # Disegna grigliato per pannelli con effetto 3D semplificato
        pannelli_x = math.floor(larghezza / self.pannello_larghezza)
        pannelli_y = math.floor(lunghezza / self.pannello_altezza)
        
        for i in range(pannelli_x):
            for j in range(pannelli_y):
                x1 = offset_x + (i * self.pannello_larghezza * scala)
                y1 = offset_y + (j * self.pannello_altezza * scala)
                x2 = x1 + (self.pannello_larghezza * scala)
                y2 = y1 + (self.pannello_altezza * scala)
                
                # Colore del pannello con leggero gradiente per effetto 3D
                panel_color = "#1E90FF"  # Blu fotovoltaico
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=panel_color, outline="#0000CD"
                )
                
                # Linee delle celle fotovoltaiche
                cell_width = (x2 - x1) / 3
                cell_height = (y2 - y1) / 2
                
                # Celle orizzontali
                for ci in range(1, 3):
                    self.canvas.create_line(
                        x1 + ci * cell_width, y1,
                        x1 + ci * cell_width, y2,
                        fill="#0000CD", width=1
                    )
                
                # Celle verticali
                self.canvas.create_line(
                    x1, y1 + cell_height,
                    x2, y1 + cell_height,
                    fill="#0000CD", width=1
                )
        
        # Disegna i posti auto con effetto 3D semplificato
        if num_posti_auto > 0:
            disposizione = self.disposizione_var.get()
            
            if disposizione == "lineare":
                # Posti auto in fila singola
                for i in range(num_posti_auto):
                    x1 = offset_x + (i * self.posto_auto_larghezza * scala)
                    y1 = offset_y + ((lunghezza - self.posto_auto_lunghezza) / 2) * scala
                    x2 = x1 + (self.posto_auto_larghezza * scala)
                    y2 = y1 + (self.posto_auto_lunghezza * scala)
                    
                    # Area parcheggio ombreggiata
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="#F0F0F0", outline="#0066CC", width=2
                    )
                    
                    # Disegna una semplice silhouette di auto dall'alto
                    car_width = self.posto_auto_larghezza * scala * 0.7
                    car_length = self.posto_auto_lunghezza * scala * 0.8
                    car_x1 = x1 + (self.posto_auto_larghezza * scala - car_width) / 2
                    car_y1 = y1 + (self.posto_auto_lunghezza * scala - car_length) / 2
                    car_x2 = car_x1 + car_width
                    car_y2 = car_y1 + car_length
                    
                    # Corpo auto
                    self.canvas.create_oval(
                        car_x1, car_y1, car_x2, car_y2,
                        fill="#3366CC", outline="#000000"
                    )
                    
                    # Numero posto auto
                    self.canvas.create_text(
                        x1 + 15, y1 + 15,
                        text=f"P{i+1}",
                        fill="#0066CC",
                        font=("Arial", 9, "bold"),
                        anchor="nw"
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
                    
                    # Area parcheggio ombreggiata
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="#F0F0F0", outline="#0066CC", width=2
                    )
                    
                    # Disegna una semplice silhouette di auto dall'alto
                    car_width = self.posto_auto_larghezza * scala * 0.7
                    car_length = self.posto_auto_lunghezza * scala * 0.8
                    car_x1 = x1 + (self.posto_auto_larghezza * scala - car_width) / 2
                    car_y1 = y1 + (self.posto_auto_lunghezza * scala - car_length) / 2
                    car_x2 = car_x1 + car_width
                    car_y2 = car_y1 + car_length
                    
                    # Corpo auto
                    self.canvas.create_oval(
                        car_x1, car_y1, car_x2, car_y2,
                        fill="#CC3366", outline="#000000"
                    )
                    
                    # Numero posto auto
                    self.canvas.create_text(
                        x1 + 15, y1 + 15,
                        text=f"P{i+1}",
                        fill="#0066CC",
                        font=("Arial", 9, "bold"),
                        anchor="nw"
                    )
                
                # Seconda fila
                for i in range(fila2):
                    x1 = offset_x + (i * self.posto_auto_larghezza * scala)
                    y1 = offset_y + self.posto_auto_lunghezza * scala
                    x2 = x1 + (self.posto_auto_larghezza * scala)
                    y2 = y1 + (self.posto_auto_lunghezza * scala)
                    
                    # Area parcheggio ombreggiata
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="#F0F0F0", outline="#0066CC", width=2
                    )
                    
                    # Disegna una semplice silhouette di auto dall'alto
                    car_width = self.posto_auto_larghezza * scala * 0.7
                    car_length = self.posto_auto_lunghezza * scala * 0.8
                    car_x1 = x1 + (self.posto_auto_larghezza * scala - car_width) / 2
                    car_y1 = y1 + (self.posto_auto_lunghezza * scala - car_length) / 2
                    car_x2 = car_x1 + car_width
                    car_y2 = car_y1 + car_length
                    
                    # Corpo auto
                    self.canvas.create_oval(
                        car_x1, car_y1, car_x2, car_y2,
                        fill="#66CC33", outline="#000000"
                    )
                    
                    # Numero posto auto
                    self.canvas.create_text(
                        x1 + 15, y1 + 15,
                        text=f"P{i+fila1+1}",
                        fill="#0066CC",
                        font=("Arial", 9, "bold"),
                        anchor="nw"
                    )
        
        # Aggiungi info sul progetto
        info_x = offset_x + 10
        info_y = offset_y + lunghezza * scala + 15
        
        self.canvas.create_text(
            info_x, info_y,
            text=f"Struttura: {num_pali_x}x{num_pali_y} pali, altezza {altezza} cm, {num_pannelli} pannelli",
            font=("Arial", 9),
            fill="#333333",
            anchor="nw"
        )
        
        # Aggiungi una legenda
        legend_x = offset_x + larghezza * scala - 150
        legend_y = offset_y + lunghezza * scala + 15
        
        self.canvas.create_rectangle(
            legend_x, legend_y,
            legend_x + 12, legend_y + 12,
            fill="#1E90FF", outline="#0000CD"
        )
        self.canvas.create_text(
            legend_x + 17, legend_y + 6,
            text="Pannelli fotovoltaici",
            font=("Arial", 9),
            fill="#333333",
            anchor="w"
        )
        
        # Aggiungi coordinate e scala
        self.canvas.create_line(
            offset_x, offset_y + lunghezza * scala + 40,
            offset_x + 100, offset_y + lunghezza * scala + 40,
            fill="#333333", width=2,
            arrow="both"
        )
        self.canvas.create_text(
            offset_x + 50, offset_y + lunghezza * scala + 45,
            text=f"{(100/scala):.0f} cm",
            font=("Arial", 9),
            fill="#333333"
        )
    
    def disegna_vista_isometrica(self, larghezza, lunghezza, altezza, num_pali_x, num_pali_y, num_posti_auto, num_pannelli):
        # Pulisci il canvas
        self.canvas_iso.delete("all")
        
        # Ottieni dimensioni del canvas
        canvas_width = self.canvas_iso.winfo_width()
        canvas_height = self.canvas_iso.winfo_height()
        
        # Se il canvas non è ancora disegnato, usa dimensioni predefinite
        if canvas_width < 10:
            canvas_width = 600
        if canvas_height < 10:
            canvas_height = 350
        
        # Parametri di proiezione isometrica
        angolo = 30  # gradi
        sin_a = math.sin(math.radians(angolo))
        cos_a = math.cos(math.radians(angolo))
        
        # Fattore di scala per adattare al canvas
        max_dim = max(larghezza, lunghezza, altezza)
        scala_base = min(canvas_width, canvas_height) * 0.4 / max_dim
        
        # Applica il fattore di zoom
        scala = scala_base * self.zoom_factor_iso
        
        # Offset per centrare il disegno
        offset_x = canvas_width * 0.5
        offset_y = canvas_height * 0.3
        
        # Funzione per convertire coordinate 3D in 2D con proiezione isometrica
        def iso(x, y, z):
            # Proiezione isometrica semplificata
            ix = offset_x + (x - y) * cos_a * scala
            iy = offset_y + (x + y) * sin_a * scala - z * scala
            return ix, iy
        
        # Aggiungi un titolo
        self.canvas_iso.create_text(
            canvas_width / 2, 15,
            text=f"Vista 3D - Dimensioni: {larghezza/100:.1f}m x {lunghezza/100:.1f}m x {altezza/100:.1f}m",
            font=("Arial", 12, "bold"),
            fill=self.color_accent
        )
        
        # Disegna il terreno (griglia)
        self.canvas_iso.create_polygon(
            iso(0, 0, 0),
            iso(larghezza, 0, 0),
            iso(larghezza, lunghezza, 0),
            iso(0, lunghezza, 0),
            fill="#E8E8E8", outline="#BBBBBB", width=1
        )
        
        # Disegna i pali verticali
        distanza_pali_x = larghezza / (num_pali_x - 1) if num_pali_x > 1 else larghezza
        distanza_pali_y = lunghezza / (num_pali_y - 1) if num_pali_y > 1 else lunghezza
        
        for i in range(num_pali_x):
            x = i * distanza_pali_x
            for j in range(num_pali_y):
                y = j * distanza_pali_y
                if (i == 0 or i == num_pali_x - 1 or j == 0 or j == num_pali_y - 1):  # Solo i pali perimetrali
                    # Disegna palo con facce visibili
                    palo_spessore = 10  # Spessore del palo
                    
                    # Faccia frontale del palo
                    self.canvas_iso.create_polygon(
                        iso(x - palo_spessore/2, y - palo_spessore/2, 0),
                        iso(x + palo_spessore/2, y - palo_spessore/2, 0),
                        iso(x + palo_spessore/2, y - palo_spessore/2, altezza),
                        iso(x - palo_spessore/2, y - palo_spessore/2, altezza),
                        fill=self.color_accent, outline="#000000", width=1
                    )
                    
                    # Faccia laterale del palo
                    self.canvas_iso.create_polygon(
                        iso(x + palo_spessore/2, y - palo_spessore/2, 0),
                        iso(x + palo_spessore/2, y + palo_spessore/2, 0),
                        iso(x + palo_spessore/2, y + palo_spessore/2, altezza),
                        iso(x + palo_spessore/2, y - palo_spessore/2, altezza),
                        fill="#E67E00", outline="#000000", width=1
                    )
                    
                    # Top del palo
                    self.canvas_iso.create_polygon(
                        iso(x - palo_spessore/2, y - palo_spessore/2, altezza),
                        iso(x + palo_spessore/2, y - palo_spessore/2, altezza),
                        iso(x + palo_spessore/2, y + palo_spessore/2, altezza),
                        iso(x - palo_spessore/2, y + palo_spessore/2, altezza),
                        fill="#FFB366", outline="#000000", width=1
                    )
        
        # Disegna le traverse orizzontali (struttura del tetto)
        traverse_spessore = 8
        
        # Traverse nel senso della larghezza
        for j in range(num_pali_y):
            y = j * distanza_pali_y
            if j == 0 or j == num_pali_y - 1:  # Solo le traverse sui lati esterni
                self.canvas_iso.create_polygon(
                    iso(0, y, altezza),
                    iso(larghezza, y, altezza),
                    iso(larghezza, y, altezza + traverse_spessore),
                    iso(0, y, altezza + traverse_spessore),
                    fill="#CD8500", outline="#000000", width=1
                )
        
        # Traverse nel senso della lunghezza
        for i in range(num_pali_x):
            x = i * distanza_pali_x
            if i == 0 or i == num_pali_x - 1:  # Solo le traverse sui lati esterni
                self.canvas_iso.create_polygon(
                    iso(x, 0, altezza),
                    iso(x, lunghezza, altezza),
                    iso(x, lunghezza, altezza + traverse_spessore),
                    iso(x, 0, altezza + traverse_spessore),
                    fill="#CD8500", outline="#000000", width=1
                )
        
        # Disegna il tetto (supporto per pannelli fotovoltaici)
        tetto_spessore = 5
        self.canvas_iso.create_polygon(
            iso(0, 0, altezza + traverse_spessore),
            iso(larghezza, 0, altezza + traverse_spessore),
            iso(larghezza, lunghezza, altezza + traverse_spessore),
            iso(0, lunghezza, altezza + traverse_spessore),
            fill="#D3D3D3", outline="#A9A9A9", width=1
        )
        
        # Disegna i pannelli fotovoltaici
        pannelli_larghezza = math.floor(larghezza / self.pannello_larghezza)
        pannelli_lunghezza = math.floor(lunghezza / self.pannello_altezza)
        pannello_spessore = 3
        
        for i in range(pannelli_larghezza):
            for j in range(pannelli_lunghezza):
                x_start = i * self.pannello_larghezza
                y_start = j * self.pannello_altezza
                x_end = x_start + self.pannello_larghezza
                y_end = y_start + self.pannello_altezza
                
                # Pannello solare 
                self.canvas_iso.create_polygon(
                    iso(x_start, y_start, altezza + traverse_spessore + tetto_spessore),
                    iso(x_end, y_start, altezza + traverse_spessore + tetto_spessore),
                    iso(x_end, y_end, altezza + traverse_spessore + tetto_spessore),
                    iso(x_start, y_end, altezza + traverse_spessore + tetto_spessore),
                    fill="#1E90FF", outline="#0000CD", width=1
                )
                
                # Lato del pannello (spessore)
                self.canvas_iso.create_polygon(
                    iso(x_start, y_start, altezza + traverse_spessore + tetto_spessore),
                    iso(x_start, y_end, altezza + traverse_spessore + tetto_spessore),
                    iso(x_start, y_end, altezza + traverse_spessore + tetto_spessore + pannello_spessore),
                    iso(x_start, y_start, altezza + traverse_spessore + tetto_spessore + pannello_spessore),
                    fill="#0000CD", outline="#000000", width=1
                )
                
                # Divisioni nelle celle fotovoltaiche
                cell_width = self.pannello_larghezza / 3
                cell_height = self.pannello_altezza / 2
                
                # Divisioni orizzontali
                for ci in range(1, 3):
                    x_cell = x_start + ci * cell_width
                    self.canvas_iso.create_line(
                        iso(x_cell, y_start, altezza + traverse_spessore + tetto_spessore + 0.1),
                        iso(x_cell, y_end, altezza + traverse_spessore + tetto_spessore + 0.1),
                        fill="#000099", width=1
                    )
                
                # Divisione verticale
                y_cell = y_start + cell_height
                self.canvas_iso.create_line(
                    iso(x_start, y_cell, altezza + traverse_spessore + tetto_spessore + 0.1),
                    iso(x_end, y_cell, altezza + traverse_spessore + tetto_spessore + 0.1),
                    fill="#000099", width=1
                )
        
        # Disegna i posti auto se specificati
        if num_posti_auto > 0:
            disposizione = self.disposizione_var.get()
            
            # Funzione per disegnare un'auto in prospettiva
            def disegna_auto(x_start, y_start, colore="#3366CC"):
                auto_larghezza = self.posto_auto_larghezza * 0.7
                auto_lunghezza = self.posto_auto_lunghezza * 0.8
                auto_altezza = 120
                
                # Posizione dell'auto centrata nel posto auto
                x_centro = x_start + (self.posto_auto_larghezza - auto_larghezza) / 2
                y_centro = y_start + (self.posto_auto_lunghezza - auto_lunghezza) / 2
                
                # Base dell'auto
                self.canvas_iso.create_polygon(
                    iso(x_centro, y_centro, 0),
                    iso(x_centro + auto_larghezza, y_centro, 0),
                    iso(x_centro + auto_larghezza, y_centro + auto_lunghezza, 0),
                    iso(x_centro, y_centro + auto_lunghezza, 0),
                    fill=colore, outline="#000000", width=1
                )
                
                # Corpo principale dell'auto
                body_height = auto_altezza * 0.5
                self.canvas_iso.create_polygon(
                    iso(x_centro, y_centro, 0),
                    iso(x_centro + auto_larghezza, y_centro, 0),
                    iso(x_centro + auto_larghezza, y_centro + auto_lunghezza, 0),
                    iso(x_centro, y_centro + auto_lunghezza, 0),
                    iso(x_centro, y_centro, body_height),
                    iso(x_centro + auto_larghezza, y_centro, body_height),
                    iso(x_centro + auto_larghezza, y_centro + auto_lunghezza, body_height),
                    iso(x_centro, y_centro + auto_lunghezza, body_height),
                    fill=colore, outline="#000000", width=1
                )
                
                # Finestrini - tetto dell'auto
                roof_x_inset = auto_larghezza * 0.15
                roof_y_inset = auto_lunghezza * 0.15
                self.canvas_iso.create_polygon(
                    iso(x_centro + roof_x_inset, y_centro + roof_y_inset, body_height),
                    iso(x_centro + auto_larghezza - roof_x_inset, y_centro + roof_y_inset, body_height),
                    iso(x_centro + auto_larghezza - roof_x_inset, y_centro + auto_lunghezza - roof_y_inset, body_height),
                    iso(x_centro + roof_x_inset, y_centro + auto_lunghezza - roof_y_inset, body_height),
                    iso(x_centro + roof_x_inset, y_centro + roof_y_inset, auto_altezza),
                    iso(x_centro + auto_larghezza - roof_x_inset, y_centro + roof_y_inset, auto_altezza),
                    iso(x_centro + auto_larghezza - roof_x_inset, y_centro + auto_lunghezza - roof_y_inset, auto_altezza),
                    iso(x_centro + roof_x_inset, y_centro + auto_lunghezza - roof_y_inset, auto_altezza),
                    fill="#111111", outline="#000000", width=1
                )
            
            if disposizione == "lineare":
                # Posti auto in fila singola
                for i in range(num_posti_auto):
                    x_start = i * self.posto_auto_larghezza
                    y_start = (lunghezza - self.posto_auto_lunghezza) / 2
                    
                    # Disegna delimitazioni del posto auto
                    self.canvas_iso.create_polygon(
                        iso(x_start, y_start, 0),
                        iso(x_start + self.posto_auto_larghezza, y_start, 0),
                        iso(x_start + self.posto_auto_larghezza, y_start + self.posto_auto_lunghezza, 0),
                        iso(x_start, y_start + self.posto_auto_lunghezza, 0),
                        fill="#F0F0F0", outline="#0066CC", width=1
                    )
                    
                    # Disegna l'auto
                    disegna_auto(x_start, y_start, "#3366CC")
                    
                    # Numero del posto auto
                    self.canvas_iso.create_text(
                        iso(x_start + 20, y_start + 20, 1),
                        text=f"P{i+1}",
                        fill="#0066CC",
                        font=("Arial", 9, "bold")
                    )
                    
            else:  # doppia fila
                # Calcola quante auto per fila
                file = math.ceil(num_posti_auto / 2)
                fila1 = min(file, num_posti_auto)
                fila2 = max(0, num_posti_auto - fila1)
                
                # Prima fila
                for i in range(fila1):
                    x_start = i * self.posto_auto_larghezza
                    y_start = 0
                    
                    # Delimitazioni posto auto
                    self.canvas_iso.create_polygon(
                        iso(x_start, y_start, 0),
                        iso(x_start + self.posto_auto_larghezza, y_start, 0),
                        iso(x_start + self.posto_auto_larghezza, y_start + self.posto_auto_lunghezza, 0),
                        iso(x_start, y_start + self.posto_auto_lunghezza, 0),
                        fill="#F0F0F0", outline="#0066CC", width=1
                    )
                    
                    # Auto
                    disegna_auto(x_start, y_start, "#CC3366")
                    
                    # Numero posto
                    self.canvas_iso.create_text(
                        iso(x_start + 20, y_start + 20, 1),
                        text=f"P{i+1}",
                        fill="#0066CC",
                        font=("Arial", 9, "bold")
                    )
                
                # Seconda fila
                for i in range(fila2):
                    x_start = i * self.posto_auto_larghezza
                    y_start = self.posto_auto_lunghezza
                    
                    # Delimitazioni posto auto
                    self.canvas_iso.create_polygon(
                        iso(x_start, y_start, 0),
                        iso(x_start + self.posto_auto_larghezza, y_start, 0),
                        iso(x_start + self.posto_auto_larghezza, y_start + self.posto_auto_lunghezza, 0),
                        iso(x_start, y_start + self.posto_auto_lunghezza, 0),
                        fill="#F0F0F0", outline="#0066CC", width=1
                    )
                    
                    # Auto
                    disegna_auto(x_start, y_start, "#66CC33")
                    
                    # Numero posto
                    self.canvas_iso.create_text(
                        iso(x_start + 20, y_start + 20, 1),
                        text=f"P{i+fila1+1}",
                        fill="#0066CC",
                        font=("Arial", 9, "bold")
                    )
        
        # Aggiungi info sul progetto
        info_y = canvas_height - 60
        
        self.canvas_iso.create_text(
            canvas_width / 2, info_y,
            text=f"Struttura: {num_pali_x}x{num_pali_y} pali, {num_pannelli} pannelli, {num_posti_auto} posti auto",
            font=("Arial", 10),
            fill="#333333"
        )
        self.canvas_iso.create_text(
            canvas_width / 2, info_y + 20,
            text=f"Dimensioni: {larghezza/100:.1f}m x {lunghezza/100:.1f}m x {altezza/100:.1f}m",
            font=("Arial", 10),
            fill="#333333"
        )

if __name__ == "__main__":
    app = TettoiaCalculator()
    app.mainloop()