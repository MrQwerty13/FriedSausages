from database import SessionLocal, engine, Base
from models import Device, ComplianceRule

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()

    if not db.query(Device).first():
        router = Device(
            name="Router-01",
            ip_address="192.168.1.1",
            vendor="Cisco",
            device_type="Router",
            os_version="IOS 15.4",
            status="online"
        )
        db.add(router)

    if not db.query(ComplianceRule).first():
        rules = [
            ComplianceRule(name="Запрет Telnet", description="Обнаружен включенный Telnet", pattern="transport input telnet", severity="high", recommendation="Использовать SSH"),
            ComplianceRule(name="Слабый SNMP", description="Используется public community", pattern="snmp-server community public", severity="medium", recommendation="Сменить community string"),
            ComplianceRule(name="Опасный ACL", description="Слишком широкие разрешения", pattern="permit ip any any", severity="critical", recommendation="Настроить строгий ACL"),
            ComplianceRule(name="Отсутствие логов", description="Не настроена отправка логов", pattern="logging host", severity="warning", recommendation="Указать сервер логирования")
        ]
        db.add_all(rules)

    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
