import { Counter, Registry, collectDefaultMetrics } from 'prom-client'

const register = new Registry()
collectDefaultMetrics({ register })

export const requestCounter = new Counter({
  name: 'http_requests_total',
  help: 'Total number of API requests',
  labelNames: ['route'],
})

register.registerMetric(requestCounter)
export { register }
