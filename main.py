import typer
from rich.console import Console
from text_processing import extract_text_from_pdf
from ai_engine import summarize_text, generate_audio
import os

app = typer.Typer()
console = Console()

@app.command()
def convert(
    input_pdf: str = typer.Argument(..., help="Path to the input PDF file"),
    output_audio: str = typer.Option("output.mp3", help="Path to save the output audio file")
):
    """
    Convert a research paper PDF into a 2-minute audio summary.
    """
    console.print(f"[bold green]Starting conversion for:[/bold green] {input_pdf}")

    try:
        # 1. Extract Text
        with console.status("[bold blue]Extracting text from PDF...[/bold blue]"):
            text = extract_text_from_pdf(input_pdf)
            console.print(f"[green]✓ Text extracted ({len(text)} characters)[/green]")

        # 2. Summarize
        with console.status("[bold blue]Generating podcast script...[/bold blue]"):
            script = summarize_text(text)
            console.print("[green]✓ Script generated[/green]")
            console.print(f"[dim]{script[:200]}...[/dim]") # Preview

        # 3. Generate Audio
        with console.status("[bold blue]Generating audio...[/bold blue]"):
            generate_audio(script, output_audio)
            console.print(f"[bold green]✓ Audio saved to {output_audio}[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    app()
