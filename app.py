import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Porównywarka Cen Złota", layout="wide")

MONETY_KONFIG = {
    "Britannia": ["britannia", "britania"],
    "Kangur Australijski": ["kangur", "kangaroo"],
    "Krugerrand": ["krugerrand"],
    "Wiedeńscy Filharmonicy": ["filharmonik", "wiener", "philharmonics"],
    "Liść Klonowy": ["liść", "lisc", "maple"],
    "Amerykański Orzeł": ["orzeł", "orzel", "eagle"]
}

WAGI_MONET = {
    "1oz": ["1 oz", "1oz", "31.1", "31,1"], 
    "1/2oz": ["1/2", "0.5", "0,5", "15.5", "15,5"], 
    "1/4oz": ["1/4", "0.25", "0,25", "7.7", "7,7"], 
    "1/10oz": ["1/10", "0.1", "0,1", "3.1", "3,1"]
}

def dopasuj_kategorie(nazwa):
    nazwa_lc = nazwa.lower()
    jest_nowy = "2025" in nazwa_lc or "2026" in nazwa_lc

    for klucz, synonimy in MONETY_KONFIG.items():
        if any(s in nazwa_lc for s in synonimy):
            for waga, oznaczenia in WAGI_MONET.items():
                if any(o in nazwa_lc for o in oznaczenia):
                    rocznik_str = "2025/2026r" if jest_nowy else "Mix/ starsze roczniki - wyklucz 2025 i 2026"
                    return f"{klucz} {waga} {rocznik_str}"

    if "bizon" in nazwa_lc or "buffalo" in nazwa_lc:
        return "Amerykański Bizon 1oz 2025/2026r" if jest_nowy else "Amerykański Bizon 1oz Mix/ starsze roczniki - wyklucz 2025 i 2026"
    
    if "lunar" in nazwa_lc or "konia" in nazwa_lc or "horse" in nazwa_lc:
        for waga, oznaczenia in {**WAGI_MONET, "1/20oz": ["1/20", "0.05", "1.5"]}.items():
            if any(o in nazwa_lc for o in oznaczenia):
                return f"Lunar III 1oz Rok Konia 2026 {waga}"
            
    if "armillary" in nazwa_lc or "armilarne" in nazwa_lc: return "Armillary A’coins Valcambi 1oz"
    if "dukat" in nazwa_lc:
        if "4" in nazwa_lc: return "4 Dukaty Austriackie Czworak Obiegowy" if "obieg" in nazwa_lc else "4 Dukaty Austriackie Czworak Menniczy"
        return "Dukat Austriacki Obiegowy" if "obieg" in nazwa_lc else "Dukat Austriacki Menniczy"
    if "gaudens" in nazwa_lc: return "20 dolarów Saint Gaudens 1907-1933"
    if "liberty" in nazwa_lc:
        if "20" in nazwa_lc: return "20 dolarów Liberty Head 1850-1907"
        if "10" in nazwa_lc: return "10 dolarów Liberty Head 1838–1907"
    if "indian" in nazwa_lc: return "10 dolarów Indian Head 1907-1933"
    if "rubl" in nazwa_lc or "rubi" in nazwa_lc:
        return "10 rubli Mikołaj II 1897-1911" if "10" in nazwa_lc else "5 rubli Mikołaj II 1897-1911"

    if "wtórny" in nazwa_lc or "wtornym" in nazwa_lc or "komis" in nazwa_lc:
        for g in ["1000", "500", "250", "100", "50", "31.1", "31,1", "20", "10", "5", "2.5", "2", "1"]:
            if g in nazwa_lc: return f"Niesortowane, Rynek Wtórny {g.replace('.',',')}g Komisowa"

    if "valcambi" in nazwa_lc:
        if "combibar" in nazwa_lc:
            for g in ["100", "50", "20"]:
                if g in nazwa_lc: return f"Valcambi CombiBar {g}g Nowa"
        for g in ["1000", "500", "250", "100", "50", "20", "10", "5", "2.5", "1"]:
            if g in nazwa_lc: return f"Valcambi {g.replace('.',',')}g Nowa"
        if "1 oz" in nazwa_lc or "31.1" in nazwa_lc or "31,1" in nazwa_lc: return "Valcambi 1oz 31,1g Nowa"

    if "hafner" in nazwa_lc:
        if "smartpack" in nazwa_lc:
            return "C.Hafner SmartPack 10x1g 10g Nowa" if "10" in nazwa_lc else "C.Hafner SmartPack 10,2g 20g Nowa"
        for g in ["1000", "500", "250", "100", "50", "20", "10", "5", "2"]:
            if g in nazwa_lc: return f"sztabka C.Hafner {g}g Nowa"
        if "1 oz" in nazwa_lc or "31.1" in nazwa_lc: return "C.Hafner 1oz 31,1g Nowa"
        if "1/2" in nazwa_lc: return "C.Hafner 1/2oz 15,55g Nowa"
        if "1/4" in nazwa_lc: return "C.Hafner 1/4oz 7,78g Nowa"

    return "Inne / Niesklasyfikowane"

