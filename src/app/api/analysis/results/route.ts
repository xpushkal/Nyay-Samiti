import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

/**
 * POST /api/analysis/results
 * Receive analysis results from ML service
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const {
      analysis_id,
      document_id,
      document_name,
      analysis_type,
      status,
      timestamp,
      results,
      metadata,
      error,
    } = body

    // Update analysis in database
    const analysis = await prisma.analysis.update({
      where: { id: analysis_id },
      data: {
        status: status,
        results: results,
        error: error,
        progress: status === 'completed' ? 100 : 0,
        completedAt: status === 'completed' ? new Date() : null,
      },
    })

    console.log(`✅ Analysis results received: ${analysis_id}`)

    return NextResponse.json({
      success: true,
      message: 'Analysis results received successfully',
      data: {
        analysis_id: analysis.id,
        stored_at: new Date().toISOString(),
      },
    })
  } catch (error: any) {
    console.error('❌ Failed to store analysis results:', error)
    return NextResponse.json(
      {
        success: false,
        error: error.message,
      },
      { status: 500 }
    )
  }
}
