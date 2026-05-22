import cloudscraper
from bs4 import BeautifulSoup
import csv
import os
import locale
from datetime import datetime

def scarica_e_aggiorna():
    # Imposta la lingua italiana
    try:
        locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
    except locale.Error:
        pass

    url = "https://www.superenalotto.net/"
    scraper = cloudscraper.create_scraper()
    file_csv = 'storico_completo.csv'
    
    try:
        # 1. Scarica la pagina
        response = scraper.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        container = soup.find('ul', class_='balls')
        if not container:
            print("Nessun container trovato.")
            return

        # 2. Estrai i numeri (6 + 1 Jolly + 1 Superstar)
        numeri = [li.get_text(strip=True) for li in container.find_all('li', class_=['ball', 'jolly', 'superstar'])]
        
        if len(numeri) != 8:
            print(f"Dati non completi (trovati {len(numeri)}).")
            return

        data_oggi = datetime.now().strftime('%d-%b').lower()
        riga_nuova = [data_oggi] + numeri
        
        # 3. Lettura "pulita" del CSV esistente
        righe_esistenti = []
        if os.path.exists(file_csv):
            with open(file_csv, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                # Ignoriamo le righe vuote filtrando i dati
                righe_esistenti = [row for row in reader if any(row)]

        # 4. Controllo duplicati
        if righe_esistenti:
            ultima_riga = righe_esistenti[-1]
            if riga_nuova == ultima_riga:
                print("Estrazione già presente. Nessuna scrittura.")
                return

        # 5. Scrittura (newline='' è fondamentale per evitare righe vuote extra)
        with open(file_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(riga_nuova)
        
        print("Riga scritta correttamente senza righe vuote.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    scarica_e_aggiorna()