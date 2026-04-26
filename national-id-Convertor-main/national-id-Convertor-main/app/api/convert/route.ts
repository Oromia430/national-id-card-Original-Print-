import { NextRequest, NextResponse } from 'next/server';
import { validateID, type IDInfo } from '@/lib/idUtils';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { id } = body;

    if (!id || typeof id !== 'string') {
      return NextResponse.json(
        { error: 'ID is required and must be a string' },
        { status: 400 }
      );
    }

    if (id.trim().length === 0) {
      return NextResponse.json(
        { error: 'ID cannot be empty' },
        { status: 400 }
      );
    }

    // Validate and convert the ID
    const result: IDInfo = validateID(id);

    return NextResponse.json({
      success: true,
      data: result,
    });
  } catch (error) {
    console.error('Error converting ID:', error);
    return NextResponse.json(
      { error: 'Internal server error', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const id = searchParams.get('id');

  if (!id) {
    return NextResponse.json(
      { error: 'ID parameter is required' },
      { status: 400 }
    );
  }

  try {
    const result: IDInfo = validateID(id);

    return NextResponse.json({
      success: true,
      data: result,
    });
  } catch (error) {
    console.error('Error converting ID:', error);
    return NextResponse.json(
      { error: 'Internal server error', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

