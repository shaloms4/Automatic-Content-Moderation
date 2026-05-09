import sqlite3
from datetime import datetime
from typing import List, Dict

class ModerationDatabase:
    def __init__(self, db_name="moderation_logs.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Create the database table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS moderation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                original_text TEXT,
                moderated_text TEXT,
                toxicity_score REAL,
                is_toxic INTEGER,
                raw_model_score REAL,
                method TEXT,
                flagged_words TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_moderation(self, result: Dict):
        """Save a moderation result to database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        flagged = result["rule_based"].get("flagged_words", [])
        flagged_str = ", ".join(flagged) if flagged else ""
        
        cursor.execute('''
            INSERT INTO moderation_logs 
            (timestamp, original_text, moderated_text, toxicity_score, 
             is_toxic, raw_model_score, method, flagged_words)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            result["original_text"],
            result["moderated_text"],
            result["toxicity_score"],
            1 if result["is_toxic"] else 0,
            result.get("raw_model_score", 0.0),
            result["method"],
            flagged_str
        ))
        
        conn.commit()
        conn.close()

    def get_history(self, limit: int = 20) -> List[Dict]:
        """Retrieve recent moderation history"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # This allows us to get dict-like rows
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM moderation_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]

    def get_stats(self) -> Dict:
        """Get basic statistics"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM moderation_logs")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM moderation_logs WHERE is_toxic = 1")
        toxic_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_moderations": total,
            "toxic_count": toxic_count,
            "clean_count": total - toxic_count
        }


# For testing
if __name__ == "__main__":
    db = ModerationDatabase()
    print("✅ Database initialized successfully!")
    print("Stats:", db.get_stats())