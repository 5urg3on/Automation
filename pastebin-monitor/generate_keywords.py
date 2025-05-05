def generate_keywords(domains):
    keywords = set()
    for domain in domains:
        name = domain.split('.')[0]

        keywords.update({
            name,
            domain,
            domain.replace('.', ''),
            f"{name}@{domain}",
            f"contact@{domain}",
            f"support@{domain}",
            f"info@{domain}",
            f"{name}admin",
            f"{name}123"
        })
    
    return list(keywords)
