<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerador de Anúncios - Layout Profissional</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }
        
        body {
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .ad-container {
            width: 1080px;
            height: 1080px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            position: relative;
        }
        
        .ad-header {
            background: linear-gradient(to right, #e74c3c, #c0392b);
            padding: 25px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
        }
        
        .logo {
            font-size: 46px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .shipping-info {
            display: flex;
            gap: 15px;
        }
        
        .shipping-badge {
            background-color: white;
            color: #e74c3c;
            padding: 12px 20px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 26px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        
        .product-section {
            padding: 40px;
            display: flex;
            height: calc(100% - 130px);
        }
        
        .product-image {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
        }
        
        .product-image img {
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
        }
        
        .product-info {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 0 40px;
        }
        
        .product-title {
            font-size: 52px;
            font-weight: 800;
            margin-bottom: 30px;
            line-height: 1.2;
            color: #2c3e50;
            text-transform: uppercase;
        }
        
        .product-description {
            font-size: 36px;
            font-weight: 600;
            margin-bottom: 40px;
            color: #7f8c8d;
            line-height: 1.3;
        }
        
        .product-highlight {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 50px;
            color: #e74c3c;
            line-height: 1.3;
        }
        
        .pricing {
            margin-bottom: 40px;
        }
        
        .original-price {
            font-size: 42px;
            text-decoration: line-through;
            color: #95a5a6;
            margin-bottom: 15px;
        }
        
        .current-price {
            font-size: 72px;
            font-weight: 900;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .discount-badge {
            display: inline-block;
            background: linear-gradient(to right, #27ae60, #2ecc71);
            color: white;
            padding: 15px 30px;
            border-radius: 12px;
            font-size: 46px;
            font-weight: 800;
        }
        
        .cta-button {
            background: linear-gradient(to right, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 25px 50px;
            font-size: 38px;
            font-weight: 700;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 30px;
            box-shadow: 0 6px 15px rgba(52, 152, 219, 0.3);
        }
        
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(52, 152, 219, 0.4);
        }
        
        .rating {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-top: 30px;
            font-size: 32px;
            color: #7f8c8d;
        }
        
        .stars {
            color: #f1c40f;
            font-size: 36px;
        }
        
        .footer-note {
            position: absolute;
            bottom: 30px;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 28px;
            color: #7f8c8d;
        }
        
        @media (max-width: 1120px) {
            .ad-container {
                transform: scale(0.8);
            }
        }
    </style>
</head>
<body>
    <div class="ad-container">
        <div class="ad-header">
            <div class="logo">ESCOLHASHOP</div>
            <div class="shipping-info">
                <div class="shipping-badge">COMPRAS ATÉ 12H</div>
                <div class="shipping-badge">ENVIO NO MESMO DIA</div>
            </div>
        </div>
        
        <div class="product-section">
            <div class="product-image">
                <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='500' viewBox='0 0 500 500'%3E%3Crect width='500' height='500' fill='%23e9ecef'/%3E%3Cpath d='M250,150 L325,250 L275,350 L225,350 L175,250 Z' fill='%233498db' stroke='%232980b9' stroke-width='15'/%3E%3Ccircle cx='250' cy='250' r='80' fill='%23e74c3c' stroke='%23c0392b' stroke-width='15'/%3E%3Ctext x='250' y='420' font-family='Arial' font-size='30' font-weight='bold' text-anchor='middle' fill='%237f8c8d'%3EIMAGEM DO PRODUTO%3C/text%3E%3C/svg%3E" alt="Produto">
            </div>
            
            <div class="product-info">
                <h1 class="product-title">TORNEIRA JARDIM ESFERA COM PORTA CADEADO</h1>
                
                <p class="product-description">Torneira de esfera com porta cadeado em metal resistente para parede externa</p>
                
                <p class="product-highlight">MELHOR TORNEIRA ESFERA COM PORTA CADEADO DA SHOPEE!</p>
                
                <div class="pricing">
                    <div class="original-price">De: R$ 119,99</div>
                    <div class="current-price">POR: R$ 22,99</div>
                    <div class="discount-badge">81% OFF</div>
                </div>
                
                <div class="rating">
                    <div class="stars">★★★★★</div>
                    <div>(4.8) 2.478 avaliações</div>
                </div>
                
                <button class="cta-button">COMPRAR AGORA</button>
            </div>
        </div>
        
        <div class="footer-note">
            ⚡ Frete Grátis • 💯 Garantia de 1 Ano • 🔄 Troca Fácil
        </div>
    </div>
</body>
</html>
