# Pruebas básicas de los catálogos del dominio.
import unittest
from app.services import TICKET_TYPES, PRIORITIES, STATUSES

class TicketRulesTests(unittest.TestCase):
    """Verifica las opciones válidas definidas para los tickets."""
    def test_types(self):
        self.assertEqual(TICKET_TYPES, {"Petición", "Incidencia", "Requerimiento"})
    def test_priorities(self):
        self.assertEqual(PRIORITIES, {"L1", "L2", "L3"})
    def test_statuses(self):
        self.assertEqual(STATUSES, {"Pendiente", "Atendido", "Rechazado"})

if __name__ == "__main__":
    unittest.main()
