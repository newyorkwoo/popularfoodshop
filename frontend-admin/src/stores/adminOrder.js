import { defineStore } from 'pinia'
import { ref } from 'vue'

const SEED_VERSION = 3

const SEED_ORDERS = [
  // ── Jan 25 ──
  {
    id: 1, orderNumber: 'PFS20250125001', customer: '王小明', date: '2025-01-25', total: 2560, status: 'processing',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '王小明', phone: '0912-345-678', address: '台北市大安區美食路 123 號 5 樓', method: '宅配' },
    customerInfo: { name: '王小明', email: 'wang@example.com', phone: '0912-345-678' },
    subtotal: 2560, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 2, orderNumber: 'PFS20250125002', customer: '李美麗', date: '2025-01-25', total: 1890, status: 'pending',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 2, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '李美麗', phone: '0923-456-789', address: '台北市信義區食光大道 456 號', method: '超商取貨' },
    customerInfo: { name: '李美麗', email: 'li@example.com', phone: '0923-456-789' },
    subtotal: 1830, shippingFee: 60, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── Jan 24 ──
  {
    id: 3, orderNumber: 'PFS20250124003', customer: '張大華', date: '2025-01-24', total: 3200, status: 'shipped',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 2, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 2, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '張大華', phone: '0934-567-890', address: '新北市板橋區味覺街 789 號 3 樓', method: '宅配' },
    customerInfo: { name: '張大華', email: 'zhang@example.com', phone: '0934-567-890' },
    subtotal: 3040, shippingFee: 160, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 4, orderNumber: 'PFS20250124004', customer: '陳小芳', date: '2025-01-24', total: 680, status: 'completed',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '陳小芳', phone: '0945-678-901', address: '桃園市中壢區美味巷 12 號', method: '超商取貨' },
    customerInfo: { name: '陳小芳', email: 'chen@example.com', phone: '0945-678-901' },
    subtotal: 680, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  // ── Jan 23 ──
  {
    id: 5, orderNumber: 'PFS20250123005', customer: '林志偉', date: '2025-01-23', total: 950, status: 'completed',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '林志偉', phone: '0956-789-012', address: '台中市西屯區饕客路 88 號', method: '宅配' },
    customerInfo: { name: '林志偉', email: 'lin@example.com', phone: '0956-789-012' },
    subtotal: 950, shippingFee: 0, paymentMethod: '銀行轉帳', adminNote: '',
  },
  {
    id: 6, orderNumber: 'PFS20250123006', customer: '黃雅婷', date: '2025-01-23', total: 1580, status: 'cancelled',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 1, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '黃雅婷', phone: '0967-890-123', address: '高雄市前鎮區食尚路 66 號', method: '宅配' },
    customerInfo: { name: '黃雅婷', email: 'huang@example.com', phone: '0967-890-123' },
    subtotal: 1600, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── Jan 22 ──
  {
    id: 7, orderNumber: 'PFS20250122007', customer: '吳佳琳', date: '2025-01-22', total: 2400, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 2, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' }],
    shipping: { name: '吳佳琳', phone: '0978-901-234', address: '台北市中山區茶香路 22 號', method: '宅配' },
    customerInfo: { name: '吳佳琳', email: 'wu@example.com', phone: '0978-901-234' },
    subtotal: 2400, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 8, orderNumber: 'PFS20250122008', customer: '許文豪', date: '2025-01-22', total: 3840, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 3, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '許文豪', phone: '0989-012-345', address: '新北市永和區美味街 33 號', method: '宅配' },
    customerInfo: { name: '許文豪', email: 'hsu@example.com', phone: '0989-012-345' },
    subtotal: 3840, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── Jan 20 ──
  {
    id: 9, orderNumber: 'PFS20250120009', customer: '趙雅芬', date: '2025-01-20', total: 1360, status: 'completed',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 2, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '趙雅芬', phone: '0911-111-222', address: '台中市北屯區橄欖路 15 號', method: '宅配' },
    customerInfo: { name: '趙雅芬', email: 'zhao@example.com', phone: '0911-111-222' },
    subtotal: 1360, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  {
    id: 10, orderNumber: 'PFS20250120010', customer: '劉建志', date: '2025-01-20', total: 1600, status: 'shipped',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 1, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '劉建志', phone: '0922-333-444', address: '高雄市左營區和牛巷 7 號', method: '宅配' },
    customerInfo: { name: '劉建志', email: 'liu@example.com', phone: '0922-333-444' },
    subtotal: 1600, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── Jan 18 ──
  {
    id: 11, orderNumber: 'PFS20250118011', customer: '蔡佩怡', date: '2025-01-18', total: 1900, status: 'completed',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 2, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '蔡佩怡', phone: '0933-555-666', address: '台南市東區松露街 99 號', method: '超商取貨' },
    customerInfo: { name: '蔡佩怡', email: 'tsai@example.com', phone: '0933-555-666' },
    subtotal: 1900, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 12, orderNumber: 'PFS20250118012', customer: '楊宗翰', date: '2025-01-18', total: 960, status: 'completed',
    items: [{ name: '北海道十勝鮮奶油', category: '乳製品', quantity: 3, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '楊宗翰', phone: '0944-777-888', address: '桃園市龜山區乳品路 5 號', method: '宅配' },
    customerInfo: { name: '楊宗翰', email: 'yang@example.com', phone: '0944-777-888' },
    subtotal: 960, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  // ── Jan 16 ──
  {
    id: 13, orderNumber: 'PFS20250116013', customer: '鄭雅文', date: '2025-01-16', total: 2560, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '鄭雅文', phone: '0955-999-000', address: '新竹市東區和牛大道 18 號', method: '宅配' },
    customerInfo: { name: '鄭雅文', email: 'zheng@example.com', phone: '0955-999-000' },
    subtotal: 2560, shippingFee: 0, paymentMethod: '銀行轉帳', adminNote: '',
  },
  {
    id: 14, orderNumber: 'PFS20250116014', customer: '周俊宏', date: '2025-01-16', total: 1630, status: 'completed',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '周俊宏', phone: '0966-111-333', address: '台北市松山區美食街 50 號', method: '超商取貨' },
    customerInfo: { name: '周俊宏', email: 'zhou@example.com', phone: '0966-111-333' },
    subtotal: 1630, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── Jan 14 ──
  {
    id: 15, orderNumber: 'PFS20250114015', customer: '謝佳蓉', date: '2025-01-14', total: 1200, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' }],
    shipping: { name: '謝佳蓉', phone: '0977-222-444', address: '南投縣鹿谷鄉茶園路 1 號', method: '宅配' },
    customerInfo: { name: '謝佳蓉', email: 'xie@example.com', phone: '0977-222-444' },
    subtotal: 1200, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 16, orderNumber: 'PFS20250114016', customer: '何承恩', date: '2025-01-14', total: 640, status: 'completed',
    items: [{ name: '北海道十勝鮮奶油', category: '乳製品', quantity: 2, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '何承恩', phone: '0988-333-555', address: '台北市大同區乳香巷 8 號', method: '超商取貨' },
    customerInfo: { name: '何承恩', email: 'he@example.com', phone: '0988-333-555' },
    subtotal: 640, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  // ── Jan 12 ──
  {
    id: 17, orderNumber: 'PFS20250112017', customer: '曾雅惠', date: '2025-01-12', total: 3480, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '曾雅惠', phone: '0911-444-666', address: '台中市南屯區饕客路 30 號', method: '宅配' },
    customerInfo: { name: '曾雅惠', email: 'zeng@example.com', phone: '0911-444-666' },
    subtotal: 3510, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── Jan 10 ──
  {
    id: 18, orderNumber: 'PFS20250110018', customer: '蕭志豪', date: '2025-01-10', total: 1280, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '蕭志豪', phone: '0922-555-777', address: '高雄市三民區和牛路 12 號', method: '宅配' },
    customerInfo: { name: '蕭志豪', email: 'xiao@example.com', phone: '0922-555-777' },
    subtotal: 1280, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 19, orderNumber: 'PFS20250110019', customer: '葉淑芬', date: '2025-01-10', total: 2080, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 1, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '葉淑芬', phone: '0933-666-888', address: '台北市內湖區食材街 77 號', method: '宅配' },
    customerInfo: { name: '葉淑芬', email: 'ye@example.com', phone: '0933-666-888' },
    subtotal: 2200, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── Jan 8 ──
  {
    id: 20, orderNumber: 'PFS20250108020', customer: '廖家銘', date: '2025-01-08', total: 1900, status: 'completed',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 2, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '廖家銘', phone: '0944-777-999', address: '桃園市中壢區松露巷 25 號', method: '宅配' },
    customerInfo: { name: '廖家銘', email: 'liao@example.com', phone: '0944-777-999' },
    subtotal: 1900, shippingFee: 0, paymentMethod: '銀行轉帳', adminNote: '',
  },
  // ── 2026-02-01 ──
  {
    id: 21, orderNumber: 'PFS20260201001', customer: '邱怡君', date: '2026-02-01', total: 1280, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '邱怡君', phone: '0912-100-001', address: '台北市大安區忠孝東路 100 號', method: '宅配' },
    customerInfo: { name: '邱怡君', email: 'qiu@example.com', phone: '0912-100-001' },
    subtotal: 1280, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 22, orderNumber: 'PFS20260201002', customer: '潘柏翰', date: '2026-02-01', total: 2150, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '潘柏翰', phone: '0923-200-002', address: '新北市三重區中正路 55 號', method: '宅配' },
    customerInfo: { name: '潘柏翰', email: 'pan@example.com', phone: '0923-200-002' },
    subtotal: 2150, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── 2026-02-02 ──
  {
    id: 23, orderNumber: 'PFS20260202001', customer: '呂淑玲', date: '2026-02-02', total: 680, status: 'completed',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '呂淑玲', phone: '0934-300-003', address: '桃園市桃園區中山路 32 號', method: '超商取貨' },
    customerInfo: { name: '呂淑玲', email: 'lu@example.com', phone: '0934-300-003' },
    subtotal: 680, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  {
    id: 24, orderNumber: 'PFS20260202002', customer: '洪志成', date: '2026-02-02', total: 3200, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 2, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '洪志成', phone: '0945-400-004', address: '台中市西區民生路 88 號', method: '宅配' },
    customerInfo: { name: '洪志成', email: 'hong@example.com', phone: '0945-400-004' },
    subtotal: 3200, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-03 ──
  {
    id: 25, orderNumber: 'PFS20260203001', customer: '馬文傑', date: '2026-02-03', total: 1900, status: 'completed',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 2, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '馬文傑', phone: '0956-500-005', address: '台南市中西區民族路 12 號', method: '宅配' },
    customerInfo: { name: '馬文傑', email: 'ma@example.com', phone: '0956-500-005' },
    subtotal: 1900, shippingFee: 0, paymentMethod: '銀行轉帳', adminNote: '',
  },
  {
    id: 26, orderNumber: 'PFS20260203002', customer: '宋雅婷', date: '2026-02-03', total: 1880, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '宋雅婷', phone: '0967-600-006', address: '新北市永和區永貞路 33 號', method: '超商取貨' },
    customerInfo: { name: '宋雅婷', email: 'song@example.com', phone: '0967-600-006' },
    subtotal: 1880, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-04 ──
  {
    id: 27, orderNumber: 'PFS20260204001', customer: '范智勇', date: '2026-02-04', total: 2230, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '范智勇', phone: '0978-700-007', address: '台北市中山區南京東路 77 號', method: '宅配' },
    customerInfo: { name: '范智勇', email: 'fan@example.com', phone: '0978-700-007' },
    subtotal: 2230, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  {
    id: 28, orderNumber: 'PFS20260204002', customer: '石佩珊', date: '2026-02-04', total: 960, status: 'completed',
    items: [{ name: '北海道十勝鮮奶油', category: '乳製品', quantity: 3, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '石佩珊', phone: '0989-800-008', address: '桃園市龜山區文化路 15 號', method: '超商取貨' },
    customerInfo: { name: '石佩珊', email: 'shi@example.com', phone: '0989-800-008' },
    subtotal: 960, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  // ── 2026-02-05 ──
  {
    id: 29, orderNumber: 'PFS20260205001', customer: '江宏偉', date: '2026-02-05', total: 2400, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 2, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' }],
    shipping: { name: '江宏偉', phone: '0911-900-009', address: '台中市北屯區崇德路 200 號', method: '宅配' },
    customerInfo: { name: '江宏偉', email: 'jiang@example.com', phone: '0911-900-009' },
    subtotal: 2400, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 30, orderNumber: 'PFS20260205002', customer: '游美玲', date: '2026-02-05', total: 1360, status: 'completed',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 2, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '游美玲', phone: '0922-010-010', address: '高雄市左營區博愛路 88 號', method: '宅配' },
    customerInfo: { name: '游美玲', email: 'you@example.com', phone: '0922-010-010' },
    subtotal: 1360, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── 2026-02-06 ──
  {
    id: 31, orderNumber: 'PFS20260206001', customer: '鄧雅琪', date: '2026-02-06', total: 3840, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 3, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '鄧雅琪', phone: '0933-110-011', address: '台北市信義區松仁路 66 號', method: '宅配' },
    customerInfo: { name: '鄧雅琪', email: 'deng@example.com', phone: '0933-110-011' },
    subtotal: 3840, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 32, orderNumber: 'PFS20260206002', customer: '羅建中', date: '2026-02-06', total: 1270, status: 'completed',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 1, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '羅建中', phone: '0944-120-012', address: '新竹市東區光復路 120 號', method: '宅配' },
    customerInfo: { name: '羅建中', email: 'luo@example.com', phone: '0944-120-012' },
    subtotal: 1270, shippingFee: 0, paymentMethod: '銀行轉帳', adminNote: '',
  },
  // ── 2026-02-07 ──
  {
    id: 33, orderNumber: 'PFS20260207001', customer: '盧怡欣', date: '2026-02-07', total: 2480, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '盧怡欣', phone: '0955-130-013', address: '台北市松山區民生東路 150 號', method: '宅配' },
    customerInfo: { name: '盧怡欣', email: 'lu2@example.com', phone: '0955-130-013' },
    subtotal: 2480, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 34, orderNumber: 'PFS20260207002', customer: '方俊傑', date: '2026-02-07', total: 680, status: 'cancelled',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '方俊傑', phone: '0966-140-014', address: '台中市南屯區大墩路 30 號', method: '超商取貨' },
    customerInfo: { name: '方俊傑', email: 'fang@example.com', phone: '0966-140-014' },
    subtotal: 680, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── 2026-02-08 ──
  {
    id: 35, orderNumber: 'PFS20260208001', customer: '施佩臻', date: '2026-02-08', total: 3240, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '施佩臻', phone: '0977-150-015', address: '新北市板橋區文化路 200 號', method: '宅配' },
    customerInfo: { name: '施佩臻', email: 'shih@example.com', phone: '0977-150-015' },
    subtotal: 3240, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 36, orderNumber: 'PFS20260208002', customer: '段志遠', date: '2026-02-08', total: 1590, status: 'completed',
    items: [{ name: '北海道十勝鮮奶油', category: '乳製品', quantity: 2, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '段志遠', phone: '0988-160-016', address: '高雄市三民區建工路 55 號', method: '宅配' },
    customerInfo: { name: '段志遠', email: 'duan@example.com', phone: '0988-160-016' },
    subtotal: 1590, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  // ── 2026-02-09 ──
  {
    id: 37, orderNumber: 'PFS20260209001', customer: '姚雅慧', date: '2026-02-09', total: 1200, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' }],
    shipping: { name: '姚雅慧', phone: '0911-170-017', address: '台北市內湖區成功路 88 號', method: '宅配' },
    customerInfo: { name: '姚雅慧', email: 'yao@example.com', phone: '0911-170-017' },
    subtotal: 1200, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-10 ──
  {
    id: 38, orderNumber: 'PFS20260210001', customer: '朱家豪', date: '2026-02-10', total: 1920, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 2, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '朱家豪', phone: '0922-180-018', address: '台中市西屯區台灣大道 300 號', method: '宅配' },
    customerInfo: { name: '朱家豪', email: 'zhu@example.com', phone: '0922-180-018' },
    subtotal: 1920, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  {
    id: 39, orderNumber: 'PFS20260210002', customer: '余佳蓉', date: '2026-02-10', total: 1900, status: 'completed',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 2, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '余佳蓉', phone: '0933-190-019', address: '桃園市中壢區中央路 60 號', method: '超商取貨' },
    customerInfo: { name: '余佳蓉', email: 'yu@example.com', phone: '0933-190-019' },
    subtotal: 1900, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-11 ──
  {
    id: 40, orderNumber: 'PFS20260211001', customer: '傅智偉', date: '2026-02-11', total: 2040, status: 'completed',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 3, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '傅智偉', phone: '0944-200-020', address: '台南市安平區安北路 45 號', method: '宅配' },
    customerInfo: { name: '傅智偉', email: 'fu@example.com', phone: '0944-200-020' },
    subtotal: 2040, shippingFee: 0, paymentMethod: '銀行轉帳', adminNote: '',
  },
  {
    id: 41, orderNumber: 'PFS20260211002', customer: '高淑芬', date: '2026-02-11', total: 2150, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '高淑芬', phone: '0955-210-021', address: '新北市新莊區中正路 180 號', method: '宅配' },
    customerInfo: { name: '高淑芬', email: 'gao@example.com', phone: '0955-210-021' },
    subtotal: 2150, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-12 ──
  {
    id: 42, orderNumber: 'PFS20260212001', customer: '董建國', date: '2026-02-12', total: 2560, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '董建國', phone: '0966-220-022', address: '台北市大同區承德路 99 號', method: '宅配' },
    customerInfo: { name: '董建國', email: 'dong@example.com', phone: '0966-220-022' },
    subtotal: 2560, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 43, orderNumber: 'PFS20260212002', customer: '沈怡婷', date: '2026-02-12', total: 1000, status: 'completed',
    items: [{ name: '北海道十勝鮮奶油', category: '乳製品', quantity: 1, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' },
            { name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '沈怡婷', phone: '0977-230-023', address: '高雄市前鎮區中山路 150 號', method: '超商取貨' },
    customerInfo: { name: '沈怡婷', email: 'shen@example.com', phone: '0977-230-023' },
    subtotal: 1000, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── 2026-02-13 ──
  {
    id: 44, orderNumber: 'PFS20260213001', customer: '孫志明', date: '2026-02-13', total: 3350, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 2, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '孫志明', phone: '0988-240-024', address: '台北市萬華區漢中街 50 號', method: '宅配' },
    customerInfo: { name: '孫志明', email: 'sun@example.com', phone: '0988-240-024' },
    subtotal: 3350, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 45, orderNumber: 'PFS20260213002', customer: '鍾佩君', date: '2026-02-13', total: 1280, status: 'shipped',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '鍾佩君', phone: '0911-250-025', address: '新北市中和區景安路 70 號', method: '宅配' },
    customerInfo: { name: '鍾佩君', email: 'zhong@example.com', phone: '0911-250-025' },
    subtotal: 1280, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  // ── 2026-02-14 ──
  {
    id: 46, orderNumber: 'PFS20260214001', customer: '蘇俊宏', date: '2026-02-14', total: 3830, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 1, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '蘇俊宏', phone: '0922-260-026', address: '台北市大安區仁愛路 200 號', method: '宅配' },
    customerInfo: { name: '蘇俊宏', email: 'su@example.com', phone: '0922-260-026' },
    subtotal: 3830, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 47, orderNumber: 'PFS20260214002', customer: '韓雅萍', date: '2026-02-14', total: 2400, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 2, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' }],
    shipping: { name: '韓雅萍', phone: '0933-270-027', address: '台中市南區復興路 120 號', method: '宅配' },
    customerInfo: { name: '韓雅萍', email: 'han@example.com', phone: '0933-270-027' },
    subtotal: 2400, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  {
    id: 48, orderNumber: 'PFS20260214003', customer: '魏家銘', date: '2026-02-14', total: 2310, status: 'completed',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 2, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '魏家銘', phone: '0944-280-028', address: '新北市土城區中央路 80 號', method: '超商取貨' },
    customerInfo: { name: '魏家銘', email: 'wei@example.com', phone: '0944-280-028' },
    subtotal: 2310, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-15 ──
  {
    id: 49, orderNumber: 'PFS20260215001', customer: '秦美華', date: '2026-02-15', total: 2480, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' }],
    shipping: { name: '秦美華', phone: '0955-290-029', address: '台南市北區成功路 36 號', method: '宅配' },
    customerInfo: { name: '秦美華', email: 'qin@example.com', phone: '0955-290-029' },
    subtotal: 2480, shippingFee: 0, paymentMethod: '銀行轉帳', adminNote: '',
  },
  {
    id: 50, orderNumber: 'PFS20260215002', customer: '田建文', date: '2026-02-15', total: 1640, status: 'completed',
    items: [{ name: '北海道十勝鮮奶油', category: '乳製品', quantity: 3, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' },
            { name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '田建文', phone: '0966-300-030', address: '桃園市平鎮區環南路 22 號', method: '宅配' },
    customerInfo: { name: '田建文', email: 'tian@example.com', phone: '0966-300-030' },
    subtotal: 1640, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  // ── 2026-02-16 ──
  {
    id: 51, orderNumber: 'PFS20260216001', customer: '龔雅玲', date: '2026-02-16', total: 950, status: 'completed',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '龔雅玲', phone: '0977-310-031', address: '台北市中正區忠孝西路 10 號', method: '超商取貨' },
    customerInfo: { name: '龔雅玲', email: 'gong@example.com', phone: '0977-310-031' },
    subtotal: 950, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-17 ──
  {
    id: 52, orderNumber: 'PFS20260217001', customer: '賴志雄', date: '2026-02-17', total: 3200, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 2, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '賴志雄', phone: '0988-320-032', address: '新北市蘆洲區中正路 250 號', method: '宅配' },
    customerInfo: { name: '賴志雄', email: 'lai@example.com', phone: '0988-320-032' },
    subtotal: 3200, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 53, orderNumber: 'PFS20260217002', customer: '柯怡芳', date: '2026-02-17', total: 1880, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '柯怡芳', phone: '0911-330-033', address: '台中市東區建國路 55 號', method: '宅配' },
    customerInfo: { name: '柯怡芳', email: 'ke@example.com', phone: '0911-330-033' },
    subtotal: 1880, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── 2026-02-18 ──
  {
    id: 54, orderNumber: 'PFS20260218001', customer: '尤俊傑', date: '2026-02-18', total: 2220, status: 'completed',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 2, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 1, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '尤俊傑', phone: '0922-340-034', address: '高雄市鼓山區美術東路 80 號', method: '宅配' },
    customerInfo: { name: '尤俊傑', email: 'you2@example.com', phone: '0922-340-034' },
    subtotal: 2220, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 55, orderNumber: 'PFS20260218002', customer: '王小明', date: '2026-02-18', total: 1280, status: 'processing',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '王小明', phone: '0912-345-678', address: '台北市大安區美食路 123 號 5 樓', method: '宅配' },
    customerInfo: { name: '王小明', email: 'wang@example.com', phone: '0912-345-678' },
    subtotal: 1280, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-19 ──
  {
    id: 56, orderNumber: 'PFS20260219001', customer: '李美麗', date: '2026-02-19', total: 2150, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '李美麗', phone: '0923-456-789', address: '台北市信義區食光大道 456 號', method: '超商取貨' },
    customerInfo: { name: '李美麗', email: 'li@example.com', phone: '0923-456-789' },
    subtotal: 2150, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  {
    id: 57, orderNumber: 'PFS20260219002', customer: '張大華', date: '2026-02-19', total: 1360, status: 'completed',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 2, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '張大華', phone: '0934-567-890', address: '新北市板橋區味覺街 789 號 3 樓', method: '宅配' },
    customerInfo: { name: '張大華', email: 'zhang@example.com', phone: '0934-567-890' },
    subtotal: 1360, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-20 ──
  {
    id: 58, orderNumber: 'PFS20260220001', customer: '陳小芳', date: '2026-02-20', total: 1600, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 1, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '陳小芳', phone: '0945-678-901', address: '桃園市中壢區美味巷 12 號', method: '宅配' },
    customerInfo: { name: '陳小芳', email: 'chen@example.com', phone: '0945-678-901' },
    subtotal: 1600, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  {
    id: 59, orderNumber: 'PFS20260220002', customer: '林志偉', date: '2026-02-20', total: 950, status: 'shipped',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '林志偉', phone: '0956-789-012', address: '台中市西屯區饕客路 88 號', method: '宅配' },
    customerInfo: { name: '林志偉', email: 'lin@example.com', phone: '0956-789-012' },
    subtotal: 950, shippingFee: 0, paymentMethod: '銀行轉帳', adminNote: '',
  },
  // ── 2026-02-21 ──
  {
    id: 60, orderNumber: 'PFS20260221001', customer: '吳佳琳', date: '2026-02-21', total: 3600, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 3, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' }],
    shipping: { name: '吳佳琳', phone: '0978-901-234', address: '台北市中山區茶香路 22 號', method: '宅配' },
    customerInfo: { name: '吳佳琳', email: 'wu@example.com', phone: '0978-901-234' },
    subtotal: 3600, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 61, orderNumber: 'PFS20260221002', customer: '許文豪', date: '2026-02-21', total: 1960, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '許文豪', phone: '0989-012-345', address: '新北市永和區美味街 33 號', method: '宅配' },
    customerInfo: { name: '許文豪', email: 'hsu@example.com', phone: '0989-012-345' },
    subtotal: 1960, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── 2026-02-22 ──
  {
    id: 62, orderNumber: 'PFS20260222001', customer: '趙雅芬', date: '2026-02-22', total: 1590, status: 'completed',
    items: [{ name: '北海道十勝鮮奶油', category: '乳製品', quantity: 2, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '趙雅芬', phone: '0911-111-222', address: '台中市北屯區橄欖路 15 號', method: '宅配' },
    customerInfo: { name: '趙雅芬', email: 'zhao@example.com', phone: '0911-111-222' },
    subtotal: 1590, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 63, orderNumber: 'PFS20260222002', customer: '劉建志', date: '2026-02-22', total: 2480, status: 'cancelled',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '劉建志', phone: '0922-333-444', address: '高雄市左營區和牛巷 7 號', method: '宅配' },
    customerInfo: { name: '劉建志', email: 'liu@example.com', phone: '0922-333-444' },
    subtotal: 2480, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-23 ──
  {
    id: 64, orderNumber: 'PFS20260223001', customer: '蔡佩怡', date: '2026-02-23', total: 1630, status: 'completed',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '蔡佩怡', phone: '0933-555-666', address: '台南市東區松露街 99 號', method: '超商取貨' },
    customerInfo: { name: '蔡佩怡', email: 'tsai@example.com', phone: '0933-555-666' },
    subtotal: 1630, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  {
    id: 65, orderNumber: 'PFS20260223002', customer: '楊宗翰', date: '2026-02-23', total: 2560, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '楊宗翰', phone: '0944-777-888', address: '桃園市龜山區乳品路 5 號', method: '宅配' },
    customerInfo: { name: '楊宗翰', email: 'yang@example.com', phone: '0944-777-888' },
    subtotal: 2560, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  // ── 2026-02-24 ──
  {
    id: 66, orderNumber: 'PFS20260224001', customer: '鄭雅文', date: '2026-02-24', total: 1840, status: 'completed',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 2, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '鄭雅文', phone: '0955-999-000', address: '新竹市東區和牛大道 18 號', method: '宅配' },
    customerInfo: { name: '鄭雅文', email: 'zheng@example.com', phone: '0955-999-000' },
    subtotal: 1840, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 67, orderNumber: 'PFS20260224002', customer: '周俊宏', date: '2026-02-24', total: 1900, status: 'completed',
    items: [{ name: '義大利松露醬', category: '調味醬料', quantity: 2, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '周俊宏', phone: '0966-111-333', address: '台北市松山區美食街 50 號', method: '宅配' },
    customerInfo: { name: '周俊宏', email: 'zhou@example.com', phone: '0966-111-333' },
    subtotal: 1900, shippingFee: 0, paymentMethod: '貨到付款', adminNote: '',
  },
  // ── 2026-02-25 ──
  {
    id: 68, orderNumber: 'PFS20260225001', customer: '謝佳蓉', date: '2026-02-25', total: 3160, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '謝佳蓉', phone: '0977-222-444', address: '南投縣鹿谷鄉茶園路 1 號', method: '宅配' },
    customerInfo: { name: '謝佳蓉', email: 'xie@example.com', phone: '0977-222-444' },
    subtotal: 3160, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 69, orderNumber: 'PFS20260225002', customer: '何承恩', date: '2026-02-25', total: 1280, status: 'completed',
    items: [{ name: '北海道十勝鮮奶油', category: '乳製品', quantity: 4, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '何承恩', phone: '0988-333-555', address: '台北市大同區乳香巷 8 號', method: '超商取貨' },
    customerInfo: { name: '何承恩', email: 'he@example.com', phone: '0988-333-555' },
    subtotal: 1280, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  // ── 2026-02-26 ──
  {
    id: 70, orderNumber: 'PFS20260226001', customer: '曾雅惠', date: '2026-02-26', total: 3510, status: 'completed',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' }],
    shipping: { name: '曾雅惠', phone: '0911-444-666', address: '台中市南屯區饕客路 30 號', method: '宅配' },
    customerInfo: { name: '曾雅惠', email: 'zeng@example.com', phone: '0911-444-666' },
    subtotal: 3510, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 71, orderNumber: 'PFS20260226002', customer: '蕭志豪', date: '2026-02-26', total: 1880, status: 'shipped',
    items: [{ name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' },
            { name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 1, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' }],
    shipping: { name: '蕭志豪', phone: '0922-555-777', address: '高雄市三民區和牛路 12 號', method: '宅配' },
    customerInfo: { name: '蕭志豪', email: 'xiao@example.com', phone: '0922-555-777' },
    subtotal: 1880, shippingFee: 0, paymentMethod: '銀行轉帳', adminNote: '',
  },
  // ── 2026-02-27 ──
  {
    id: 72, orderNumber: 'PFS20260227001', customer: '葉淑芬', date: '2026-02-27', total: 2550, status: 'pending',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 1, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' },
            { name: '義大利松露醬', category: '調味醬料', quantity: 1, price: 950, image: 'https://placehold.co/60x60/F5F3FF/7C3AED?text=松露醬' },
            { name: '北海道十勝鮮奶油', category: '乳製品', quantity: 1, price: 320, image: 'https://placehold.co/60x60/EFF6FF/2563EB?text=鮮奶油' }],
    shipping: { name: '葉淑芬', phone: '0933-666-888', address: '台北市內湖區食材街 77 號', method: '宅配' },
    customerInfo: { name: '葉淑芬', email: 'ye@example.com', phone: '0933-666-888' },
    subtotal: 2550, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
  {
    id: 73, orderNumber: 'PFS20260227002', customer: '廖家銘', date: '2026-02-27', total: 3080, status: 'processing',
    items: [{ name: '台灣高山烏龍茶禮盒', category: '茶葉飲品', quantity: 2, price: 1200, image: 'https://placehold.co/60x60/ECFDF5/059669?text=烏龍茶' },
            { name: '有機冷壓初榨橄欖油', category: '調味醬料', quantity: 1, price: 680, image: 'https://placehold.co/60x60/F0FDF4/16A34A?text=橄欖油' }],
    shipping: { name: '廖家銘', phone: '0944-777-999', address: '桃園市中壢區松露巷 25 號', method: '宅配' },
    customerInfo: { name: '廖家銘', email: 'liao@example.com', phone: '0944-777-999' },
    subtotal: 3080, shippingFee: 0, paymentMethod: 'LINE Pay', adminNote: '',
  },
  {
    id: 74, orderNumber: 'PFS20260227003', customer: '邱怡君', date: '2026-02-27', total: 2560, status: 'pending',
    items: [{ name: '日本A5和牛火鍋片', category: '肉品海鮮', quantity: 2, price: 1280, image: 'https://placehold.co/60x60/FFF3E0/EA580C?text=和牛' }],
    shipping: { name: '邱怡君', phone: '0912-100-001', address: '台北市大安區忠孝東路 100 號', method: '宅配' },
    customerInfo: { name: '邱怡君', email: 'qiu@example.com', phone: '0912-100-001' },
    subtotal: 2560, shippingFee: 0, paymentMethod: '信用卡', adminNote: '',
  },
]

export const useAdminOrderStore = defineStore('adminOrder', () => {
  const storedVer = Number(localStorage.getItem('adminOrdersVer') || 0)
  const stored = storedVer >= SEED_VERSION ? localStorage.getItem('adminOrders') : null
  const orders = ref(stored ? JSON.parse(stored) : JSON.parse(JSON.stringify(SEED_ORDERS)))

  function persist() {
    localStorage.setItem('adminOrders', JSON.stringify(orders.value))
    localStorage.setItem('adminOrdersVer', String(SEED_VERSION))
  }

  function getOrder(id) {
    return orders.value.find(o => o.id === Number(id))
  }

  function updateStatus(id, status) {
    const order = getOrder(id)
    if (order) {
      order.status = status
      persist()
    }
  }

  function updateNote(id, note) {
    const order = getOrder(id)
    if (order) {
      order.adminNote = note
      persist()
    }
  }

  return { orders, getOrder, updateStatus, updateNote }
})
