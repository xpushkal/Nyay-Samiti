import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

/**
 * GET /api/documents/[id]
 * Fetch document for ML analysis
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const documentId = params.id

    const document = await prisma.document.findUnique({
      where: { id: documentId },
    })

    if (!document) {
      return NextResponse.json(
        { error: 'Document not found' },
        { status: 404 }
      )
    }

    console.log(`📄 Document fetched: ${documentId}`)

    return NextResponse.json({
      document_id: document.id,
      name: document.name,
      content: document.content,
      content_type: document.contentType,
      size: document.size,
      uploaded_at: document.uploadedAt.toISOString(),
    })
  } catch (error: any) {
    console.error('❌ Failed to fetch document:', error)
    return NextResponse.json(
      {
        error: error.message,
      },
      { status: 500 }
    )
  }
}

/**
 * DELETE /api/documents/[id]
 * Delete document and all associated analyses
 */
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const documentId = params.id

    // Check if document exists
    const document = await prisma.document.findUnique({
      where: { id: documentId },
      include: {
        analyses: true,
      },
    })

    if (!document) {
      return NextResponse.json(
        { error: 'Document not found' },
        { status: 404 }
      )
    }

    // Delete all associated analyses first
    await prisma.analysis.deleteMany({
      where: { documentId: documentId },
    })

    // Delete the document
    await prisma.document.delete({
      where: { id: documentId },
    })

    console.log(`🗑️  Document deleted: ${documentId} (${document.name})`)
    console.log(`   - Removed ${document.analyses.length} associated analysis/analyses`)

    return NextResponse.json({
      success: true,
      message: 'Document and associated analyses deleted successfully',
      deletedDocument: {
        id: document.id,
        name: document.name,
      },
      deletedAnalyses: document.analyses.length,
    })
  } catch (error: any) {
    console.error('❌ Failed to delete document:', error)
    return NextResponse.json(
      {
        error: error.message,
      },
      { status: 500 }
    )
  }
}
