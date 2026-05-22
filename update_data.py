import requests
from bs4 import BeautifulSoup
import csv
import os

# Maschera per sembrare un browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def scarica_e_aggiorna():
    url = "https://www.superenalotto.net/"
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cerchiamo il contenitore delle palline che hai trovato nella foto
        container = soup.find('ul', class_='balls')
        
        if container:
            # Estraiamo il testo di ogni elemento 'li' dentro la lista
            numeri = [li.text.strip() for li in container.find_all('li')]
            
            print(f"Numeri trovati: {numeri}")
            
            # Scriviamo i dati nel CSV
            # 'a' sta per append (aggiunge in coda senza cancellare il vecchio)
            with open('storico_completo.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(numeri)
            
            print("Dati salvati nel CSV con successo!")
        else:
            print("Errore: Impossibile trovare la lista dei numeri (ul.balls) nella pagina.")
            exit(1)

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
        exit(1)

if __name__ == "__main__":
    scarica_e_aggiorna()