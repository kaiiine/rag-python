import re

def clean_text(text):
    """
    Nettoie le texte extrait du PDF pour améliorer la qualité des embeddings
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Supprimer les caractères de contrôle et les caractères non imprimables
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Normaliser les espaces multiples en un seul espace
    text = re.sub(r'\s+', ' ', text)
    
    # Supprimer les tirets de césure en fin de ligne
    text = re.sub(r'-\s*\n\s*', '', text)
    
    # Supprimer les sauts de ligne multiples
    text = re.sub(r'\n\s*\n', '\n', text)
    if re.match(r'^\s*\d+\s*$', text.strip()):
        return ""
    
    # Supprimer les en-têtes et pieds de page récurrents (ajustable selon vos PDFs)
    text = re.sub(r'^\s*page\s+\d+.*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Supprimer les URLs et emails pour éviter le bruit
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    
    # Nettoyer les caractères spéciaux répétés
    text = re.sub(r'[^\w\s\.,;:!?()[\]{}"\'-]+', ' ', text)
    
    # Supprimer les espaces en début et fin
    text = text.strip()
    
    # Retourner vide si le texte est trop court après nettoyage
    if len(text) < 10:
        return ""
    
    return text