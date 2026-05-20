import { requestCounter } from '@/lib/metrics'

export async function POST(req: Request) {
  requestCounter.labels('/api/notify').inc()
  return new Response('Notification accepted')
}
