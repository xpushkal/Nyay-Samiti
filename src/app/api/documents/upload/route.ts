import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { mlService } from '@/lib/ml-service'

/**
 * POST /api/documents/upload
 * Upload document and trigger ML analysis
 */
export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File
    
    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      )
    }

    // Read file content
    const content = await file.text()

    // Store document in database
    const document = await prisma.document.create({
      data: {
        name: file.name,
        content: content,
        size: file.size,
        contentType: file.type || 'text/plain',
      },
    })

    // Create analysis record
    const analysis = await prisma.analysis.create({
      data: {
        documentId: document.id,
        status: 'pending',
        progress: 0,
      },
    })

        // Trigger ML analysis asynchronously
    setTimeout(async () => {
      try {
        await mlService.analyzeDocument({
          analysis_id: analysis.id,
          document_id: document.id,
          document_text: content,
          analysis_type: 'comprehensive',
        })
      } catch (error) {
        console.error('Failed to trigger ML analysis:', error)
        await prisma.analysis.update({
          where: { id: analysis.id },
          data: {
            status: 'failed',
            error: 'Failed to trigger ML analysis',
          },
        })
      }
    }, 100)

    console.log(`✅ Document uploaded: ${document.id}, Analysis: ${analysis.id}`)

    return NextResponse.json({
      success: true,
      document_id: document.id,
      analysis_id: analysis.id,
      message: 'Document uploaded and analysis queued',
    })
  } catch (error: any) {
    console.error('❌ Upload failed:', error)
    return NextResponse.json(
      {
        success: false,
        error: error.message,
      },
      { status: 500 }
    )
  }
}
