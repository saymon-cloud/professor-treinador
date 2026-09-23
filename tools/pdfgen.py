# -*- coding: utf-8 -*-
"""
Gerador de PDF minimalista, sem dependências externas (só stdlib).

Usado para montar os arquivos de "correção" (gabarito comentado) de provas
enviadas pela aluna, e guardá-los dentro da pasta da disciplina em
Treinador/data/correcoes/<disciplina>/. Texto acentuado usa WinAnsiEncoding
(compatível com Helvetica padrão do PDF, cobre a Latin-1 do português).
"""

import zlib


PAGE_W, PAGE_H = 595, 842  # A4 em pontos
MARGIN_L, MARGIN_R, MARGIN_TOP, MARGIN_BOTTOM = 50, 50, 60, 50
LINE_H_BODY = 14
LINE_H_TITLE = 22


def _wrap(text, max_chars):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        candidate = (cur + " " + w).strip()
        if len(candidate) > max_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = candidate
    if cur:
        lines.append(cur)
    return lines


def _pdf_escape(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class PdfBuilder:
    def __init__(self):
        self.pages = []  # cada página é uma lista de "linhas" (font, size, text, indent)
        self._cur = []
        self._y = PAGE_H - MARGIN_TOP

    def _new_page(self):
        if self._cur:
            self.pages.append(self._cur)
        self._cur = []
        self._y = PAGE_H - MARGIN_TOP

    def _ensure_space(self, needed):
        if self._y - needed < MARGIN_BOTTOM:
            self._new_page()

    def title(self, text):
        self._ensure_space(LINE_H_TITLE)
        self._cur.append(("Helvetica-Bold", 16, text, 0))
        self._y -= LINE_H_TITLE + 6

    def meta(self, text):
        self._ensure_space(LINE_H_BODY)
        self._cur.append(("Helvetica", 10, text, 0))
        self._y -= LINE_H_BODY

    def spacer(self, h=8):
        self._y -= h

    def heading(self, text):
        self._ensure_space(LINE_H_BODY + 4)
        self._cur.append(("Helvetica-Bold", 12, text, 0))
        self._y -= LINE_H_BODY + 2

    def body(self, text, indent=0, bold=False, max_chars=95):
        font = "Helvetica-Bold" if bold else "Helvetica"
        for line in _wrap(text, max_chars - indent // 5):
            self._ensure_space(LINE_H_BODY)
            self._cur.append((font, 10, line, indent))
            self._y -= LINE_H_BODY

    def finish(self):
        if self._cur:
            self.pages.append(self._cur)
        return self.pages

    def build(self):
        pages = self.finish()
        objects = []  # lista de bytes de cada objeto indireto (1-indexado)

        def add_obj(content_bytes):
            objects.append(content_bytes)
            return len(objects)

        font_helv = add_obj(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        )
        font_helv_bold = add_obj(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        )

        page_ids = []
        content_ids = []
        for page_lines in pages:
            stream_parts = [b"BT"]
            y = PAGE_H - MARGIN_TOP
            for font, size, text, indent in page_lines:
                stream_parts.append(f"/F{'2' if font.endswith('Bold') else '1'} {size} Tf".encode("latin-1"))
                x = MARGIN_L + indent
                stream_parts.append(f"1 0 0 1 {x} {y} Tm".encode("latin-1"))
                enc_text = _pdf_escape(text).encode("cp1252", errors="replace").decode("latin-1")
                stream_parts.append(f"({enc_text}) Tj".encode("latin-1"))
                y -= LINE_H_TITLE if size >= 16 else LINE_H_BODY
            stream_parts.append(b"ET")
            stream = b"\n".join(stream_parts)
            compressed = zlib.compress(stream)
            content_id = add_obj(
                (f"<< /Length {len(compressed)} /Filter /FlateDecode >>\nstream\n").encode("latin-1")
                + compressed
                + b"\nendstream"
            )
            content_ids.append(content_id)

        pages_obj_id = len(objects) + 1 + len(pages)  # calculado depois; placeholder
        # Cria os objetos de página (cada um referencia o Pages pai, calculado ao final)
        pages_id_placeholder = None
        page_obj_indices = []
        for content_id in content_ids:
            idx = add_obj(b"__PAGE_PLACEHOLDER__")
            page_obj_indices.append((idx, content_id))

        pages_id = add_obj(b"__PAGES_PLACEHOLDER__")
        catalog_id = add_obj(
            f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("latin-1")
        )

        kids = " ".join(f"{idx} 0 R" for idx, _ in page_obj_indices)
        objects[pages_id - 1] = (
            f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_indices)} "
            f"/MediaBox [0 0 {PAGE_W} {PAGE_H}] "
            f"/Resources << /Font << /F1 {font_helv} 0 R /F2 {font_helv_bold} 0 R >> >> >>"
        ).encode("latin-1")

        for idx, content_id in page_obj_indices:
            objects[idx - 1] = (
                f"<< /Type /Page /Parent {pages_id} 0 R /Contents {content_id} 0 R >>"
            ).encode("latin-1")

        # Monta o arquivo PDF final
        out = [b"%PDF-1.4\n"]
        offsets = [0]
        pos = len(out[0])
        for i, obj in enumerate(objects, start=1):
            header = f"{i} 0 obj\n".encode("latin-1")
            trailer = b"\nendobj\n"
            chunk = header + obj + trailer
            offsets.append(pos)
            out.append(chunk)
            pos += len(chunk)

        xref_pos = pos
        xref = [f"xref\n0 {len(objects) + 1}\n".encode("latin-1")]
        xref.append(b"0000000000 65535 f \n")
        for off in offsets[1:]:
            xref.append(f"{off:010d} 00000 n \n".encode("latin-1"))
        trailer = (
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_pos}\nendref\n"
        ).replace("endref", "%%EOF").encode("latin-1")

        return b"".join(out) + b"".join(xref) + trailer


def write_correction_pdf(output_path, title, meta_lines, sections):
    """
    sections: lista de (heading, [linhas de corpo já formatadas])
    """
    pdf = PdfBuilder()
    pdf.title(title)
    for line in meta_lines:
        pdf.meta(line)
    pdf.spacer(10)
    for heading, body_lines in sections:
        pdf.heading(heading)
        for line, indent, bold in body_lines:
            pdf.body(line, indent=indent, bold=bold)
        pdf.spacer(6)

    data = pdf.build()
    with open(output_path, "wb") as f:
        f.write(data)
    return output_path
