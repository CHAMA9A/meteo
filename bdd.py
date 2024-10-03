import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import requests
from mysql.connector import errorcode

class Database:
    def __init__(self):
        self.cnn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="api"
        )
        self.cursor = self.cnn.cursor()

    def close_connection(self):
        self.cursor.close()
        self.cnn.close()

    def authenticate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        user = self.cursor.fetchone()
        return user

    def register_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.cursor.execute(query, (username, password))
        self.cnn.commit()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Choisir une action")

        # Ajouter deux boutons pour choisir entre connexion et inscription
        self.btn_login = tk.Button(root, text="Se connecter", command=self.show_login)
        self.btn_register = tk.Button(root, text="S'inscrire", command=self.show_register)

        self.btn_login.pack(pady=20)
        self.btn_register.pack(pady=20)

    def clear_window(self):
        """Efface tous les widgets de la fenêtre"""
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def show_login(self):
        """Affiche l'interface de connexion"""
        self.clear_window()
        self.connexion_interface = ConnexionInterface(self.root, database, self.show_weather_app)
        
        # Bouton pour passer à l'inscription
        self.btn_to_register = tk.Button(self.root, text="Passer à l'inscription", command=self.show_register)
        self.btn_to_register.pack(pady=10)

    def show_register(self):
        """Affiche l'interface d'inscription"""
        self.clear_window()
        self.inscription_interface = InscriptionInterface(self.root, database, self.show_login)
        
        # Bouton pour passer à la connexion
        self.btn_to_login = tk.Button(self.root, text="Passer à la connexion", command=self.show_login)
        self.btn_to_login.pack(pady=10)

    def show_weather_app(self):
        """Affiche l'application météo après la connexion"""
        self.clear_window()
        weather_root = tk.Tk()
        weather_app = WeatherApp(weather_root)
        weather_root.mainloop()

class ConnexionInterface:
    def __init__(self, root, database, on_login_success):
        self.root = root
        self.database = database
        self.on_login_success = on_login_success
        self.root.title("Interface de Connexion")

        self.label_username = tk.Label(root, text="Nom d'utilisateur:")
        self.label_password = tk.Label(root, text="Mot de passe:")

        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()

        self.btn_login = tk.Button(root, text="Se connecter", command=self.login)
        self.btn_login.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        user = self.database.authenticate_user(username, password)

        if user:
            messagebox.showinfo("Connexion Réussie", "Bienvenue, {}".format(username))
            self.on_login_success()  # Rediriger vers l'application météo
            self.root.destroy()  # Fermer la fenêtre de connexion
        else:
            messagebox.showerror("Erreur de Connexion", "Nom d'utilisateur ou mot de passe incorrects")

class InscriptionInterface:
    def __init__(self, root, database, on_register_success):
        self.root = root
        self.database = database
        self.on_register_success = on_register_success
        self.root.title("Interface d'Inscription")

        self.label_username = tk.Label(root, text="Nom d'utilisateur:")
        self.label_password = tk.Label(root, text="Mot de passe:")

        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()

        self.btn_register = tk.Button(root, text="S'inscrire", command=self.register)
        self.btn_register.pack(pady=10)

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Vérifier si l'utilisateur existe déjà
        existing_user = self.database.authenticate_user(username, password)

        if existing_user:
            messagebox.showerror("Erreur d'Inscription", "Nom d'utilisateur déjà pris")
        else:
            # Enregistrer le nouvel utilisateur
            self.database.register_user(username, password)
            messagebox.showinfo("Inscription Réussie", "Bienvenue, {}! Vous êtes inscrit.".format(username))
            self.on_register_success()  # Rediriger vers la connexion

class WeatherApp:
    def __init__(self, root):
        try:
            self.cnn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="api",
            )
            print('Database connection successful')
            self.cursor = self.cnn.cursor()
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(e)

        self.root = root
        self.root.title("Weather Data App")

        # Labels
        self.city_label = tk.Label(root, text="City:")
        self.city_label.grid(row=0, column=0, padx=10, pady=10)

        # Entry for City
        self.city_entry = tk.Entry(root)
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)

        # Button to fetch weather data
        self.fetch_button = tk.Button(root, text="Fetch Weather", command=self.fetch_weather)
        self.fetch_button.grid(row=0, column=2, padx=10, pady=10)

        # Initialize variables
        self.weather_main = ""
        self.weather_description = ""
        self.temperature = 0
        self.humidity = 0
        self.wind_speed = 0
        self.timestamp = None

    def fetch_weather(self):
        CITY = self.city_entry.get()

        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        API_key = "29dbd531505e36f7ee10e4fc02a8b2be"
        url = f"{base_url}q={CITY}&appid={API_key}"
        response = requests.get(url).json()

        self.weather_main = response['weather'][0]['main']
        self.weather_description = response['weather'][0]['description']
        self.temperature = response['main']['temp']
        self.humidity = response['main']['humidity']
        self.wind_speed = response['wind']['speed']
        self.timestamp = datetime.fromtimestamp(response['dt'])

        messagebox.showinfo("Weather Data", f"Weather in {CITY}:\n"
                                            f"Main: {self.weather_main}\n"
                                            f"Description: {self.weather_description}\n"
                                            f"Temperature: {self.temperature}°C\n"
                                            f"Humidity: {self.humidity}%\n"
                                            f"Wind Speed: {self.wind_speed} m/s\n"
                                            f"Timestamp: {self.timestamp}")

        sql = "INSERT INTO weatherdata (city, weather_main, weather_description, temperature, humidity, wind_speed, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (CITY, self.weather_main, self.weather_description, self.temperature, self.humidity, self.wind_speed, self.timestamp)
        self.cursor.execute(sql, val)
        self.cnn.commit()

    def __del__(self):
        if hasattr(self, 'cnn'):
            if self.cnn.is_connected():
                self.cursor.close()
                self.cnn.close()

if __name__ == "__main__":
    root = tk.Tk()

    # Connexion à la base de données
    database = Database()

    # Interface principale
    main_app = MainApp(root)

    root.mainloop()

    # Fermer la connexion à la base de données à la fin du programme
    database.close_connection()
