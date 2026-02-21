"""
Seed data script — 初始化資料庫種子資料
Usage: python -m app.seeds.seed
"""

import asyncio
import sys
from pathlib import Path

# Add root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session, init_db
from app.models.brand import Brand
from app.models.category import Category
from app.models.content import Announcement, Banner, FeaturedSection
from app.models.product import Product, ProductImage
from app.models.shipping import ShippingMethod
from app.models.user import User
from app.utils.helpers import generate_slug
from app.utils.security import hash_password


async def seed_users(db: AsyncSession):
    """建立預設管理員和測試帳號"""
    users = [
        User(
            email="admin@popularfoodshop.com",
            password_hash=hash_password("Admin@123456"),
            name="系統管理員",
            role="super_admin",
            is_active=True,
            is_verified=True,
            points=0,
            credits=0,
        ),
        User(
            email="editor@popularfoodshop.com",
            password_hash=hash_password("Editor@123456"),
            name="內容編輯",
            role="editor",
            is_active=True,
            is_verified=True,
            points=0,
            credits=0,
        ),
        User(
            email="user@example.com",
            password_hash=hash_password("User@123456"),
            name="測試會員",
            phone="0912345678",
            role="customer",
            is_active=True,
            is_verified=True,
            points=100,
            credits=0,
        ),
    ]
    for u in users:
        db.add(u)
    print(f"  ✓ Created {len(users)} users")


async def seed_categories(db: AsyncSession):
    """建立商品分類"""
    categories_data = [
        {"name": "零食餅乾", "slug": "snacks", "description": "各式零食、餅乾、糖果", "sort_order": 1, "children": [
            {"name": "洋芋片", "slug": "chips", "sort_order": 1},
            {"name": "巧克力", "slug": "chocolate", "sort_order": 2},
            {"name": "糖果", "slug": "candy", "sort_order": 3},
            {"name": "堅果", "slug": "nuts", "sort_order": 4},
        ]},
        {"name": "飲品", "slug": "beverages", "description": "茶飲、咖啡、果汁", "sort_order": 2, "children": [
            {"name": "茶飲", "slug": "tea", "sort_order": 1},
            {"name": "咖啡", "slug": "coffee", "sort_order": 2},
            {"name": "果汁", "slug": "juice", "sort_order": 3},
            {"name": "氣泡水", "slug": "sparkling-water", "sort_order": 4},
        ]},
        {"name": "即食料理", "slug": "ready-meals", "description": "即食、微波、加熱即食", "sort_order": 3, "children": [
            {"name": "泡麵", "slug": "instant-noodles", "sort_order": 1},
            {"name": "冷凍食品", "slug": "frozen-food", "sort_order": 2},
            {"name": "罐頭", "slug": "canned-food", "sort_order": 3},
        ]},
        {"name": "調味料", "slug": "seasonings", "description": "醬料、油、調味品", "sort_order": 4, "children": [
            {"name": "醬油", "slug": "soy-sauce", "sort_order": 1},
            {"name": "食用油", "slug": "cooking-oil", "sort_order": 2},
            {"name": "香料", "slug": "spices", "sort_order": 3},
        ]},
        {"name": "麵包烘焙", "slug": "bakery", "description": "麵包、蛋糕、烘焙材料", "sort_order": 5, "children": [
            {"name": "吐司麵包", "slug": "bread", "sort_order": 1},
            {"name": "蛋糕", "slug": "cake", "sort_order": 2},
            {"name": "烘焙材料", "slug": "baking-supplies", "sort_order": 3},
        ]},
        {"name": "有機健康", "slug": "organic", "description": "有機、無添加、健康食品", "sort_order": 6, "children": [
            {"name": "有機穀物", "slug": "organic-grains", "sort_order": 1},
            {"name": "保健食品", "slug": "supplements", "sort_order": 2},
            {"name": "養生茶", "slug": "herbal-tea", "sort_order": 3},
        ]},
    ]

    count = 0
    for cat_data in categories_data:
        children_data = cat_data.pop("children", [])
        parent = Category(**cat_data, image=f"https://placehold.co/400x300?text={cat_data['name']}")
        db.add(parent)
        await db.flush()
        count += 1

        for child_data in children_data:
            child = Category(**child_data, parent_id=parent.id, image=f"https://placehold.co/400x300?text={child_data['name']}")
            db.add(child)
            count += 1

    print(f"  ✓ Created {count} categories")


