from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Configuração da Thumbnail
config = {
    "background_color": (20, 40, 80),  # Azul escuro
    "title": "Meus 5 projetos",
    "highlight": "FAVORITOS",
    "subtitle": "de Python e SQL",
    "author": "Luciano Vasconcelos",
    "logos": ["python.png", "duckdb.png", "spark.png", "docker.png"],  # Caminhos das logos
    "output": "thumbnail.png",
    "font_path": "arial.ttf"  # Ajuste para a fonte que você tiver disponível
}

# Tamanho da imagem
width, height = 1280, 720

# Criando a imagem de fundo
img = Image.new("RGB", (width, height), config["background_color"])
draw = ImageDraw.Draw(img)

# Carregando as fontes
font_title = ImageFont.truetype(config["font_path"], 80)
font_highlight = ImageFont.truetype(config["font_path"], 100)
font_subtitle = ImageFont.truetype(config["font_path"], 60)
font_author = ImageFont.truetype(config["font_path"], 50)

# Posições iniciais
x_start = 50
y_start = 100

# 1. Desenhar título
draw.text((x_start, y_start), config["title"], font=font_title, fill="white")

# 2. Desenhar destaque (highlight) dentro de uma caixa vermelha
#    Primeiro medimos o texto usando textbbox:
highlight_bbox = draw.textbbox((0, 0), config["highlight"], font=font_highlight)
highlight_width = highlight_bbox[2] - highlight_bbox[0]
highlight_height = highlight_bbox[3] - highlight_bbox[1]

# Posição da caixa
highlight_box_x = x_start
highlight_box_y = y_start + 90

# Desenha o retângulo vermelho com margem
margin = 10
draw.rectangle(
    [
        (highlight_box_x, highlight_box_y),
        (highlight_box_x + highlight_width + 2*margin,
         highlight_box_y + highlight_height + 2*margin)
    ],
    fill="red"
)

# Desenha o texto do highlight
draw.text(
    (highlight_box_x + margin, highlight_box_y + margin),
    config["highlight"], font=font_highlight, fill="white"
)

# 3. Desenhar subtítulo
draw.text((x_start, y_start + 200), config["subtitle"], font=font_subtitle, fill="white")

# 4. Desenhar autor (na parte de baixo)
draw.text((x_start, height - 100), config["author"], font=font_author, fill="white")

# 5. Adicionar logos
logo_x_start = x_start
logo_y_start = height - 180
logo_size = (100, 100)  # Tamanho fixo das logos

for logo_path in config["logos"]:
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize(logo_size)
        img.paste(logo, (logo_x_start, logo_y_start), logo)
        logo_x_start += 130  # Espaçamento entre as logos
    except Exception as e:
        print(f"Erro ao carregar {logo_path}: {e}")

# 6. Salvar a imagem final
img.save(config["output"])
print(f"Thumbnail gerada: {config['output']}")
