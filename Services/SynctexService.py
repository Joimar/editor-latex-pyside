import os
from dataclasses import dataclass
from typing import Optional


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

