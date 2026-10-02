# claude-usage-widget

Widget de escritorio, siempre visible, que muestra cuánto llevás usado del plan Max de
Claude Code en las ventanas de **5 horas** y de **7 días**.

```
┌──────────────┐
│ 5h:   42.3%  │
│ Wk:   18.7%  │
└──────────────┘
```

Verde por debajo del 60 %, amarillo hasta el 85 % y rojo después. Se actualiza cada 2 minutos.

## Uso

Necesita Python 3 con Tkinter (`sudo apt install python3-tk` en Debian y Ubuntu) y una sesión
de Claude Code iniciada, para que exista `~/.claude/.credentials.json`.

```bash
python3 widget.py   # en primer plano
./run.sh            # en segundo plano, con log en /tmp/claude-usage-widget.log
```

Se mueve arrastrando con el click izquierdo y se cierra con doble click o click derecho. Para
frenar la instancia de fondo: `pkill -f 'python3 widget.py'`.

## Cómo funciona

Lee el token OAuth del archivo de credenciales de Claude Code y consulta el mismo endpoint
interno que usa `/usage` (`api.anthropic.com/api/oauth/usage`). Como no es una API pública,
si cambia, el widget muestra `err<código>` u `offline` hasta que se actualice.
