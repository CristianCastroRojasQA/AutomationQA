import time
from core.utils.logger import get_logger


class DataFactory:
    """
    Generador centralizado de datos de prueba para todos los productos.

    Responsabilidad: proveer valores unicos, estructuras de datos
    y fixtures reutilizables para evitar colisiones en base de datos
    y garantizar trazabilidad en los datos de prueba.

    Uso:
        from core.utils.data_factory import DataFactory
        nombre = DataFactory.generar_nombre_unico("Marca_Test")
    """

    _log = get_logger("DataFactory")

    @staticmethod
    def generar_nombre_unico(prefijo: str = "QA_Test") -> str:
        """
        Genera un nombre unico con timestamp para evitar colisiones en DB.

        Args:
            prefijo: Prefijo descriptivo del tipo de dato (ej: 'Marca', 'Tecnologia').

        Returns:
            str: Nombre unico con formato '{prefijo}_{timestamp}'.
        """
        nombre_generado = f"{prefijo}_{int(time.time())}"
        DataFactory._log.debug(
            f"Generando dato unico: '{prefijo}' -> '{nombre_generado}'"
        )
        return nombre_generado
