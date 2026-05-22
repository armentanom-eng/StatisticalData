import cloudscraper
from bs4 import BeautifulSoup
import csv
import os

def scarica_e_aggiorna():
    url = "https://www.superenalotto.net/"
    file_csv = 'storico_completo.csv'
    
    # Configuriamo il browser per sembrare un vero utente
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'firefox', 'platform': 'windows', 'desktop': True}
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    # Mappa per trasformare i mesi
    mesi_map = {
        'gennaio': 'gen', 'febbraio': 'feb', 'marzo': 'mar', 'aprile': 'apr',
        'maggio': 'mag', 'giugno': 'giu', 'luglio': 'lug', 'agosto': 'ago',
        'settembre': 'set', 'ottobre': 'ott', 'novembre': 'nov', 'dicembre': 'dic'
    }

    try:
        # Tentiamo il download con timeout esteso
        response = scraper.get(url, timeout=60, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. ESTRAZIONE DATA
        data_span = soup.find('span', class_='date')
        data_estrazione = "data-ignota"
        if data_span:
            testo = data_span.get_text(strip=True).lower()
            parti = testo.split()
            if len(parti) >= 3:
                giorno = parti[1].zfill(2)
                mese_full = parti[2]
                mese = mesi_map.get(mese_full, mese_full[:3])
                data_estrazione = f"{giorno}-{mese}"

        # 2. ESTRAZIONE NUMERI
        container = soup.find('ul', class_='balls')
        if not container:
            print("Errore: Container 'balls' non trovato.")
            return

        numeri = [li.get_text(strip=True) for li in container.find_all('li', class_=['ball', 'jolly', 'superstar'])]
        
        if len(numeri) != 8:
            print(f"Errore: Trovati {len(numeri)} elementi, attesi 8.")
            return

        riga_nuova = [data_estrazione] + numeri

        # 3. CONTROLLO DUPLICATI
        if os.path.exists(file_csv):
            with open(file_csv, 'r', encoding='utf-8') as f:
                reader = list(csv.reader(f, delimiter=';'))
                if reader and reader[-1] == riga_nuova:
                    print("Estrazione già presente. Nessuna modifica.")
                    return

        # 4. SCRITTURA SICURA (evita righe vuote e accodamenti errati)
        file_esiste = os.path.exists(file_csv) and os.path.getsize(file_csv) > 0
        
        with open(file_csv, 'a', newline='', encoding='utf-8') as f:
            if file_esiste:
                # Controlla se l'ultima riga finisce con a capo
                with open(file_csv, 'rb') as f_check:
                    f_check.seek(-1, os.SEEK_END)
                    if f_check.read(1) != b'\n':
                        f.write('\n')
            
            writer = csv.writer(f, delimiter=';')
            writer.writerow(riga_nuova)
            
        print(f"Salvataggio completato: {riga_nuova}")

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    scarica_e_aggiorna()