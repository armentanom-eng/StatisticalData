import cloudscraper
from bs4 import BeautifulSoup
import csv
import os

def scarica_e_aggiorna():
    url = "https://www.superenalotto.net/"
    scraper = cloudscraper.create_scraper()
    file_csv = 'storico_completo.csv'
    
    # Dizionario per tradurre i mesi estesi in abbreviazioni
    mesi_map = {
        'gennaio': 'gen', 'febbraio': 'feb', 'marzo': 'mar', 'aprile': 'apr',
        'maggio': 'mag', 'giugno': 'giu', 'luglio': 'lug', 'agosto': 'ago',
        'settembre': 'set', 'ottobre': 'ott', 'novembre': 'nov', 'dicembre': 'dic'
    }

    try:
        response = scraper.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. ESTRAZIONE DATA
        # Cerchiamo lo span con classe 'date' come visto nello screenshot
        data_span = soup.find('span', class_='date')
        data_estrazione = "data-ignota"
        if data_span:
            # Esempio testo: "Giovedì 21 maggio 2026"
            testo = data_span.get_text(strip=True).lower()
            parti = testo.split() 
            # Dividiamo: ["giovedì", "21", "maggio", "2026"]
            if len(parti) >= 3:
                giorno = parti[1].zfill(2) # Forza 2 cifre (es: 01 invece di 1)
                mese_full = parti[2]
                mese = mesi_map.get(mese_full, mese_full[:3]) # Prende abbreviazione
                data_estrazione = f"{giorno}-{mese}"

        # 2. ESTRAZIONE NUMERI
        container = soup.find('ul', class_='balls')
        if not container:
            print("Nessun container trovato.")
            return

        # Estraiamo i 6 numeri + Jolly + Superstar
        numeri = [li.get_text(strip=True) for li in container.find_all('li', class_=['ball', 'jolly', 'superstar'])]
        
        if len(numeri) != 8:
            print(f"Dati non completi: trovati {len(numeri)} elementi.")
            return

        riga_nuova = [data_estrazione] + numeri

        # 3. SCRITTURA SICURA E PULITA
        # Leggiamo il file per verificare se è già presente l'estrazione
        if os.path.exists(file_csv):
            with open(file_csv, 'r', encoding='utf-8') as f:
                reader = list(csv.reader(f, delimiter=';'))
                if reader:
                    ultima_riga = reader[-1]
                    # Se l'ultima riga è identica (data + numeri), fermiamoci
                    if ultima_riga == riga_nuova:
                        print("Estrazione già aggiornata.")
                        return

        # 4. SCRITTURA
        # Verifichiamo se serve un "a capo" prima di scrivere
        file_esiste = os.path.exists(file_csv) and os.path.getsize(file_csv) > 0
        
        with open(file_csv, 'a', newline='', encoding='utf-8') as f:
            if file_esiste:
                # Controlliamo l'ultimo byte del file
                with open(file_csv, 'rb') as f_check:
                    f_check.seek(-1, os.SEEK_END)
                    if f_check.read(1) != b'\n':
                        f.write('\n') # Forza l'a capo se mancante
            
            writer = csv.writer(f, delimiter=';')
            writer.writerow(riga_nuova)
            
        print(f"Salvataggio effettuato: {riga_nuova}")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    scarica_e_aggiorna()