// National ID utility functions

export interface IDInfo {
  isValid: boolean;
  format?: string;
  extractedInfo?: {
    dateOfBirth?: string;
    gender?: string;
    placeOfIssue?: string;
    checksum?: string;
  };
  convertedFormats?: {
    [key: string]: string;
  };
}

// Validate Egyptian National ID (14 digits)
export function validateEgyptianID(id: string): IDInfo {
  const cleaned = id.replace(/\D/g, '');
  
  if (cleaned.length !== 14) {
    return { isValid: false };
  }

  // Extract date of birth (YYMMDD format)
  const year = parseInt(cleaned.substring(0, 2));
  const month = parseInt(cleaned.substring(2, 4));
  const day = parseInt(cleaned.substring(4, 6));
  
  // Determine century based on year
  let fullYear = 1900 + year;
  if (year < 20) {
    fullYear = 2000 + year;
  }

  // Extract gender (7th digit: 1-2 = male, 3-4 = female)
  const genderDigit = parseInt(cleaned[6]);
  const gender = genderDigit <= 2 ? 'Male' : 'Female';

  // Extract governorate code (8th-9th digits)
  const governorateCode = cleaned.substring(7, 9);

  // Extract serial number (10th-13th digits)
  const serialNumber = cleaned.substring(9, 13);

  // Validate checksum (14th digit)
  let sum = 0;
  for (let i = 0; i < 13; i++) {
    const digit = parseInt(cleaned[i]);
    if (i % 2 === 0) {
      sum += digit;
    } else {
      sum += digit * 2 > 9 ? digit * 2 - 9 : digit * 2;
    }
  }
  const checksum = (10 - (sum % 10)) % 10;
  const isValid = checksum === parseInt(cleaned[13]);

  return {
    isValid,
    format: 'Egyptian National ID',
    extractedInfo: {
      dateOfBirth: `${fullYear}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`,
      gender,
      placeOfIssue: `Governorate Code: ${governorateCode}`,
      checksum: cleaned[13],
    },
    convertedFormats: {
      'Original': cleaned,
      'Standard Format': `${cleaned.substring(0, 7)}-${cleaned.substring(7, 9)}-${cleaned.substring(9, 13)}-${cleaned[13]}`,
      'With Spaces': `${cleaned.substring(0, 4)} ${cleaned.substring(4, 8)} ${cleaned.substring(8, 12)} ${cleaned.substring(12)}`,
      'Grouped Format': `${cleaned.substring(0, 1)}-${cleaned.substring(1, 7)}-${cleaned.substring(7, 13)}-${cleaned[13]}`,
      'Readable': `${cleaned.substring(0, 2)}/${cleaned.substring(2, 4)}/${cleaned.substring(4, 6)} ${cleaned.substring(6, 9)} ${cleaned.substring(9, 13)} ${cleaned[13]}`,
    },
  };
}

// Validate Saudi National ID (10 digits)
export function validateSaudiID(id: string): IDInfo {
  const cleaned = id.replace(/\D/g, '');
  
  if (cleaned.length !== 10) {
    return { isValid: false };
  }

  // Extract date of birth (YYMMDD format from first 6 digits)
  const year = parseInt(cleaned.substring(0, 2));
  const month = parseInt(cleaned.substring(2, 4));
  const day = parseInt(cleaned.substring(4, 6));
  
  let fullYear = 1400 + year; // Hijri calendar base

  // Extract gender (10th digit: 1 = male, 2 = female)
  const genderDigit = parseInt(cleaned[9]);
  const gender = genderDigit === 1 ? 'Male' : 'Female';

  return {
    isValid: true,
    format: 'Saudi National ID',
    extractedInfo: {
      dateOfBirth: `${fullYear}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')} (Hijri)`,
      gender,
    },
    convertedFormats: {
      'Original': cleaned,
      'Standard Format': `${cleaned.substring(0, 1)}-${cleaned.substring(1, 5)}-${cleaned.substring(5, 9)}-${cleaned[9]}`,
      'With Spaces': `${cleaned.substring(0, 1)} ${cleaned.substring(1, 5)} ${cleaned.substring(5, 9)} ${cleaned[9]}`,
      'With Dots': `${cleaned.substring(0, 1)}.${cleaned.substring(1, 5)}.${cleaned.substring(5, 9)}.${cleaned[9]}`,
    },
  };
}

// Generic ID validator that tries to detect format
export function validateID(id: string): IDInfo {
  const cleaned = id.replace(/\D/g, '');
  
  if (cleaned.length === 14) {
    return validateEgyptianID(id);
  } else if (cleaned.length === 10) {
    return validateSaudiID(id);
  } else if (cleaned.length === 9) {
    // US SSN format
    return {
      isValid: cleaned.length === 9,
      format: 'US SSN Format',
      convertedFormats: {
        'Standard': `${cleaned.substring(0, 3)}-${cleaned.substring(3, 5)}-${cleaned.substring(5)}`,
        'No Dashes': cleaned,
      },
    };
  } else if (cleaned.length >= 8 && cleaned.length <= 12) {
    // Generic format with multiple conversion options
    const formats: { [key: string]: string } = {
      'Original': cleaned,
      'With Dashes (4-4-4)': cleaned.match(/.{1,4}/g)?.join('-') || cleaned,
      'With Spaces (4-4-4)': cleaned.match(/.{1,4}/g)?.join(' ') || cleaned,
      'With Dots (4-4-4)': cleaned.match(/.{1,4}/g)?.join('.') || cleaned,
    };
    
    // Add format-specific conversions based on length
    if (cleaned.length === 9) {
      formats['SSN Format'] = `${cleaned.substring(0, 3)}-${cleaned.substring(3, 5)}-${cleaned.substring(5)}`;
    } else if (cleaned.length === 10) {
      formats['Phone Format'] = `(${cleaned.substring(0, 3)}) ${cleaned.substring(3, 6)}-${cleaned.substring(6)}`;
    } else if (cleaned.length === 12) {
      formats['Credit Card Style'] = `${cleaned.substring(0, 4)} ${cleaned.substring(4, 8)} ${cleaned.substring(8)}`;
    }
    
    return {
      isValid: true,
      format: 'Generic ID Format',
      convertedFormats: formats,
    };
  }

  return { isValid: false };
}

// Convert ID to different formats
export function convertIDFormat(id: string, targetFormat: string): string {
  const cleaned = id.replace(/\D/g, '');
  
  switch (targetFormat) {
    case 'dashes':
      return cleaned.match(/.{1,4}/g)?.join('-') || cleaned;
    case 'spaces':
      return cleaned.match(/.{1,4}/g)?.join(' ') || cleaned;
    case 'dots':
      return cleaned.match(/.{1,4}/g)?.join('.') || cleaned;
    case 'no-separator':
      return cleaned;
    default:
      return cleaned;
  }
}

