import cloudscraper
from bs4 import BeautifulSoup
import csv

def scarica_e_aggiorna():
    url = "https://www.superenalotto.net/"
    # Cloudscraper crea una sessione che simula un browser reale in modo molto più efficace
    scraper = cloudscraper.create_scraper()
    
    try:
        # Il timeout di 30 secondi rimane
        response = scraper.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        container = soup.find('ul', class_='balls')
        
        if container:
            numeri = [li.text.strip() for li in container.find_all('li')]
            print(f"Numeri trovati: {numeri}")
            
            with open('storico_completo.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(numeri)
            print("Dati salvati con successo!")
        else:
            print("Errore: Impossibile trovare la lista dei numeri.")
            exit(1)

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
        exit(1)

if __name__ == "__main__":
    scarica_e_aggiorna()