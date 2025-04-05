/**
 * File handling operations for the POSCAR/CIF converter
 */

import { state } from './main.js';
import { updateFileList } from './ui.js';
import { convertFile, updateStatus } from './converter.js';
import { getFileType, extractDescriptionFromContent } from './utils.js';

/**
 * Handle file upload event
 * @param {Event} event - File input change event
 */
export function handleFileUpload(event) {
  const fileList = event.target.files;
  if (!fileList.length) return;
  
  updateStatus(`Processing ${fileList.length} files...`);
  
  Array.from(fileList).forEach(file => {
    const fileType = getFileType(file.name);
    if (!fileType) {
      console.warn(`Unsupported file format: ${file.name}`);
      return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
      const fileId = 'file_' + (state.fileCounter++);
      const content = e.target.result;
      
      state.files[fileId] = {
        name: file.name,
        content: content,
        type: fileType,
        description: extractDescriptionFromContent(content, fileType, file.name),
        convertedContent: null,
        convertedType: null
      };
      
      updateFileList();
      updateStatus("Files uploaded successfully!", "success");
    };
    
    reader.readAsText(file);
  });
  
  // Reset file input to allow selecting the same file again
  event.target.value = null;
}

/**
 * Download a single file (original or converted)
 * @param {string} fileId - ID of the file to download
 */
export function downloadFile(fileId) {
  const file = state.files[fileId];
  let content, filename;
  
  if (file.convertedContent) {
    content = file.convertedContent;
    if (file.convertedType === 'cif') {
      filename = `${file.description}.cif`;
    } else {
      filename = `${file.description}.poscar`;
    }
  } else {
    content = file.content;
    filename = file.name;
  }
  
  const blob = new Blob([content], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

/**
 * Download all files (original and converted)
 * @returns {Promise<void>}
 */
export async function downloadAll() {
  // Convert unconverted files first
  const promises = [];
  Object.keys(state.files).forEach(fileId => {
    const file = state.files[fileId];
    if (!file.convertedContent) {
      if (file.type === 'poscar') {
        promises.push(convertFile(fileId, 'to-cif'));
      } else if (file.type === 'cif') {
        promises.push(convertFile(fileId, 'to-poscar'));
      }
    }
  });
  
  try {
    if (promises.length > 0) {
      updateStatus("Converting remaining files...");
      await Promise.all(promises);
    }
    
    // Download all files
    Object.keys(state.files).forEach(fileId => {
      downloadFile(fileId);
    });
    
    updateStatus("All files downloaded!", "success");
  } catch (error) {
    updateStatus("Some files could not be processed", "error");
  }
}

/**
 * Remove a file from the list
 * @param {string} fileId - ID of the file to remove
 */
export function removeFile(fileId) {
  delete state.files[fileId];
  updateFileList();
}
