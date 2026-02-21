import { defineStore } from 'pinia'
import { ref } from 'vue'

const SEED_VERSION = 2

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
