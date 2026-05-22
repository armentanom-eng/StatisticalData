import cloudscraper
from bs4 import BeautifulSoup
import csv
import os

def scarica_e_aggiorna():
    url = "https://www.superenalotto.net/"
    scraper = cloudscraper.create_scraper()
    
    # Nome del file
    file_csv = 'storico_completo.csv'
    
    try:
        # 1. Scarica la pagina
        response = scraper.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Cerca il contenitore
        container = soup.find('ul', class_='balls')
        
        if not container:
            print("Nessuna estrazione trovata (container non presente). Nessuna scrittura eseguita.")
            return # Esce senza fare nulla

        # 3. Estrai i numeri (6 + 1 Jolly + 1 Superstar)
        # Cerchiamo le classi specifiche
        numeri = [li.get_text(strip=True) for li in container.find_all('li', class_=['ball', 'jolly', 'superstar'])]
        
        # Validazione: devono esserci esattamente 8 elementi
        if len(numeri) != 8:
            print(f"Estratti {len(numeri)} elementi, ma ne servono 8. Dati incompleti, nessuna scrittura.")
            return

        print(f"Numeri rilevati: {numeri}")

        # 4. Controllo duplicati rispetto all'ultima riga
        ultima_riga = []
        if os.path.exists(file_csv):
            with open(file_csv, 'r', encoding='utf-8') as f:
                reader = list(csv.reader(f))
                if reader:
                    ultima_riga = reader[-1] # Prende l'ultima riga del file

        # Se i numeri nuovi sono uguali agli ultimi salvati, non scriviamo
        if numeri == ultima_riga:
            print("Dati già presenti nel CSV. Nessuna nuova scrittura.")
            return

        # 5. Scrittura nuova riga
        with open(file_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(numeri)
        
        print("Nuova estrazione salvata correttamente nel CSV!")

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    scarica_e_aggiorna()