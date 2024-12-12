# Language Flying Game

A Django-based educational game that teaches Spanish language skills through virtual travel across Mexico, Argentina, and Spain.

## Features

- Interactive dialogue scenarios with NPCs
- Multiple locations with unique cultural contexts
- Progress tracking and scoring system
- RESTful API for game state management
- Admin interface for content management

## Setup

1. Create and activate Conda environment:
```bash
conda create -n language-game python=3.11
conda activate language-game
```

2. Install dependencies:
```bash
conda install -c conda-forge django djangorestframework pygame pillow python-dotenv django-cors-headers
```

3. Apply database migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `/api/locations/` - List and detail of game locations
- `/api/dialogues/` - Dialogue scenarios for each location
- `/api/progress/` - Player progress tracking
- `/admin/` - Admin interface for content management

## Project Structure

- `game/` - Main Django app
  - `models.py` - Database models
  - `views.py` - API views
  - `serializers.py` - REST framework serializers
  - `urls.py` - URL routing
  - `admin.py` - Admin interface configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 
