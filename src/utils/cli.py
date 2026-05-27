"""
Rich CLI interface for the RAG chatbot.
"""
import sys
from typing import TYPE_CHECKING

from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.status import Status
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

if TYPE_CHECKING:
    from src.core.chatbot import RAGChatbot

# ── Theme ──────────────────────────────────────────────────────────────────────

_THEME = Theme(
    {
        "rag.border": "bright_black",
        "rag.user": "bold cyan",
        "rag.ai": "bold white",
        "rag.cmd": "dim cyan",
        "rag.dim": "dim white",
        "rag.debug": "yellow",
        "rag.success": "green",
        "rag.error": "bold red",
        "rag.warning": "yellow",
    }
)

console = Console(theme=_THEME, highlight=False)

# ── Static content ──────────────────────────────────────────────────────────────

_HEADER = Panel(
    Align.center(
        Text.assemble(
            ("RAG", "bold cyan"),
            ("  Assistant\n", "bold white"),
            ("Legal Document Intelligence", "dim white"),
        )
    ),
    box=box.DOUBLE_EDGE,
    border_style="rag.border",
    padding=(1, 6),
)

_HELP = (
    "  [rag.cmd]/debug[/]   Affiche les documents récupérés par la recherche\n"
    "  [rag.cmd]/clear[/]   Efface l'écran\n"
    "  [rag.cmd]/help[/]    Affiche cette aide\n"
    "  [rag.cmd]/quit[/]    Quitte le programme"
)

_QUIT_CMDS = {"/quit", "/exit", "q", "quit", "exit"}

# ── Helpers ─────────────────────────────────────────────────────────────────────


def _print_header() -> None:
    console.print()
    console.print(_HEADER)
    console.print(
        "[rag.dim]  /help pour les commandes · /quit pour quitter[/]",
        justify="center",
    )
    console.print()


def _print_debug_panel(documents: list) -> None:
    if not documents:
        console.print(
            Panel(
                "[rag.dim]Aucun document trouvé dans la base.[/]",
                title="[rag.debug]● Debug[/]",
                border_style="rag.debug",
                box=box.SIMPLE,
            )
        )
        return

    table = Table(
        box=box.SIMPLE,
        border_style="rag.border",
        show_header=True,
        header_style="rag.dim",
        padding=(0, 1),
        expand=True,
    )
    table.add_column("#", style="rag.dim", width=2, no_wrap=True)
    table.add_column("Source", style="cyan", no_wrap=True)
    table.add_column("Page", style="rag.dim", width=6, no_wrap=True)
    table.add_column("Aperçu", style="white")

    for i, doc in enumerate(documents, 1):
        filename = doc.metadata.get("filename", "Inconnu")
        page = str(
            doc.metadata.get("page_number", doc.metadata.get("entry_index", "—"))
        )
        preview = doc.page_content[:120].replace("\n", " ").rstrip() + "…"
        table.add_row(str(i), filename, page, preview)

    console.print(
        Panel(
            table,
            title=f"[rag.debug]● Debug  ·  {len(documents)} document(s) récupéré(s)[/]",
            border_style="rag.debug",
            box=box.SIMPLE,
        )
    )


# ── Main loop ───────────────────────────────────────────────────────────────────


def chat_loop(chatbot: "RAGChatbot") -> None:
    """Main interactive loop with Rich display."""
    _print_header()
    debug_mode = False

    while True:
        # ── Prompt ──────────────────────────────────────────────────────────────
        console.print(Rule(style="rag.border"))
        try:
            question = console.input("[rag.user]  Vous[/]  ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[rag.dim]  Au revoir ![/]")
            break

        if not question:
            continue

        # ── Built-in commands ────────────────────────────────────────────────────
        cmd = question.lower()

        if cmd in _QUIT_CMDS:
            console.print("[rag.dim]  Au revoir ![/]")
            break

        if cmd == "/help":
            console.print(
                Panel(_HELP, border_style="rag.border", box=box.SIMPLE, padding=(0, 1))
            )
            continue

        if cmd == "/clear":
            console.clear()
            _print_header()
            continue

        if cmd == "/debug":
            debug_mode = not debug_mode
            state = "[rag.success]activé[/]" if debug_mode else "[rag.dim]désactivé[/]"
            console.print(f"  [rag.dim]Mode debug {state}[/]")
            continue

        # ── Retrieval ────────────────────────────────────────────────────────────
        documents = []
        with Status(
            "[rag.dim]  Recherche de documents…[/]",
            console=console,
            spinner="dots",
            spinner_style="cyan",
        ):
            try:
                documents = chatbot.retrieve(question)
            except Exception as exc:
                console.print(f"\n  [rag.error]Erreur lors de la récupération :[/] {exc}")
                continue

        if debug_mode:
            _print_debug_panel(documents)

        if not documents:
            console.print(
                Panel(
                    "[rag.dim]Aucune information pertinente trouvée dans la base de données.[/]",
                    border_style="rag.border",
                    box=box.SIMPLE,
                    padding=(0, 2),
                )
            )
            continue

        # ── Streaming response ───────────────────────────────────────────────────
        console.print()
        console.print("[rag.ai]  Assistant[/]")
        console.print()

        full_text = ""
        try:
            with Live(
                Markdown(" "),
                console=console,
                refresh_per_second=15,
                vertical_overflow="visible",
            ) as live:
                for chunk in chatbot.stream(question, documents):
                    full_text += chunk
                    live.update(Markdown(full_text))

        except KeyboardInterrupt:
            console.print("\n[rag.dim]  Génération interrompue.[/]")
        except Exception as exc:
            console.print(f"\n  [rag.error]Erreur :[/] {exc}")

        console.print()