async def seed_brands(db: AsyncSession):
    """建立品牌"""
    brands_data = [
        {"name": "義美", "slug": "imei", "description": "台灣老字號食品品牌", "country": "台灣", "sort_order": 1},
        {"name": "統一", "slug": "uni-president", "description": "台灣最大食品集團", "country": "台灣", "sort_order": 2},
        {"name": "桂格", "slug": "quaker", "description": "全球知名穀物品牌", "country": "美國", "sort_order": 3},
        {"name": "明治", "slug": "meiji", "description": "日本百年食品品牌", "country": "日本", "sort_order": 4},
        {"name": "樂事", "slug": "lays", "description": "全球最受歡迎的洋芋片", "country": "美國", "sort_order": 5},
        {"name": "光泉", "slug": "kuangchuan", "description": "台灣知名乳品品牌", "country": "台灣", "sort_order": 6},
        {"name": "AGF", "slug": "agf", "description": "日本專業咖啡品牌", "country": "日本", "sort_order": 7},
        {"name": "金車", "slug": "kingcar", "description": "伯朗咖啡母公司", "country": "台灣", "sort_order": 8},
        {"name": "Lindt 瑞士蓮", "slug": "lindt", "description": "瑞士頂級巧克力", "country": "瑞士", "sort_order": 9},
        {"name": "日清", "slug": "nissin", "description": "杯麵發明者", "country": "日本", "sort_order": 10},
    ]
    for b in brands_data:
        brand = Brand(**b, logo=f"https://placehold.co/200x80?text={b['name']}")
        db.add(brand)
    print(f"  ✓ Created {len(brands_data)} brands")


