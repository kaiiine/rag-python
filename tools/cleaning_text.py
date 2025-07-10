import re

def cleaning(text):
    """
    Nettoie un texte en préservant la structure utile (titres, montants, ponctuation)
    pour optimiser la compréhension par un LLM, en contexte juridique.
    """
    if not text or not isinstance(text, str):
        return ""

    # Supprimer les emojis et symboles Unicode très spécifiques (hors €)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symboles & pictos
        u"\U0001F680-\U0001F6FF"  # transport
        u"\U0001F1E0-\U0001F1FF"  # drapeaux
        u"\U00002702-\U000027B0"  # dingbats, flèches, etc.
        u"\U000024C2-\U0001F251"  # divers
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)

    # Supprimer les caractères de contrôle invisibles
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

    # Enlever les césures de mots sur retour à la ligne
    text = re.sub(r'-\s*\n\s*', '', text)

    # Nettoyage des sauts de ligne multiples
    text = re.sub(r'\n{2,}', '\n', text)

    # Supprimer les numéros de page ou headers classiques
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*page\s+\d+.*$', '', text, flags=re.IGNORECASE | re.MULTILINE)

    # Nettoyer les caractères spéciaux (mais conserver € % § et tirets)
    text = re.sub(r'[^\w\s.,;:!?(){}\[\]\'"«»€%§\-]', ' ', text)

    # Réduire les répétitions inutiles de ponctuation
    text = re.sub(r'([^\w\s])\1{2,}', r'\1', text)

    # Remplacer certaines puces de liste par un tiret standard
    text = re.sub(r'[•·▪‣]', '-', text)

    # Normaliser les espaces
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.replace('\xa0', ' ')

    # Normaliser les espaces avant/près des €
    text = re.sub(r'\s*€', ' €', text)  # force un espace avant €
    text = re.sub(r'€\s+', '€', text)   # supprime les espaces après €


    # Nettoyage ligne par ligne avec préservation des blocs
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()

        # Ajouter un saut de ligne après un "bloc-titre" très court et en majuscules
        if line.isupper() and len(line) < 60:
            cleaned_lines.append(line)
            cleaned_lines.append("")  # saut de ligne pour segmentation logique
        elif line and re.search(r'[a-zA-Z0-9]', line):
            cleaned_lines.append(line)

    cleaned_text = '\n'.join(cleaned_lines).strip()

    return cleaned_text if len(cleaned_text) >= 4 else ""
