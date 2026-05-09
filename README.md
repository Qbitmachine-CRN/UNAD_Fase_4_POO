# Software FJ — Sistema de gestión (UNAD · Programación orientada a objetos)

Proyecto académico que integra **dominio (core)**, **servicios concretos**, **utilidades (logs y excepciones)** e **interfaz gráfica (Tkinter)** para gestionar clientes, cotizar servicios y crear o confirmar reservas.

## Requisitos

- **Python 3.10+** (probado con 3.13).
- **Tkinter** incluido con la instalación estándar de Python en Windows. Si falta, instala Python desde [python.org](https://www.python.org/downloads/) marcando la opción *tcl/tk*.

No hay dependencias externas en `pip`; el código usa solo la biblioteca estándar.

## Cómo ejecutar

Abre una terminal en la **carpeta raíz del proyecto** (donde está `main.py`).

| Comando | Descripción |
|--------|-------------|
| `python main.py` o `py main.py` | Abre la **interfaz gráfica** (menú Clientes, Reservas, Servicios). |
| `python main.py sim` | Ejecuta solo la **simulación por consola** (varias operaciones válidas e inválidas) sin abrir ventanas. |

Los eventos y errores relevantes se escriben en **`log_eventos.txt`** en la raíz del proyecto.

## Estructura del repositorio

```
UNAD_Fase_4_POO/
├── main.py                 # Punto de entrada: GUI o simulación
├── log_eventos.txt         # Registro de eventos (generado al ejecutar)
├── core/                   # Dominio: entidades y reglas de negocio
│   ├── base.py             # EntidadBase (ABC)
│   ├── cliente.py          # Cliente con validaciones
│   └── reserva.py          # Reserva, estados y confirmación/cancelación
├── servicios/              # Polimorfismo sobre Servicio (ABC)
│   ├── base_servicio.py    # Contrato: costo, validación, costo avanzado
│   ├── asesoria.py
│   ├── equipo.py
│   └── sala.py
├── utils/                  # Transversal
│   ├── excepciones.py      # Jerarquía SoftwareFJError, ValidacionError, etc.
│   └── logger.py           # registrar_evento / registrar_excepcion → archivo
└── gui/                    # Interfaz Tkinter
    ├── __init__.py         # Exporta iniciar_app y componentes
    ├── componentes.py      # Estilo oscuro, combobox, botones del menú
    └── ventana_principal.py  # Vistas Clientes, Reservas, Servicios
```

## Capas del sistema

1. **`core`**: `Cliente` (identificador, nombre, email, teléfono validados) y `Reserva` (cliente + instancia de `Servicio` + duración en horas, estados y `confirmar` / `cancelar`).
2. **`servicios`**: `Asesoria`, `AlquilerEquipo` y `ReservaSala` heredan de `Servicio`; implementan `calcular_costo`, `validar_parametros`, `describir_servicio` y pueden usar `calcular_costo_avanzado` (impuesto y descuento opcionales).
3. **`utils`**: excepciones tipadas para mensajes claros y registro en archivo con bloqueo para escrituras seguras.
4. **`gui`**: usa las mismas clases que `main.py` en la simulación; comboboxes con etiquetas en español; formulario de clientes se limpia tras un guardado exitoso.

## Objetivo académico (UNAD)

Consolidar **POO** (herencia, polimorfismo, encapsulación), **manejo de excepciones** (`try` / `except` / `else` / `finally`, encadenamiento) y **separación por paquetes** en un ejercicio de integración del curso de Programación.

## Licencia y uso

Uso **formativo / académico**. Ajusta autores o datos del curso en este archivo si tu docente lo solicita.
