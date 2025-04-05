/**
 * Utility functions for the POSCAR/CIF converter
 */

/**
 * Determine file type based on file extension
 * @param {string} filename - Name of the file
 * @returns {string|null} - 'cif', 'poscar', or null if unsupported
 */
export function getFileType(filename) {
  const ext = filename.toLowerCase().split('.').pop();
  if (ext === 'cif') return 'cif';
  if (ext === 'poscar' || ext === 'vasp') return 'poscar';
  return null;
}

/**
 * Extract description/name from file content or filename
 * @param {string} content - File content
 * @param {string} fileType - Type of file ('poscar' or 'cif')
 * @param {string} filename - Original filename
 * @returns {string} - Extracted description or original filename without extension
 */
export function extractDescriptionFromContent(content, fileType, filename) {
  // First use original filename without extension as the base name
  const baseFilename = filename.split('.').slice(0, -1).join('.');
  if (baseFilename) {
    return baseFilename;
  }
  
  // Fallback to extracting from content
  if (fileType === 'poscar') {
    // First line of POSCAR file is the description/name
    const firstLine = content.trim().split('\n')[0];
    return firstLine || 'structure';
  } else if (fileType === 'cif') {
    // Find data_ tag in CIF file
    const match = content.match(/data_([^\s]+)/);
    if (match && match[1]) return match[1];
    return 'structure';
  }
  return 'structure';
}
