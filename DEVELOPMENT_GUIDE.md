# 🛠️ Guide de Développement - JowAfrique

## 🚀 Démarrage rapide

### Prérequis
- **Node.js** 18+ et npm
- **Python** 3.8+
- **Git**
- **VS Code** (recommandé)

### Installation
```bash
# Cloner le projet
git clone <repository-url>
cd JowAfrique

# Installer les dépendances
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### Démarrage en développement
```bash
# Terminal 1 - Backend
cd backend
python api.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## 🏗️ Architecture du code

### Backend (Flask)

#### Structure des fichiers
```
backend/
├── api.py                 # Point d'entrée API
├── database.py            # Gestionnaire de base de données
├── models.py              # Modèles de données
├── security.py            # Sécurité et validation
├── services/              # Logique métier
│   ├── meal_service.py    # Service des repas
│   └── plan_service.py    # Service des plans
└── requirements.txt       # Dépendances
```

#### Conventions de code
- **Nommage** : snake_case pour les fonctions et variables
- **Classes** : PascalCase
- **Constantes** : UPPER_CASE
- **Docstrings** : Format Google

#### Exemple de service
```python
class MealService:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add_meal(self, meal_data: Dict[str, Any]) -> int:
        """Ajoute un nouveau repas.
        
        Args:
            meal_data: Données du repas
            
        Returns:
            ID du repas créé
            
        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation
        if not meal_data.get('recipe_name'):
            raise ValueError("Le nom de la recette est requis")
        
        # Logique métier
        meal = Meal(
            id=None,
            recipe_name=meal_data['recipe_name'],
            # ...
        )
        return self.db.add_meal_to_plan(meal)
```

### Frontend (Next.js + TypeScript)

#### Structure des fichiers
```
frontend/src/
├── app/                   # Pages Next.js 13+
│   ├── layout.tsx         # Layout principal
│   └── page.tsx           # Page d'accueil
├── components/            # Composants React
│   ├── ui/                # Composants UI réutilisables
│   └── *.tsx              # Pages et composants
├── hooks/                 # Hooks personnalisés
├── lib/                   # Utilitaires
├── services/              # Services API
└── types/                 # Types TypeScript
```

#### Conventions de code
- **Nommage** : PascalCase pour les composants, camelCase pour les fonctions
- **Fichiers** : PascalCase pour les composants, camelCase pour les utilitaires
- **Types** : Interface avec préfixe I ou suffixe Type

#### Exemple de composant
```typescript
interface MealCardProps {
  meal: Meal;
  onToggleFavorite?: (mealId: number) => void;
  onRate?: (mealId: number, rating: number) => void;
  variant?: 'default' | 'compact' | 'featured';
}

export default function MealCard({ 
  meal, 
  onToggleFavorite, 
  onRate, 
  variant = 'default' 
}: MealCardProps) {
  const [isLoading, setIsLoading] = useState(false);
  
  const handleToggleFavorite = async () => {
    setIsLoading(true);
    try {
      await onToggleFavorite?.(meal.id);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="overflow-hidden">
      {/* Contenu du composant */}
    </Card>
  );
}
```

---

## 🗄️ Base de données

### Modèles de données

#### Meal
```python
@dataclass
class Meal:
    id: Optional[int]
    day_of_week: str
    meal_type: MealType
    recipe_name: str
    jow_recipe_id: Optional[str] = None
    jow_recipe_url: Optional[str] = None
    main_ingredient: Optional[str] = None
    cuisine_type: Optional[CuisineType] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    is_favorite: bool = False
    rating: int = 0
    notes: Optional[str] = None
    plan_id: Optional[int] = None
```

#### WeeklyPlan
```python
@dataclass
class WeeklyPlan:
    id: Optional[int]
    plan_name: str
    week_start_date: date
    total_budget_estimate: Optional[float] = None
    generated_by_ai: bool = True
    created_at: Optional[datetime] = None
```

### Migrations
Pour ajouter une nouvelle colonne :
1. Modifier le modèle dans `models.py`
2. Ajouter la migration dans `database.py`
3. Tester avec des données existantes

```python
# Exemple de migration
def add_new_column():
    with self.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            ALTER TABLE meal_slots 
            ADD COLUMN new_field TEXT
        """)
        conn.commit()
```

---

## 🧪 Tests

### Tests Backend

#### Structure des tests
```
backend/tests/
├── test_api.py            # Tests des endpoints
├── test_services.py        # Tests des services
├── test_database.py        # Tests de la base de données
└── conftest.py            # Configuration pytest
```

