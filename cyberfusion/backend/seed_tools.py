import os
from app import app, db
from models import Tool

TOOLS = [
    {"name": "Nmap", "description": "Network scanning tool", "category": "whitehat", "install_cmd": "apt-get install -y nmap", "run_cmd": "nmap -h"},
    {"name": "Nikto", "description": "Web server scanner", "category": "whitehat", "install_cmd": "apt-get install -y nikto", "run_cmd": "nikto -h"},
    {"name": "OWASP ZAP", "description": "Web application security scanner", "category": "whitehat", "install_cmd": "apt-get install -y zaproxy", "run_cmd": "zap.sh -h"},
    # ... (add more as in previous messages)
]

if __name__ == "__main__":
    with app.app_context():
        for t in TOOLS:
            if not Tool.query.filter_by(name=t["name"]).first():
                tool = Tool(**t)
                db.session.add(tool)
        db.session.commit()
        print("Seeded tools to the database.")