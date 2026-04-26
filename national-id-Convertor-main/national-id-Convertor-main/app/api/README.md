# National ID Converter API

Backend API endpoints for the National ID Converter application.

## Endpoints

### 1. POST /api/convert
Convert and validate a national ID number.

**Request Body:**
```json
{
  "id": "12345678901234"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "isValid": true,
    "format": "Egyptian National ID",
    "extractedInfo": {
      "dateOfBirth": "1990-01-15",
      "gender": "Male",
      "placeOfIssue": "Governorate Code: 01",
      "checksum": "5"
    },
    "convertedFormats": {
      "Original": "12345678901234",
      "Standard Format": "1234567-89-0123-4",
      "With Spaces": "1234 5678 9012 34",
      "Grouped Format": "1-234567-890123-4",
      "Readable": "12/34/56 789 0123 4"
    }
  }
}
```

**GET /api/convert?id=12345678901234**
Same functionality but using query parameter.

---

### 2. POST /api/validate
Validate a national ID with optional format specification.

**Request Body:**
```json
{
  "id": "12345678901234",
  "format": "egyptian" // optional: "egyptian" | "saudi"
}
```

**Response:**
```json
{
  "success": true,
  "isValid": true,
  "format": "Egyptian National ID",
  "data": {
    "isValid": true,
    "format": "Egyptian National ID",
    "extractedInfo": { ... },
    "convertedFormats": { ... }
  }
}
```

---

### 3. POST /api/batch
Convert multiple IDs in a single request (max 100).

**Request Body:**
```json
{
  "ids": [
    "12345678901234",
    "98765432109876",
    "11111111111111"
  ]
}
```

**Response:**
```json
{
  "success": true,
  "total": 3,
  "successCount": 2,
  "failureCount": 1,
  "results": [
    {
      "index": 0,
      "id": "12345678901234",
      "success": true,
      "data": { ... }
    },
    {
      "index": 1,
      "id": "98765432109876",
      "success": true,
      "data": { ... }
    },
    {
      "index": 2,
      "id": "11111111111111",
      "success": false,
      "error": "Invalid ID format"
    }
  ]
}
```

---

### 4. POST /api/formats
Convert ID to a specific format.

**Request Body:**
```json
{
  "id": "12345678901234",
  "format": "dashes" // "dashes" | "spaces" | "dots" | "no-separator"
}
```

**Response:**
```json
{
  "success": true,
  "original": "12345678901234",
  "format": "dashes",
  "converted": "1234-5678-9012-34"
}
```

---

### 5. GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "National ID Converter API",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "error": "Error message",
  "message": "Detailed error message (optional)"
}
```

**Status Codes:**
- `400` - Bad Request (invalid input)
- `500` - Internal Server Error

## Usage Examples

### Using fetch in JavaScript/TypeScript:

```typescript
// Convert ID
const response = await fetch('/api/convert', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ id: '12345678901234' }),
});
const data = await response.json();

// Validate ID
const validateResponse = await fetch('/api/validate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ id: '12345678901234', format: 'egyptian' }),
});
const validateData = await validateResponse.json();

// Batch convert
const batchResponse = await fetch('/api/batch', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ ids: ['12345678901234', '98765432109876'] }),
});
const batchData = await batchResponse.json();
```

## Rate Limiting

Currently, there are no rate limits implemented. For production use, consider adding rate limiting middleware.

## Security Notes

- All endpoints validate input data
- IDs are sanitized before processing
- Maximum batch size is limited to 100 IDs
- Error messages don't expose sensitive information

