from src.adapters.repository import InMemoryRepository
from src.services import WarehouseService
from src.domain.warehouse import Movement
from datetime import datetime

repo = InMemoryRepository()
movements = [
    Movement('mix_001','P001','Testprodukt',100,'IN','Großeinkauf',datetime(2024,1,1,9,0,0),'admin'),
    Movement('mix_002','P001','Testprodukt',-20,'OUT','Verkauf',datetime(2024,1,1,10,0,0),'user1'),
    Movement('mix_003','P001','Testprodukt',5,'CORRECTION','Bestandskorrektur',datetime(2024,1,1,11,0,0),'admin'),
    Movement('mix_004','P001','Testprodukt',-3,'OUT','Retour',datetime(2024,1,1,12,0,0),'user2'),
]
for m in movements:
    repo.save_movement(m)
service = WarehouseService(repo)
print(service.generate_statistics_report())
