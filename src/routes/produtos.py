import requests
from io import BytesIO
import csv
import os
from flask import Blueprint, jsonify, request
from PIL import Image, ImageDraw, ImageFont
import io
import base64

produtos_bp = Blueprint('produtos', __name__)

def carregar_produtos():
    """Carrega os produtos do arquivo CSV"""
    produtos = []
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'produtos.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Filtrar apenas produtos com desconto significativo
                try:
                    discount = float(row.get('discount_percentage', 0))
                    if discount > 20:  # Apenas produtos com mais de 20% de desconto
                        produto = {
                            'id': row.get('itemid', ''),
                            'title': row.get('title', ''),
                            'description': row.get('description', ''),
                            'price': float(row.get('price', 0)),
                            'sale_price': float(row.get('sale_price', 0)),
                            'discount_percentage': discount,
                            'image_link': row.get('image_link', ''),
                            'product_link': row.get('product_link', ''),
                            'category': row.get('global_category1', ''),
                            'rating': float(row.get('item_rating', 0))
                        }
                        # VERIFICAÇÃO EXTRA: Se image_link estiver vazio, tente image_link_3
                        if not produto['image_link'] or produto['image_link'].strip() == '':
                            produto['image_link'] = row.get('image_link_3', '')
                        
                        produtos.append(produto)
                except (ValueError, TypeError) as e:
                    print(f"Erro ao processar produto: {str(e)}")
                    continue
    except FileNotFoundError:
        print("Arquivo produtos.csv não encontrado!")
        return []
    except Exception as e:
        print(f"Erro ao ler CSV: {str(e)}")
        return []
    
    # Ordenar por desconto (maior primeiro)
    produtos.sort(key=lambda x: x['discount_percentage'], reverse=True)
    print(f"Carregados {len(produtos)} produtos com desconto > 20%")
    return produtos

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    """Retorna a lista de produtos"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    search = request.args.get('search', '')
    
    produtos = carregar_produtos()
    
    # Filtrar por busca se fornecida
    if search:
        produtos = [p for p in produtos if search.lower() in p['title'].lower() or search.lower() in p['description'].lower()]
    
    # Paginação
    start = (page - 1) * per_page
    end = start + per_page
    produtos_pagina = produtos[start:end]
    
    return jsonify({
        'produtos': produtos_pagina,
        'total': len(produtos),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(produtos) + per_page - 1) // per_page
    })

@produtos_bp.route('/produto/<produto_id>', methods=['GET'])
def obter_produto(produto_id):
    """Retorna um produto específico"""
    produtos = carregar_produtos()
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    
    if produto:
        return jsonify(produto)
    else:
        return jsonify({'error': 'Produto não encontrado'}), 404

def gerar_anuncio(produto):
    """Gera uma imagem de anúncio baseada no modelo"""
    try:
        # Criar uma imagem 1080x1080 com fundo branco (alterado de preto para branco)
        width, height = 1080, 1080
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Cores - ajustadas para layout mais clean
        cor_titulo_loja = '#e74c3c'  # Vermelho (destaque)
        cor_linha = '#bdc3c7'        # Cinza claro
        cor_titulo_produto = '#2c3e50' # Azul escuro
        cor_preco_original = '#7f8c8d' # Cinza
        cor_preco_promocional = '#e74c3c' # Vermelho
        cor_desconto = '#27ae60'      # Verde
        cor_descricao = '#34495e'     # Azul mais escuro
        cor_fundo_destaque = '#f8f9fa' # Cinza muito claro
        
        try:
            # Tentar usar fontes TrueType
            font_loja = ImageFont.truetype("arial.ttf", 50)        # Nome da loja - MAIOR
            font_titulo = ImageFont.truetype("arial.ttf", 36)      # Título do produto
            font_preco = ImageFont.truetype("arial.ttf", 42)       # Preços 
            font_desconto = ImageFont.truetype("arial.ttf", 48)    # Desconto 
            font_descricao = ImageFont.truetype("arial.ttf", 30)   # Descrição
        except IOError:
            # Se não encontrar as fontes TrueType, usar fallback
            font_loja = ImageFont.load_default()
            font_titulo = ImageFont.load_default()
            font_preco = ImageFont.load_default()
            font_desconto = ImageFont.load_default()
            font_descricao = ImageFont.load_default()
        
        # Cabeçalho com fundo colorido
        draw.rectangle([0, 0, width, 120], fill='#e74c3c')
        
        # Nome da loja no topo (centralizado)
        draw.text((width//2, 60), 'ESCOLHASHOP', fill='white', font=font_loja, anchor='mm')
        
        # Linha separadora
        draw.rectangle([50, 130, width-50, 135], fill=cor_linha)
        
        # Título do produto (quebrar em linhas se muito longo)
        titulo = produto['title'][:70]  # Limitar tamanho
        y_titulo = 180
        
        # Quebrar título em múltiplas linhas se necessário
        palavras = titulo.split()
        linhas = []
        linha_atual = ""
        
        for palavra in palavras:
            if len(linha_atual + palavra) < 30:
                linha_atual += palavra + " "
            else:
                if linha_atual:
                    linhas.append(linha_atual.strip())
                linha_atual = palavra + " "
        
        if linha_atual:
            linhas.append(linha_atual.strip())
        
        for i, linha in enumerate(linhas[:3]):  # Máximo 3 linhas
            draw.text((width//2, y_titulo + i*50), linha, fill=cor_titulo_produto, font=font_titulo, anchor='mm')
        
        # Área para imagem do produto
        img_y = 350
        img_height = 400
        
        try:
            # CORREÇÃO: Verificar e completar URL da imagem
            image_link = produto['image_link']
            
            # Se a URL estiver vazia, use placeholder
            if not image_link or image_link.strip() == '':
                raise Exception("URL da imagem está vazia")
            
            # Se a URL não começar com http, adicione https://
            if not image_link.startswith(('http://', 'https://')):
                image_link = 'https://' + image_link
            
            # Baixar imagem real do produto
            response = requests.get(image_link, timeout=10)
            response.raise_for_status()
            
            # Carregar imagem
            produto_img = Image.open(BytesIO(response.content))
            
            # Redimensionar mantendo proporção
            produto_img.thumbnail((600, 400))
            
            # Calcular posição para centralizar
            img_width, img_height = produto_img.size
            x_pos = (width - img_width) // 2
            y_pos = img_y + (400 - img_height) // 2
            
            # Colar imagem no anúncio
            img.paste(produto_img, (x_pos, y_pos))
            
        except Exception as e:
            # Fallback: desenhar retângulo placeholder
            draw.rectangle([(width-500)//2, img_y, (width+500)//2, img_y + 400], outline=cor_linha, width=2)
            draw.text((width//2, img_y + 200), 'IMAGEM DO PRODUTO', fill=cor_linha, font=font_titulo, anchor='mm')
            print(f"Erro ao carregar imagem: {str(e)}")
        
        # Área de preços com fundo destacado
        preco_y = img_y + img_height + 30
        draw.rectangle([50, preco_y, width-50, preco_y + 180], fill=cor_fundo_destaque)
        
        # Preço original (riscado)
        preco_original = f"De: R$ {produto['price']:.2f}"
        draw.text((width//2, preco_y + 40), preco_original, fill=cor_preco_original, font=font_preco, anchor='mm')
        
        # Linha sobre o preço original (simulando riscado)
        bbox = draw.textbbox((0, 0), preco_original, font=font_preco)
        text_width = bbox[2] - bbox[0]
        start_x = width//2 - text_width//2
        end_x = width//2 + text_width//2
        draw.line([start_x, preco_y + 50, end_x, preco_y + 50], fill=cor_preco_original, width=3)
        
        # Preço promocional
        preco_promocional = f"POR: R$ {produto['sale_price']:.2f}"
        draw.text((width//2, preco_y + 90), preco_promocional, fill=cor_preco_promocional, font=font_preco, anchor='mm')
        
        # Desconto
        desconto_text = f"{int(produto['discount_percentage'])}% OFF"
        draw.text((width//2, preco_y + 140), desconto_text, fill=cor_desconto, font=font_desconto, anchor='mm')
        
        # Rodapé com informações adicionais
        rodape_y = height - 80
        draw.rectangle([0, rodape_y, width, height], fill='#f1f2f6')
        
        # Descrição adicional
        descricao = "⚡ Entrega Rápida | ✅ Garantia | 🔄 Devolução Fácil"
        draw.text((width//2, rodape_y + 40), descricao, fill=cor_descricao, font=font_descricao, anchor='mm')
        
        return img
        
    except Exception as e:
        print(f"Erro ao gerar anúncio: {str(e)}")
        # Retornar uma imagem de erro
        img = Image.new('RGB', (1080, 1080), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((540, 540), f"Erro: {str(e)}", fill='red', font=ImageFont.load_default())
        return img

@produtos_bp.route('/gerar-anuncio/<produto_id>', methods=['POST'])
def gerar_anuncio_produto(produto_id):
    """Gera um anúncio para um produto específico"""
    produtos = carregar_produtos()
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    try:
        # Gerar a imagem do anúncio
        img = gerar_anuncio(produto)
        
        # Converter para base64 para enviar via JSON
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'image': f"data:image/png;base64,{img_str}",
            'produto': produto
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar anúncio: {str(e)}'}), 500
