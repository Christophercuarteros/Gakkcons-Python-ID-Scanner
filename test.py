import tkinter as tk
from PIL import Image, ImageTk
import csv
import requests

class StudentLog:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Log")
        self.master.geometry("1280x720")  # Set window size to 1920x1080
        self.master.minsize(1280, 720)
        self.master.maxsize(1280, 720)
        self.frame = tk.Frame(self.master, bg="white")  # Set background color to white
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)  # Place the frame to fill the entire window
        self.slideshow_active = False
        self.create_first_page()

    def create_first_page(self):
        self.start_idleness_monitor()
        self.label_top = tk.Label(self.frame, text="Kindly Scan the QR Code in your ID", font=("Arial", 24), bg="white")
        self.label_top.place(x=400, y=60)  # Place the label at coordinates (500, 50)

        # Create the entry widget for user input with validation
        self.entry = tk.Entry(self.frame, width=40, validate="key")
        self.entry['validatecommand'] = (self.entry.register(self.validate_entry), '%d', '%i', '%S', '%P', '%s', '%v', '%V', '%W', '%e')
        self.entry.place(x=11500, y=80)  # Place the entry widget at coordinates (500, 80)
        
        # Bind keypress event to capture information
        self.entry.bind('<Return>', lambda event: self.capture_information(event))

        # Focus the entry widget so that the user can immediately start typing
        self.entry.focus_set()

        # Load and display an animated GIF image
        self.image_frames = []
        self.load_image_frames("qr-code.gif", 0)  # Load frames of the GIF
        self.current_frame = 0
        self.animate_gif()

        # bg image
        upper = Image.open("upper.png")
        upper =upper.resize((400, 300))
        photo = ImageTk.PhotoImage(upper)
        self.static_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.static_image_label.image = photo  
        self.static_image_label.place(x=930, y=0)

        lower = Image.open("lower.png")
        lower = lower.resize((400, 300))
        photo = ImageTk.PhotoImage(lower)
        self.lower_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.lower_image_label.image = photo
        self.lower_image_label.place(x=0, y=420)

        ustp = Image.open("ustp.png")
        ustp = ustp.resize((100, 100))
        photo = ImageTk.PhotoImage(ustp)
        self.upper_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.upper_image_label.image = photo  
        self.upper_image_label.place(x=20, y=10)
        
        dit = Image.open("dit.jpg")
        dit = dit.resize((100, 100))
        photo = ImageTk.PhotoImage(dit)
        self.dit_label = tk.Label(self.frame, image=photo, bg="blue", borderwidth= 1)
        self.dit_label.image = photo  
        self.dit_label.place(x=150, y=10)
        
        citc = Image.open("citc.jpg")
        citc = citc.resize((200, 100))
        photo = ImageTk.PhotoImage(citc)
        self.citc_label = tk.Label(self.frame, image=photo, bg="blue", borderwidth= 1)
        self.citc_label.image = photo  
        self.citc_label.place(x=1050, y=10)
        
    def start_idleness_monitor(self):
        self.idle_counter = 0
        self.frame.bind("<Motion>", self.reset_idleness_counter)
        self.check_idleness()
        print("Monitoring Started")

    def reset_idleness_counter(self, event):
        self.idle_counter = 0
    
    def stop_idleness_monitor(self):
        self.frame.unbind("<Motion>")
        self.check_idleness = lambda: None
        print("Monitoring is stopped")

    def check_idleness(self):   
        if self.slideshow_active:
            # Slideshow is active, stop idleasness monitoring
            self.idle_counter = 0
        else:
            # Slideshow is not active, continue idleness monitoring
            if self.idle_counter >= 50:  # Assuming 50 iterations equals to 5 seconds
                self.show_slideshow()
                self.idle_counter = 0
            else:
                self.idle_counter += 1
        self.master.after(100, self.check_idleness)

    def show_slideshow(self):
        # Create a Toplevel window for the slideshow
        self.slideshow_active = True 
        self.slideshow_window = tk.Toplevel(self.frame)
        self.slideshow_window.overrideredirect(True)  # Remove window decorations

        # Bind click event to close the slideshow when clicked
        self.slideshow_window.bind("<Button-1>", lambda event: self.close_slideshow())

        # Load images for the slideshow
        self.slideshow_images = []
        for i in range(1, 5):  # Assuming you have images named slide1.jpg, slide2.jpg, slide3.jpg
            image = Image.open(f"sample_{i}.png")
            image = image.resize((1280,720))
            photo = ImageTk.PhotoImage(image)
            self.slideshow_images.append(photo)

        # Create a label to display the images
        self.slideshow_label = tk.Label(self.slideshow_window, bg="white")
        self.slideshow_label.pack()

        # Show the first image
        self.current_slideshow_image = 0
        self.update_slideshow()

    def update_slideshow(self):
        self.slideshow_label.config(image=self.slideshow_images[self.current_slideshow_image])

        # Display the next image after 3 seconds
        self.current_slideshow_image += 1
        if self.current_slideshow_image >= len(self.slideshow_images):
            self.current_slideshow_image = 0
        self.slideshow_label.after(7000, self.update_slideshow)

    def close_slideshow(self):
        if self.slideshow_window:
            self.slideshow_window.destroy()
            self.idle_counter = 0
            self.slideshow_active = False  # Reset slideshow active flag

    def validate_entry(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name, event=None):
        if trigger_type in ('key', 'focusout') and action == '1':
            self.capture_information(event)
            return True
        else:
            return False

    def capture_information(self, event):
        try:
            input_text = self.entry.get()
            result = None

            for i in range(len(input_text)):
                if input_text[i].isdigit():
                    if i + 10 <= len(input_text) and input_text[i:i+10].isdigit():
                        result = input_text[i:i+10]
                        break
            # Validate student ID
            if len(result) == 10 and result.isdigit():
                # Print the student ID
                print("Student ID:", result)
                comparison_results = self.go_to_compare(result)
                # Hide the entry widget
                self.id_label = tk.Label(self.frame, text=f"Student ID = {result}")
                self.id_label.place(x=535, y=200)  # Adjusted coordinates to be visible
                self.id_label.configure(bg='white', fg='#FF0000', font=('Arial', 15))
                # Create and display the second page

                self.create_second_page(result, comparison_results)
            else:
                error_label = tk.Label(self.frame, text=f"INVALID QR CODE, PLEASE TRY AGAIN!")
                error_label.place(x=535, y=200)  # Adjusted coordinates to be visible
                self.frame.after(5000, error_label.destroy)  # Remove the error label after 5 seconds
                error_label.configure(bg='#white', fg='#FF0000', font=('Arial', 20))       
        except Exception as e:
            print(e)  
            
    def go_to_compare(self, result):
        csv_files = ['official_list_it_students.csv']
        # Initialize comparison_results as an empty string
        comparison_results = ""
        for csv_file in csv_files:
            with open(csv_file, 'r', encoding="latin-1") as file:
                csv_reader = csv.reader(file)
                
                # Skip header row
                next(csv_reader, None)

                for row in csv_reader:
                    # Assuming result is compared with the second column
                    if result == row[0]:
                        # Store result from the third column
                        comparison_results = row[1]
                        print(f"Match found in {csv_file}. Value of 3rd column: {row[2]}")
                        return comparison_results  # Stop searching if a match is found

        print(f"No match found in any CSV file.")
        return comparison_results
    
    def fetch_instructors(self):
        url = "https://student-log-web.onrender.com/get-instructors"  # Replace with your server address
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print("Failed to fetch instructors:", response.status_code)
                return None
        except Exception as e:
            print("Error fetching instructors:", e)
            return None

    def create_second_page(self, result, comparison_results):
        # Clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.stop_idleness_monitor()
        
        # bg image
        upper = Image.open("upper.png")
        upper =upper.resize((400, 300))
        photo = ImageTk.PhotoImage(upper)
        self.static_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.static_image_label.image = photo  
        self.static_image_label.place(x=900, y=0)

        lower = Image.open("lower.png")
        lower = lower.resize((400, 300))
        photo = ImageTk.PhotoImage(lower)
        self.lower_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.lower_image_label.image = photo
        self.lower_image_label.place(x=0, y=350)

        ustp = Image.open("ustp.png")
        ustp = ustp.resize((100, 100))
        photo = ImageTk.PhotoImage(ustp)
        self.upper_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.upper_image_label.image = photo  
        self.upper_image_label.place(x=20, y=10)
        
        dit = Image.open("dit.jpg")
        dit = dit.resize((100, 100))
        photo = ImageTk.PhotoImage(dit)
        self.dit_label = tk.Label(self.frame, image=photo, bg="blue", borderwidth= 1)
        self.dit_label.image = photo  
        self.dit_label.place(x=150, y=10)
        
        citc = Image.open("citc.jpg")
        citc = citc.resize((200, 100))
        photo = ImageTk.PhotoImage(citc)
        self.citc_label = tk.Label(self.frame, image=photo, bg="blue", borderwidth= 1)
        self.citc_label.image = photo  
        self.citc_label.place(x=1050, y=10)
        
        # Display result and comparison_results
        stud_id_label = tk.Label(self.frame, text=f"Student ID:", font=("Arial", 18, "bold"), bg="white")
        stud_id_label.place(x=300, y=180)
        
        self.stud_id_entry = tk.Entry(self.frame, width=40, font=("Arial", 18), validate="key")
        self.stud_id_entry.place(x=500, y=180)
        self.stud_id_entry.insert(0, result)
        self.stud_id_entry.config(state="disabled")
        
        name_entry_label = tk.Label(self.frame, text=f"Name:", font=("Arial", 18, "bold"), bg="white")
        name_entry_label.place(x=300, y=230)
        
        self.name_entry = tk.Entry(self.frame, width=40, font=("Arial", 18), validate="key")
        self.name_entry.place(x=500, y=230)

        if comparison_results:
            # Set the value of nameEntry to comparison_result
            self.name_entry.insert(0, comparison_results)
            # Disable the nameEntry widget
            self.name_entry.config(state="disabled")
        else:
            name = "STUDENT GUEST"
            self.name_entry.insert(0, name)
            # Disable the nameEntry widget
            self.name_entry.config(state="disabled")
        
        # Entry for purpose
        purpose_label = tk.Label(self.frame, text="Purpose:", font=("Arial", 18, "bold"), bg="white")
        purpose_label.place(x=300, y=280)
        
        self.purpose_entry = tk.Entry(self.frame, width=40, font=("Arial", 18), validate="key", bg="#eeeeee")
        self.purpose_entry.place(x=500, y=280)
        
        # Dropdown button for selecting instructor
        instructor_label = tk.Label(self.frame, text="Instructor:", font=("Arial", 18, "bold"), bg="white")
        instructor_label.place(x=300, y=330)
        
        # Fetch instructors data
        instructors_data = self.fetch_instructors()
        if instructors_data:
            instructor_options = [instructor['instructor_name'] for instructor in instructors_data]  # Extracting names from JSON data
        else:
            instructor_options = ["Babia, Jhon Harvey", "Baldelovar, Arlene", "Barbosa, Jocelyn", "Bernardo, John Benedict L.", "Blanco, Geraldine", "Calo, Al Monte Vince", "Chio, Ma. Esther", "Dal, Petal May M.", "Edo, Arnel", "Garrido, Jocelyn", "Haguisan, Rhea Suzette", "Llevado, Jomar", "Miñoza Jr., Dario", "Pachica, Archie",
"Raboy, Love Jhoye", "Rojo, Jay Noel", "Saledaien, Jc Vanny Mill", "Tamayo, Loredel", "Tong, Sigfred", "Uy, Ulrich Lee", "Vallar, Charlane", "Eder, Marilyn" "Esclamado, Maricel", "Landicho, Junar", "Ampolitod, Kenneth",]  # Default options if fetching fails

        self.instructor_var = tk.StringVar(self.frame)
        self.instructor_var.set("Select Instructor")
        self.instructor_dropdown = tk.OptionMenu(self.frame, self.instructor_var, *instructor_options)
        self.instructor_dropdown.place(x=500, y=330)
        

        # keyboard
        keyboard_overlay = tk.Canvas(self.frame, width=1200, height=280, bg='#222937', borderwidth=0,  highlightthickness=0)
        keyboard_overlay.place(x=35, y=425)   
        
        # exit button & submit button
        exit_button_image = Image.open("exitbutton.png")
        exit_button_image = exit_button_image.resize((150, 50))  
        exit_button_photo = ImageTk.PhotoImage(exit_button_image)
        exit_button = tk.Button(self.frame, image=exit_button_photo, command=self.go_to_first_page, borderwidth=0, highlightthickness=0, bg='#222937')
        exit_button.image = exit_button_photo
        exit_button.place(x=1080, y=640)

        submit_button_image = Image.open("submitbutton.png")
        submit_button_image = submit_button_image.resize((150, 50))  
        submit_button_photo = ImageTk.PhotoImage(submit_button_image)
        submit_button = tk.Button(self.frame, image=submit_button_photo, command=self.submit_data, borderwidth=0, highlightthickness=0, bg='#222937')
        submit_button.image = submit_button_photo
        submit_button.place(x=920, y=640)
        
        # Function to handle button clicks
        def button_click(number):
            current_text = self.purpose_entry.get()
            self.purpose_entry.insert(len(current_text), str(number))
            
        #
        q_button_path = "q.png"
        q_image = Image.open(q_button_path)
        q_image = q_image.resize((110, 50))
        q_image = ImageTk.PhotoImage(q_image)

        buttonQ = tk.Button(self.frame, image=q_image, borderwidth=0,  highlightthickness=0, command=lambda: button_click("Q"), bg="#222937", activebackground="#191851")
        buttonQ.image = q_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonQ.pack()
        buttonQ.place(x=40, y=460)

        #2 key
        w_button_path = "w.png"
        w_image = Image.open(w_button_path)
        w_image = w_image.resize((110, 50))
        w_image = ImageTk.PhotoImage(w_image)

        buttonW = tk.Button(self.frame, image=w_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("W"), bg="#222937", activebackground="#191851")
        buttonW.image = w_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonW.pack()
        buttonW.place(x=160, y=460)

        #3 key
        e_button_path = "e.png"
        e_image = Image.open(e_button_path)
        e_image = e_image.resize((110, 50))
        e_image = ImageTk.PhotoImage(e_image)

        buttonE = tk.Button(self.frame, image=e_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("E"), bg="#222937", activebackground="#191851")
        buttonE.image = e_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonE.pack()
        buttonE.place(x=280, y=460)

        #4 key
        r_button_path = "r.png"
        r_image = Image.open(r_button_path)
        r_image = r_image.resize((110, 50))
        r_image = ImageTk.PhotoImage(r_image)
    
        buttonR = tk.Button(self.frame, image=r_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("R"), bg="#222937", activebackground="#191851")
        buttonR.image = r_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonR.pack()
        buttonR.place(x=400, y=460)
    
        #5 key
        t_button_path = "t.png"
        t_image = Image.open(t_button_path)
        t_image = t_image.resize((110, 50))
        t_image = ImageTk.PhotoImage(t_image)
    
        buttonT = tk.Button(self.frame, image=t_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("T"), bg="#222937", activebackground="#191851")
        buttonT.image = t_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonT.pack()
        buttonT.place(x=520, y=460)
    
        #6 key
        y_button_path = "y.png"
        y_image = Image.open(y_button_path)
        y_image = y_image.resize((110, 50))
        y_image = ImageTk.PhotoImage(y_image)
    
        buttonY = tk.Button(self.frame, image=y_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("Y"), bg="#222937", activebackground="#191851")
        buttonY.image = y_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonY.pack()
        buttonY.place(x=640, y=460)
    
        #7 key
        u_button_path = "u.png"
        u_image = Image.open(u_button_path)
        u_image = u_image.resize((110, 50))
        u_image = ImageTk.PhotoImage(u_image)
    
        buttonU = tk.Button(self.frame, image=u_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("U"), bg="#222937", activebackground="#191851")
        buttonU.image = u_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonU.pack()
        buttonU.place(x=760, y=460)
    
        #8 key
        i_button_path = "i.png"
        i_image = Image.open(i_button_path)
        i_image = i_image.resize((110, 50))
        i_image = ImageTk.PhotoImage(i_image)
    
        buttonI = tk.Button(self.frame, image=i_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("I"), bg="#222937", activebackground="#191851")
        buttonI.image = i_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonI.pack()
        buttonI.place(x=880, y=460)
    
        #9 key
        o_button_path = "o.png"
        o_image = Image.open(o_button_path)
        o_image = o_image.resize((110, 50))
        o_image = ImageTk.PhotoImage(o_image)
    
        buttonO = tk.Button(self.frame, image=o_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("O"), bg="#222937", activebackground="#191851")
        buttonO.image = o_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonO.pack()
        buttonO.place(x=1000, y=460)
    
        #0 key
        p_button_path = "p.png"
        p_image = Image.open(p_button_path)
        p_image = p_image.resize((110, 50))
        p_image = ImageTk.PhotoImage(p_image)
    
        buttonP = tk.Button(self.frame, image=p_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("P"), bg="#222937", activebackground="#191851")
        buttonP.image = p_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonP.pack()
        buttonP.place(x=1120, y=460)
        #######################################################################################################################################
        #
        a_button_path = "a.png"
        a_image = Image.open(a_button_path)
        a_image = a_image.resize((110, 50))
        a_image = ImageTk.PhotoImage(a_image)
    
        buttonA = tk.Button(self.frame, image=a_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("A"), bg="#222937", activebackground="#191851")
        buttonA.image = a_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonA.pack()
        buttonA.place(x=100, y=520)
    
        #2 key
        s_button_path = "s.png"
        s_image = Image.open(s_button_path)
        s_image = s_image.resize((110, 50))
        s_image = ImageTk.PhotoImage(s_image)
    
        buttonS = tk.Button(self.frame, image=s_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("S"), bg="#222937", activebackground="#191851")
        buttonS.image = s_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonS.pack()
        buttonS.place(x=220, y=520)
    
        #3 key
        d_button_path = "d.png"
        d_image = Image.open(d_button_path)
        d_image = d_image.resize((110, 50))
        d_image = ImageTk.PhotoImage(d_image)
    
        buttonD = tk.Button(self.frame, image=d_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("D"), bg="#222937", activebackground="#191851")
        buttonD.image = d_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonD.pack()
        buttonD.place(x=340, y=520)
    
        #4 key
        f_button_path = "f.png"
        f_image = Image.open(f_button_path)
        f_image = f_image.resize((110, 50))
        f_image = ImageTk.PhotoImage(f_image)
    
        buttonF = tk.Button(self.frame, image=f_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("F"), bg="#222937", activebackground="#191851")
        buttonF.image = f_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonF.pack()
        buttonF.place(x=460, y=520)
    
        #5 key
        g_button_path = "g.png"
        g_image = Image.open(g_button_path)
        g_image = g_image.resize((110, 50))
        g_image = ImageTk.PhotoImage(g_image)
    
        buttonG = tk.Button(self.frame, image=g_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("G"), bg="#222937", activebackground="#191851")
        buttonG.image = g_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonG.pack()
        buttonG.place(x=580, y=520)
    
        #6 key
        h_button_path = "h.png"
        h_image = Image.open(h_button_path)
        h_image = h_image.resize((110, 50))
        h_image = ImageTk.PhotoImage(h_image)
    
        buttonH = tk.Button(self.frame, image=h_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("H"), bg="#222937", activebackground="#191851")
        buttonH.image = h_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonH.pack()
        buttonH.place(x=700, y=520)
    
        #7 key
        j_button_path = "j.png"
        j_image = Image.open(j_button_path)
        j_image = j_image.resize((110, 50))
        j_image = ImageTk.PhotoImage(j_image)
    
        buttonJ = tk.Button(self.frame, image=j_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("J"), bg="#222937", activebackground="#191851")
        buttonJ.image = j_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonJ.pack()
        buttonJ.place(x=820, y=520)
    
        #8 key
        k_button_path = "k.png"
        k_image = Image.open(k_button_path)
        k_image = k_image.resize((110, 50))
        k_image = ImageTk.PhotoImage(k_image)
    
        buttonK = tk.Button(self.frame, image=k_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("K"), bg="#222937", activebackground="#191851")
        buttonK.image = k_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonK.pack()
        buttonK.place(x=940, y=520)
    
        #9 key
        l_button_path = "l.png"
        l_image = Image.open(l_button_path)
        l_image = l_image.resize((110, 50))
        l_image = ImageTk.PhotoImage(l_image)
    
        buttonL = tk.Button(self.frame, image=l_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("L"), bg="#222937", activebackground="#191851")
        buttonL.image = l_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonL.pack()
        buttonL.place(x=1060, y=520)
        #######################################################################################################################################
    
        #3 key
        z_button_path = "z.png"
        z_image = Image.open(z_button_path)
        z_image = z_image.resize((110, 50))
        z_image = ImageTk.PhotoImage(z_image)
    
        buttonZ = tk.Button(self.frame, image=z_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("Z"), bg="#222937", activebackground="#191851")
        buttonZ.image = z_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonZ.pack()
        buttonZ.place(x=160, y=580)
    
        #4 key
        x_button_path = "x.png"
        x_image = Image.open(x_button_path)
        x_image = x_image.resize((110, 50))
        x_image = ImageTk.PhotoImage(x_image)
    
        buttonX = tk.Button(self.frame, image=x_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("X"), bg="#222937", activebackground="#191851")
        buttonX.image = x_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonX.pack()
        buttonX.place(x=280, y=580)
    
        #5 key
        c_button_path = "c.png"
        c_image = Image.open(c_button_path)
        c_image = c_image.resize((110, 50))
        c_image = ImageTk.PhotoImage(c_image)
    
        buttonC = tk.Button(self.frame, image=c_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("C"), bg="#222937", activebackground="#191851")
        buttonC.image = c_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonC.pack()
        buttonC.place(x=400, y=580)
    
        #6 key
        v_button_path = "v.png"
        v_image = Image.open(v_button_path)
        v_image = v_image.resize((110, 50))
        v_image = ImageTk.PhotoImage(v_image)
    
        buttonV = tk.Button(self.frame, image=v_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("V"), bg="#222937", activebackground="#191851")
        buttonV.image = v_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonV.pack()
        buttonV.place(x=520, y=580)
    
        #7 key
        b_button_path = "b.png"
        b_image = Image.open(b_button_path)
        b_image = b_image.resize((110, 50))
        b_image = ImageTk.PhotoImage(b_image)
    
        buttonB = tk.Button(self.frame, image=b_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("B"), bg="#222937", activebackground="#191851")
        buttonB.image = b_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonB.pack()
        buttonB.place(x=640, y=580)
    
        #8 key
        n_button_path = "n.png"
        n_image = Image.open(n_button_path)
        n_image = n_image.resize((110, 50))
        n_image = ImageTk.PhotoImage(n_image)
    
        buttonN = tk.Button(self.frame, image=n_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("N"), bg="#222937", activebackground="#191851")
        buttonN.image = n_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonN.pack()
        buttonN.place(x=760, y=580)
    
        #9 key
        m_button_path = "m.png"
        m_image = Image.open(m_button_path)
        m_image = m_image.resize((110, 50))
        m_image = ImageTk.PhotoImage(m_image)
    
        buttonM = tk.Button(self.frame, image=m_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("M"), bg="#222937", activebackground="#191851")
        buttonM.image = m_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonM.pack()
        buttonM.place(x=880, y=580)
        #######################################################################################################################################
    
        #delete button function
        def delete_button_command():
            current_text = self.purpose_entry.get()
            self.purpose_entry.delete(len(current_text) - 1)
    
        #Backspace Button
        backspace_button_path = "backspace.png"
        backspace_image = Image.open(backspace_button_path)
        backspace_image = backspace_image.resize((200, 50))
        backspace_image = ImageTk.PhotoImage(backspace_image)
    
        backspaceButton = tk.Button(self.frame, image=backspace_image, highlightthickness=0, borderwidth=0, command=delete_button_command, bg="#222937", activebackground="#191851")
        backspaceButton.image = backspace_image  # Keep a reference to the image to prevent it from being garbage collected
        backspaceButton.pack()
        backspaceButton.place(x=1000, y=580)
        #######################################################################################################################################
    
        #
        dash_button_path = "dash.png"
        dash_image = Image.open(dash_button_path)
        dash_image = dash_image.resize((110, 50))
        dash_image = ImageTk.PhotoImage(dash_image)
    
        buttonDash = tk.Button(self.frame, image=dash_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("-"), bg="#222937", activebackground="#191851")
        buttonDash.image = dash_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonDash.pack()
        buttonDash.place(x=40, y=640)
    
        #2 key
        comma_button_path = "comma.png"
        comma_image = Image.open(comma_button_path)
        comma_image = comma_image.resize((110, 50))
        comma_image = ImageTk.PhotoImage(comma_image)
    
        buttonComma = tk.Button(self.frame, image=comma_image, borderwidth=0, highlightthickness=0, command=lambda: button_click(","), bg="#222937", activebackground="#191851")
        buttonComma.image = comma_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonComma.pack()
        buttonComma.place(x=160, y=640)
    
        #3 key
        period_button_path = "period.png"
        period_image = Image.open(period_button_path)
        period_image = period_image.resize((110, 50))
        period_image = ImageTk.PhotoImage(period_image)
    
        buttonPeriod = tk.Button(self.frame, image=period_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("."), bg="#222937", activebackground="#191851")
        buttonPeriod.image = period_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonPeriod.pack()
        buttonPeriod.place(x=280, y=640)
    
        #4 key
        space_button_path = "space.png"
        space_image = Image.open(space_button_path)
        space_image = space_image.resize((380, 50))
        space_image = ImageTk.PhotoImage(space_image)
    
        buttonSpace = tk.Button(self.frame, image=space_image, borderwidth=0, highlightthickness=0, command=lambda: button_click(" "), bg="#222937", activebackground="#191851")
        buttonSpace.image = space_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonSpace.pack()
        buttonSpace.place(x=400, y=640)
    
        #5 key
        enye_button_path = "enye.png"
        enye_image = Image.open(enye_button_path)
        enye_image = enye_image.resize((110, 50))
        enye_image = ImageTk.PhotoImage(enye_image)
    
        buttonEnye = tk.Button(self.frame, image=enye_image, borderwidth=0, highlightthickness=0, command=lambda: button_click("Ñ"), bg="#222937", activebackground="#191851")
        buttonEnye.image = enye_image  # Keep a reference to the image to prevent it from being garbage collected
        buttonEnye.pack()
        buttonEnye.place(x=790, y=640)
        
    
    def submit_data(self):
        try:
            # Collect data from entry widgets and dropdown
            student_id = self.stud_id_entry.get()
            name = self.name_entry.get()
            purpose = self.purpose_entry.get()
            selected_instructor = self.instructor_var.get()
            
            # POST request to Node.js server
            # https://student-log-web.onrender.com
            node_server_url = 'submit_log'
            node_server_data = {
                'stud_num': student_id,
                'stud_name': name,
                'stud_purpose': purpose,
                'stud_instructor': selected_instructor,
                'stud_log_date': '',
                'stud_log_time': ''
            }
            requests.post(node_server_url, json=node_server_data, verify=False)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.go_to_last()
    
    def go_to_last(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
                # bg image
        upper = Image.open("upper.png")
        upper =upper.resize((400, 300))
        photo = ImageTk.PhotoImage(upper)
        self.static_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.static_image_label.image = photo  
        self.static_image_label.place(x=900, y=0)

        lower = Image.open("lower.png")
        lower = lower.resize((400, 300))
        photo = ImageTk.PhotoImage(lower)
        self.lower_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.lower_image_label.image = photo
        self.lower_image_label.place(x=0, y=420)

        ustp = Image.open("ustp.png")
        ustp = ustp.resize((100, 100))
        photo = ImageTk.PhotoImage(ustp)
        self.upper_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.upper_image_label.image = photo  
        self.upper_image_label.place(x=20, y=10)
        
        dit = Image.open("dit.jpg")
        dit = dit.resize((100, 100))
        photo = ImageTk.PhotoImage(dit)
        self.dit_label = tk.Label(self.frame, image=photo, bg="blue", borderwidth= 1)
        self.dit_label.image = photo  
        self.dit_label.place(x=150, y=10)
        
        citc = Image.open("citc.jpg")
        citc = citc.resize((200, 100))
        photo = ImageTk.PhotoImage(citc)
        self.citc_label = tk.Label(self.frame, image=photo, bg="blue", borderwidth= 1)
        self.citc_label.image = photo  
        self.citc_label.place(x=1050, y=10)
        
        statement = Image.open("statement.png")
        statement = statement.resize((650, 350))
        photo = ImageTk.PhotoImage(statement)
        self.upper_image_label = tk.Label(self.frame, image=photo, bg="white")
        self.upper_image_label.image = photo
        self.upper_image_label.place(x=320, y=200)
        
        # Schedule the go_to_first_page() function to be called after 5 seconds
        self.master.after(5000, self.go_to_first_page)
        
    def load_image_frames(self, filename, index):
        try:
            self.image = Image.open(filename)
            while True:
                self.image.seek(index)  # Go to the specified frame
                self.image_frames.append(ImageTk.PhotoImage(self.image.copy()))
                index += 1
        except EOFError:
            pass

    def animate_gif(self):
        self.label_image = tk.Label(self.frame, bg="white")
        self.label_image.place(x=330, y=140)  # Place the label at coordinates (430, 180)
        self.update_image()

    def update_image(self):
        self.label_image.config(image=self.image_frames[self.current_frame])
        
    def original_check_idleness(self):   
        if self.slideshow_active:
            # Slideshow is active, stop idleasness monitoring
            self.idle_counter = 0
        else:
            # Slideshow is not active, continue idleness monitoring
            if self.idle_counter >= 50:  # Assuming 50 iterations equals to 5 seconds
                self.show_slideshow()
                self.idle_counter = 0
            else:
                self.idle_counter += 1
        self.master.after(100, self.check_idleness)
        
    def go_to_first_page(self):
        # Destroy current widgets in the frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        # Recreate the first page
        self.check_idleness = self.original_check_idleness
        self.create_first_page()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentLog(root)
    root.mainloop()
