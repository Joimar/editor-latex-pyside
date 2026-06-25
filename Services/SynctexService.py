import os
from dataclasses import dataclass
from typing import Optional
import subprocess


@dataclass
class SyncPoint:
    """Representa um ponto de sincronização: PDF → Código"""
    file_path: str  # Arquivo .tex
    line: int  # Linha no código
    column: int  # Coluna no código
    page: int  # Página do PDF
    h: float  # Posição horizontal no PDF (em bp)
    v: float  # Posição vertical no PDF (em bp)


class SynctexService:
    """Serviço para consultar sincronização SyncTeX via linha de comando."""

    def __init__(self, synctex_file_path: str):
        self.synctex_file = synctex_file_path

    def pdf_to_source(self, page: int, x: float, y: float) -> Optional[SyncPoint]:
        """
       Converte coordenadas do PDF (clique) para posição no código fonte.

       Args:
           page: Número da página (1-based)
           x: Posição horizontal em pixels do viewport
           y: Posição vertical em pixels do viewport

       Returns:
           SyncPoint com a localização no código, ou None se não encontrar
       """

        if not os.path.exists(self.synctex_file):
            return None

        # synctex edit -o PageNum:x:y:file.pdf
        pdf_path = self.synctex_file.replace(".synctex.gz", ".pdf")

        # O comando synctex espera coordenadas em bp (big points, 72 bp = 1 polegada)
        # Precisamos converter pixels do viewport para bp do PDF
        # Isso depende do zoom e DPI — veremos no PdfView

        cmd = [
            "synctex",
            "edit",
            "-o",
            f"{page}:{x}:{y}:{pdf_path}"
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(pdf_path)
            )

            if result.returncode != 0:
                return None

            return self._parse_synctex_output(result.stdout)

        except FileNotFoundError:
            # synctex não encontrado no PATH
            print("synctex não encontrado. Instale o TeX Live.")
            return None

    def _parse_synctex_output(self, output: str) -> Optional[SyncPoint]:
        """Parseia a saída do comando synctex."""
        # Saída típica:
        # SyncTeX result begin
        # Input:/caminho/para/arquivo.tex:123:456:*
        # ...
        # SyncTeX result end

        for line in output.splitlines():
            if line.startswith("Input:"):
                # Formato: Input:path:line:column:offset
                parts = line[6:].split(":")
            if len(parts) >= 3:
                return SyncPoint(
                    file_path=parts[0],
                    line=int(parts[1]),
                    column=int(parts[2]) if parts[2] != "*" else 0,
                    page=0,  # Não usado aqui
                    h=0.0,
                    v=0.0
                )

        return None

    def source_to_pdf(self, file_path: str, line: int, column: int = 0) -> Optional[SyncPoint]:
        """
        Forward search: código → PDF (para scroll automático no PDF)
        """

        pdf_path = self.synctex_file.replace(".synctex.gz", ".pdf")

        cmd = [
            "synctex",
            "view",
            "-i",
            f"{line}:{column}:{file_path}",
            "-o",
            pdf_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return None

            return self._parse_view_output(result.stdout)

        except FileNotFoundError:
            return None

    def _parse_view_output(self, output: str) -> Optional[SyncPoint]:
        """Parseia saída do synctex view."""
        page = 0
        h = v = 0.0

        for line in output.splitlines():
            if line.startswith("Page:"):
                page = int(line.split(":")[1])
            elif line.startswith("h:"):
                h = float(line.split(":")[1])
            elif line.startswith("v:"):
                v = float(line.split(":")[1])

        if page > 0:
            return SyncPoint(
                file_path="",
                line=0,
                column=0,
                page=page,
                h=h,
                v=v
            )
        return None
