import { NextRequest, NextResponse } from 'next/server';
import { validateID, validateEgyptianID, validateSaudiID, type IDInfo } from '@/lib/idUtils';

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

    let result: IDInfo;

    // If format is specified, use specific validator
    if (format === 'egyptian') {
      result = validateEgyptianID(id);
    } else if (format === 'saudi') {
      result = validateSaudiID(id);
    } else {
      // Auto-detect format
      result = validateID(id);
    }

    return NextResponse.json({
      success: true,
      isValid: result.isValid,
      format: result.format,
      data: result,
    });
  } catch (error) {
    console.error('Error validating ID:', error);
    return NextResponse.json(
      { error: 'Internal server error', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

