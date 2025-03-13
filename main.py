from PIL import Image, ImageDraw, ImageFont

# ---------------------
# CONFIGURAÇÕES
# ---------------------
config = {
    # Imagem de fundo (frame do vídeo) que será redimensionada para 1280x720
    "background_image": "luciano.png",  # Ajuste para o nome correto
    
    # Se a imagem de fundo não for encontrada, usamos uma cor de fallback
    "background_color": (20, 40, 80),
    
    # Textos
    "title": "Meus 5 projetos",
    "highlight": "FAVORITOS",
    "subtitle": "de Python e SQL",
    "author": "Luciano Vasconcelos",
    
    # Logos (caminhos dos arquivos PNG)
    "logos": ["python.png", "duckdb.png", "spark.png", "docker.png"],
    
    # Caminho de saída
    "output": "thumbnail.png",
    
    # Fonte TTF disponível no seu sistema ou pasta do projeto
    "font_path": "arial.ttf"
}

# Tamanho da thumbnail
WIDTH, HEIGHT = 1280, 720

# ---------------------
# CARREGAR BACKGROUND
# ---------------------
try:
    # Convert para RGBA para podermos aplicar transparência
    bg = Image.open(config["background_image"]).convert("RGBA")
    # Redimensiona para o tamanho definido (1280x720)
    bg = bg.resize((WIDTH, HEIGHT))
except Exception as e:
    print(f"Não foi possível carregar '{config['background_image']}': {e}")
    print("Usando cor de fundo em vez da imagem.")
    bg = Image.new("RGBA", (WIDTH, HEIGHT), config["background_color"])

# ---------------------
# ESCURECER A IMAGEM (Overlay)
# ---------------------
# Criamos um overlay preto semi-transparente para escurecer o fundo
overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 120))  # 120 de alpha
bg = Image.alpha_composite(bg, overlay)

draw = ImageDraw.Draw(bg)

# ---------------------
# CARREGAR FONTES
# ---------------------
# Ajuste os tamanhos conforme desejar
font_title = ImageFont.truetype(config["font_path"], 80)
font_highlight = ImageFont.truetype(config["font_path"], 80)
font_subtitle = ImageFont.truetype(config["font_path"], 60)
font_author = ImageFont.truetype(config["font_path"], 50)

# ---------------------
# POSICIONAMENTO
# ---------------------
# Ajuste conforme desejar
x_margin = 50
y_title = 50           # Posição vertical do título
y_highlight = 160      # Posição vertical do destaque
y_subtitle = 280       # Posição vertical do subtítulo

# Espaço para logos e autor no rodapé
logos_y = HEIGHT - 140

# ---------------------
# DESENHAR TÍTULO
# ---------------------
draw.text((x_margin, y_title), config["title"], font=font_title, fill="white")

# ---------------------
# DESTAQUE (HIGHLIGHT)
# ---------------------
highlight_bbox = draw.textbbox((0, 0), config["highlight"], font=font_highlight)
highlight_w = highlight_bbox[2] - highlight_bbox[0]
highlight_h = highlight_bbox[3] - highlight_bbox[1]

rect_margin = 5
rect_x1 = x_margin
rect_y1 = y_highlight
rect_x2 = x_margin + highlight_w + 2*rect_margin
rect_y2 = y_highlight + highlight_h + 2*rect_margin

# Retângulo vermelho
draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill="red")
# Texto
draw.text(
    (rect_x1 + rect_margin, rect_y1 + rect_margin),
    config["highlight"],
    font=font_highlight,
    fill="white"
)

# ---------------------
# DESENHAR SUBTÍTULO
# ---------------------
draw.text((x_margin, y_subtitle), config["subtitle"], font=font_subtitle, fill="white")

# ---------------------
# DESENHAR LOGOS (NA ESQUERDA, NO RODAPÉ)
# ---------------------
logo_x = x_margin
logo_size = (80, 80)  # Tamanho das logos

for logo_path in config["logos"]:
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize(logo_size)
        bg.paste(logo, (logo_x, logos_y), logo)
        logo_x += logo_size[0] + 20  # Espaçamento horizontal
    except Exception as e:
        print(f"Erro ao carregar logo {logo_path}: {e}")

# ---------------------
# DESENHAR AUTOR (NO RODAPÉ, À DIREITA)
# ---------------------
author_text = config["author"]
author_bbox = draw.textbbox((0, 0), author_text, font=font_author)
author_w = author_bbox[2] - author_bbox[0]
author_h = author_bbox[3] - author_bbox[1]

# Posição para ficar no canto inferior direito (com margem)
author_x = WIDTH - author_w - x_margin
author_y = HEIGHT - author_h - 40

draw.text((author_x, author_y), author_text, font=font_author, fill="white")

# ---------------------
# SALVAR IMAGEM
# ---------------------
bg.save(config["output"])
print(f"Thumbnail gerada em: {config['output']}")
