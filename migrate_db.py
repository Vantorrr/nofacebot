"""
Database migration script for adding new application fields.
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add new fields to applications table."""
    db_path = "app.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Создаем backup
        backup_path = f"app_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        with open(db_path, 'rb') as f:
            backup_data = f.read()
        with open(backup_path, 'wb') as f:
            f.write(backup_data)
        print(f"✅ Created backup: {backup_path}")
        
        # Добавляем новые поля
        new_fields = [
            "subcategory TEXT",
            "budget TEXT", 
            "timeline TEXT",
            "has_content TEXT",
            "has_design TEXT",
            "support_level TEXT",
            "additional_options TEXT"
        ]
        
        for field in new_fields:
            try:
                cursor.execute(f"ALTER TABLE applications ADD COLUMN {field}")
                print(f"✅ Added field: {field}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"⚠️ Field already exists: {field}")
                else:
                    print(f"❌ Error adding field {field}: {e}")
        
        conn.commit()
        conn.close()
        
        print("✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    success = migrate_database()
    if success:
        print("🎉 Migration completed!")
    else:
        print("💥 Migration failed!") 