#### Exemple de test
```python
import pytest
from api import app
from database import DatabaseManager

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_plans(client):
    """Test de récupération des plans."""
    response = client.get('/api/plans')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_create_plan(client):
    """Test de création d'un plan."""
    plan_data = {
        'planName': 'Test Plan',
        'weekStartDate': '2024-01-15',
        'preferences': {
            'cuisines': ['cameroun'],
            'budget': 'modéré',
            'light': False,
            'vegetarian': False
        }
    }
    response = client.post('/api/plans', json=plan_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'id' in data
```

### Tests Frontend

#### Structure des tests
```
frontend/src/
├── __tests__/
│   ├── components/        # Tests des composants
│   ├── hooks/            # Tests des hooks
│   └── services/         # Tests des services
└── setupTests.ts         # Configuration Jest
```

#### Exemple de test
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import MealCard from '@/components/MealCard';

const mockMeal = {
  id: 1,
  name: 'Poulet DG',
  cuisine: 'cameroun',
  rating: 5,
  isFavorite: true
};

describe('MealCard', () => {
  it('affiche le nom du repas', () => {
    render(<MealCard meal={mockMeal} />);
    expect(screen.getByText('Poulet DG')).toBeInTheDocument();
  });

  it('appelle onToggleFavorite quand on clique sur le bouton favori', () => {
    const mockToggle = jest.fn();
    render(<MealCard meal={mockMeal} onToggleFavorite={mockToggle} />);
    
    const favoriteButton = screen.getByRole('button', { name: /favorite/i });
    fireEvent.click(favoriteButton);
    
    expect(mockToggle).toHaveBeenCalledWith(1);
  });
});
```

### Exécution des tests
```bash
# Backend
cd backend
python -m pytest tests/ -v

# Frontend
cd frontend
npm test
```

---

## 🔧 Configuration et environnement

### Variables d'environnement

#### Backend (.env)
```bash
# Base de données
DB_PATH=jowafrique.db
DB_BACKUP_PATH=backups/

# API
API_PORT=5000
API_HOST=0.0.0.0
DEBUG=True

# Sécurité
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Services externes
JOW_API_KEY=your-jow-api-key
OPENAI_API_KEY=your-openai-key
```

#### Frontend (.env.local)
```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_WS_URL=ws://localhost:5000

# Analytics
NEXT_PUBLIC_GA_ID=your-ga-id

# Features
NEXT_PUBLIC_ENABLE_OFFLINE=true
NEXT_PUBLIC_ENABLE_PUSH=true
```

### Configuration de développement

#### VS Code Settings
```json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "typescript.preferences.importModuleSpecifier": "relative",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

#### Extensions recommandées
- **Python** : Python, Pylance
- **TypeScript** : TypeScript Importer, ES7+ React/Redux/React-Native snippets
- **Git** : GitLens
- **Docker** : Docker

---

## 🚀 Déploiement

### Développement local

#### Avec Docker
```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

#### Sans Docker
```bash
# Backend
cd backend
python api.py

# Frontend
cd frontend
npm run dev
```

### Staging/Production

#### Build
```bash
# Frontend
cd frontend
npm run build

# Backend (avec Gunicorn)
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

#### Variables d'environnement production
```bash
# Backend
DEBUG=False
DB_PATH=/app/data/jowafrique.db
API_HOST=0.0.0.0

# Frontend
NEXT_PUBLIC_API_URL=https://api.jowafrique.com
```

---

## 🐛 Debug et dépannage

### Problèmes courants

#### Backend
1. **ImportError** : Vérifier le PYTHONPATH
2. **Database locked** : Arrêter tous les processus Python
3. **Port already in use** : Changer le port ou tuer le processus

#### Frontend
1. **Module not found** : Vérifier les imports et les chemins
2. **Build failed** : Vérifier les types TypeScript
3. **API connection** : Vérifier l'URL de l'API

### Outils de debug

#### Backend
```python
# Logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Debugger
import pdb; pdb.set_trace()

# Profiling
import cProfile
cProfile.run('your_function()')
```

#### Frontend
```typescript
// Console logging
console.log('Debug:', data);

// React DevTools
// Installer l'extension Chrome

// Network debugging
// Utiliser les DevTools du navigateur
```

---

## 📚 Ressources

### Documentation
- **Flask** : https://flask.palletsprojects.com/
- **Next.js** : https://nextjs.org/docs
- **TypeScript** : https://www.typescriptlang.org/docs/
- **Tailwind CSS** : https://tailwindcss.com/docs

### Outils
- **Postman** : Test des APIs
- **Insomnia** : Alternative à Postman
- **DB Browser for SQLite** : Visualisation de la base de données
- **React DevTools** : Debug des composants React

### Bonnes pratiques
- **Git** : Commits atomiques, messages clairs
- **Code** : DRY, SOLID, Clean Code
- **Tests** : TDD, couverture > 80%
- **Sécurité** : Validation des entrées, sanitisation

---

*Guide de développement - Dernière mise à jour : 2024-01-15*
