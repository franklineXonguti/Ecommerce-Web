# Database Migration Guide

This guide explains how to manage database migrations for the SmartCommerce backend.

## Initial Setup

### 1. Create Initial Migrations (Already Done)

Initial migration files have been created manually in each app's `migrations/` directory. These define the database schema for all models.

### 2. Apply Migrations

```bash
# From backend directory
python manage.py migrate
```

This will create all database tables according to the migration files.

## Making Changes to Models

When you modify models, you need to create and apply new migrations:

### 1. Create Migration

```bash
python manage.py makemigrations
```

This will detect changes to your models and create new migration files.

### 2. Review Migration

Check the generated migration file in `<app>/migrations/` to ensure it's correct.

### 3. Apply Migration

```bash
python manage.py migrate
```

### 4. Commit Migration Files

Always commit migration files to version control:
```bash
git add <app>/migrations/
git commit -m "feat: add migration for <description>"
```

## Common Migration Tasks

### Check Migration Status

```bash
# Show all migrations and their status
python manage.py showmigrations

# Show migrations for specific app
python manage.py showmigrations user_accounts
```

### Rollback Migration

```bash
# Rollback to specific migration
python manage.py migrate <app_name> <migration_name>

# Rollback all migrations for an app
python manage.py migrate <app_name> zero
```

### Create Empty Migration

```bash
# For data migrations or custom operations
python manage.py makemigrations --empty <app_name>
```

## Data Migrations

For populating or transforming data, create a data migration:

```python
# Example data migration
from django.db import migrations

def populate_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Category.objects.create(name='Electronics', slug='electronics')
    Category.objects.create(name='Clothing', slug='clothing')

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_categories),
    ]
```

## Production Migrations

### Before Deploying

1. **Test migrations locally**:
```bash
python manage.py migrate --plan
```

2. **Backup database**:
```bash
pg_dump smartcommerce > backup_$(date +%Y%m%d_%H%M%S).sql
```

3. **Review migration SQL**:
```bash
python manage.py sqlmigrate <app_name> <migration_number>
```

### During Deployment

1. **Put application in maintenance mode** (if needed)

2. **Apply migrations**:
```bash
python manage.py migrate --noinput
```

3. **Verify migration success**:
```bash
python manage.py showmigrations
```

4. **Restart application services**

### Rollback Plan

Always have a rollback plan:
1. Keep database backup
2. Know the previous migration number
3. Test rollback in staging first

## Migration Best Practices

1. **Never edit applied migrations**: Create new migrations instead
2. **Keep migrations small**: One logical change per migration
3. **Test migrations**: Test both forward and backward migrations
4. **Use RunPython carefully**: Ensure data migrations are idempotent
5. **Avoid circular dependencies**: Be careful with ForeignKey relationships
6. **Document complex migrations**: Add comments explaining the purpose
7. **Squash old migrations**: Periodically squash migrations to reduce clutter

## Squashing Migrations

After accumulating many migrations, you can squash them:

```bash
# Squash migrations 0001 through 0010
python manage.py squashmigrations <app_name> 0010
```

## Troubleshooting

### Migration Conflicts

If you encounter migration conflicts:
```bash
# Merge migrations
python manage.py makemigrations --merge
```

### Fake Migrations

If you need to mark a migration as applied without running it:
```bash
python manage.py migrate --fake <app_name> <migration_name>
```

### Reset Migrations (Development Only)

**WARNING**: This will delete all data!

```bash
# Drop all tables
python manage.py flush

# Delete migration files (keep __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recreate migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Migration Files Structure

```
app_name/
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py      # Initial models
│   ├── 0002_add_field.py    # Add new field
│   └── 0003_data_migration.py  # Data migration
```

## Additional Resources

- [Django Migrations Documentation](https://docs.djangoproject.com/en/4.2/topics/migrations/)
- [Django Migration Operations Reference](https://docs.djangoproject.com/en/4.2/ref/migration-operations/)
