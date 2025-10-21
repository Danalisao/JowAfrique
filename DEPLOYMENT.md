# 🚀 Guide de Déploiement JowAfrique

## 📋 Prérequis

### Système
- **Node.js** 18+ et npm
- **Python** 3.8+ et pip
- **Git** pour cloner le repository

### Services externes
- **Clé API Gemini** : [Google AI Studio](https://aistudio.google.com/)
- **Compte Jow** : Pas de clé API requise (librairie officielle)

## 🔧 Installation

### 1. Cloner le repository
```bash
git clone https://github.com/votre-username/jowafrique.git
cd jowafrique
```

### 2. Configuration des variables d'environnement
```bash
# Copier le fichier d'exemple
cp backend/.env.example backend/.env

# Éditer le fichier .env
nano backend/.env
```

**Variables requises :**
```env
# Sécurité
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here

# Base de données
DB_PATH=jowafrique.db
DEBUG=False
```

### 3. Installation des dépendances

#### Backend
```bash
cd backend
pip install -r requirements.txt
cd ..
```

#### Frontend
```bash
cd frontend
npm install
cd ..
```

## 🏗️ Build et Démarrage

### Option 1 : Scripts automatisés

#### Linux/macOS
```bash
# Build
./scripts/build.sh

# Démarrage production
./scripts/start-prod.sh
```

#### Windows
```powershell
# Build
.\scripts\build.ps1

# Démarrage production
.\scripts\start-prod.ps1
```

### Option 2 : Manuel

#### Backend
```bash
cd backend
python api.py
```

#### Frontend (nouveau terminal)
```bash
cd frontend
npm run build
npm start
```

## 🐳 Déploiement avec Docker

### 1. Build et démarrage
```bash
# Build des images
docker-compose -f docker-compose.prod.yml build

# Démarrage des services
docker-compose -f docker-compose.prod.yml up -d
```

### 2. Vérification
```bash
# Statut des services
docker-compose -f docker-compose.prod.yml ps

# Logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 3. Arrêt
```bash
docker-compose -f docker-compose.prod.yml down
```

## 🌐 Accès à l'application

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:5000
- **Avec Nginx** : http://localhost (port 80)

## 📊 Monitoring

### Logs
```bash
# Logs backend
tail -f backend/logs/app.log

# Logs frontend
tail -f frontend/.next/logs

# Logs Docker
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Santé de l'application
```bash
# API Health
curl http://localhost:5000/api/plans

# Frontend Health
curl http://localhost:3000
```

## 🔒 Sécurité en Production

### 1. Variables d'environnement
- ✅ Utiliser des clés secrètes fortes
- ✅ Ne jamais commiter le fichier `.env`
- ✅ Utiliser un gestionnaire de secrets (HashiCorp Vault, AWS Secrets Manager)

### 2. Base de données
- ✅ Sauvegardes régulières
- ✅ Chiffrement des données sensibles
- ✅ Accès restreint

### 3. Réseau
- ✅ HTTPS obligatoire en production
- ✅ Firewall configuré
- ✅ Rate limiting activé

## 🚀 Déploiement Cloud

### Heroku
```bash
# Installation Heroku CLI
# Configuration des variables d'environnement
heroku config:set GEMINI_API_KEY=your-key
heroku config:set SECRET_KEY=your-secret

# Déploiement
git push heroku main
```

### AWS/GCP/Azure
- Utiliser les services de conteneurs (ECS, Cloud Run, Container Instances)
- Configurer un load balancer
- Utiliser une base de données managée
- Configurer le monitoring (CloudWatch, Stackdriver, Application Insights)

## 🔧 Maintenance

### Sauvegardes
```bash
# Base de données
cp backend/jowafrique.db backups/jowafrique-$(date +%Y%m%d).db

# Logs
tar -czf logs-$(date +%Y%m%d).tar.gz logs/
```

### Mises à jour
```bash
# Pull des dernières modifications
git pull origin main

# Rebuild
./scripts/build.sh

# Redémarrage
./scripts/start-prod.sh
```

## 🆘 Dépannage

### Problèmes courants

#### Backend ne démarre pas
```bash
# Vérifier les logs
tail -f backend/logs/app.log

# Vérifier les ports
netstat -tulpn | grep :5000

# Vérifier les dépendances
pip list | grep -E "(flask|google-generativeai|jow-api)"
```

#### Frontend ne se connecte pas à l'API
```bash
# Vérifier la configuration
cat frontend/.env.local

# Vérifier la connectivité
curl http://localhost:5000/api/plans
```

#### Images Jow ne s'affichent pas
- Vérifier la configuration CORS
- Vérifier les domaines autorisés dans `next.config.js`
- Vérifier la connectivité internet

## 📞 Support

- **Documentation** : [DOCUMENTATION.md](./DOCUMENTATION.md)
- **Issues** : [GitHub Issues](https://github.com/votre-username/jowafrique/issues)
- **Email** : support@jowafrique.com

---

**JowAfrique** - Planification de dîners intelligente pour l'Afrique 🇨🇲✨