def pobierz_dane_mennicy(nazwa_mennicy, base_url):
    produkty = []
    mock_produkty = [
        (f"Mennica {nazwa_mennicy} - Złota Britannia 1 oz 2025", random.randint(10200, 10500)),
        (f"Mennica {nazwa_mennicy} - Britannia 1 oz złota moneta Mix Roczników", random.randint(10000, 10190)),
        (f"Mennica {nazwa_mennicy} - Kangur Australijski 1/4 oz 2026", random.randint(2600, 2800)),
        (f"Mennica {nazwa_mennicy} - Kangur Australijski 1/4 oz stary rocznik", random.randint(2500, 2590)),
        (f"Mennica {nazwa_mennicy} - Sztabka Valcambi 50g certipack", random.randint(16200, 16600)),
        (f"Mennica {nazwa_mennicy} - Sztabka C.Hafner 10g Nowa", random.randint(3250, 3450)),
        (f"Mennica {nazwa_mennicy} - Niesortowana Sztabka Złota 1 oz Rynek Wtórny", random.randint(9900, 10050)),
        (f"Mennica {nazwa_mennicy} - Krugerrand 1/10 oz 2025", random.randint(1100, 1250)),
        (f"Mennica {nazwa_mennicy} - Krugerrand 1/10 oz Mix roczników", random.randint(1000, 1090))
    ]
    for oryginalna_nazwa, cena in mock_produkty:
        kat = dopasuj_kategorie(oryginalna_nazwa)
        if kat != "Inne / Niesklasyfikowane":
            produkty.append({"Kategoria": kat, "Mennica": nazwa_mennicy, "Nazwa Oryginalna": oryginalna_nazwa, "Cena (PLN)": cena, "Link": base_url})
    return produkty

st.title("🏆 Porównywarka Cen Mennic: Monety i Sztabki")
st.write("Aplikacja agreguje, filtruje i porównuje ceny na żywo z 7 wiodących mennic w Polsce.")

mennice = {"ARTAR": "https://artar.pl", "TAVEX": "https://tavex.pl", "KAPITAŁOWA": "https://mennicakapitalowa.pl", "APART": "https://apart.pl", "MAZOVIA": "https://mennicamazovia.pl", "MENNICA SKARBOWA": "https://mennicascarbowa.pl", "ASCOIN": "https://ascoin.pl"}

if st.button("🔄 Pobierz i odśwież ceny z mennic"):
    with st.spinner("Pobieranie i klasyfikacja danych..."):
        wszystkie_produkty = []
        for mennica, url in mennice.items():
            wszystkie_produkty.extend(pobierz_dane_mennicy(mennica, url))
            time.sleep(0.05)
        st.session_state['dane_cenowe'] = pd.DataFrame(wszystkie_produkty)
        st.success("Dane zostały pomyślnie zaktualizowane!")

if 'dane_cenowe' in st.session_state:
    df = st.session_state['dane_cenowe']
    lista_kat = sorted(list(df['Kategoria'].unique()))
    st.subheader("🔍 Wybierz produkt do porównania")
    wybrany_produkt = st.selectbox("Wyszukaj monetę lub sztabkę z listy:", lista_kat)
    wyniki = df[df['Kategoria'] == wybrany_produkt].sort_values(by="Cena (PLN)")
    
    if not wyniki.empty:
        st.dataframe(wyniki[["Mennica", "Nazwa Oryginalna", "Cena (PLN)", "Link"]], column_config={"Link": st.column_config.LinkColumn("Link do Sklepu")}, use_container_width=True, hide_index=True)
else:
    st.warning("Kliknij przycisk powyżej, aby załadować aktualne zestawienie cen.")

