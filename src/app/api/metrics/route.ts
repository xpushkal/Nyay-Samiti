// app/api/metrics/route.ts

import { NextResponse } from 'next/server'
import { Registry, collectDefaultMetrics } from 'prom-client'

// Global registry
const register = new Registry()

// Prevent duplicate metric registration on hot reload
let metricsCollected = false
if (!metricsCollected) {
  collectDefaultMetrics({ register })
  metricsCollected = true
}

export async function GET() {
  const metrics = await register.metrics()
  return new NextResponse(metrics, {
    status: 200,
    headers: {
      'Content-Type': register.contentType,
    },
  })
}
