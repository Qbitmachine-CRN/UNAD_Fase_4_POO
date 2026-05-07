from abc import ABC, abstractmethod

class EntidadBase(ABC):
    """
    Clase abstracta base para todas las entidades del sistema.
    Todo objeto que represente una entidad debe heredar de esta clase.
    """

    @abstractmethod
    def __str__(self):
        """Toda entidad debe tener una representación en texto."""
        pass
