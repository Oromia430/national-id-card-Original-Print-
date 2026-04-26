# National ID Converter Dashboard

A modern web application for converting, validating, and extracting information from national ID numbers.

## Features

- ✅ **ID Conversion**: Convert IDs between different formats (with dashes, spaces, dots, etc.)
- ✅ **ID Validation**: Validate national ID numbers based on country-specific rules
- ✅ **Information Extraction**: Extract embedded information like date of birth, gender, and place of issue
- ✅ **Multiple Format Support**: Supports Egyptian (14 digits), Saudi (10 digits), and other formats
- ✅ **Modern UI**: Beautiful, responsive design with dark mode support
- ✅ **Copy to Clipboard**: Easy copy functionality for converted formats

## Supported ID Formats

- **Egyptian National ID**: 14 digits
  - Extracts: Date of birth, gender, governorate code, checksum validation
- **Saudi National ID**: 10 digits
  - Extracts: Date of birth (Hijri calendar), gender
- **Generic Formats**: 8-12 digits
  - Format conversion support

## Tech Stack

- **Next.js 14**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Lucide React**: Icons

## Project Structure

```
├── app/
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page
│   └── globals.css      # Global styles
├── components/
│   └── IDConverter.tsx  # Main converter component
├── lib/
│   └── idUtils.ts       # ID validation and conversion utilities
└── package.json
```

## Usage

1. Enter a national ID number in the input field
2. Click "Convert" or press Enter
3. View validation results, extracted information, and converted formats
4. Click the copy icon to copy any converted format to clipboard

## License

MIT

