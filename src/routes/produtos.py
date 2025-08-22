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
        # Criar uma imagem 1080x1080 com fundo branco
        width, height = 1080, 1080
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Configurar cores
        cor_fundo_header = '#e74c3c'
        cor_texto_header = 'white'
        cor_titulo = '#2c3e50'
        cor_descricao = '#7f8c8d'
        cor_destaque = '#e74c3c'
        cor_preco_original = '#95a5a6'
        cor_preco_promocional = '#2c3e50'
        cor_desconto = '#27ae60'
        cor_fundo_botao = '#3498db'
        
        # Configurar fontes (aumentei os tamanhos)
        try:
            font_header = ImageFont.truetype("arial.ttf", 46)
            font_titulo = ImageFont.truetype("arial.ttf", 52)
            font_descricao = ImageFont.truetype("arial.ttf", 36)
            font_destaque = ImageFont.truetype("arial.ttf", 42)
            font_preco_original = ImageFont.truetype("arial.ttf", 42)
            font_preco_promocional = ImageFont.truetype("arial.ttf", 72)
            font_desconto = ImageFont.truetype("arial.ttf", 46)
            font_botao = ImageFont.truetype("arial.ttf", 38)
        except IOError:
            # Fallback para fontes padrão (aumentar tamanho)
            font_header = ImageFont.load_default()
            font_titulo = ImageFont.load_default()
            font_descricao = ImageFont.load_default()
            font_destaque = ImageFont.load_default()
            font_preco_original = ImageFont.load_default()
            font_preco_promocional = ImageFont.load_default()
            font_desconto = ImageFont.load_default()
            font_botao = ImageFont.load_default()
        
        # Desenhar cabeçalho
        draw.rectangle([(0, 0), (width, 130)], fill=cor_fundo_header)
        draw.text((40, 65), 'ESCOLHASHOP', fill=cor_texto_header, font=font_header, anchor='lm')
        
        # Badges de entrega
        draw.text((width-300, 45), 'COMPRAS ATÉ 12H', fill=cor_texto_header, font=font_descricao, anchor='lm')
        draw.text((width-300, 85), 'ENVIO NO MESMO DIA', fill=cor_texto_header, font=font_descricao, anchor='lm')
        
        # Título do produto
        titulo = produto['title']
        if len(titulo) > 40:  # Limitar tamanho do título
            titulo = titulo[:37] + '...'
        
        draw.text((width//2, 230), titulo, fill=cor_titulo, font=font_titulo, anchor='mm')
        
        # Descrição do produto
        descricao = produto['description']
        if len(descricao) > 60:  # Limitar tamanho da descrição
            descricao = descricao[:57] + '...'
        
        draw.text((width//2, 320), descricao, fill=cor_descricao, font=font_descricao, anchor='mm')
        
        # Texto de destaque
        draw.text((width//2, 400), "MELHOR OFERTA COM DESCONTO DA SHOPEE!", fill=cor_destaque, font=font_destaque, anchor='mm')
        
        # Preços
        preco_original = f"De: R$ {produto['price']:.2f}"
        preco_promocional = f"POR: R$ {produto['sale_price']:.2f}"
        desconto = f"{int(produto['discount_percentage'])}% OFF"
        
        draw.text((width//2, 500), preco_original, fill=cor_preco_original, font=font_preco_original, anchor='mm')
        draw.text((width//2, 580), preco_promocional, fill=cor_preco_promocional, font=font_preco_promocional, anchor='mm')
        draw.text((width//2, 670), desconto, fill=cor_desconto, font=font_desconto, anchor='mm')
        
        # Botão de compra
        draw.rectangle([(width//2 - 200, 750), (width//2 + 200, 830)], fill=cor_fundo_botao)
        draw.text((width//2, 790), "COMPRAR AGORA", fill='white', font=font_botao, anchor='mm')
        
        # Rodapé
        rodape = "⚡ Frete Grátis • 💯 Garantia • 🔄 Troca Fácil"
        draw.text((width//2, 950), rodape, fill=cor_descricao, font=font_descricao, anchor='mm')
        
        return img
        
    except Exception as e:
        print(f"Erro ao gerar anúncio: {str(e)}")
        # Retornar uma imagem de erro
        img = Image.new('RGB', (1080, 1080), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((540, 540), f"Erro: {str(e)}", fill='red', anchor='mm')
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