async def seed_products(db: AsyncSession):
    """建立示範商品"""
    products_data = [
        {
            "name": "義美小泡芙 — 巧克力口味",
            "description": "經典台灣零食，酥脆外皮搭配濃郁巧克力內餡，一口一個剛剛好。",
            "price": 59,
            "sale_price": 49,
            "sku": "IMEI-PF-CHOC-001",
            "stock": 200,
            "unit": "包",
            "origin": "台灣",
            "shelf_life": "12 個月",
            "storage": "常溫保存，避免高溫",
            "category_slug": "snacks",
            "brand_slug": "imei",
            "is_new": False,
            "is_featured": True,
            "tags": ["零食", "巧克力", "義美"],
        },
        {
            "name": "樂事洋芋片 — 經典原味",
            "description": "嚴選優質馬鈴薯，薄切酥炸，撒上恰到好處的海鹽，口感輕脆。",
            "price": 45,
            "sku": "LAYS-OG-001",
            "stock": 300,
            "unit": "包",
            "origin": "台灣",
            "shelf_life": "9 個月",
            "storage": "常溫保存",
            "category_slug": "chips",
            "brand_slug": "lays",
            "is_new": False,
            "is_featured": True,
            "tags": ["洋芋片", "零食"],
        },
        {
            "name": "Lindt 瑞士蓮 Excellence 85%",
            "description": "85% 可可含量，口感醇厚，微苦回甘，巧克力愛好者首選。",
            "price": 189,
            "sale_price": 159,
            "sku": "LINDT-EX85-001",
            "stock": 80,
            "unit": "片",
            "origin": "瑞士",
            "shelf_life": "18 個月",
            "storage": "陰涼乾燥保存，避免陽光直射",
            "category_slug": "chocolate",
            "brand_slug": "lindt",
            "is_new": True,
            "is_featured": True,
            "tags": ["巧克力", "進口", "高可可"],
        },
        {
            "name": "AGF Blendy 濃縮咖啡球 — 無糖",
            "description": "日本 AGF 出品，一顆即溶，加入牛奶或水即可享受香醇咖啡。",
            "price": 199,
            "sku": "AGF-BLD-NS-001",
            "stock": 120,
            "unit": "袋",
            "origin": "日本",
            "shelf_life": "12 個月",
            "storage": "常溫保存",
            "category_slug": "coffee",
            "brand_slug": "agf",
            "is_new": True,
            "is_featured": False,
            "tags": ["咖啡", "即溶", "日本"],
        },
        {
            "name": "日清杯麵 — 海鮮味",
            "description": "經典杯麵，海鮮湯頭鮮美，加入蝦肉、魚板等豐富配料。",
            "price": 39,
            "sku": "NISSIN-CUP-SF-001",
            "stock": 500,
            "unit": "杯",
            "origin": "日本",
            "shelf_life": "8 個月",
            "storage": "常溫保存",
            "category_slug": "instant-noodles",
            "brand_slug": "nissin",
            "is_new": False,
            "is_featured": True,
            "tags": ["泡麵", "日本", "海鮮"],
        },
        {
            "name": "桂格大燕麥片",
            "description": "100% 澳洲進口燕麥，高纖維、低 GI，健康早餐首選。",
            "price": 149,
            "sale_price": 129,
            "sku": "QKR-OAT-001",
            "stock": 150,
            "unit": "罐",
            "origin": "澳洲",
            "shelf_life": "24 個月",
            "storage": "開封後密封保存",
            "category_slug": "organic-grains",
            "brand_slug": "quaker",
            "is_new": False,
            "is_featured": False,
            "tags": ["燕麥", "健康", "早餐"],
        },
        {
            "name": "光泉鮮乳 — 全脂 936ml",
            "description": "每日新鮮直送，100% 台灣乳源，濃醇香的好味道。",
            "price": 78,
            "sku": "KC-MILK-936-001",
            "stock": 60,
            "unit": "瓶",
            "origin": "台灣",
            "shelf_life": "14 天",
            "storage": "冷藏 0-7°C",
            "category_slug": "beverages",
            "brand_slug": "kuangchuan",
            "is_new": False,
            "is_featured": False,
            "tags": ["鮮乳", "冷藏"],
        },
        {
            "name": "金車伯朗咖啡 — 藍山風味",
            "description": "經典罐裝咖啡，藍山風味，方便攜帶，隨時享受咖啡時光。",
            "price": 25,
            "sku": "KC-BC-BM-001",
            "stock": 400,
            "unit": "罐",
            "origin": "台灣",
            "shelf_life": "12 個月",
            "storage": "常溫保存",
            "category_slug": "coffee",
            "brand_slug": "kingcar",
            "is_new": False,
            "is_featured": False,
            "tags": ["咖啡", "罐裝"],
        },
        {
            "name": "明治巧克力 — 牛奶口味",
            "description": "日本明治經典牛奶巧克力，細膩滑順，甜而不膩。",
            "price": 69,
            "sku": "MEIJI-CHOC-MILK-001",
            "stock": 180,
            "unit": "盒",
            "origin": "日本",
            "shelf_life": "12 個月",
            "storage": "陰涼保存",
            "category_slug": "chocolate",
            "brand_slug": "meiji",
            "is_new": False,
            "is_featured": True,
            "tags": ["巧克力", "日本", "明治"],
        },
        {
            "name": "統一肉燥麵 — 經典原味 5入",
            "description": "台灣經典泡麵，濃郁肉燥醬包，懷舊好味道。",
            "price": 55,
            "sku": "UNI-MR-OG-005",
            "stock": 350,
            "unit": "袋",
            "origin": "台灣",
            "shelf_life": "8 個月",
            "storage": "常溫保存",
            "category_slug": "instant-noodles",
            "brand_slug": "uni-president",
            "is_new": False,
            "is_featured": False,
            "tags": ["泡麵", "統一", "肉燥"],
        },
    ]

    await db.flush()  # flush categories & brands

    # Fetch all categories and brands for mapping
    from sqlalchemy import select

    cat_result = await db.execute(select(Category))
    cats = {c.slug: c.id for c in cat_result.scalars().all()}

    brand_result = await db.execute(select(Brand))
    brands = {b.slug: b.id for b in brand_result.scalars().all()}

    for pd in products_data:
        category_slug = pd.pop("category_slug")
        brand_slug = pd.pop("brand_slug")

        product = Product(
            name=pd["name"],
            slug=generate_slug(pd["name"]),
            description=pd["description"],
            price=pd["price"],
            sale_price=pd.get("sale_price"),
            sku=pd["sku"],
            stock=pd["stock"],
            unit=pd.get("unit"),
            origin=pd.get("origin"),
            shelf_life=pd.get("shelf_life"),
            storage=pd.get("storage"),
            tags=pd.get("tags", []),
            category_id=cats.get(category_slug),
            brand_id=brands.get(brand_slug),
            is_active=True,
            is_new=pd.get("is_new", False),
            is_featured=pd.get("is_featured", False),
        )
        db.add(product)
        await db.flush()

        # Add placeholder image
        db.add(ProductImage(
            product_id=product.id,
            url=f"https://placehold.co/600x600?text={product.name[:10]}",
            alt_text=product.name,
            sort_order=0,
        ))

    print(f"  ✓ Created {len(products_data)} products")


