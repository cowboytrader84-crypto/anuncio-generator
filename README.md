# 🛍️ Gerador de Anúncios - EscolhaShop

Uma aplicação web completa para gerar anúncios profissionais automaticamente a partir de produtos do CSV da Shopee.

## ✨ Funcionalidades

- **Carregamento Automático**: Carrega produtos do arquivo CSV da Shopee
- **Filtros Inteligentes**: Exibe apenas produtos com desconto superior a 20%
- **Busca Avançada**: Pesquise produtos por nome ou descrição
- **Paginação**: Navegue facilmente entre milhares de produtos
- **Geração de Anúncios**: Crie anúncios profissionais em PNG (1080x1080) com um clique
- **Download Direto**: Baixe os anúncios gerados instantaneamente
- **Interface Responsiva**: Funciona perfeitamente em desktop e mobile

## 🚀 Como Executar a Aplicação

### Pré-requisitos
- Python 3.11 ou superior
- Sistema operacional: Windows, macOS ou Linux

### Passo a Passo

1. **Navegue até o diretório da aplicação**:
   ```bash
   cd anuncio-generator
   ```

2. **Ative o ambiente virtual**:
   ```bash
   source venv/bin/activate
   ```
   
   *No Windows, use:*
   ```bash
   venv\\Scripts\\activate
   ```

3. **Instale as dependências** (se necessário):
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**:
   ```bash
   python src/main.py
   ```

5. **Acesse a aplicação**:
   - Abra seu navegador
   - Vá para: `http://localhost:5000`

## 📊 Dados dos Produtos

A aplicação carrega automaticamente os produtos do arquivo `src/produtos.csv`. Este arquivo contém:

- **3.779 produtos** com desconto superior a 20%
- **189 páginas** de produtos (20 produtos por página)
- Informações completas: título, preços, desconto, categoria, avaliação, links

### Campos Disponíveis:
- Título do produto
- Preço original e promocional
- Percentual de desconto
- Categoria
- Avaliação (estrelas)
- Link da imagem
- Link do produto

## 🎨 Geração de Anúncios

### Características dos Anúncios Gerados:
- **Formato**: PNG 1080x1080 pixels
- **Layout Profissional**: Baseado no modelo fornecido
- **Elementos Incluídos**:
  - Nome da loja (ESCOLHASHOP)
  - Título do produto
  - Preços (original riscado e promocional)
  - Percentual de desconto
  - Área para imagem do produto
  - Design atrativo com cores contrastantes

### Como Gerar um Anúncio:
1. Navegue pelos produtos ou use a busca
2. Clique no botão "🎨 Gerar Anúncio" do produto desejado
3. Aguarde a geração (alguns segundos)
4. Clique em "📥 Baixar Anúncio PNG" para salvar

## 🔧 Estrutura do Projeto

```
anuncio-generator/
├── src/
│   ├── routes/
│   │   ├── produtos.py      # API para produtos e geração de anúncios
│   │   └── user.py          # API de usuários (template)
│   ├── models/
│   │   └── user.py          # Modelos de dados
│   ├── static/
│   │   ├── index.html       # Interface principal
│   │   └── anuncio_modelo.png # Modelo de referência
│   ├── database/
│   │   └── app.db           # Banco de dados SQLite
│   ├── produtos.csv         # Dados dos produtos da Shopee
│   └── main.py              # Aplicação principal Flask
├── venv/                    # Ambiente virtual Python
├── requirements.txt         # Dependências do projeto
└── README.md               # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Geração de Imagens**: Pillow (PIL)
- **Banco de Dados**: SQLite
- **Estilo**: CSS Grid, Flexbox, Gradientes

## 📱 Interface da Aplicação

### Tela Principal:
- **Cabeçalho**: Título e descrição da aplicação
- **Controles**: Barra de busca e botões de ação
- **Estatísticas**: Total de produtos, página atual, total de páginas
- **Grid de Produtos**: Cards com informações e botão de geração
- **Paginação**: Navegação entre páginas

### Modal de Anúncio:
- **Visualização**: Preview do anúncio gerado
- **Download**: Botão para baixar em PNG
- **Responsivo**: Adapta-se a diferentes tamanhos de tela

## 🎯 Casos de Uso

### Para Afiliados:
- Encontre rapidamente produtos com alto desconto
- Gere anúncios profissionais em segundos
- Use nos stories, posts e reels das redes sociais
- Economize tempo na criação de conteúdo

### Para Lojas:
- Promova produtos em liquidação
- Crie materiais de marketing padronizados
- Destaque ofertas especiais
- Mantenha identidade visual consistente

## 🔄 Atualizando os Produtos

Para atualizar os produtos:

1. Substitua o arquivo `src/produtos.csv` pelo novo CSV da Shopee
2. Reinicie a aplicação
3. Os novos produtos serão carregados automaticamente

**Formato do CSV**: O arquivo deve manter a mesma estrutura com as colunas:
- `title`, `price`, `sale_price`, `discount_percentage`, `image_link`, `product_link`, etc.

## 🚨 Solução de Problemas

### Erro ao Carregar Produtos:
- Verifique se o arquivo `src/produtos.csv` existe
- Confirme se o formato do CSV está correto
- Reinicie a aplicação

### Erro na Geração de Anúncios:
- Verifique se a biblioteca Pillow está instalada: `pip install Pillow`
- Confirme se há espaço em disco suficiente
- Tente com outro produto

### Aplicação Não Abre:
- Verifique se a porta 5000 está livre
- Confirme se o ambiente virtual está ativo
- Verifique se todas as dependências estão instaladas

## 📞 Suporte

Se encontrar problemas:

1. Verifique se seguiu todos os passos de instalação
2. Confirme se o ambiente virtual está ativo
3. Verifique se todas as dependências estão instaladas
4. Reinicie a aplicação

## 🎉 Pronto para Usar!

Sua aplicação está configurada e pronta para gerar anúncios profissionais automaticamente. Aproveite a praticidade de ter milhares de produtos organizados e a capacidade de criar materiais de marketing em segundos!

---

**Desenvolvido com ❤️ para facilitar o trabalho de afiliados e profissionais de marketing digital.**

