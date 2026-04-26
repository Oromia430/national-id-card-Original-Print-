import { NextRequest, NextResponse } from 'next/server';
import { convertIDFormat } from '@/lib/idUtils';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { id, format } = body;

    if (!id || typeof id !== 'string') {
      return NextResponse.json(
        { error: 'ID is required and must be a string' },
        { status: 400 }
      );
    }

    if (!format || typeof format !== 'string') {
      return NextResponse.json(
        { error: 'Format is required and must be a string' },
        { status: 400 }
      );
    }

    const validFormats = ['dashes', 'spaces', 'dots', 'no-separator'];
    if (!validFormats.includes(format)) {
      return NextResponse.json(
        { error: `Format must be one of: ${validFormats.join(', ')}` },
        { status: 400 }
      );
    }

    const converted = convertIDFormat(id, format);

    return NextResponse.json({
      success: true,
      original: id,
      format,
      converted,
    });
  } catch (error) {
    console.error('Error converting format:', error);
    return NextResponse.json(
      { error: 'Internal server error', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