async def seed_shipping_methods(db: AsyncSession):
    """建立運送方式"""
    methods = [
        ShippingMethod(name="宅配到府", code="home-delivery", description="黑貓宅急便，1-3 個工作天送達", fee=100, free_threshold=1500, estimated_days="1-3 天", sort_order=1),
        ShippingMethod(name="超商取貨", code="convenience-store", description="7-11 / 全家 / 萊爾富取貨", fee=60, free_threshold=800, estimated_days="2-4 天", sort_order=2),
        ShippingMethod(name="冷藏宅配", code="cold-delivery", description="冷藏專車配送", fee=200, free_threshold=2000, estimated_days="1-2 天", sort_order=3),
    ]
    for m in methods:
        db.add(m)
    print(f"  ✓ Created {len(methods)} shipping methods")


async def seed_content(db: AsyncSession):
    """建立首頁內容"""
    from datetime import datetime

    banners = [
        Banner(
            title="夏日特賣 全館85折",
            subtitle="限時三天，結帳輸入 SUMMER85",
            image_url="https://placehold.co/1920x600?text=Summer+Sale+85%25+OFF",
            mobile_image_url="https://placehold.co/800x800?text=Summer+Sale",
            link_url="/products?tag=summer",
            sort_order=1,
            is_active=True,
            starts_at=datetime.utcnow(),
        ),
        Banner(
            title="新品上架 — 瑞士蓮精品巧克力",
            subtitle="品味頂級可可的純粹",
            image_url="https://placehold.co/1920x600?text=Lindt+New+Arrival",
            mobile_image_url="https://placehold.co/800x800?text=Lindt",
            link_url="/brands/lindt",
            sort_order=2,
            is_active=True,
            starts_at=datetime.utcnow(),
        ),
        Banner(
            title="滿 $1500 免運費",
            subtitle="全站商品，輕鬆湊免運",
            image_url="https://placehold.co/1920x600?text=Free+Shipping+$1500",
            mobile_image_url="https://placehold.co/800x800?text=Free+Shipping",
            link_url="/products",
            sort_order=3,
            is_active=True,
            starts_at=datetime.utcnow(),
        ),
    ]
    for b in banners:
        db.add(b)

    announcements = [
        Announcement(
            title="🎉 新會員註冊即送 100 點購物金！",
            content="立即註冊成為會員，享受首購優惠",
            type="promotion",
            link_url="/register",
            is_active=True,
            starts_at=datetime.utcnow(),
        ),
        Announcement(
            title="📦 物流公告：颱風期間配送可能延遲",
            content="受天氣影響，部分地區配送時間可能延長 1-2 天",
            type="warning",
            is_active=True,
            starts_at=datetime.utcnow(),
        ),
    ]
    for a in announcements:
        db.add(a)

    sections = [
        FeaturedSection(
            title="本週精選",
            subtitle="編輯嚴選好物",
            type="product_grid",
            config={"filter": "is_featured", "limit": 8},
            sort_order=1,
            is_active=True,
        ),
        FeaturedSection(
            title="新品上架",
            subtitle="最新到貨商品",
            type="product_carousel",
            config={"filter": "is_new", "limit": 12},
            sort_order=2,
            is_active=True,
        ),
        FeaturedSection(
            title="熱銷排行",
            subtitle="大家都在買",
            type="product_ranking",
            config={"sort": "sold_count", "limit": 10},
            sort_order=3,
            is_active=True,
        ),
    ]
    for s in sections:
        db.add(s)

    print(f"  ✓ Created {len(banners)} banners, {len(announcements)} announcements, {len(sections)} featured sections")


async def main():
    print("🌱 Seeding database...")
    await init_db()

    async with async_session() as db:
        try:
            await seed_users(db)
            await seed_categories(db)
            await seed_brands(db)
            await seed_products(db)
            await seed_shipping_methods(db)
            await seed_content(db)
            await db.commit()
            print("\n✅ Seed complete!")
        except Exception as e:
            await db.rollback()
            print(f"\n❌ Seed failed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
