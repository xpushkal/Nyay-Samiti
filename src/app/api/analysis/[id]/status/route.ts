import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

/**
 * PATCH /api/analysis/[id]/status
 * Update analysis status and progress
 */
export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json()
    const { status, progress, message } = body
    const analysisId = params.id

    const analysis = await prisma.analysis.update({
      where: { id: analysisId },
      data: {
        status,
        progress: progress || 0,
      },
    })

    console.log(`📊 Analysis ${analysisId} updated: ${status} (${progress}%)`)

    return NextResponse.json({
      success: true,
      message: `Status updated to ${status}`,
      data: {
        analysis_id: analysis.id,
        status: analysis.status,
        progress: analysis.progress,
        started_at: analysis.startedAt.toISOString(),
      },
    })
  } catch (error: any) {
    console.error('❌ Failed to update analysis status:', error)
    return NextResponse.json(
      {
        success: false,
        error: error.message,
      },
      { status: 500 }
    )
  }
}

/**
 * GET /api/analysis/[id]/status
 * Get current analysis status
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const analysisId = params.id

    const analysis = await prisma.analysis.findUnique({
      where: { id: analysisId },
      include: {
        document: {
          select: {
            name: true,
          },
        },
      },
    })

    if (!analysis) {
      return NextResponse.json(
        { error: 'Analysis not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      analysis_id: analysis.id,
      status: analysis.status,
      progress: analysis.progress,
      started_at: analysis.startedAt.toISOString(),
      completed_at: analysis.completedAt?.toISOString() || null,
      document_name: analysis.document.name,
    })
  } catch (error: any) {
    console.error('❌ Failed to get analysis status:', error)
    return NextResponse.json(
      {
        error: error.message,
      },
      { status: 500 }
    )
  }
}
