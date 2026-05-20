import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

/**
 * GET /api/documents/[id]/content
 * Get just document content (lightweight)
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const documentId = params.id

    const document = await prisma.document.findUnique({
      where: { id: documentId },
      select: {
        id: true,
        content: true,
        contentType: true,
      },
    })

    if (!document) {
      return NextResponse.json(
        { error: 'Document not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      document_id: document.id,
      content: document.content,
      content_type: document.contentType || 'text/plain',
    })
  } catch (error: any) {
    console.error('❌ Failed to fetch document content:', error)
    return NextResponse.json(
      {
        error: error.message,
      },
      { status: 500 }
    )
  }
}
