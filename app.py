import streamlit as st
import pandas as pd
from datetime import datetime
import joblib
import time
day = datetime.now().weekday() # Donne un chiffre de 0 (lundi) à 6 (dimanche)

#Import sources model et features;
model = joblib.load('models/model_detection.joblib')
features= joblib.load('models/features_list.joblib')

st.subheader("Sentry🛡️Card Fraud detection ___ _ ")
st.divider()


profil_client= {
    "avg_amt":45,
    "avg_dist_km":3.2,
    "ecart_type_dist_habituel_km":2.2,
    "fav_categories":["food_dining","shopping_pos",
                      "health_fitness","gas_transport","misc_net"]}

#----------------------------------------------


#---LIGNE Montant------------------------------
# defintion des colonnes
col1, col2,col3 = st.columns([2, 2, 4]) #col3 est vide
col1.write("###### Montant:💵")
# On stocke la saisie dans une variable en passant par col2
user_montant = col2.text_input("Label1", placeholder="0.00", label_visibility="collapsed", key="input_montant")

try:
    if user_montant:
        amt = float(user_montant.replace(',', '.'))
    else:
        amt= 0.0
except ValueError:
    st.write("⚠️ Format invalide: chiffres attendus")
    amt = 0.0


#---LIGNE Heure---------------------------------
col4, col5,col6 = st.columns([2, 2, 4]) 
col4.write("###### Heure:🕒")
user_heure = col5.text_input("Label2", placeholder="ex : 10", label_visibility="collapsed", key="input_heure")

try:
    if user_heure:
        hour = int(user_heure)
        if not 0 <= hour <=23:
            st.write("⚠️ Format invalide: nombre entier entre 0 et 23")
    else:
        hour= 0
except ValueError:
    st.write("⚠️ Format invalide: nombre entier entre 0 et 23")
    hour = 0



# --- LIGNE Distance client / magasin -------------------------
col7, col8, col9 = st.columns([2, 2, 4])

col7.write("###### Distance Achat:🏠")

user_distance = col8.text_input( "Label_distance",placeholder=" Distance actuelle km",label_visibility="collapsed",key="input_distance"
)

try:
    if user_distance:
         dist_client_merch_km= float(user_distance.replace(',', '.'))
       
    else:
        dist_client_merch_km= 0
except ValueError:
    st.write("⚠️ Format invalide : nombre ")
    dist_client_merch_km = 0



# --- LIGNE Zone habituelle -------------------------
col10, col11, col12 = st.columns([2, 2, 4])

col10.write("###### Rayon Client:📍")

col11.write(
    f"Rayon habituel : {profil_client['avg_dist_km']} km")

col11.caption("")

#--------------------------------------------------
traduction_magasin = {
    "food_dining": "Restauration",
    "gas_transport": " Carburant",
    "grocery_net": "Epicerie_Web",
    "grocery_pos": "Courses alimentaires",
    "health_fitness": "Santé & Fitness",
    "home": " Ameublement",
    "kids_pets": "Famille & Animaux",
    "misc_net": "Services en ligne",
    "misc_pos": "Commerce  divers",
    "personal_care": "Beauté Santé",
    "shopping_net": "E-commerce",
    "shopping_pos": "Commerce de détail",
    "travel": "Voyage"
}

#---LIGNE Magasins--------------------------------------
categories_display = [
    "food_dining", "gas_transport", "grocery_net", "grocery_pos", 
    "health_fitness", "home", "kids_pets", "misc_net", 
    "misc_pos", "personal_care", "shopping_net", "shopping_pos", "travel"
]
col13, col14,col15 = st.columns([2, 2, 4]) 
col13.write("###### Enseigne:🏪")
user_magasin = col14.selectbox("Magasins",options=list(traduction_magasin.values()), label_visibility="collapsed", key="input_magasin")
#-------------------------------------------------------------


# variable utilise les valeur du dictionnaire 'client type'
dist_moyen_habitude =profil_client["avg_dist_km"]
moyenne_client = profil_client["avg_amt"] 


# reconstruction du ddataframe,  on calcule les ratios AVANT de remplir le DataFrame:

#Ratio distance compare la distance actuelle à la moyenne habituelle
if dist_moyen_habitude !=0:
    ratio_dist = dist_client_merch_km/ dist_moyen_habitude
