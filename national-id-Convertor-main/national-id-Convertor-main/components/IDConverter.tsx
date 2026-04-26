'use client';

import React, { useState, useEffect } from 'react';
import { validateID, convertIDFormat, type IDInfo } from '@/lib/idUtils';
import { convertID as convertIDAPI } from '@/lib/api';
import { Copy, Check, AlertCircle, Info, Calendar, User, MapPin, RefreshCw, Server, Loader2 } from 'lucide-react';

export default function IDConverter() {
  const [idInput, setIdInput] = useState('');
  const [idInfo, setIdInfo] = useState<IDInfo | null>(null);
  const [copied, setCopied] = useState<string | null>(null);
  const [autoConvert, setAutoConvert] = useState(true);
  const [useAPI, setUseAPI] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (autoConvert && idInput.trim()) {
      handleConvert();
    } else if (!idInput.trim()) {
      setIdInfo(null);
      setError(null);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [idInput, autoConvert, useAPI]);

  const handleConvert = async () => {
    if (!idInput.trim()) {
      setIdInfo(null);
      setError(null);
      return;
    }

    setError(null);
    setLoading(true);

    try {
      if (useAPI) {
        // Use backend API
        const response = await convertIDAPI(idInput);
        if (response.success && response.data) {
          setIdInfo(response.data);
        } else {
          setError('Failed to convert ID');
        }
      } else {
        // Use client-side validation
        const result = validateID(idInput);
        setIdInfo(result);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setIdInfo(null);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text: string, format: string) => {
    navigator.clipboard.writeText(text);
    setCopied(format);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                National ID Converter
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Convert, validate, and extract information from national ID numbers
              </p>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Main Converter Card */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
          <div className="mb-6">
            <label htmlFor="id-input" className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
              Enter National ID Number
            </label>
            <div className="flex gap-3">
              <div className="flex-1 relative">
                <input
                  id="id-input"
                  type="text"
                  value={idInput}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setIdInput(e.target.value)}
                  onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === 'Enter' && handleConvert()}
                  placeholder="Enter your national ID number (e.g., 12345678901234)"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white outline-none transition text-base font-mono"
                />
              </div>
              <button
                onClick={handleConvert}
                disabled={!idInput.trim() || loading}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium rounded-md transition-colors shadow-sm hover:shadow flex items-center gap-2 whitespace-nowrap"
              >
                {loading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <RefreshCw className="w-4 h-4" />
                )}
                {loading ? 'Processing...' : 'Convert'}
              </button>
            </div>
            <div className="mt-3 flex items-center justify-between flex-wrap gap-3">
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Supports: Egyptian (14 digits) • Saudi (10 digits) • Other formats
              </p>
              <div className="flex items-center gap-4">
                <label className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={autoConvert}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setAutoConvert(e.target.checked)}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500 border-gray-300"
                  />
                  Auto-convert
                </label>
                <label className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={useAPI}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUseAPI(e.target.checked)}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500 border-gray-300"
                  />
                  <Server className="w-3 h-3" />
                  API Mode
                </label>
              </div>
            </div>
            {error && (
              <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
                <p className="text-sm text-red-700 dark:text-red-300 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4" />
                  {error}
                </p>
              </div>
            )}
          </div>

          {/* Results */}
          {idInfo && idInput.trim() && (
            <div className="space-y-6 mt-6 border-t border-gray-200 dark:border-gray-700 pt-6">
              {/* Validation Status */}
              <div className={`p-4 rounded-md flex items-start gap-3 ${
                idInfo.isValid 
                  ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800' 
                  : 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
              }`}>
                {idInfo.isValid ? (
                  <Check className="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 mt-0.5 flex-shrink-0" />
                )}
                <div className="flex-1">
                  <h3 className={`font-semibold mb-1 ${
                    idInfo.isValid 
                      ? 'text-green-900 dark:text-green-100' 
                      : 'text-red-900 dark:text-red-100'
                  }`}>
                    {idInfo.isValid ? 'Valid ID Format' : 'Invalid ID Format'}
                  </h3>
                  {idInfo.format && (
                    <p className={`text-sm ${
                      idInfo.isValid 
                        ? 'text-green-700 dark:text-green-300' 
                        : 'text-red-700 dark:text-red-300'
                    }`}>
                      Format: {idInfo.format}
                    </p>
                  )}
                </div>
              </div>

              {/* Extracted Information */}
              {idInfo.extractedInfo && idInfo.isValid && (
                <div className="bg-gray-50 dark:bg-gray-800/50 rounded-md p-6 border border-gray-200 dark:border-gray-700">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-5 flex items-center gap-2">
                    <Info className="w-5 h-5 text-blue-600" />
                    Extracted Information
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    {idInfo.extractedInfo.dateOfBirth && (
                      <div className="flex items-start gap-3 p-3 bg-white dark:bg-gray-700 rounded-md">
                        <Calendar className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                        <div className="flex-1">
                          <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">Date of Birth</p>
                          <p className="text-base font-semibold text-gray-900 dark:text-white">
                            {idInfo.extractedInfo.dateOfBirth}
                          </p>
                        </div>
                      </div>
                    )}
                    {idInfo.extractedInfo.gender && (
                      <div className="flex items-start gap-3 p-3 bg-white dark:bg-gray-700 rounded-md">
                        <User className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                        <div className="flex-1">
                          <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">Gender</p>
                          <p className="text-base font-semibold text-gray-900 dark:text-white">
                            {idInfo.extractedInfo.gender}
                          </p>
                        </div>
                      </div>
                    )}
                    {idInfo.extractedInfo.placeOfIssue && (
                      <div className="flex items-start gap-3 p-3 bg-white dark:bg-gray-700 rounded-md">
                        <MapPin className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                        <div className="flex-1">
                          <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">Place of Issue</p>
                          <p className="text-base font-semibold text-gray-900 dark:text-white">
                            {idInfo.extractedInfo.placeOfIssue}
                          </p>
                        </div>
                      </div>
                    )}
                    {idInfo.extractedInfo.checksum && (
                      <div className="flex items-start gap-3 p-3 bg-white dark:bg-gray-700 rounded-md">
                        <Info className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                        <div className="flex-1">
                          <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">Checksum</p>
                          <p className="text-base font-semibold text-gray-900 dark:text-white">
                            {idInfo.extractedInfo.checksum}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Converted Formats */}
              {idInfo.convertedFormats && Object.keys(idInfo.convertedFormats).length > 0 && (
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      Converted Formats
                    </h3>
                    <span className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-full">
                      {Object.keys(idInfo.convertedFormats).length} formats
                    </span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {Object.entries(idInfo.convertedFormats).map(([format, value]) => {
                      const formatValue = String(value);
                      return (
                        <div
                          key={format}
                          className="bg-gray-50 dark:bg-gray-800/50 rounded-md p-4 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 hover:shadow-sm transition-all"
                        >
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide">
                              {format}
                            </span>
                            <button
                              onClick={() => handleCopy(formatValue, format)}
                              className="p-1.5 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors group"
                              title="Copy to clipboard"
                            >
                              {copied === format ? (
                                <Check className="w-4 h-4 text-green-600" />
                              ) : (
                                <Copy className="w-4 h-4 text-gray-500 dark:text-gray-400 group-hover:text-blue-600" />
                              )}
                            </button>
                          </div>
                          <p className="font-mono text-gray-900 dark:text-white break-all text-sm bg-white dark:bg-gray-700 p-3 rounded border border-gray-200 dark:border-gray-600">
                            {formatValue}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div className="bg-white dark:bg-gray-800 rounded-md shadow-sm border border-gray-200 dark:border-gray-700 p-5 hover:shadow-md transition-shadow">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-md flex items-center justify-center">
                <Info className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Egyptian ID</h3>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              14 digits format. Contains date of birth, gender, and governorate information.
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500 font-mono bg-gray-50 dark:bg-gray-700 px-2 py-1 rounded">
              YYMMDDGSSSSSC
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-md shadow-sm border border-gray-200 dark:border-gray-700 p-5 hover:shadow-md transition-shadow">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-md flex items-center justify-center">
                <Info className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Saudi ID</h3>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              10 digits format. Contains date of birth and gender information.
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500 font-mono bg-gray-50 dark:bg-gray-700 px-2 py-1 rounded">
              YYMMDDSSSG
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-md shadow-sm border border-gray-200 dark:border-gray-700 p-5 hover:shadow-md transition-shadow">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-md flex items-center justify-center">
                <Info className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Other Formats</h3>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Supports various ID formats (8-12 digits) with format conversion capabilities.
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500 font-mono bg-gray-50 dark:bg-gray-700 px-2 py-1 rounded">
              SSN, Generic IDs
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

