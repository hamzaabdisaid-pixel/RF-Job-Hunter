# RF Job Hunter France

Tableau de bord de veille emploi RF, accessible sur téléphone.

## État réel au 15 octobre 2026
- Tableau de bord `index.html` créé, avec classement prioritaire 1–3 ans et autres offres.
- Les fiches actuellement présentes sont des résultats publics à revérifier. Certains liens mènent à des recherches Apec et non à des annonces individuelles.
- **Aucune collecte automatisée des quatre plateformes ni notification push autonome n'est encore opérationnelle.**
- Les postes à caractère civil non confirmé sont marqués « à vérifier ».

## Publier sur GitHub Pages
1. Le dépôt est privé. Sur un compte GitHub Free, aller dans Settings > General > Danger Zone > Change repository visibility > Public. **Attention : cela rend les fichiers du dépôt publics.**
2. Aller dans Settings > Pages > Build and deployment et sélectionner **GitHub Actions** comme source.
3. Ouvrir l'onglet Actions et lancer « Publish RF Job Hunter dashboard » si nécessaire.
4. Une fois le déploiement confirmé, visiter https://hamzaabdisaid-pixel.github.io/RF-Job-Hunter/

## Surveillance réelle à développer
Pour couvrir LinkedIn, Apec, Hellowork et Indeed, il faut connecter des sources autorisées (API, flux ou alertes), stocker les offres, vérifier l'expérience, dédupliquer et filtrer la défense. Les notifications automatiques nécessitent ensuite un service push et les autorisations Android. Aucun résultat ne doit être inventé.
