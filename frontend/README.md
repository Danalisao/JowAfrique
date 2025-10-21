# JowAfrique Frontend

Frontend Next.js responsive mobile-first pour l'application de planification de repas JowAfrique.

## 🚀 Fonctionnalités

- **Design Mobile-First** : Interface optimisée pour mobile avec possibilité de transformation en PWA
- **Thème Sombre** : Interface moderne avec thème sombre et accents verts
- **Navigation Intuitive** : Navigation par onglets en bas d'écran
- **Planification de Repas** : Interface pour planifier les repas de la semaine
- **Suivi de Progression** : Suivi en temps réel de la préparation des repas
- **Responsive Design** : Adaptation automatique à différentes tailles d'écran

## 🛠️ Technologies

- **Next.js 14** : Framework React avec App Router
- **TypeScript** : Typage statique
- **Tailwind CSS** : Framework CSS utility-first
- **Lucide React** : Icônes modernes
- **Framer Motion** : Animations fluides
- **PWA Ready** : Prêt pour installation mobile

## 📱 Écrans Implémentés

1. **Page Principale** : Accueil avec sélection de date et cartes de repas
2. **Page Scrollée** : Vue détaillée des repas planifiés
3. **Progression - Pré-cuisson** : Compte à rebours avant cuisson
4. **Progression - Cuisson** : Suivi de la cuisson en cours
5. **Progression - Livraison** : Suivi de la livraison avec carte

## 🚀 Installation

```bash
# Installer les dépendances
npm install

# Lancer en mode développement
npm run dev

# Build pour production
npm run build

# Lancer en production
npm start
```

## 📱 PWA

L'application est configurée comme Progressive Web App (PWA) :
- Installation sur mobile possible
- Mode hors-ligne basique
- Icônes adaptatives
- Thème sombre natif

## 🎨 Design System

### Couleurs
- **Primaire** : Vert (#22c55e)
- **Sombre** : Palette de gris foncés
- **Texte** : Blanc et gris clair

### Typographie
- **Police** : Inter (Google Fonts)
- **Hiérarchie** : Tailles et poids variés

### Composants
- **StatusBar** : Barre de statut mobile
- **BottomNavigation** : Navigation principale
- **MealCard** : Carte de repas
- **DatePicker** : Sélecteur de date
- **ProgressPage** : Page de progression

## 🔗 Intégration Backend

L'application est prête pour l'intégration avec le backend Python :
- API calls vers `/api/plans`
- Gestion des repas et favoris
- Synchronisation des données

## 📦 Structure

```
src/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx
│   └── manifest.json
├── components/
│   ├── StatusBar.tsx
│   ├── BottomNavigation.tsx
│   ├── MainPage.tsx
│   ├── DatePicker.tsx
│   ├── MealCard.tsx
│   └── ProgressPage.tsx
└── types/
    └── index.ts
```