else:
    ratio_dist =0.0                                                      # Sécurité : évite la division par zéro si le client n'a pas d'historique



#Ration de montant
if moyenne_client !=0:                                                   #Ce ratio permet au modèle d'évaluer l'anomalie du montant actuel
    ratio_amt_vs_client = amt / moyenne_client
else:
    ratio_amt_vs_client = 1.0                                           # CAS NOUVEAU CLIENT : Si la moyenne est inconnue (0), on fixe le ratio à 1.0


#-----------------------------------------------------------
#toutes le oolonnes du df sont a zero
df_features = pd.DataFrame(0, index=[0], columns=features)

#je recreer le dataframe :
df_features.loc[0,"amt"]= amt
df_features.loc[0,"hour"]= hour
df_features.loc[0, "day"] = day
df_features.loc[0,"dist_client_merch_km"]= dist_client_merch_km
df_features.loc[0,"dist_moyen_habitude"]= dist_moyen_habitude
df_features.loc[0, "ratio_distance"] = ratio_dist #  variable de calcu
df_features.loc[0, "ratio_amount_vs_client"] = ratio_amt_vs_client

#----------------------------------------------------------
#Definition d'un client type



# on remet les bon noms pour le modele
inverse_traduction = {v:k for k, v in traduction_magasin.items()}

#on récupere les transaction interface
transaction = {
    "amt": amt,
    "distance_km": dist_client_merch_km,
    "category": inverse_traduction[user_magasin]
}
#-------------------------------------------------


#fonction applique sur la transaction
def analyse_transaction(transaction, profil_client):
    alertes = []
    if transaction["amt"] > profil_client["avg_amt"] *3 :
        alertes.append("🔴Montant 3x supérieur aux habitudes du client.")

    if transaction["distance_km"]> profil_client["avg_dist_km"]*3:
        alertes.append("🟠Distance géographique inhabituelle.")

    if transaction["category"] not in profil_client["fav_categories"]:
        alertes.append("🟠Magasin rarement utilisé par ce client.")

  
    return alertes


#---------------------------------------------------------------------
#Je remets à 1 la colonne 'choisi par l'utilisateur on allumme l'interupteur(One-Hot Encoding)
colonnes_category =f"category_{transaction['category']}"
if colonnes_category in df_features.columns:
    df_features.loc[0, colonnes_category] = 1
#-----------------------------------------------------------------------

#creation bouton
col16, col17,col18 = st.columns([4,2,2]) 
if col16.button("⚡Sentry Check ", use_container_width=True):
    
    #alerte metier
    alertes = analyse_transaction(transaction, profil_client)
   
    if alertes:
   #regle métier
        for element in alertes:
            st.write(element)
    else:
        st.write("🟢 Pas de comportement inhabituel détecté.")        


    # Modèle ML
    proba_fraud = model.predict_proba(df_features)[0][1] ## predict_proba renvoie [proba_normal, proba_fraud]
    st.write(f"Probabilité de fraude : {proba_fraud:.2%}")

    current_ratio = df_features.loc[0, "ratio_distance"] ###################
    st.write(f"Ratio distance : {current_ratio:.2f}")
#--------


    # 1. Logique de décision
# 1. On définit les variables de décision
    
    if proba_fraud >= 0.75 or len(alertes)>=2 :
        verdict = "Transaction suspecte"
        icone = "🔴"
    elif proba_fraud >=0.65 or len(alertes) ==1:
        verdict = "A surveiller"
        icone = "🟠"
    else:
        verdict = "Transaction conforme"
        icone = "🟢"

    
    # 2. Affichage style "Alerte" (Standard Streamlit)
    col19, col20,col218 = st.columns([4,2,2]) 
    col19.info(f"{icone} {verdict}")


        #-----------------------

#st.write("🔧 Debug technique (colonnes envoyées) :", df_features[df_features > 0].dropna(axis=1))

#with st.expander("ℹ️ Comment cette analyse est faite ?"):
    #st.write("""
    #Le modèle analyse :
    #- le montant de la transaction
    #- l'heure
    #- la distance entre le client et le magasin
    #- les habitudes de déplacement
    #- le type de magasin

    #Il compare cette transaction à des milliers de cas passés
    #pour estimer si le comportement est habituel ou atypique.
   # """)


