import { NextRequest, NextResponse } from 'next/server';
import { validateID, type IDInfo } from '@/lib/idUtils';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { ids } = body;

    if (!ids || !Array.isArray(ids)) {
      return NextResponse.json(
        { error: 'ids must be an array' },
        { status: 400 }
      );
    }

    if (ids.length === 0) {
      return NextResponse.json(
        { error: 'ids array cannot be empty' },
        { status: 400 }
      );
    }

    if (ids.length > 100) {
      return NextResponse.json(
        { error: 'Maximum 100 IDs allowed per batch' },
        { status: 400 }
      );
    }

    const results = ids.map((id: string, index: number) => {
      try {
        if (typeof id !== 'string') {
          return {
            index,
            id,
            success: false,
            error: 'ID must be a string',
          };
        }

        const result: IDInfo = validateID(id);
        return {
          index,
          id,
          success: true,
          data: result,
        };
      } catch (error) {
        return {
          index,
          id,
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    });

    const successCount = results.filter((r) => r.success).length;
    const failureCount = results.length - successCount;

    return NextResponse.json({
      success: true,
      total: results.length,
      successCount,
      failureCount,
      results,
    });
  } catch (error) {
    console.error('Error processing batch:', error);
    return NextResponse.json(
      { error: 'Internal server error', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

