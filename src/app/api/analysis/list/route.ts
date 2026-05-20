import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

/**
 * GET /api/analysis/list
 * Get all analyses with stats
 */
export async function GET() {
  try {
    const analyses = await prisma.analysis.findMany({
      include: {
        document: {
          select: {
            name: true,
          },
        },
      },
      orderBy: {
        startedAt: 'desc',
      },
      take: 50,
    })

    const stats = await prisma.analysis.groupBy({
      by: ['status'],
      _count: true,
    })

    const statsMap = {
      total: analyses.length,
      completed: stats.find(s => s.status === 'completed')?._count || 0,
      processing: stats.find(s => s.status === 'processing')?._count || 0,
      failed: stats.find(s => s.status === 'failed')?._count || 0,
    }

    const formattedAnalyses = analyses.map(analysis => ({
      id: analysis.id,
      documentId: analysis.documentId,
      documentName: analysis.document.name,
      status: analysis.status,
      progress: analysis.progress,
      results: analysis.results,
      startedAt: analysis.startedAt.toISOString(),
      completedAt: analysis.completedAt?.toISOString(),
    }))

    return NextResponse.json({
      analyses: formattedAnalyses,
      stats: statsMap,
    })
  } catch (error: any) {
    console.error('❌ Failed to fetch analyses:', error)
    return NextResponse.json(
      {
        error: error.message,
        analyses: [],
        stats: { total: 0, completed: 0, processing: 0, failed: 0 },
      },
      { status: 500 }
    )
  }
}
