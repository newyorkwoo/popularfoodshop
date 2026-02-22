/**
 * Vite plugin: shared product status mock API.
 *
 * Serves a tiny JSON-file-backed REST endpoint so admin and consumer
 * frontends can share product status (active / archived) without a
 * real backend.
 *
 * Endpoints:
 *   GET  /api/product-status          → returns { [productId]: status }
 *   POST /api/product-status          → body { id, status } → writes to file
 *   POST /api/product-status/bulk     → body { products: [{ id, status }] }
 */
import fs from 'node:fs'
import path from 'node:path'

const STATUS_FILE = path.resolve(
  new URL('.', import.meta.url).pathname,
  '../shared/product-status.json',
)

function readStatus() {
  try {
    return JSON.parse(fs.readFileSync(STATUS_FILE, 'utf-8'))
  } catch {
    return {}
  }
}

function writeStatus(data) {
  fs.mkdirSync(path.dirname(STATUS_FILE), { recursive: true })
  fs.writeFileSync(STATUS_FILE, JSON.stringify(data, null, 2), 'utf-8')
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = ''
    req.on('data', (chunk) => (body += chunk))
    req.on('end', () => {
      try {
        resolve(JSON.parse(body))
      } catch {
        reject(new Error('Invalid JSON'))
      }
    })
  })
}

export default function sharedProductStatus() {
  return {
    name: 'shared-product-status',
    configureServer(server) {
      // GET /api/product-status
      server.middlewares.use('/api/product-status', async (req, res, next) => {
        // CORS – allow cross-port requests during dev
        res.setHeader('Access-Control-Allow-Origin', '*')
        res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type')

        if (req.method === 'OPTIONS') {
          res.statusCode = 204
          return res.end()
        }

        // GET – return entire status map
        if (req.method === 'GET') {
          res.setHeader('Content-Type', 'application/json')
          return res.end(JSON.stringify(readStatus()))
        }

        // POST /api/product-status/bulk
        if (req.method === 'POST' && req.url?.startsWith('/bulk')) {
          try {
            const { products } = await parseBody(req)
            const status = readStatus()
            for (const p of products) {
              status[String(p.id)] = p.status
            }
            writeStatus(status)
            res.setHeader('Content-Type', 'application/json')
            return res.end(JSON.stringify({ ok: true }))
          } catch (e) {
            res.statusCode = 400
            return res.end(JSON.stringify({ error: e.message }))
          }
        }

        // POST /api/product-status  (single)
        if (req.method === 'POST') {
          try {
            const { id, status: newStatus } = await parseBody(req)
            const status = readStatus()
            status[String(id)] = newStatus
            writeStatus(status)
            res.setHeader('Content-Type', 'application/json')
            return res.end(JSON.stringify({ ok: true }))
          } catch (e) {
            res.statusCode = 400
            return res.end(JSON.stringify({ error: e.message }))
          }
        }

        next()
      })
    },
  }
}
